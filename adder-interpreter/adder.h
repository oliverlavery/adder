#ifndef ADDER_H_INCLUDED

#ifndef ADDER_API_INCLUDED
#define ADDER_API_INCLUDED

#if defined(SWIG)
#define ADDERAPI
#elif defined(ADDER_EXPORTS)
#define ADDERAPI __declspec(dllexport) 
#else
#define ADDERAPI __declspec(dllimport) 
#endif
#pragma warning(disable:4311)
#pragma warning(disable:4312)

//#define ADDER_TRACE
#ifdef ADDER_TRACE
#define TRACE( a ) a
#else
#define TRACE( a )
#endif

#endif

extern "C" {
#include "libdisasm/src/libdis.h"
}
// catch exceptions during callbacks
#define SAFE_CALLBACKS

// number of bytes we can overwrite in a splice.
#define MAX_SPLICE_LENGTH 32

// The code pages allocated for splices come from
// a seperate heap. These control the size.
#define SPLICE_HEAP_MIN 4096
#define SPLICE_HEAP_MAX 4096 << 6

// Functions to dynamically create a console for GUI apps.
ADDERAPI void CreateConsole(char *title);
ADDERAPI void DestroyConsole();

// Functions to get library addrs
ADDERAPI void *LoadLibraryPy( char *name );
ADDERAPI void *GetProcAddressPy( void *module, char *name );

// Functions for thread marking 
// These are used to prevent cycles in splices
// call mark_thread to prevent recursion
ADDERAPI void mark_thread( bool );
ADDERAPI bool is_marked_thread();

// Returns true when interpreter has been injected
// into a host process
ADDERAPI bool is_hosted_interpreter();
// Resume execution of the host process
ADDERAPI void release_host_process();
// Wait for host process to shut down
ADDERAPI void wait_for_shutdown();

// Register structure
typedef int int32;
typedef unsigned int uint32;
typedef short int int16;
typedef unsigned short int uint16;
typedef signed char int8;
typedef unsigned char uint8;

struct registers32 {
	uint32 eflags;
	uint32 edi;
	uint32 esi;
	uint32 ebp;
	uint32 esp;
	uint32 ebx;
	uint32 edx;
	uint32 ecx;
	uint32 eax;
};


struct registers16 {
	uint16 flags;
	uint16 flags_pad;
	uint16 di;
	uint16 di_pad;
	uint16 si;
	uint16 si_pad;
	uint16 bp;
	uint16 bp_pad;
	uint16 sp;
	uint16 sp_pad;
	uint16 bx;
	uint16 bx_pad;
	uint16 dx;
	uint16 dx_pad;
	uint16 cx;
	uint16 cx_pad;
	uint16 ax;
	uint16 ax_pad;
};



struct registers8 {
	uint16 _flags;
	uint16 _flags_pad;
	uint16 _di;
	uint16 _di_pad;
	uint16 _si;
	uint16 _si_pad;
	uint16 _bp;
	uint16 _bp_pad;
	uint16 _sp;
	uint16 _sp_pad;
	uint8 bl;
	uint8 bh;
	uint16 bx_pad;
	uint8 dl;
	uint8 dh;
	uint16 dx_pad;
	uint8 cl;
	uint8 ch;
	uint16 cx_pad;
	uint8 al;
	uint8 ah;
	uint16 ax_pad;
};

union registers {
	struct registers32 r32;
	struct registers16 r16;
	struct registers8 r8;
};


class ADDERAPI splice_heap {
public:
	splice_heap( size_t, size_t );
	~splice_heap();

	void *alloc( size_t );
	void free( void *);

protected:
	void *hHeap;
};

typedef void (*raw_splice_func)( registers *, void * ) ;

class ADDERAPI raw_splice {
public:
	raw_splice();
	raw_splice( void *python_ptr );
	~raw_splice();

	bool install();
	bool uninstall();
	bool is_installed();

	bool set_address( void * );
	bool set_address( int );
	void *get_address();

	raw_splice_func get_pre_func();
	bool set_pre_func( raw_splice_func );

	raw_splice_func get_post_func();
	bool set_post_func( raw_splice_func );

protected:
	bool installed;
	void *address;
	char old_code[MAX_SPLICE_LENGTH];
	size_t old_code_length;
	void *stub_block;
	raw_splice_func pre_func;
	raw_splice_func post_func;

	static splice_heap heap;

};

// debugging trace callbacks
ADDERAPI raw_splice_func get_pre_trace();
ADDERAPI raw_splice_func get_post_trace();

class splice;

class ADDERAPI splice_callback {
public:
	splice_callback() {};
	virtual ~splice_callback() {};
	virtual void run( registers*, splice* ) {};
};

class ADDERAPI splice : protected raw_splice {
public:
	splice();
	splice( void * p );
	~splice();

	bool install();
	bool uninstall();
	bool is_installed();

	bool set_address( void * );
	bool set_address( int );
	void *get_address();

	bool set_pre_callback( splice_callback * );
	splice_callback *get_pre_callback();
	void del_pre_callback();

	bool set_post_callback( splice_callback * );
	splice_callback *get_post_callback();
	void del_post_callback();

	// test code
	void dummy_call_pre( registers *r);
	void dummy_call_post( registers *r);

#ifndef SWIG
	friend unsigned long __stdcall thread_call_pre( void * );
#endif
	// end of test code
protected:
	splice_callback *pre_callback;
	splice_callback *post_callback;

	static void pre_func(registers *, void *) ;
	static void post_func(registers *, void *) ;
};

// C only. Fns for safely calling python API from a new thread
#ifndef SWIG
//extern PyInterpreterState *g_interpreter;
//extern static PyThreadState *GetPyThreadState();
ADDERAPI void LockPython();
ADDERAPI void ReleasePython();
#endif



// ADE32 Disassembler (consts and structs must match ADE32 header & lib)

class x86_instruction;

extern "C" {

ADDERAPI unsigned long x86_get_instruction( void *python_ptr, x86_instruction* );
ADDERAPI unsigned long x86_put_instruction( void *python_ptr, x86_instruction* );

}


// This class is packed(1) for compat with ADE32
// XXX: this is gross. ADE32 data should be a member of wrapper class
#pragma pack(push)
#pragma pack(1)

class ADDERAPI x86_instruction
{
public:

// ADE32 Constants

#ifndef SWIG
	static const unsigned long C_ERROR;// = 0xFFFFFFFF;
	static const unsigned long C_ADDR1;// =  0x00000001;
	static const unsigned long C_ADDR2;// =  0x00000002;
	static const unsigned long C_ADDR4;// =  0x00000004;
	static const unsigned long C_LOCK;// =  0x00000008;
	static const unsigned long C_67;//    =  0x00000010;
	static const unsigned long C_66;//    =  0x00000020;
	static const unsigned long C_REP;//   =  0x00000040;
	static const unsigned long C_SEG;//   =  0x00000080;
	static const unsigned long C_ANYPREFIX;// = (C_66+C_67+C_LOCK+C_REP+C_SEG);
	static const unsigned long C_DATA1;// =  0x00000100;
	static const unsigned long C_DATA2;// =  0x00000200;
	static const unsigned long C_DATA4;// =  0x00000400;
	static const unsigned long C_SIB;//   =  0x00000800;
	static const unsigned long C_ADDR67;// = 0x00001000;
	static const unsigned long C_DATA66;// = 0x00002000;
	static const unsigned long C_MODRM;// = 0x00004000;
	static const unsigned long C_BAD;//    = 0x00008000;
	static const unsigned long C_OPCODE2;// = 0x00010000;
	static const unsigned long C_REL;//    = 0x00020000;
	static const unsigned long C_STOP;//   = 0x00040000;
#endif

// LibDisasm Constants

#ifndef SWIG
	/* Operand and instruction types */
	/*                   Permissions: */
	static const unsigned int C_OP_R         ;      /* operand is READ */
	static const unsigned int C_OP_W         ;      /* operand is WRITTEN */
	static const unsigned int C_OP_X         ;      /* operand is EXECUTED */
	/*                   Types: */
	static const unsigned int C_OP_UNK       ;      /* unknown operand */     
	static const unsigned int C_OP_REG       ;      /* register */
	static const unsigned int C_OP_IMM       ;      /* immediate value */
	static const unsigned int C_OP_REL       ;      /* relative Address [offset from IP] */
	static const unsigned int C_OP_ADDR      ;      /* Absolute Address */
	static const unsigned int C_OP_EXPR      ;      /* Address Expression [e.g. SIB byte] */
	static const unsigned int C_OP_PTR       ;      /* Operand is an Address containing a Pointer */
	static const unsigned int C_OP_OFF       ;      /* Operand is an offset from a seg/selector */
	/*                   Modifiers: */
	static const unsigned int C_OP_SIGNED    ;   /* operand is signed */
	static const unsigned int C_OP_STRING    ;   /* operand a string */
	static const unsigned int C_OP_CONST     ;   /* operand is a constant */
	static const unsigned int C_OP_EXTRASEG  ;   /* seg overrides */
	static const unsigned int C_OP_CODESEG   ;
	static const unsigned int C_OP_STACKSEG  ;
	static const unsigned int C_OP_DATASEG   ;
	static const unsigned int C_OP_DATA1SEG  ;
	static const unsigned int C_OP_DATA2SEG  ;
	/*                   Size: */
	static const unsigned int C_OP_BYTE      ;   /* operand is 8 bits/1 byte  */
	static const unsigned int C_OP_HWORD     ;   /* operand is .5 mach word (Intel 16 bits) */
	static const unsigned int C_OP_WORD      ;   /* operand is 1 machine word (Intel 32 bits) */
	static const unsigned int C_OP_DWORD     ;   /* operand is 2 mach words (Intel 64 bits) */
	static const unsigned int C_OP_QWORD     ;   /* operand is 4 mach words (Intel 128 bits) */
	static const unsigned int C_OP_SREAL     ;   /* operand is 32 bits/4 bytes */
	static const unsigned int C_OP_DREAL     ;   /* operand is 64 bits/8 bytes */
	static const unsigned int C_OP_XREAL     ;   /* operand is 40 bits/10 bytes */
	static const unsigned int C_OP_BCD       ;   /* operand is 40 bits/10 bytes */            
	static const unsigned int C_OP_SIMD      ;   /* operand is 128 bits/16 bytes */            
	static const unsigned int C_OP_FPENV     ;   /* operand is 224 bits/28 bytes */            

	/* operand masks */
	static const unsigned int C_OP_PERM_MASK ;  /* perms are NOT mutually exclusive */
	static const unsigned int C_OP_TYPE_MASK ;  /* types are mututally exclusive */
	static const unsigned int C_OP_MOD_MASK  ;  /* mods are NOT mutually exclusive */
	static const unsigned int C_OP_SEG_MASK  ;  /* segs are NOT mutually exclusive */
	static const unsigned int C_OP_SIZE_MASK ;  /* sizes are mutually exclusive */

	static const unsigned int C_OP_REG_MASK    ; /* lower WORD is register ID */
	static const unsigned int C_OP_REGTBL_MASK ; /* higher word is register type [gen/dbg] */

	/* instruction types [groups] */
	static const unsigned int C_INS_EXEC		;
	static const unsigned int C_INS_ARITH		;
	static const unsigned int C_INS_LOGIC		;
	static const unsigned int C_INS_STACK		;
	static const unsigned int C_INS_COND		;
	static const unsigned int C_INS_LOAD		;
	static const unsigned int C_INS_ARRAY		;
	static const unsigned int C_INS_BIT		;
	static const unsigned int C_INS_FLAG		;
	static const unsigned int C_INS_FPU		;
	static const unsigned int C_INS_TRAPS		;
	static const unsigned int C_INS_SYSTEM	;
	static const unsigned int C_INS_OTHER		;

	/* C_INS_EXEC group */
	static const unsigned int C_INS_BRANCH	;	/* Unconditional branch */
	static const unsigned int C_INS_BRANCHCC	;	/* Conditional branch */
	static const unsigned int C_INS_CALL		;	/* Jump to subroutine */
	static const unsigned int C_INS_CALLCC	;	/* Jump to subroutine */
	static const unsigned int C_INS_RET		;	/* Return from subroutine */
	static const unsigned int C_INS_LOOP		;	/* loop to local label */

	/* C_INS_ARITH group */
	static const unsigned int C_INS_ADD 		;
	static const unsigned int C_INS_SUB		;
	static const unsigned int C_INS_MUL		;
	static const unsigned int C_INS_DIV		;
	static const unsigned int C_INS_INC		;	/* increment */
	static const unsigned int C_INS_DEC		;	/* decrement */
	static const unsigned int C_INS_SHL		;	/* shift right */
	static const unsigned int C_INS_SHR		;	/* shift left */
	static const unsigned int C_INS_ROL		;	/* rotate left */
	static const unsigned int C_INS_ROR		;	/* rotate right */

	/* C_INS_LOGIC group */
	static const unsigned int C_INS_AND		;
	static const unsigned int C_INS_OR		;
	static const unsigned int C_INS_XOR		;
	static const unsigned int C_INS_NOT		;
	static const unsigned int C_INS_NEG		;

	/* C_INS_STACK group */
	static const unsigned int C_INS_PUSH		;
	static const unsigned int C_INS_POP		;
	static const unsigned int C_INS_PUSHREGS	;	/* push register context */
	static const unsigned int C_INS_POPREGS	;	/* pop register context */
	static const unsigned int C_INS_PUSHFLAGS	;	/* push all flags */
	static const unsigned int C_INS_POPFLAGS	;	/* pop all flags */
	static const unsigned int C_INS_ENTER		;	/* enter stack frame */
	static const unsigned int C_INS_LEAVE		;	/* leave stack frame */

	/* C_INS_COND group */
	static const unsigned int C_INS_TEST		;
	static const unsigned int C_INS_CMP		;

	/* C_INS_LOAD group */
	static const unsigned int C_INS_MOV		;
	static const unsigned int C_INS_MOVCC		;
	static const unsigned int C_INS_XCHG		;
	static const unsigned int C_INS_XCHGCC	;

	/* C_INS_ARRAY group */
	static const unsigned int C_INS_STRCMP	;
	static const unsigned int C_INS_STRLOAD	;
	static const unsigned int C_INS_STRMOV	;
	static const unsigned int C_INS_STRSTOR	;
	static const unsigned int C_INS_XLAT		;

	/* C_INS_BIT group */
	static const unsigned int C_INS_BITTEST	;
	static const unsigned int C_INS_BITSET	;
	static const unsigned int C_INS_BITCLR	;

	/* C_INS_FLAG group */
	static const unsigned int C_INS_CLEARCF	;	/* clear Carry flag */
	static const unsigned int C_INS_CLEARZF	;	/* clear Zero flag */
	static const unsigned int C_INS_CLEAROF	;	/* clear Overflow flag */
	static const unsigned int C_INS_CLEARDF	;	/* clear Direction flag */
	static const unsigned int C_INS_CLEARSF	;	/* clear Sign flag */
	static const unsigned int C_INS_CLEARPF	;	/* clear Parity flag */
	static const unsigned int C_INS_SETCF		;
	static const unsigned int C_INS_SETZF		;
	static const unsigned int C_INS_SETOF		;
	static const unsigned int C_INS_SETDF		;
	static const unsigned int C_INS_SETSF		;
	static const unsigned int C_INS_SETPF		;
	static const unsigned int C_INS_TOGCF		;	/* toggle */
	static const unsigned int C_INS_TOGZF		;
	static const unsigned int C_INS_TOGOF		;
	static const unsigned int C_INS_TOGDF		;
	static const unsigned int C_INS_TOGSF		;
	static const unsigned int C_INS_TOGPF		;

	/* C_INS_FPU */

	/* C_INS_TRAP */
	static const unsigned int C_INS_TRAP		;		/* generate trap */
	static const unsigned int C_INS_TRAPCC	;		/* conditional trap gen */
	static const unsigned int C_INS_TRET		;		/* return from trap */
	static const unsigned int C_INS_BOUNDS	;		/* gen bounds trap */
	static const unsigned int C_INS_DEBUG		;		/* gen breakpoint trap */
	static const unsigned int C_INS_TRACE		;		/* gen single step trap */
	static const unsigned int C_INS_INVALIDOP	;		/* gen invalid instruction */
	static const unsigned int C_INS_OFLOW		;		/* gen overflow trap */

	/* C_INS_SYSTEM */
	static const unsigned int C_INS_HALT		;		/* halt machine */
	static const unsigned int C_INS_IN		;		/* input form port */
	static const unsigned int C_INS_OUT		;		/* output to port */
	static const unsigned int C_INS_CPUID		;		/* identify cpu */

	/* C_INS_OTHER */
	static const unsigned int C_INS_NOP		;
	static const unsigned int C_INS_BCDCONV	;	/* convert to/from BCD */
	static const unsigned int C_INS_SZCONV	;	/* convert size of operand */
	 
	/* instruction size */
	static const unsigned int C_INS_BYTE      ;   /* operand is  8 bits/1 byte  */
	static const unsigned int C_INS_WORD      ;   /* operand is 16 bits/2 bytes */
	static const unsigned int C_INS_DWORD      ;   /* operand is 32 bits/4 bytes */
	static const unsigned int C_INS_QWORD      ;   /* operand is 64 bits/8 bytes */
	/* instruction modifiers */
	static const unsigned int C_INS_REPZ     ;
	static const unsigned int C_INS_REPNZ    ;  
	static const unsigned int C_INS_LOCK     ; /* lock bus */
	static const unsigned int C_INS_DELAY    ; /* branch delay slot */

	static const unsigned int C_INS_TYPE_MASK	;
	static const unsigned int C_INS_GROUP_MASK	;
	static const unsigned int C_INS_SIZE_MASK   ;
	static const unsigned int C_INS_MOD_MASK    ;
#endif

	x86_instruction() {
		memset( this, 0, sizeof(x86_instruction) );
		defaddr = 4;
		defdata = 4;
		instr_valid = false;
	}

	x86_instruction( void *p ) {
		memset( this, 0, sizeof(x86_instruction) );
		defaddr = 4;
		defdata = 4;
		disassemble( p );
	}

	x86_instruction( char *in_str, int len ) {
		memset( this, 0, sizeof(x86_instruction) );
		defaddr = 4;
		defdata = 4;
		disassemble( (void*)in_str );
	}

	void disassemble( void *p ) {
		memset( this, 0, sizeof(x86_instruction) );
		defaddr = 4;
		defdata = 4;
		instr_valid = false;
		x86_get_instruction( p, this );
	}

	unsigned long to_bytes( void *rbuffer, size_t len ) {
		return x86_put_instruction( (void*)rbuffer, this );
	}

	unsigned long write( void *p ) {
		return x86_put_instruction( p, this );
	}

	char *to_str(char *str, size_t len);

	bool is_valid() {
		if (!instr_valid) update_instr();
		return m_instr.size != 0;
	}

	// ADE32 accessors / mutators

	unsigned int get_len() {
		return len;
	}

	unsigned long get_flags() {
		return flag;
	}

	void set_flags( unsigned long flags ) {
		flag = flags;
		instr_valid = false;
	}

	unsigned long get_addrsize() {
		return addrsize;
	}

	void set_addrsize( unsigned long a ) {
		addrsize = a;
		instr_valid = false;
	}

	unsigned long get_datasize() {
		return datasize;
	}

	void set_datasize( unsigned long d ) {
		datasize = d;
		instr_valid = false;
	}

	unsigned char get_rep() {
		return rep;
	}

	void set_rep( unsigned char c ) {
		rep = c;
		instr_valid = false;
	}

	unsigned char get_seg() {
		return rep;
	}

	void set_seg( unsigned char c ) {
		rep = c;
		instr_valid = false;
	}

	unsigned char get_opcode() {
		return opcode;
	}

	void set_opcode( unsigned char c ) {
		opcode = c;
		instr_valid = false;
	}

	unsigned char get_opcode2() {
		return opcode2;
	}

	void set_opcode2( unsigned char c ) {
		opcode2 = c;
		instr_valid = false;
	}

	unsigned char get_modrm() {
		return modrm;
	}

	void set_modrm( unsigned char c ) {
		modrm = c;
		instr_valid = false;
	}

	unsigned char get_sib() {
		return sib;
	}

	void set_sib( unsigned char c ) {
		sib = c;
		instr_valid = false;
	}

	unsigned char get_addr_u8( int n ) {
		if (n > 7) return 0;
		return addr.b[n];
	}

	void set_addr_u8( unsigned char c, int n ) {
		if (n > 7) return;
		addr.b[n] = c;
		instr_valid = false;
	}

	signed char get_addr_s8( int n ) {
		if (n > 7) return 0;
		return addr.c[n];
	}

	void set_addr_s8( signed char c, int n ) {
		if (n > 7) return;
		addr.c[n] = c;
		instr_valid = false;
	}

	unsigned short get_addr_u16( int n ) {
		if (n > 3) return 0;
		return addr.w[n];
	}

	void set_addr_u16( unsigned short s, int n ) {
		if (n > 3) return;
		addr.w[n] = s;
		instr_valid = false;
	}

	signed short get_addr_s16( int n ) {
		if (n > 3) return 0;
		return addr.s[n];
	}

	void set_addr_s16( signed short s, int n ) {
		if (n > 3) return;
		addr.s[n] = s;
		instr_valid = false;
	}

	unsigned long get_addr_u32( int n ) {
		if (n > 1) return 0;
		return addr.d[n];
	}

	void set_addr_u32( unsigned long l, int n ) {
		if (n > 1) return;
		addr.d[n] = l;
		instr_valid = false;
	}

	signed long get_addr_s32( int n ) {
		if (n > 1) return 0;
		return addr.l[n];
	}

	void set_addr_s32( signed long l, int n ) {
		if (n > 1) return;
		addr.l[n] = l;
		instr_valid = false;
	}

	unsigned char get_data_u8( int n ) {
		if (n > 7) return 0;
		return data.b[n];
	}

	void set_data_u8( unsigned char c, int n ) {
		if (n > 7) return;
		data.b[n] = c;
		instr_valid = false;
	}

	signed char get_data_s8( int n ) {
		if (n > 7) return 0;
		return data.c[n];
	}

	void set_data_s8( signed char c, int n ) {
		if (n > 7) return;
		data.c[n] = c;
		instr_valid = false;
	}

	unsigned short get_data_u16( int n ) {
		if (n > 3) return 0;
		return data.w[n];
	}

	void set_data_u16( unsigned short s, int n ) {
		if (n > 3) return;
		data.w[n] = s;
		instr_valid = false;
	}

	signed short get_data_s16( int n ) {
		if (n > 3) return 0;
		return data.s[n];
	}

	void set_data_s16( signed short s, int n ) {
		if (n > 3) return;
		data.s[n] = s;
		instr_valid = false;
	}

	unsigned long get_data_u32( int n ) {
		if (n > 1) return 0;
		return data.d[n];
	}

	void set_data_u32( unsigned long l, int n ) {
		if (n > 1) return;
		data.d[n] = l;
		instr_valid = false;
	}

	signed long get_data_s32( int n ) {
		if (n > 1) return 0;
		return data.l[n];
	}

	void set_data_s32( signed long l, int n ) {
		if (n > 1) return;
		data.l[n] = l;
		instr_valid = false;
	}

	// LibDis accessors
	const char *get_mnemonic() {
		if (!instr_valid) update_instr();
		return m_instr.mnemonic;
	}

	unsigned int get_mnemonic_flags() {
		if (!instr_valid) update_instr();
		return (unsigned int)m_instr.mnemType;
	}

	const char *get_dest() {
		if (!instr_valid) update_instr();
		return m_instr.dest;
	}

	unsigned int get_dest_flags() {
		if (!instr_valid) update_instr();
		return (unsigned int)m_instr.destType;
	}

	const char *get_src() {
		if (!instr_valid) update_instr();
		return m_instr.src;
	}

	unsigned int get_src_flags() {
		if (!instr_valid) update_instr();
		return (unsigned int)m_instr.srcType;
	}

	const char *get_aux() {
		if (!instr_valid) update_instr();
		return m_instr.aux;
	}

	unsigned int get_aux_flags() {
		if (!instr_valid) update_instr();
		return (unsigned int)m_instr.auxType;
	}

	unsigned int get_size() {
		if (!instr_valid) update_instr();
		return (unsigned int)m_instr.size;
	}

protected:
	static bool initialized;
	static void init();

	int update_instr();

	// ADE32 disasm_struct. Storage must match
	// XXX move this goo into a member?
	unsigned char  defaddr;         // 00
	unsigned char  defdata;         // 01
	unsigned int len;             // 02 03 04 05
	unsigned long flag;            // 06 07 08 09
	unsigned long addrsize;        // 0A 0B 0C 0D
	unsigned long datasize;        // 0E 0F 10 11
	unsigned char  rep;             // 12
	unsigned char  seg;             // 13
	unsigned char  opcode;          // 14
	unsigned char  opcode2;         // 15
	unsigned char  modrm;           // 16
	unsigned char  sib;             // 17
	union {
		unsigned char  b[8];       // 18 19 1A 1B  1C 1D 1E 1F
		unsigned short  w[4];
		unsigned long d[2];
		signed char  c[8];
		signed short s[4];
		signed long  l[2];
	} addr;
	union {
		unsigned char  b[8];       // 20 21 22 23  24 25 26 27
		unsigned short  w[4];
		unsigned long d[2];
		signed char  c[8];
		signed short s[4];
		signed long  l[2];
	} data;

	// For intermediate copies
	char m_bytes[16];
	// LibDisAsm instr struct (extended data)
	struct instr m_instr;
	// delay creation of above member until accessed (optimization)
	bool instr_valid;

}; 

#pragma pack(pop)


#endif // header guard
