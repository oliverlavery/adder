from adder import *
from adder.util import stack_frame
import win32api
import win32con
import string
from socket import htonl
import sys

CreateConsole("Adder Console")

if not is_hosted_interpreter():
    print "This script must be invoked using adderload.exe"
    raw_input("Press Enter To Exit")
    sys.exit()

def str_guid( d1, d2, d3, d4, d5 ):
    s1 = hex( d1 )
    s1 = s1.replace( "0x", "" )
    s1 = s1.replace( "L", "" )
    pad = ""
    for i in range( 8 - len(s1) ):
        pad += "0"
    s1 = pad + s1
    
    s2 = hex( d2 )
    s2 = s2.replace( "0x", "" )
    s2 = s2.replace( "L", "" )
    pad = ""
    for i in range( 4 - len(s2) ):
        pad += "0"
    s2 = pad + s2

    s3 = hex( d3 )
    s3 = s3.replace( "0x", "" )
    pad = ""
    for i in range( 4 - len(s3) ):
        pad += "0"
    s3 = pad + s3

    s4 = hex( ( ( htonl( d4 ) & 0xFFFF0000 ) >> 16 ) & 0xFFFF )
    s4 = s4.replace( "0x", "" )
    s4 = s4.replace( "L", "" )
    pad = ""
    for i in range( 4 - len(s4) ):
        pad += "0"
    s4 = pad + s4

    d5 = ( ( htonl(d4) & 0xFFFF ) << 32L ) | ( htonl(d5) & 0xFFFFFFFFL )
    s5 = hex( d5 )
    s5 = s5.replace( "0x", "" )
    s5 = s5.replace( "L", "" )
    pad = ""
    for i in range( 12 - len(s5) ):
        pad += "0"
    s5 = pad + s5
    return "{" + s1 + "-" + s2 + "-" + s3 + "-" + s4 + "-" + s5 + "}"

printed = []
class CoGetClassObject_callback(splice_callback):
    def __init__( self ):
        splice_callback.__init__( self )

    def run( self, r, s ):
        global printed
        try:
            frame = stack_frame( r, "I" )
            p = ptr( frame.args[0] )
            d1 = p.read_int()
            p += 4
            d2 = p.read_short()
            p += 2
            d3 = p.read_short()
            p += 2
            d4 = p.read_int()
            p += 4
            d5 = p.read_int()
            guid = str_guid( d1, d2, d3, d4, d5 )
            if guid not in printed:
                try:
                    key = win32api.RegOpenKeyEx( win32con.HKEY_CLASSES_ROOT, "CLSID\\" + guid, 0, win32con.KEY_READ )
                    val = win32api.RegQueryValueEx( key, "" )
                    print guid + " - " + val[0]
                    printed += [ guid ]
                except:
                    print guid + " - <UNREGISTERED>"
                    printed += [ guid ]
        except:
            print sys.exc_info()[0]
            
m = LoadLibrary('ole32')
p = GetProcAddress( m, 'CoCreateInstance' )
s = splice( p )
s.set_pre_callback( CoGetClassObject_callback().__disown__() )
s.install()
p = GetProcAddress( m, 'CoCreateInstanceEx' )
s2 = splice( p )
s2.set_pre_callback( CoGetClassObject_callback().__disown__() )
s2.install()
p = GetProcAddress( m, 'CoGetClassObject' )
s3 = splice( p )
s3.set_pre_callback( CoGetClassObject_callback().__disown__() )
s3.install()
release_host_process()
interact()
wait_for_shutdown()
