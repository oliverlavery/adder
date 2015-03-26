#include <stdio.h>
#include <windows.h>
#include <detours.h>
#include <stddef.h>
#include <string>

#define arrayof(x)		(sizeof(x)/sizeof(x[0]))
//#define VERBOSE 1
void PrintUsage(void)
{
	printf("Usage:\n"
		   "    adderload.exe [options] [command line]\n"
		   "Options:\n"
		   "\t-p:\"[python script] [script command line]\"\n\t\tStart the process with python script\n"
		   "\t-?\n\t\t: This help screen.\n");
}

inline PBYTE DetourGenMovEax(PBYTE pbCode, UINT32 nValue)
{
    *pbCode++ = 0xB8;
    *((UINT32*&)pbCode)++ = nValue;
    return pbCode;
}

inline PBYTE DetourGenMovEbx(PBYTE pbCode, UINT32 nValue)
{
    *pbCode++ = 0xBB;
    *((UINT32*&)pbCode)++ = nValue;
    return pbCode;
}

inline PBYTE DetourGenMovEcx(PBYTE pbCode, UINT32 nValue)
{
    *pbCode++ = 0xB9;
    *((UINT32*&)pbCode)++ = nValue;
    return pbCode;
}

inline PBYTE DetourGenMovEdx(PBYTE pbCode, UINT32 nValue)
{
    *pbCode++ = 0xBA;
    *((UINT32*&)pbCode)++ = nValue;
    return pbCode;
}

inline PBYTE DetourGenMovEsi(PBYTE pbCode, UINT32 nValue)
{
    *pbCode++ = 0xBE;
    *((UINT32*&)pbCode)++ = nValue;
    return pbCode;
}

inline PBYTE DetourGenMovEdi(PBYTE pbCode, UINT32 nValue)
{
    *pbCode++ = 0xBF;
    *((UINT32*&)pbCode)++ = nValue;
    return pbCode;
}

inline PBYTE DetourGenMovEbp(PBYTE pbCode, UINT32 nValue)
{
    *pbCode++ = 0xBD;
    *((UINT32*&)pbCode)++ = nValue;
    return pbCode;
}

inline PBYTE DetourGenMovEsp(PBYTE pbCode, UINT32 nValue)
{
    *pbCode++ = 0xBC;
    *((UINT32*&)pbCode)++ = nValue;
    return pbCode;
}

inline PBYTE DetourGenPush(PBYTE pbCode, UINT32 nValue)
{
    *pbCode++ = 0x68;
    *((UINT32*&)pbCode)++ = nValue;
    return pbCode;
}

inline PBYTE DetourGenPushEax(PBYTE pbCode)
{
    *pbCode++ = 0x50;
    return pbCode;
}

inline PBYTE DetourGenPushad(PBYTE pbCode)
{
    *pbCode++ = 0x60;
    return pbCode;
}

inline PBYTE DetourGenPopad(PBYTE pbCode)
{
    *pbCode++ = 0x61;
    return pbCode;
}

inline PBYTE DetourGenJmp(PBYTE pbCode, PBYTE pbJmpDst, PBYTE pbJmpSrc = 0)
{
    if (pbJmpSrc == 0) {
        pbJmpSrc = pbCode;
    }
    *pbCode++ = 0xE9;
    *((INT32*&)pbCode)++ = pbJmpDst - (pbJmpSrc + 5);
    return pbCode;
}

inline PBYTE DetourGenCall(PBYTE pbCode, PBYTE pbJmpDst, PBYTE pbJmpSrc = 0)
{
    if (pbJmpSrc == 0) {
        pbJmpSrc = pbCode;
    }
    *pbCode++ = 0xE8;
    *((INT32*&)pbCode)++ = pbJmpDst - (pbJmpSrc + 5);
    return pbCode;
}

inline PBYTE DetourGenCallEax(PBYTE pbCode)
{
    *pbCode++ = 0xFF;
    *pbCode++ = 0xD0;
    return pbCode;
}

inline PBYTE DetourGenBreak(PBYTE pbCode)
{
    *pbCode++ = 0xcc;
    return pbCode;
}

inline PBYTE DetourGenRet(PBYTE pbCode)
{
    *pbCode++ = 0xc3;
    return pbCode;
}

inline PBYTE DetourGenNop(PBYTE pbCode)
{
    *pbCode++ = 0x90;
    return pbCode;
}

inline PBYTE GetLoadLibraryA()
{
	HMODULE hmod = LoadLibrary("kernel32");
	return (PBYTE)GetProcAddress( hmod, "LoadLibraryA" );
}

inline PBYTE GetGetProcAddress()
{
	HMODULE hmod = LoadLibrary("kernel32");
	return (PBYTE)GetProcAddress( hmod, "GetProcAddress" );
}

static BOOL InjectLibrary(HANDLE hProcess,
                          HANDLE hThread,
						  PBYTE pfLoadLibrary,
						  PBYTE pfGetProcAddress,
						  PBYTE pbData,
						  DWORD cbData,
						  PBYTE pbProcName,
						  DWORD cbProcName,
						  PBYTE pbArgs,
						  DWORD cbArgs)
{
	BOOL fSucceeded = FALSE;
    DWORD nProtect = 0;
    DWORD nWritten = 0;
    CONTEXT cxt;
    UINT32 nCodeBase;
    PBYTE pbCode;

    struct Code
    {
        BYTE rbCode[128];
        union
        {
            WCHAR   wzLibFile[512];
            CHAR    szLibFile[512];
        };
        union
        {
            WCHAR   wzProcName[512];
            CHAR    szProcName[512];
        };
        union
        {
            WCHAR   wzArgs[512];
            CHAR    szArgs[512];
        };
    } code;

    SuspendThread(hThread);
    
    ZeroMemory(&cxt, sizeof(cxt));
    cxt.ContextFlags = CONTEXT_FULL;
    if (!GetThreadContext(hThread, &cxt)) {
		goto finish;
    }

#if VERBOSE
    printf("  ContextFlags: %08x\n", cxt.ContextFlags);
    printf("  EIP=%04x:%08x ESP=%04x:%08x EBP=%08x\n",
           cxt.SegCs & 0xffff, cxt.Eip, cxt.SegSs & 0xffff, cxt.Esp, cxt.Ebp);
    printf("  DS=%04x ES=%04x FS=%04x GS=%04x EFL=%08x\n",
           cxt.SegDs & 0xffff, cxt.SegEs & 0xffff,
           cxt.SegFs & 0xffff, cxt.SegGs & 0xffff,
           cxt.EFlags);
    printf("  EAX=%08x EBX=%08x ECX=%08x EDX=%08x ESI=%08x EDI=%08x\n",
           cxt.Eax, cxt.Ebx, cxt.Ecx, cxt.Edx, cxt.Esi, cxt.Edi);
#endif    

    nCodeBase = (cxt.Esp - sizeof(code)) & ~0x1fu;        // Cache-line align.
    pbCode = code.rbCode;

    if (pbData) {
        CopyMemory(code.szLibFile, pbData, cbData);
        pbCode = DetourGenPush(pbCode, nCodeBase + offsetof(Code, szLibFile));
        pbCode = DetourGenCall(pbCode, pfLoadLibrary,
                               (PBYTE)nCodeBase + (pbCode - code.rbCode));
    }
    if (pbProcName) {
        CopyMemory(code.szProcName, pbProcName, cbProcName);
//		pbCode = DetourGenBreak( pbCode );
        pbCode = DetourGenPush(pbCode, nCodeBase + offsetof(Code, szProcName));
        pbCode = DetourGenPushEax(pbCode);
        pbCode = DetourGenCall(pbCode, pfGetProcAddress,
                               (PBYTE)nCodeBase + (pbCode - code.rbCode));
		if (pbArgs) {
	        CopyMemory(code.szArgs, pbArgs, cbArgs);
	        pbCode = DetourGenPush(pbCode, nCodeBase + offsetof(Code, szArgs));			
		}
		pbCode = DetourGenCallEax( pbCode );
    }
    
    pbCode = DetourGenMovEax(pbCode, cxt.Eax);
    pbCode = DetourGenMovEbx(pbCode, cxt.Ebx);
    pbCode = DetourGenMovEcx(pbCode, cxt.Ecx);
    pbCode = DetourGenMovEdx(pbCode, cxt.Edx);
    pbCode = DetourGenMovEsi(pbCode, cxt.Esi);
    pbCode = DetourGenMovEdi(pbCode, cxt.Edi);
    pbCode = DetourGenMovEbp(pbCode, cxt.Ebp);
    pbCode = DetourGenMovEsp(pbCode, cxt.Esp);
    pbCode = DetourGenJmp(pbCode, (PBYTE)cxt.Eip,
                          (PBYTE)nCodeBase + (pbCode - code.rbCode));
    
    cxt.Esp = nCodeBase - 4;
    cxt.Eip = nCodeBase;

    if (!VirtualProtectEx(hProcess, (PBYTE)nCodeBase, sizeof(Code),
                          PAGE_EXECUTE_READWRITE, &nProtect)) {
        goto finish;
    }

#if VERBOSE    
//    printf("VirtualProtectEx(%08x) -> %d\n", nProtect, b);
#endif    

    if (!WriteProcessMemory(hProcess, (PBYTE)nCodeBase, &code, sizeof(Code),
                            &nWritten)) {
        goto finish;
    }

#if VERBOSE    
    printf("code: %08x..%08x (WriteProcess: %d)\n",
           nCodeBase, nCodeBase + (pbCode - code.rbCode), nWritten);
#endif
    
    if (!FlushInstructionCache(hProcess, (PBYTE)nCodeBase, sizeof(Code))) {
        goto finish;
    }
                        
    if (!SetThreadContext(hThread, &cxt)) {
        goto finish;
    }

#if VERBOSE    
    ZeroMemory(&cxt, sizeof(cxt));
    cxt.ContextFlags = CONTEXT_FULL;
    GetThreadContext(hThread, &cxt);
    printf("  EIP=%04x:%08x ESP=%04x:%08x EBP=%08x\n",
           cxt.SegCs & 0xffff, cxt.Eip, cxt.SegSs & 0xffff, cxt.Esp, cxt.Ebp);
    printf("  DS=%04x ES=%04x FS=%04x GS=%04x EFL=%08x\n",
           cxt.SegDs & 0xffff, cxt.SegEs & 0xffff,
           cxt.SegFs & 0xffff, cxt.SegGs & 0xffff,
           cxt.EFlags);
    printf("  EAX=%08x EBX=%08x ECX=%08x EDX=%08x ESI=%08x EDI=%08x\n",
           cxt.Eax, cxt.Ebx, cxt.Ecx, cxt.Edx, cxt.Esi, cxt.Edi);
#endif    
    
	fSucceeded = TRUE;
	
  finish:
    ResumeThread(hThread);
	return fSucceeded;
}

// This is an extended version of the function of the same name from Detours.
BOOL WINAPI CreateProcessWithDll(LPCSTR lpApplicationName,
                                        LPSTR lpCommandLine,
                                        LPSECURITY_ATTRIBUTES lpProcessAttributes,
                                        LPSECURITY_ATTRIBUTES lpThreadAttributes,
                                        BOOL bInheritHandles,
                                        DWORD dwCreationFlags,
                                        LPVOID lpEnvironment,
                                        LPCSTR lpCurrentDirectory,
                                        LPSTARTUPINFOA lpStartupInfo,
                                        LPPROCESS_INFORMATION lpProcessInformation,
                                        LPCSTR lpDllName,
										LPCSTR lpFunctionName,
										LPCSTR lpFunctionArgs,
                                        PDETOUR_CREATE_PROCESS_ROUTINEA pfCreateProcessA)
{
	DWORD dwMyCreationFlags = (dwCreationFlags | CREATE_SUSPENDED);
	PROCESS_INFORMATION pi;

	if (pfCreateProcessA == NULL) {
		pfCreateProcessA = CreateProcessA;
	}
	
	if (!pfCreateProcessA(lpApplicationName,
						  lpCommandLine,
						  lpProcessAttributes,
						  lpThreadAttributes,
						  bInheritHandles,
						  dwMyCreationFlags,
						  lpEnvironment,
						  lpCurrentDirectory,
						  lpStartupInfo,
						  &pi)) {
		return FALSE;
	}
	
    if (!InjectLibrary(pi.hProcess, pi.hThread, GetLoadLibraryA(), GetGetProcAddress(),
                       (PBYTE)lpDllName,
                       lpDllName ? strlen(lpDllName) + 1 : 0,
					   (PBYTE)lpFunctionName,
                       lpFunctionName ? strlen(lpFunctionName) + 1 : 0,
					   (PBYTE)lpFunctionArgs,
                       lpFunctionArgs ? strlen(lpFunctionArgs) + 1 : 0)
					   ) {
        return FALSE;
    }
	if (lpProcessInformation) {
		CopyMemory(lpProcessInformation, &pi, sizeof(pi));
	}
	if (!(dwCreationFlags & CREATE_SUSPENDED)) {
		ResumeThread(pi.hThread);
	}
	return TRUE;
}

int __cdecl main(int argc, char **argv)
{
	BOOLEAN fNeedHelp = FALSE;
	PCHAR pszScript = NULL;
	char szDllName[MAX_PATH];

	for (int arg = 1;
		 arg < argc && (argv[arg][0] == '-' || argv[arg][0] == '/');
		 arg++) {
		
        CHAR *argn = argv[arg] + 1;
        CHAR *argp = argn;
        while (*argp && *argp != ':')
            argp++;
        if (*argp == ':')
            *argp++ = '\0';
			
		switch (argn[0]) {
		  case 'p':
		  case 'P':
            pszScript = argp;
			puts( pszScript );
			break;

		  case 'h':
		  case 'H':
		  case '?':
			fNeedHelp = TRUE;
			break;
			
		  default:
			fNeedHelp = TRUE;
			printf("withdll.exe: Bad argument: %s\n", argv[arg]);
			break;
		}
	}

	if (arg >= argc) {
		fNeedHelp = TRUE;
	}
	
	if (fNeedHelp) {
		PrintUsage();
		return 1;
	}

	//////////////////////////////////////////////////////////////////////////
	STARTUPINFO si;
	PROCESS_INFORMATION pi;
	CHAR szCommand[2048];
	CHAR szExe[1024];
	CHAR szFullExe[1024] = "\0";
	PCHAR pszFileExe = NULL;
    
	ZeroMemory(&si, sizeof(si));
	ZeroMemory(&pi, sizeof(pi));
	si.cb = sizeof(si);

	szCommand[0] = L'\0';
	strcpy(szExe, argv[arg]);
	for (; arg < argc; arg++) {
		if (strchr(argv[arg], ' ') != NULL || strchr(argv[arg], '\t') != NULL) {
			strcat(szCommand, "\"");
			strcat(szCommand, argv[arg]);
			strcat(szCommand, "\"");
		}
		else {
			strcat(szCommand, argv[arg]);
		}
		
		if (arg + 1 < argc)
			strcat(szCommand, " ");
	}
	printf("adderload.exe: Starting: `%s'\n\n", szCommand);
    fflush(stdout);

	SetLastError(0);
	SearchPath(NULL, szExe, ".exe", arrayof(szFullExe), szFullExe, &pszFileExe);

	GetModuleFileName(NULL, szDllName, MAX_PATH - 1);
	std::string dllName = std::string( szDllName );
	dllName.erase( dllName.rfind("\\"), dllName.size() );
	dllName.append( "\\DLLs\\_adder.dll" );

	if (!CreateProcessWithDll(szFullExe[0] ? szFullExe : NULL,
                                    szCommand, NULL, NULL, TRUE,
                                    CREATE_DEFAULT_ERROR_MODE, NULL, NULL,
                                    &si, &pi, dllName.c_str(), "AdderProcessStartup", pszScript, NULL)) {
        printf("adderload.exe: CreateProcessWithDll failed: %d\n", GetLastError());
        ExitProcess(2);
    }
 	
	WaitForSingleObject(pi.hProcess, INFINITE);

	DWORD dwResult = 0;
	if (!GetExitCodeProcess(pi.hProcess, &dwResult)) {
		printf("adderload.exe: GetExitCodeProcess failed: %d\n", GetLastError());
		dwResult = 3;
	}
	
	return dwResult;
}
