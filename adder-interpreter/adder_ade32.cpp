#include <windows.h>

#include "adder.h"

const unsigned long x86_instruction::C_ERROR = 0xFFFFFFFF;
const unsigned long x86_instruction::C_ADDR1 =  0x00000001;
const unsigned long x86_instruction::C_ADDR2 =  0x00000002;
const unsigned long x86_instruction::C_ADDR4 =  0x00000004;
const unsigned long x86_instruction::C_LOCK =  0x00000008;
const unsigned long x86_instruction::C_67    =  0x00000010;
const unsigned long x86_instruction::C_66    =  0x00000020;
const unsigned long x86_instruction::C_REP   =  0x00000040;
const unsigned long x86_instruction::C_SEG   =  0x00000080;
const unsigned long x86_instruction::C_ANYPREFIX = (C_66+C_67+C_LOCK+C_REP+C_SEG);
const unsigned long x86_instruction::C_DATA1 =  0x00000100;
const unsigned long x86_instruction::C_DATA2 =  0x00000200;
const unsigned long x86_instruction::C_DATA4 =  0x00000400;
const unsigned long x86_instruction::C_SIB   =  0x00000800;
const unsigned long x86_instruction::C_ADDR67 = 0x00001000;
const unsigned long x86_instruction::C_DATA66 = 0x00002000;
const unsigned long x86_instruction::C_MODRM = 0x00004000;
const unsigned long x86_instruction::C_BAD    = 0x00008000;
const unsigned long x86_instruction::C_OPCODE2 = 0x00010000;
const unsigned long x86_instruction::C_REL    = 0x00020000;
const unsigned long x86_instruction::C_STOP   = 0x00040000;

#include "ade/ade32.hpp"

BOOL isInitialized = FALSE;

DWORD ade32_flagtable[512];

void init_x86() {
	ade32_init(ade32_flagtable);
}


extern "C" 
ADDERAPI unsigned long x86_get_instruction( void *python_ptr, x86_instruction *op )
{
	if ( !isInitialized ) {
		init_x86();
	}
	try {
		return ade32_disasm( (BYTE*)python_ptr, (disasm_struct*)op, ade32_flagtable );
	} catch (...) {
		return 0;
	}
}

extern "C"
ADDERAPI unsigned long x86_put_instruction( void *python_ptr, x86_instruction *op )
{
	if ( !isInitialized ) {
		init_x86();
	}
	try {
		return ade32_asm( (BYTE*)python_ptr, (disasm_struct*)op );
	} catch (...) {
		return 0;
	}
}
