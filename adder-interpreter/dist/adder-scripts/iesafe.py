from adder import *
from adder.util import stack_frame
import win32api
import win32con

if not is_hosted_interpreter():
    CreateConsole("Adder Console")
    print "This script must be invoked using adderload.exe"
    raw_input("Press Enter To Exit")
    sys.exit()

# this is a joke, obviously.
# it doesn't work in all cases, and you'll get 404s if there's a URI
# it's just meant to illustrate splices and modifying arguments
# to function calls.
class gethostbyname_callback(splice_callback):
    def __init__( self ):
        splice_callback.__init__( self )
        self.last_name = ""
        self.host = "www.mozilla.org"
        self.last_redir = False

    def run( self, r, s ):
        try:
            frame = stack_frame( r, "I" )
            p = ptr( frame.args[0] )
            name = p.read_strz(256)
            print name
            if self.last_name != name:
                print 'message'
                self.last_name = name
                self.last_redir = False
                n = win32api.MessageBox( 0, "Internet Explorer is trying to connect to " + name +"\nContinuing will allow the owners of that site\nto take full control of your computer.\n\nPress OK to Continue, or Cancel to switch to Mozilla", "Internet Explorer Security", win32con.MB_OKCANCEL | win32con.MB_SYSTEMMODAL )
                if n != win32con.IDOK :
                    print 'redirect'
                    # change the ptr. The current stack_frame object
                    # should support changing arguments.
                    frame = ptr( r.esp + 4 )                    
                    frame.write_int( int( ptr( self.host ) ) )
                    self.last_redir = True                    
            elif self.last_redir :
                frame = ptr( r.esp + 4 )                    
                frame.write_int( int( ptr( self.host ) ) )
            
        except:
            print sys.exc_info()[0]
            raise
            
m = LoadLibrary('ws2_32')
p = GetProcAddress( m, 'gethostbyname' )
s = splice( p )
s.set_pre_callback( gethostbyname_callback().__disown__() )
s.install()

release_host_process()
wait_for_shutdown()
