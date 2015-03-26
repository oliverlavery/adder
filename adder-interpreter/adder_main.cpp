#include "StdAfx.h"
#include "adder.h"

#define SHUTDOWN_TIMEOUT 10000

bool g_OwnConsole = FALSE;
PyInterpreterState *g_interpreter = NULL;
DWORD g_threadStateTlsIndex = 0;
// for recursion
DWORD g_threadMarkerTlsIndex = 0;

HANDLE g_releaseHostEvent;
HANDLE g_appShutdownEvent;
HANDLE g_pythonShutdownEvent;

bool g_hostedInterpreter = FALSE;

extern "C" {
void init_adder(void);
}

#define NULCHAR    '\0'
#define SPACECHAR  ' '
#define TABCHAR    '\t'
#define DQUOTECHAR '\"'
#define SLASHCHAR  '\\'

static void __cdecl parse_cmdline (
    char *cmdstart,
    char **argv,
    char *args,
    int *numargs,
    int *numchars
    )
{
        char *p;
        char c;
        int inquote;                    /* 1 = inside quotes */
        int copychar;                   /* 1 = copy char to *args */
        unsigned numslash;              /* num of backslashes seen */

        *numchars = 0;
        *numargs = 1;                   /* the program name at least */

        /* first scan the program name, copy it, and count the bytes */
        p = cmdstart;
        if (argv)
            *argv++ = args;

        /* A quoted program name is handled here. The handling is much
           simpler than for other arguments. Basically, whatever lies
           between the leading double-quote and next one, or a terminal null
           character is simply accepted. Fancier handling is not required
           because the program name must be a legal NTFS/HPFS file name.
           Note that the double-quote characters are not copied, nor do they
           contribute to numchars. */
        inquote = FALSE;
        do {
            if (*p == DQUOTECHAR )
            {
                inquote = !inquote;
                c = (char) *p++;
                continue;
            }
            ++*numchars;
            if (args)
                *args++ = *p;

            c = (char) *p++;
        } while ( (c != NULCHAR && (inquote || (c !=SPACECHAR && c != TABCHAR))) );

        if ( c == NULCHAR ) {
            p--;
        } else {
            if (args)
                *(args-1) = NULCHAR;
        }

        inquote = 0;

        /* loop on each argument */
        for(;;) {

            if ( *p ) {
                while (*p == SPACECHAR || *p == TABCHAR)
                    ++p;
            }

            if (*p == NULCHAR)
                break;              /* end of args */

            /* scan an argument */
            if (argv)
                *argv++ = args;     /* store ptr to arg */
            ++*numargs;

        /* loop through scanning one argument */
        for (;;) {
            copychar = 1;
            /* Rules: 2N backslashes + " ==> N backslashes and begin/end quote
               2N+1 backslashes + " ==> N backslashes + literal "
               N backslashes ==> N backslashes */
            numslash = 0;
            while (*p == SLASHCHAR) {
                /* count number of backslashes for use below */
                ++p;
                ++numslash;
            }
            if (*p == DQUOTECHAR) {
                /* if 2N backslashes before, start/end quote, otherwise
                    copy literally */
                if (numslash % 2 == 0) {
                    if (inquote) {
                        if (p[1] == DQUOTECHAR)
                            p++;    /* Double quote inside quoted string */
                        else        /* skip first quote char and copy second */
                            copychar = 0;
                    } else
                        copychar = 0;       /* don't copy quote */

                    inquote = !inquote;
                }
                numslash /= 2;          /* divide numslash by two */
            }

            /* copy slashes */
            while (numslash--) {
                if (args)
                    *args++ = SLASHCHAR;
                ++*numchars;
            }

            /* if at end of arg, break loop */
            if (*p == NULCHAR || (!inquote && (*p == SPACECHAR || *p == TABCHAR)))
                break;

            /* copy character into argument */
            if (copychar) {
                if (args)
                    *args++ = *p;
                ++*numchars;
            }
            ++p;
            }

            /* null-terminate the argument */

            if (args)
                *args++ = NULCHAR;          /* terminate string */
            ++*numchars;
        }

        /* We put one last argument in -- a null ptr */
        if (argv)
            *argv++ = NULL;
        ++*numargs;
}

void CreateConsole(char *title)
{
	if ( AllocConsole() ) {		
		SetConsoleTitle(title);
		freopen("CONIN$","r",stdin);   // reopen stdin handle as console window input
		freopen("CONOUT$","w",stdout);  // reopen stout handle as console window output
		freopen("CONOUT$","w",stderr); // reopen stderr handle as console window output
		g_OwnConsole = TRUE;
	} 
}

void DestroyConsole()
{
	if ( g_OwnConsole ) {
		FreeConsole();
	}
}

void *LoadLibraryPy( char *name ) {
	return LoadLibrary( name );
}

void *GetProcAddressPy( void *module, char *name ) {
	return GetProcAddress( (HMODULE)module, name );
}

void PutPyThreadState( PyThreadState *tstate )
{
	TlsSetValue( g_threadStateTlsIndex, tstate );
}

PyThreadState *GetPyThreadState()
{
    PyThreadState *tstate;
	tstate = (PyThreadState *)TlsGetValue( g_threadStateTlsIndex );
	if ( !tstate ) tstate = PyThreadState_New(g_interpreter);
	PutPyThreadState( tstate );
	return tstate;	
}

void mark_thread( bool mark )
{
	TlsSetValue( g_threadMarkerTlsIndex, (void *)mark );
}

bool is_marked_thread()
{
	return 0 != TlsGetValue( g_threadMarkerTlsIndex );	
}


void LockPython()
{
    PyEval_AcquireThread( GetPyThreadState() );
}

void ReleasePython()
{
	PyEval_ReleaseThread( GetPyThreadState() );
}

bool is_hosted_interpreter()
{
	return g_hostedInterpreter;
}

void release_host_process()
{
	SetEvent( g_releaseHostEvent );
}

void wait_for_shutdown()
{
	Py_BEGIN_ALLOW_THREADS;
	WaitForSingleObject( g_appShutdownEvent, INFINITE );
	Py_END_ALLOW_THREADS;
}

void InitPython( char *filename, char **argv, int argc )
{
	FILE *fp = NULL;
	PyThreadState *tstate = NULL;

	PyEval_InitThreads();
	Py_Initialize();
	PySys_SetArgv( argc, argv );
	init_adder();

	mark_thread( TRUE );
	tstate = PyThreadState_Get();
	PutPyThreadState( tstate );
	g_interpreter = tstate->interp;
//	LockPython();
/*
	fp = fopen(filename, "r");
	if (fp != NULL) {
		PyRun_SimpleFile(fp, filename);
		PyErr_Clear();
		fclose(fp);
	} else {
		CreateConsole("Adder Init Console");
		PyRun_InteractiveLoop(stdin, "Adder Console");
		PyErr_Clear();
		DestroyConsole();
	}
	*/
	mark_thread( FALSE );
	ReleasePython();
//	PyThreadState_Delete( tstate );
}

void __cdecl MainPythonThread( void *f )
{
	FILE *fp = NULL;
	char *filename = (char*)f;

	// This will prevent app shutdown until this thread is finished.
	SetEvent( g_pythonShutdownEvent );
	LockPython();
	mark_thread( TRUE );

	fp = fopen(filename, "r");
	if (fp != NULL) {
		PyRun_SimpleFile(fp, filename);
		PyErr_Clear();
		fclose(fp);
	} else {
		release_host_process();
		CreateConsole("Adder Console");
		printf("Unable to find %s\nType <Ctrl-Z> to quit, or enter python commands\n", filename);
		PyRun_InteractiveLoop(stdin, "Adder Startup Console");
		PyErr_Clear();
		DestroyConsole();
	}

//	mark_thread( FALSE );
	ReleasePython();
    PyThreadState_Delete( GetPyThreadState() );
	Py_Finalize();
	ResetEvent( g_pythonShutdownEvent );
}

extern "C"
void __declspec(dllexport) AdderProcessStartup(char *scriptargs) {
	int numargs, numchars;
	char *p;

	g_hostedInterpreter = TRUE;
	parse_cmdline ( scriptargs, NULL, NULL, &numargs, &numchars );
	p = (char *)malloc( numargs * sizeof(char *) + numchars * sizeof(char) );
	parse_cmdline( scriptargs, (char **)p, p + numargs * sizeof(char *), &numargs, &numchars );
	InitPython( ((char**)p)[0], (char**)p, numargs - 1 );
	_beginthread( &MainPythonThread, 0, ((char **)p)[0] );
	WaitForSingleObject( g_releaseHostEvent, INFINITE );
}


void AtExitHandler( void ) {
	mark_thread( TRUE );
	SetEvent( g_appShutdownEvent );
	WaitForSingleObject( g_pythonShutdownEvent, SHUTDOWN_TIMEOUT );
}

// Entry point.
extern "C"
BOOL __declspec(dllexport) APIENTRY DllMain( HINSTANCE hInstance, 
                       DWORD  ul_reason_for_call, 
                       LPVOID lpReserved
					 )
{
    if ( ul_reason_for_call == DLL_PROCESS_ATTACH ) {
		DisableThreadLibraryCalls( hInstance );
		g_threadStateTlsIndex = TlsAlloc();
		g_threadMarkerTlsIndex = TlsAlloc();
		g_releaseHostEvent = CreateEvent( NULL, TRUE, FALSE, NULL );
		g_appShutdownEvent = CreateEvent( NULL, TRUE, FALSE, NULL );
		g_pythonShutdownEvent = CreateEvent( NULL, TRUE, TRUE, NULL );
		atexit( &AtExitHandler );
	} else if ( ul_reason_for_call == DLL_PROCESS_DETACH ) {
		
	}
    return TRUE;
}