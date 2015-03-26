/* Utility to test libdisasm. Disassembles from the start of a file.  */
/* Compile with  `gcc -I. -O3 -ggdb -L. -ldisasm testdis.c -o testdis` */

#include <windows.h>

#include <stdio.h>
#include <fcntl.h>
#include <sys/stat.h>
#include <sys/types.h>
#include "libdis.h"

char *sprint_size(int type) {
	int size = type & INS_SIZE_MASK;
	switch (size){
	case INS_QWORD:
		return "qword";
	case INS_DWORD:
		return "dword";
	case INS_WORD:
		return "word";
	case INS_BYTE:
		return "byte";
	case 0:
		return "";
	default:
		return "<undefined>";
	}
	return "<unknown>";
}

char *sprint_opsize(int type) {
	int size = type & OP_SIZE_MASK;
	switch (size){
	case OP_WORD:
		return "dword";
	case OP_HWORD:
		return "word";
	case OP_BYTE:
		return "byte";
	case 0:
		return "";
	default:
		return "";
	}
	return "<unknown>";
}

int main(int argc, char *argv[])
{
	int fTarget, i = 0, n, size;
	unsigned char *buf, out[20];
	void *image;
	off_t curr_pos;
	struct instr curr_inst;
	struct stat tmpStat;
	HMODULE mod = LoadLibrary( "kernel32" );

/*

	if (argc < 2) {
		printf("Usage: %s filename\n", argv[0]);
		return 1;
	}
*/
	disassemble_init(0, ATT_SYNTAX);
//	disassemble_init(0, INTEL_SYNTAX);
	image = GetProcAddress( mod, "CreateFileW" );

	if ((int) image < 1)
		return (-1);
	buf = (unsigned char *) image;
//	close(fTarget);
//	printf("File name: %s\n", argv[1]);

	while (i < 100) {
		memset(&curr_inst, 0, sizeof (struct code));
		/* test invariant */
		size = disasm_invariant( buf + i, 1024 - i, out, 20 );
//		printf("%X\t", i);
		for ( n = 0; n < size; n++ ) {
//			printf("%02X ", out[n]);
		}
//		printf("\t\t\t;invariant bytes (signature)\n");

		/* test code */
//		printf("%X\t", i);
		size = disassemble_address(buf + i, &curr_inst);
		if (size) {
//			for (n = 0; n < 12; n++) {
//				if (n < size)
//					printf("%02X ", buf[i + n]);
//				else
//					printf("   ");
//			}
			printf("%s", curr_inst.mnemonic);
			if (curr_inst.dest[0] != 0)
				if ( (curr_inst.destType & OP_TYPE_MASK ) == OP_PTR  
					|| (curr_inst.destType & OP_TYPE_MASK ) == OP_IMM
					|| (curr_inst.destType & OP_TYPE_MASK ) == OP_EXPR
					|| (curr_inst.destType & OP_TYPE_MASK ) == OP_REL
				) {
					if ( ( curr_inst.destType & OP_TYPE_MASK ) == OP_REL ) 
						printf("\tnear %s %s", sprint_opsize(curr_inst.destType), curr_inst.dest);
					else 
						printf("\t%s %s", sprint_opsize(curr_inst.destType), curr_inst.dest);
				} else
					printf("\t%s", curr_inst.dest);

			if (curr_inst.src[0] != 0)
				if ( (curr_inst.srcType & OP_TYPE_MASK ) == OP_PTR 
					|| (curr_inst.srcType & OP_TYPE_MASK ) == OP_IMM
					|| (curr_inst.srcType & OP_TYPE_MASK ) == OP_EXPR
				) {
					printf(", %s %s", sprint_opsize(curr_inst.srcType), curr_inst.src);
				} else
					printf(", %s", curr_inst.src);
			if (curr_inst.aux[0] != 0)
				printf(", %s", curr_inst.aux);
			printf("\n");
			i += size;
		} else {
			printf("invalid opcode %02X\n", buf[i]);
			i++;
		}
	}
//	munmap(image, tmpStat.st_size);
	disassemble_cleanup();
	return 0;
}
