import struct
import code
from adder import *
from adder.mosdef import atandtscan, atandtparse

class stack_frame:
    def __init__( self, regs, format ):
        self.return_address = ptr(regs.esp).read_int()
        frame = ptr( regs.esp + 4 )
        self.args = struct.unpack( format, frame.read_bytes( struct.calcsize(format) ) );    

def dis_fn( addr ):
    p = ptr(addr)
    if not p.can_read():
        raise RuntimeError("Invalid address.")
    i = x86_instruction(p)
    print i
    while ( i.get_mnemonic_flags() & i.C_INS_TYPE_MASK ) != i.C_INS_RET:
        if str(i).startswith("ret"):
            print "Hien! buggy flag."
            break
        p += i.get_len()
        i.disassemble( p )
        print i

def asm( str ):
    tokens=atandtscan.scan(str)
    tree=atandtparse.parse(tokens)
    x=atandtparse.x86generate(tree)
    return x.value    