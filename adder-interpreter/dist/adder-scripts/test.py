import code
from adder import *
from adder.util import stack_frame
import struct
import time
import thread
import sys

# In this example we'll splice into the entry point of this function...
# HANDLE WINAPI CreateFile(
#   _In_      LPCTSTR lpFileName,
#   _In_      DWORD dwDesiredAccess,
#   _In_      DWORD dwShareMode,
#   _In_opt_  LPSECURITY_ATTRIBUTES lpSecurityAttributes,
#   _In_      DWORD dwCreationDisposition,
#   _In_      DWORD dwFlagsAndAttributes,
#   _In_opt_  HANDLE hTemplateFile
# );

class CreateFileW_callback( splice_callback ):
    def __init__( self ):
        splice_callback.__init__( self )

    def run( self, r, s ):
        print "\n---------------------------------\nCreateFileW called"
        print r
        # args are all unsigned ints (or pointers)
        # this format specifier is the same as python's struct module 
        frame = stack_frame( r, "IIIIIII" )
        print "Calling Address: " + str( ptr( frame.return_address ) )
        print "eax: " + str( r.eax )
        # ptr.read_unistrz(x) will read a unicode string of at most x characters from
        # the address associated with ptr
        print "FileName: " + ptr( frame.args[0] ).read_unistrz(1024)
        print "dwDesiredAccess: " +  hex( frame.args[1] )
        print "dwShareMode: " + hex( frame.args[2] )
        print "lpSecurityAttributes: " + str( ptr(frame.args[3]) )
        print "dwCreationDisposition: " + hex( frame.args[4] )
        print "hTemplateFile: " + hex( frame.args[5] )
        self.backtrace( r, 10 )

    def backtrace( self, regs, max_depth ):
        i = 0
        p = ptr( regs.ebp )
        print "Backtrace:"
        # less than max, valid, and aligned
        while i < max_depth and p.can_read() and (p + 8).can_read() : #and p.to_int() & 3:
            print "-- Frame %d --" % (i + 1)
            print "\tebp: 0x%x --" % p.read_int()
            print "\teip: 0x%x --" % (p + 4).read_int()
            p = ptr( p.read_int() )
            i = i + 1

# main code 
CreateConsole("Adder Console")
if not is_hosted_interpreter():
    print "This script must be invoked using adderload.exe"
    raw_input("Press Enter To Exit")
    sys.exit()

# we're looking up an exported function address, 
# but splices work at virtually any instruction boundary.
module = LoadLibrary( 'kernel32' )
# CreateFileW is the wide string (unicode) version of 
# what's called CreateFile in documentation.
# Contemporary windows has an A (ascii) and a W (wide) 
# version of every function, however the A function generally
# just call the W one.
proc = GetProcAddress( module, 'CreateFileW' )
s = splice( proc )
cb = CreateFileW_callback()
# This splice executes the callback *prior* to the instructions 
# where it was placed. __disown__ here lets it be GC'd properly.
s.set_pre_callback( cb.__disown__() )
s.install()
print sys.argv
print "Initialization Complete."
release_host_process()
interact( None, globals() )
print "Waiting for process to shutdown"
wait_for_shutdown()
print "Shutting Down..."
