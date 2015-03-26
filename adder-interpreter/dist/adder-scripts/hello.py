from adder import *
from adder.util import *
import sys

# create a console if we're hosted by a GUI app
CreateConsole("Adder Console")

#boiler plate to kill script if we're run as normal python
if not is_hosted_interpreter():
    print "This script must be invoked using adderload.exe"
    raw_input("Press Enter To Exit")
    sys.exit()
# end boiler plate

# assembly code for our new WinMain
asm_patch = """
pushl $0x0
pushl $@title
pushl $@msg
pushl $0x0
movl $@MessageBoxW, %eax
call %eax
ret
"""
title = u"\u25ba\u25ba Hello From Adder \u25c4\u25c4" # Unicode, just to be fancy...
msg = u"\u2620 Hello World! \u2620"

# good description of PE data structures in MSDN Magazine Feb 2002:
# 'Inside Windows: An In-Depth Look into the Win32 Portable Executable File Format '
m = LoadLibrary( sys.executable )
p = m
# 0x4550 is PE header signature. Multiplied by 2 'cause find_short returns an
# offset of 16 bit values and pointer arithmetic is in bytes
off = p.find_short( 0x4550, 1024 ) * 2 
p += off
p += 20 # IMAGE_FILE_HEADER
p += 20 # offset of entry point in IMAGE_OPTIONAL_HEADER32
entry_point = m + ptr( p.read_int() ) # entrypoint is an RVA so add the base addr
entry_point.set_read_only( False ) # make sure we can write to it

print "Process Entry Point: " + str( entry_point )

m = LoadLibrary( 'user32' )
p = GetProcAddress( m, 'MessageBoxW')
if p == NULL:
    raise RuntimeError('Error. Unable to find MessageBoxW')
# replace markers in the asm code string with the values we want
asm_patch = asm_patch.replace( '@MessageBoxW', str(p) )
asm_patch = asm_patch.replace( '@title', str( ptr( title ) ) )
asm_patch = asm_patch.replace( '@msg', str( ptr( msg ) ) )
print "Assembly:\n" + asm_patch + "\n"
# assemble the code 
ops = asm( asm_patch )
print "Machine code: " + repr( ops )
entry_point.write_bytes( ops )

print sys.executable + " entry-point rewritten. Continuing..."

# Release the host. This will cause the suspended main thread to
# start executing WinMain, which is now our asm_patch.
release_host_process()

# Start an interactive interpreter
interact( None, globals() )

# Input terminated (Ctrl-Z). 
print "Shutting down process..."
sys.exit()