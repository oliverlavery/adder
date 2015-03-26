#include "StdAfx.h"
#include "adder.h"
#include <typeinfo.h>

// Opcodes (cribbed from detours)
#define	   OP_JMP_SEG		0x25
#define    OP_JA            0x77
#define    OP_NOP           0x90
#define    OP_CALL          0xe8
#define    OP_JMP           0xe9
#define    OP_PREFIX        0xff
#define    OP_MOV_EAX       0xa1
#define    OP_SET_EAX       0xb8
#define    OP_JMP_EAX       0xe0
#define    OP_RET_POP       0xc2
#define    OP_RET           0xc3
#define    OP_BRK           0xcc

#define    SIZE_OF_JMP      5
#define    SIZE_OF_NOP      1
#define    SIZE_OF_BRK      1

#ifdef WIN32
#pragma warning(disable: 4309)
#endif
static char stub_bytes[] = 
{
	0x60,			// pushad
	0x9c,			// pushfd
	0x8b, 0xc4,		// mov eax, esp
	0x55,			// push ebp
	0x8b, 0xec,		// mov ebp, esp
	0x53,			// push ebx
	0x56,			// push esi
	0x57,			// push edi
	0x68, 0,0,0,0,  // push imm32
	0x50,			// push eax
	0xe8, 0,0,0,0,  // call imm32
	0x58,			// pop eax
	0x58,			// pop eax
	0x5f,			// pop edi
	0x5e,			// pop esi
	0x5b,			// pop ebx
	0x8b, 0xe5,		// mov esp, ebp
	0x5d,			// pop ebp
	0x9d,			// popfd
	0x61,			// popad
};
#define STUB_ARG 11
#define STUB_FN  17
#define STUB_SIZE 31

// for generating asm listing. DO NOT CALL
void __stub_code( void ) {
	__asm {
		pushad
		pushfd
		mov eax, esp
		push ebp
		mov ebp, esp
		push ebx
		push esi
		push edi
		push 0x12345678
		push eax
		call __stub_code
		pop eax
		pop eax
		pop edi
		pop esi
		pop ebx
		mov esp, ebp
		pop ebp
		popfd
		popad
	}
}


/* splice_heap manages allocating executable memory pages 
   this uses a seperate heap so that our code pages are less 
   likely to be intermingled with original process memory
*/
splice_heap::splice_heap( size_t min, size_t max ) {
	hHeap = (void *)HeapCreate( 0, min, max );
}

splice_heap::~splice_heap() {
	HeapDestroy( hHeap );
}

void *splice_heap::alloc(size_t size) {
	void *p;
	DWORD dwFoo;

	p = HeapAlloc( (HANDLE)hHeap, HEAP_ZERO_MEMORY, size );
	if (p) VirtualProtect( p, size, PAGE_EXECUTE_READWRITE, &dwFoo );
	return p;
}

void splice_heap::free( void *ptr) {
	HeapFree( (HANDLE)hHeap, 0, ptr );
}


/* raw_splice encapsulates splicing C functions into
   (mostly) arbitrary assembly sequences
*/

splice_heap raw_splice::heap = splice_heap( SPLICE_HEAP_MIN, SPLICE_HEAP_MAX );

raw_splice::raw_splice() {
	installed = FALSE;
	address = NULL;
	old_code_length = 0;
	stub_block = NULL;
	pre_func = NULL;
	post_func = NULL;
}


raw_splice::raw_splice( void *ptr ) {
	installed = FALSE;
	address = NULL;
	old_code_length = 0;
	stub_block = NULL;
	pre_func = NULL;
	post_func = NULL;	
	set_address( ptr );
}

raw_splice::~raw_splice() {
	MessageBox( NULL, "RAW SPLICE UNINSTALL", "RAW SPLICE UNINSTALL", MB_OK );
	uninstall();
	if ( stub_block ) raw_splice::heap.free( stub_block );
}

bool raw_splice::is_installed()
{
	return installed;
}

bool raw_splice::set_address( void *ptr )
{
	if ( is_installed() ) return FALSE;
	this->address = ptr;
	return TRUE;
}

bool raw_splice::set_address( int addr ) {
	return this->set_address( (void*)addr );
}

void *raw_splice::get_address() {
	return address;
}

raw_splice_func raw_splice::get_pre_func() {
	return pre_func;
}

bool raw_splice::set_pre_func( raw_splice_func ptr ) {
	if ( is_installed() ) return FALSE;
	this->pre_func = ptr;
	return TRUE;
}

raw_splice_func raw_splice::get_post_func() {
	return post_func;
}

bool raw_splice::set_post_func( raw_splice_func ptr ) {
	if ( is_installed() ) return FALSE;
	this->post_func = ptr;
	return TRUE;
}

bool raw_splice::install()
{
	PBYTE tmp, target, stub;
	PBYTE op;
	DWORD dwOldProtect;
	DWORD addr;
	DWORD len;
	x86_instruction x86_inst;

	size_t target_len = 0, stub_length = 0, stub_offset = 0;
	int **p;

	if ( is_installed() ) return FALSE;
	if ( IsBadCodePtr( (FARPROC) address ) || IsBadReadPtr(address, 10) ) return FALSE;

	if ( pre_func && IsBadCodePtr( (FARPROC)pre_func ) ) return FALSE;
	if ( post_func && IsBadCodePtr( (FARPROC)post_func ) ) return FALSE;
	if ( !pre_func && !post_func ) return FALSE;
	// At least everything appears valid

	// Clean up left over stub_block if it is present.
	raw_splice::heap.free( stub_block );
	stub_block = NULL;

	tmp = target = (PBYTE)address;
	while ( target_len < SIZE_OF_JMP ) {
		op = tmp;
		len = x86_get_instruction(tmp, &x86_inst );
		if ( len == 0 ) break;
		tmp = tmp + len;
		target_len = tmp - target;

		if (x86_inst.get_opcode() & x86_inst.C_BAD) return FALSE;
		if (x86_inst.get_opcode() & x86_inst.C_STOP) return FALSE;
		if (x86_inst.get_opcode() & x86_inst.C_REL) return FALSE;

		if (
            x86_inst.get_opcode() == OP_RET_POP 
			|| x86_inst.get_opcode() == OP_RET 
			|| x86_inst.get_opcode() == OP_CALL 
			)
        return FALSE;
	}
    if ( target_len < SIZE_OF_JMP ) {
        // Too few instructions.
        return FALSE;
    }
    if (target_len > MAX_SPLICE_LENGTH ) {
        // Too many instructions.
        return FALSE;
    }
	// at this point we know how many instructions to copy.
	// save them.
	memcpy( old_code, address, target_len );
	old_code_length = target_len;

	stub_length = target_len + SIZE_OF_JMP;
	if ( pre_func ) stub_length += STUB_SIZE;
	if ( post_func ) stub_length += STUB_SIZE;

	// Get some read-write-exec memory from a seperate heap
	stub_block = raw_splice::heap.alloc( stub_length );
	memset( stub_block, 0xCC, stub_length );
	stub = (PBYTE)stub_block;

	// insert call wrapper for pre_func
	if ( pre_func ) {
		memcpy( stub_block, stub_bytes, STUB_SIZE );
		p = (int **)&stub[ STUB_ARG ] ;
		*p = (int *)this;
		p = (int **)&stub[ STUB_FN ] ;
		addr = (DWORD)pre_func - (DWORD)p - sizeof(p);
		*p = (int *)addr;
		stub_offset += STUB_SIZE;
	}
	
	// insert original code.
	tmp = target = (PBYTE)address;
	stub = (PBYTE)stub_block;
	stub += stub_offset;
	memcpy( stub, tmp, target_len );

	// Old copy loop. might need this for relative address fixups
/*	size_t copied;
    for (copied = 0; copied < target_len;) {
        tmp = tmp + x86_get_instruction(tmp, &x86_inst );
		x86_put_instruction( stub, &x86_inst );
        copied = tmp - target;
        stub = ((PBYTE)stub_block) + stub_offset + copied;
    }
	stub_offset += copied; */
	stub_offset += target_len;

	stub = (PBYTE)stub_block;
	// insert call wrapper for post_func
	if ( post_func ) {
		memcpy( &stub[stub_offset], stub_bytes, STUB_SIZE );
		p = (int **)&stub[ STUB_ARG + stub_offset] ;
		*p = (int *)this;
		p = (int **)&stub[ STUB_FN + stub_offset] ;
		addr = (DWORD)post_func - (DWORD)p - sizeof(p);
		*p = (int *)addr;
		stub_offset += STUB_SIZE;
	}

	// insert our jump back to the target code
	stub[stub_offset++] = OP_JMP;
	p = (int**)&stub[stub_offset];
	addr = (DWORD)(target + target_len) - (DWORD)p - sizeof(p);
	*p = (int *)addr;

	// stub block is built, now insert the jmp to it at our target.
	FlushInstructionCache( GetCurrentProcess(), address, SIZE_OF_JMP);
	VirtualProtect( address, SIZE_OF_JMP, PAGE_EXECUTE_READWRITE, &dwOldProtect );
	target = (PBYTE)address;
	*target = OP_JMP;
	p = (int**)(target + 1);
	addr = (DWORD)stub_block - (DWORD)p - sizeof(p);
	p[0] = (int*)addr;
	FlushInstructionCache(GetCurrentProcess(), address, SIZE_OF_JMP);
	VirtualProtect( address, SIZE_OF_JMP, dwOldProtect, &dwOldProtect );

	// Done (hopefully)
	installed = TRUE;
	return TRUE;
}

bool raw_splice::uninstall()
{
	DWORD dwOldProtect;
	bool unmark = FALSE;

	if ( !is_marked_thread() ) {
		unmark = TRUE;
		mark_thread( TRUE );
	}

	if ( !is_installed() ) return FALSE;
	
	if ( IsBadCodePtr( (FARPROC) address ) 
		|| IsBadReadPtr(address, 10) )
		return FALSE;

	VirtualProtect( address, SIZE_OF_JMP, PAGE_EXECUTE_READWRITE, &dwOldProtect );
	memcpy( address, old_code, old_code_length );
	VirtualProtect( address, SIZE_OF_JMP, dwOldProtect, &dwOldProtect );

	installed = FALSE;

	if ( unmark ) {
		mark_thread(FALSE);
	}
	return TRUE;
}

// Debug stuff
void pre_trace( registers *r, void *arg ) {
	fputs("pre splice called\n", stderr);
}

void post_trace( registers *r, void *arg ) {
	fputs("post splice called\n", stderr);
}

raw_splice_func get_pre_trace()
{
	return &pre_trace;
}

raw_splice_func get_post_trace()
{
	return &post_trace;
}

splice::splice() 
	: raw_splice(),
	pre_callback(NULL),
	post_callback(NULL) 
{
}

splice::splice( void *addr ) 
	: raw_splice(addr), 
	pre_callback(NULL), 
	post_callback(NULL) 
{
}


splice::~splice() 
{
	MessageBox(NULL, "SPLICE UNINSTALL","SPLICE UNINSTALL", MB_OK);
}

bool splice::install()
{
	if ( !pre_callback && !post_callback ) return FALSE;
	return raw_splice::install();
}

bool splice::uninstall()
{
	return raw_splice::uninstall();
}

bool splice::is_installed()
{
	return raw_splice::is_installed();
}

bool splice::set_address( void *addr ) {
	return raw_splice::set_address( addr );
}

bool splice::set_address( int addr ) {
	return raw_splice::set_address( addr );
}

void *splice::get_address() {
	return raw_splice::get_address();
}

bool splice::set_pre_callback( splice_callback *s ) {
	del_pre_callback();
	bool ret = raw_splice::set_pre_func( &splice::pre_func );
	if (ret) pre_callback = s;
	return ret;
}

splice_callback *splice::get_pre_callback() {
	return pre_callback;
}

void splice::del_pre_callback() {
	if (is_installed()) uninstall();
	raw_splice::set_pre_func( NULL );
	if (pre_callback) delete pre_callback;
}

bool splice::set_post_callback( splice_callback *s ) {
	del_post_callback();
	bool ret = raw_splice::set_post_func( &splice::post_func );
	if (ret) post_callback = s;
	return ret;
}

splice_callback *splice::get_post_callback() {
	return post_callback;
}

void splice::del_post_callback() {
	if (is_installed()) uninstall();
	raw_splice::set_post_func( NULL );
	if (post_callback) delete post_callback;
}

void splice::pre_func(registers *r, void *p) {
	splice *s = (splice *)p;	

	TRACE( fputs( "splice::pre_func called\n", stderr) );
	if ( is_marked_thread() ) {
		TRACE( fputs( "splice::pre_func calling thread is within python interpreter... bailing\n", stderr) );
		return;
	}
	LockPython();
	mark_thread(TRUE);
	TRACE( fputs( "splice::pre_func invoking callback\n", stderr) );
#ifdef SAFE_CALLBACKS
	try {
#endif
	s->get_pre_callback()->run( r, s );
#ifdef SAFE_CALLBACKS
	} catch ( ... ) {
		MessageBox( NULL, "Fatal exception occured within callback.", "Really Horrible Error", MB_OK );
	}
#endif
	mark_thread(FALSE);
	ReleasePython();
}

void splice::post_func(registers *r, void *p) {
	splice *s = (splice *)p;	
	TRACE( fputs( "splice::post_func called\n", stderr) );
	if ( is_marked_thread() ) {
		TRACE( fputs( "splice::post_func calling thread is within python interpreter... bailing\n", stderr) );
		return;
	}
	LockPython();
	mark_thread(TRUE);
	TRACE( fputs( "splice::post_func invoking callback\n", stderr) );
#ifdef SAFE_CALLBACKS
	try {
#endif
	s->get_post_callback()->run( r, s );
#ifdef SAFE_CALLBACKS
	} catch ( ... ) {
		MessageBox( NULL, "Fatal exception occured within callback.", "Really Horrible Error", MB_OK );
	}
#endif
	mark_thread(FALSE);
	ReleasePython();
}

/*
splice *s;
registers *regs;
DWORD __declspec(naked)  __stdcall thread_call_pre( void * ) {
	__asm {
//		push ebx
//		push esi
//		push edi

		pushad
		pushfd
		mov eax, esp
		push ebp
		mov ebp, esp
		push ebx
		push esi
		push edi
		push s
		push eax
		call splice::pre_func
		pop eax
		pop eax
		pop edi
		pop esi
		pop ebx
		mov esp,ebp
		pop ebp
		popfd
		popad
		ret
//		pop edi
//		pop esi
//		pop ebx
//		ret 4
	}
//	s->pre_func( regs, s );
//	return 0;
}
*/
void splice::dummy_call_pre( registers *r) {
//	DWORD foo;
//	s = this;
//	regs = r;
//	CreateThread( NULL, 0, thread_call_pre, NULL, 0, &foo);
}

void splice::dummy_call_post( registers *r) {
	bool was_marked = is_marked_thread();
	mark_thread( FALSE );
	this->post_func( r, this );
	mark_thread( was_marked );
}
