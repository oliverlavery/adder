import code
from adder import *
from adder.util import stack_frame
import struct
import time
import thread
import sys

class CreateFileW_callback(splice_callback):
    def __init__( self ):
        splice_callback.__init__( self )
#    def __del__( self ):
#        splice_callback.__del__( self )  
    def run( self, r, s ):
        print "\n---------------------------------\nCreateFileW called"
        print r
        # args are all unsigned ints (or pointers)
        # this format specifier is the same as python's struct module uses
        frame = stack_frame( r, "IIIIIII" )
        print "Calling Address: " + str( ptr( frame.return_address ) )
        
        # ptr().read_unistrz(x) will read a unicode string of at most x characters from
        # the address pointed to
        print "FileName: " + ptr( frame.args[0] ).read_unistrz(1024)
        print "dwDesiredAccess: " + hex( frame.args[1] )
        print "dwShareMode: " + hex( frame.args[2] )
        print "lpSecurityAttributes: " + str( ptr(frame.args[3]) )
        print "dwCreationDisposition: " + hex( frame.args[4] )
        print "hTemplateFile: " + hex( frame.args[5] )
#        interact( None, locals())
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
            
# this is the main code 
CreateConsole("Adder Console")
module = LoadLibrary( 'kernel32' )
proc = GetProcAddress( module, 'CreateFileW' )
s = splice( proc )
cb = CreateFileW_callback()
s.set_pre_callback( cb.__disown__() )
s.install()
print sys.argv
print "init done"
release_host_process()
interact( None, globals() )
print "Waiting for process to shutdown"
wait_for_shutdown()
print "Shutting Down..."
#del s