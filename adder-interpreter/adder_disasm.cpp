#include "StdAfx.h"
#include "adder.h"

 /* Operand and instruction types */
/*                   Permissions: */
const unsigned int x86_instruction::C_OP_R         =0x001;      /* operand is READ */
const unsigned int x86_instruction::C_OP_W         =0x002;      /* operand is WRITTEN */
const unsigned int x86_instruction::C_OP_X         =0x004;      /* operand is EXECUTED */
/*                   Types: */
const unsigned int x86_instruction::C_OP_UNK       =0x000;      /* unknown operand */     
const unsigned int x86_instruction::C_OP_REG       =0x100;      /* register */
const unsigned int x86_instruction::C_OP_IMM       =0x200;      /* immediate value */
const unsigned int x86_instruction::C_OP_REL       =0x300;      /* relative Address [offset from IP] */
const unsigned int x86_instruction::C_OP_ADDR      =0x400;      /* Absolute Address */
const unsigned int x86_instruction::C_OP_EXPR      =0x500;      /* Address Expression [e.g. SIB byte] */
const unsigned int x86_instruction::C_OP_PTR       =0x600;      /* Operand is an Address containing a Pointer */
const unsigned int x86_instruction::C_OP_OFF       =0x700;      /* Operand is an offset from a seg/selector */
/*                   Modifiers: */
const unsigned int x86_instruction::C_OP_SIGNED    =0x001000;   /* operand is signed */
const unsigned int x86_instruction::C_OP_STRING    =0x002000;   /* operand a string */
const unsigned int x86_instruction::C_OP_CONST     =0x004000;   /* operand is a constant */
const unsigned int x86_instruction::C_OP_EXTRASEG  =0x010000;   /* seg overrides */
const unsigned int x86_instruction::C_OP_CODESEG   =0x020000;
const unsigned int x86_instruction::C_OP_STACKSEG  =0x030000;
const unsigned int x86_instruction::C_OP_DATASEG   =0x040000;
const unsigned int x86_instruction::C_OP_DATA1SEG  =0x050000;
const unsigned int x86_instruction::C_OP_DATA2SEG  =0x060000;
/*                   Size: */
const unsigned int x86_instruction::C_OP_BYTE      =0x100000;   /* operand is 8 bits/1 byte  */
const unsigned int x86_instruction::C_OP_HWORD     =0x200000;   /* operand is .5 mach word (Intel 16 bits) */
const unsigned int x86_instruction::C_OP_WORD      =0x300000;   /* operand is 1 machine word (Intel 32 bits) */
const unsigned int x86_instruction::C_OP_DWORD     =0x400000;   /* operand is 2 mach words (Intel 64 bits) */
const unsigned int x86_instruction::C_OP_QWORD     =0x500000;   /* operand is 4 mach words (Intel 128 bits) */
const unsigned int x86_instruction::C_OP_SREAL     =0x600000;   /* operand is 32 bits/4 bytes */
const unsigned int x86_instruction::C_OP_DREAL     =0x700000;   /* operand is 64 bits/8 bytes */
const unsigned int x86_instruction::C_OP_XREAL     =0x800000;   /* operand is 40 bits/10 bytes */
const unsigned int x86_instruction::C_OP_BCD       =0x900000;   /* operand is 40 bits/10 bytes */            
const unsigned int x86_instruction::C_OP_SIMD      =0xA00000;   /* operand is 128 bits/16 bytes */            
const unsigned int x86_instruction::C_OP_FPENV     =0xB00000;   /* operand is 224 bits/28 bytes */            

/* operand masks */
const unsigned int x86_instruction::C_OP_PERM_MASK =0x0000007;  /* perms are NOT mutually exclusive */
const unsigned int x86_instruction::C_OP_TYPE_MASK =0x0000F00;  /* types are mututally exclusive */
const unsigned int x86_instruction::C_OP_MOD_MASK  =0x00FF000;  /* mods are NOT mutual;y exclusive */
const unsigned int x86_instruction::C_OP_SEG_MASK  =0x00F0000;  /* segs are NOT mutually exclusive */
const unsigned int x86_instruction::C_OP_SIZE_MASK =0x0F00000;  /* sizes are mutually exclusive */

const unsigned int x86_instruction::C_OP_REG_MASK    =0x0000FFFF; /* lower WORD is register ID */
const unsigned int x86_instruction::C_OP_REGTBL_MASK =0xFFFF0000; /* higher word is register type [gen/dbg] */

/* instruction types [groups] */
const unsigned int x86_instruction::C_INS_EXEC		=0x1000;
const unsigned int x86_instruction::C_INS_ARITH		=0x2000;
const unsigned int x86_instruction::C_INS_LOGIC		=0x3000;
const unsigned int x86_instruction::C_INS_STACK		=0x4000;
const unsigned int x86_instruction::C_INS_COND		=0x5000;
const unsigned int x86_instruction::C_INS_LOAD		=0x6000;
const unsigned int x86_instruction::C_INS_ARRAY		=0x7000;
const unsigned int x86_instruction::C_INS_BIT		=0x8000;
const unsigned int x86_instruction::C_INS_FLAG		=0x9000;
const unsigned int x86_instruction::C_INS_FPU		=0xA000;
const unsigned int x86_instruction::C_INS_TRAPS		=0xD000;
const unsigned int x86_instruction::C_INS_SYSTEM		=0xE000;
const unsigned int x86_instruction::C_INS_OTHER		=0xF000;

/* INS_EXEC group */
const unsigned int x86_instruction::C_INS_BRANCH		=INS_EXEC | 0x01;	/* Unconditional branch */
const unsigned int x86_instruction::C_INS_BRANCHCC	=INS_EXEC | 0x02;	/* Conditional branch */
const unsigned int x86_instruction::C_INS_CALL		=INS_EXEC | 0x03;	/* Jump to subroutine */
const unsigned int x86_instruction::C_INS_CALLCC		=INS_EXEC | 0x04;	/* Jump to subroutine */
const unsigned int x86_instruction::C_INS_RET		=INS_EXEC | 0x05;	/* Return from subroutine */
const unsigned int x86_instruction::C_INS_LOOP		=INS_EXEC | 0x06;	/* loop to local label */

/* INS_ARITH group */
const unsigned int x86_instruction::C_INS_ADD 		=INS_ARITH | 0x01;
const unsigned int x86_instruction::C_INS_SUB		=INS_ARITH | 0x02;
const unsigned int x86_instruction::C_INS_MUL		=INS_ARITH | 0x03;
const unsigned int x86_instruction::C_INS_DIV		=INS_ARITH | 0x04;
const unsigned int x86_instruction::C_INS_INC		=INS_ARITH | 0x05;	/* increment */
const unsigned int x86_instruction::C_INS_DEC		=INS_ARITH | 0x06;	/* decrement */
const unsigned int x86_instruction::C_INS_SHL		=INS_ARITH | 0x07;	/* shift right */
const unsigned int x86_instruction::C_INS_SHR		=INS_ARITH | 0x08;	/* shift left */
const unsigned int x86_instruction::C_INS_ROL		=INS_ARITH | 0x09;	/* rotate left */
const unsigned int x86_instruction::C_INS_ROR		=INS_ARITH | 0x0A;	/* rotate right */

/* INS_LOGIC group */
const unsigned int x86_instruction::C_INS_AND		=INS_LOGIC | 0x01;
const unsigned int x86_instruction::C_INS_OR			=INS_LOGIC | 0x02;
const unsigned int x86_instruction::C_INS_XOR		=INS_LOGIC | 0x03;
const unsigned int x86_instruction::C_INS_NOT		=INS_LOGIC | 0x04;
const unsigned int x86_instruction::C_INS_NEG		=INS_LOGIC | 0x05;

/* INS_STACK group */
const unsigned int x86_instruction::C_INS_PUSH		=INS_STACK | 0x01;
const unsigned int x86_instruction::C_INS_POP		=INS_STACK | 0x02;
const unsigned int x86_instruction::C_INS_PUSHREGS	=INS_STACK | 0x03;	/* push register context */
const unsigned int x86_instruction::C_INS_POPREGS	=INS_STACK | 0x04;	/* pop register context */
const unsigned int x86_instruction::C_INS_PUSHFLAGS	=INS_STACK | 0x05;	/* push all flags */
const unsigned int x86_instruction::C_INS_POPFLAGS	=INS_STACK | 0x06;	/* pop all flags */
const unsigned int x86_instruction::C_INS_ENTER		=INS_STACK | 0x07;	/* enter stack frame */
const unsigned int x86_instruction::C_INS_LEAVE		=INS_STACK | 0x08;	/* leave stack frame */

/* INS_COND group */
const unsigned int x86_instruction::C_INS_TEST		=INS_COND | 0x01;
const unsigned int x86_instruction::C_INS_CMP		=INS_COND | 0x02;

/* INS_LOAD group */
const unsigned int x86_instruction::C_INS_MOV		=INS_LOAD | 0x01;
const unsigned int x86_instruction::C_INS_MOVCC		=INS_LOAD | 0x02;
const unsigned int x86_instruction::C_INS_XCHG		=INS_LOAD | 0x03;
const unsigned int x86_instruction::C_INS_XCHGCC		=INS_LOAD | 0x04;

/* INS_ARRAY group */
const unsigned int x86_instruction::C_INS_STRCMP		=INS_ARRAY | 0x01;
const unsigned int x86_instruction::C_INS_STRLOAD	=INS_ARRAY | 0x02;
const unsigned int x86_instruction::C_INS_STRMOV		=INS_ARRAY | 0x03;
const unsigned int x86_instruction::C_INS_STRSTOR	=INS_ARRAY | 0x04;
const unsigned int x86_instruction::C_INS_XLAT		=INS_ARRAY | 0x05;

/* INS_BIT group */
const unsigned int x86_instruction::C_INS_BITTEST	=INS_BIT | 0x01;
const unsigned int x86_instruction::C_INS_BITSET		=INS_BIT | 0x02;
const unsigned int x86_instruction::C_INS_BITCLR		=INS_BIT | 0x03;

/* INS_FLAG group */
const unsigned int x86_instruction::C_INS_CLEARCF	=INS_FLAG | 0x01;	/* clear Carry flag */
const unsigned int x86_instruction::C_INS_CLEARZF	=INS_FLAG | 0x02;	/* clear Zero flag */
const unsigned int x86_instruction::C_INS_CLEAROF	=INS_FLAG | 0x03;	/* clear Overflow flag */
const unsigned int x86_instruction::C_INS_CLEARDF	=INS_FLAG | 0x04;	/* clear Direction flag */
const unsigned int x86_instruction::C_INS_CLEARSF	=INS_FLAG | 0x05;	/* clear Sign flag */
const unsigned int x86_instruction::C_INS_CLEARPF	=INS_FLAG | 0x06;	/* clear Parity flag */
const unsigned int x86_instruction::C_INS_SETCF		=INS_FLAG | 0x07;
const unsigned int x86_instruction::C_INS_SETZF		=INS_FLAG | 0x08;
const unsigned int x86_instruction::C_INS_SETOF		=INS_FLAG | 0x09;
const unsigned int x86_instruction::C_INS_SETDF		=INS_FLAG | 0x0A;
const unsigned int x86_instruction::C_INS_SETSF		=INS_FLAG | 0x0B;
const unsigned int x86_instruction::C_INS_SETPF		=INS_FLAG | 0x0C;
const unsigned int x86_instruction::C_INS_TOGCF		=INS_FLAG | 0x10;	/* toggle */
const unsigned int x86_instruction::C_INS_TOGZF		=INS_FLAG | 0x20;
const unsigned int x86_instruction::C_INS_TOGOF		=INS_FLAG | 0x30;
const unsigned int x86_instruction::C_INS_TOGDF		=INS_FLAG | 0x40;
const unsigned int x86_instruction::C_INS_TOGSF		=INS_FLAG | 0x50;
const unsigned int x86_instruction::C_INS_TOGPF		=INS_FLAG | 0x60;

/* INS_FPU */

/* INS_TRAP */
const unsigned int x86_instruction::C_INS_TRAP		=INS_TRAPS | 0x01;		/* generate trap */
const unsigned int x86_instruction::C_INS_TRAPCC		=INS_TRAPS | 0x02;		/* conditional trap gen */
const unsigned int x86_instruction::C_INS_TRET		=INS_TRAPS | 0x03;		/* return from trap */
const unsigned int x86_instruction::C_INS_BOUNDS		=INS_TRAPS | 0x04;		/* gen bounds trap */
const unsigned int x86_instruction::C_INS_DEBUG		=INS_TRAPS | 0x05;		/* gen breakpoint trap */
const unsigned int x86_instruction::C_INS_TRACE		=INS_TRAPS | 0x06;		/* gen single step trap */
const unsigned int x86_instruction::C_INS_INVALIDOP	=INS_TRAPS | 0x07;		/* gen invalid instruction */
const unsigned int x86_instruction::C_INS_OFLOW		=INS_TRAPS | 0x08;		/* gen overflow trap */

/* INS_SYSTEM */
const unsigned int x86_instruction::C_INS_HALT		=INS_SYSTEM | 0x01;		/* halt machine */
const unsigned int x86_instruction::C_INS_IN			=INS_SYSTEM | 0x02;		/* input form port */
const unsigned int x86_instruction::C_INS_OUT		=INS_SYSTEM | 0x03;		/* output to port */
const unsigned int x86_instruction::C_INS_CPUID		=INS_SYSTEM | 0x04;		/* identify cpu */

/* INS_OTHER */
const unsigned int x86_instruction::C_INS_NOP		=INS_OTHER | 0x01;
const unsigned int x86_instruction::C_INS_BCDCONV	=INS_OTHER | 0x02;	/* convert to/from BCD */
const unsigned int x86_instruction::C_INS_SZCONV		=INS_OTHER | 0x03;	/* convert size of operand */
 
   /* instruction size */
const unsigned int x86_instruction::C_INS_BYTE		=0x10000;   /* operand is  8 bits/1 byte  */
const unsigned int x86_instruction::C_INS_WORD		=0x20000;   /* operand is 16 bits/2 bytes */
const unsigned int x86_instruction::C_INS_DWORD      =0x40000;   /* operand is 32 bits/4 bytes */
const unsigned int x86_instruction::C_INS_QWORD      =0x80000;   /* operand is 64 bits/8 bytes */
   /* instruction modifiers */
const unsigned int x86_instruction::C_INS_REPZ     =0x0100000;
const unsigned int x86_instruction::C_INS_REPNZ    =0x0200000;  
const unsigned int x86_instruction::C_INS_LOCK     =0x0400000; /* lock bus */
const unsigned int x86_instruction::C_INS_DELAY    =0x0800000; /* branch delay slot */

const unsigned int x86_instruction::C_INS_TYPE_MASK		=0xFFFF;
const unsigned int x86_instruction::C_INS_GROUP_MASK		=0x1000;
const unsigned int x86_instruction::C_INS_SIZE_MASK		=0xF0000;
const unsigned int x86_instruction::C_INS_MOD_MASK		=0xFF00000;

bool x86_instruction::initialized = false;

void x86_instruction::init() {
	if ( !x86_instruction::initialized ) {
		disassemble_init( 0, ATT_SYNTAX );
		x86_instruction::initialized = true;
	}
}

int x86_instruction::update_instr( ) {
	int rval;
	if ( !x86_instruction::initialized ) x86_instruction::init();
	memset( &m_instr, 0, sizeof( m_instr ) );
	memset( &m_bytes, 0, sizeof( m_bytes ) );
	write( m_bytes );
	try {
		rval = disassemble_address( (char*)&m_bytes, &m_instr);
		instr_valid = true; // it may be valid & empty if the instruction isn't recognized.
	} catch ( ... ) {
		printf("BUG: exception in x86_instruction::update_instr()\nPlease report this problem.\n");
		rval = 0; // Ack. Ack. Phbbt.
	}
	return rval;
}


char *x86_instruction::to_str(char *str, size_t len) {
	if ( !instr_valid ) update_instr();
	if ( m_instr.size == 0 ) return "<Unrecognized Instruction>";

	if (this->m_instr.src[0]) {
		snprintf(str, len, "%s\t%s", m_instr.mnemonic, m_instr.src);
		if (this->m_instr.dest[0])
			snprintf(str, len, "%s, %s", str, m_instr.dest);
	} else if (this->m_instr.dest[0]) {
		snprintf(str, len, "%s\t%s", m_instr.mnemonic, m_instr.dest);
	} else {
		snprintf(str, len, "%s", m_instr.mnemonic);
	}

	return str;
}

