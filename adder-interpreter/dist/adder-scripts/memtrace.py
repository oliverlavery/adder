import code
from adder import *
from adder.util import *
import re
import optparse
import thread
import sys

CreateConsole( version + " (memtrace)" )

if not is_hosted_interpreter():
    print "This script must be invoked using adderload.exe"
    raw_input("Press Enter To Exit")
    sys.exit()
    
splice_list = []

class graph_callback( splice_callback ):    
    def __init__( self, outfile, addr ):
        splice_callback.__init__( self )
        self.outfile = outfile
        self.addr = addr
        
    def __del__( self ):
        splice_callback.__del__( self )
        
    def run( self, r, s ):
        frame = stack_frame( r, "" )
        self.outfile.write( "(call:0x%x,0x%x,%d)\n" % ( self.addr, frame.return_address, thread.get_ident() ) )

def parse_idc( filename ):
    lst = []
    names = {}
    f = file( filename, "r" )
    s = f.readline()    
    while ( s ):
        m = re.match(r'\s*MakeFunction\s*\(\s*(0x[0-9a-fA-F]+)\s*,\s*(0x[0-9a-fA-F]+)\s*\)\s*;?\s*', s)
        if ( m != None ):
            if not names.has_key( eval(m.group(1)) ):
                name = m.group(1)
            else:
                name = names[ eval(m.group(1)) ]
            lst.append( ( eval(m.group(1)), eval(m.group(2)), name ) )
        else:
            m = re.match(r'\s*MakeName\s*\(\s*(0x[0-9a-fA-F]+)\s*,\s*\"(.+)\"\s*\)\s*;?\s*', s)
            if m != None:
                names[ eval(m.group(1)) ] = m.group(2)
        s = f.readline()
    return lst

def make_splices( lst, out_file ):
    global splice_list
    for i in lst:
        cb = graph_callback( out_file, i[0] )
        s = splice( ptr(i[0]) )
        s.set_pre_callback( cb.__disown__() )
        splice_list.append(s)
        
def install_splices():
    global splice_list
    for s in splice_list:
        if s.install() == 0:
            print "Unable to install splice at %s" % ptr( s.get_address() )

def uninstall_splices():
    global splice_list
    for s in splice_list:
        s.uninstall()


def add_library_trace( lst, lib, func ):
    mod = LoadLibrary( lib )
    proc = GetProcAddress( mod, func )
    if proc == NULL:
        print "Unable to find '%s' in DLL '%s'" % ( func, lib )
        return
    p = ptr( proc )
    pp = p + 1024
    lst.append( ( p.to_int(), pp.to_int(), lib + ":" + func ) )
    

# this is the main code

usage = "usage: %prog output-file"
parser = optparse.OptionParser(usage)
(options, args) = parser.parse_args()

if len(args) == 0:
    parser.print_help()
    sys.exit(1)
if len(args) < 1:
    parser.error("need to specify a output-file")

#idcname = args[0]
outname = args[0]
#print idcname + " " + outname

lst = []
#lst = parse_idc( idcname )
out = file( outname, "w" )
##add_library_trace( lst, 'kernel32', 'CreateFileW' )
##add_library_trace( lst, 'kernel32', 'ReadFile' )
##add_library_trace( lst, 'kernel32', 'WriteFile' )
##add_library_trace( lst, 'kernel32', 'CloseHandle' )
##add_library_trace( lst, 'kernel32', 'GetFileInformationByHandle' )
##add_library_trace( lst, 'kernel32', 'CreateFileMappingW' )
##add_library_trace( lst, 'kernel32', 'MapViewOfFile' )
##add_library_trace( lst, 'kernel32', 'MultiByteToWideChar' )
##add_library_trace( lst, 'kernel32', 'UnmapViewOfFile' )
##add_library_trace( lst, 'kernel32', 'GetACP' )
##add_library_trace( lst, 'kernel32', 'DeleteFileW' )
##add_library_trace( lst, 'kernel32', 'SetEndOfFile' )
##add_library_trace( lst, 'kernel32', 'GetUserDefaultLangID' )
##add_library_trace( lst, 'kernel32', 'FormatMessageW' )
###add_library_trace( lst, 'kernel32', 'GlobalLock' )
##add_library_trace( lst, 'kernel32', 'GetTimeFormatW' )
##add_library_trace( lst, 'kernel32', 'GetDateFormatW' )
##add_library_trace( lst, 'kernel32', 'GetUserDefaultLCID' )
##add_library_trace( lst, 'kernel32', 'GetLocalTime' )
###add_library_trace( lst, 'kernel32', 'LoadLibraryA' )
##add_library_trace( lst, 'kernel32', 'GetStartupInfoA' )
###add_library_trace( lst, 'kernel32', 'GlobalFree' )
##add_library_trace( lst, 'kernel32', 'lstrcatW' )
##add_library_trace( lst, 'kernel32', 'FindClose' )
##add_library_trace( lst, 'kernel32', 'FindFirstFileW' )
##add_library_trace( lst, 'kernel32', 'GetFileAttributesW' )
##add_library_trace( lst, 'kernel32', 'lstrcpyW' )
##add_library_trace( lst, 'kernel32', 'lstrcmpW' )
###add_library_trace( lst, 'kernel32', 'LocalFree' )
###add_library_trace( lst, 'kernel32', 'LocalAlloc' )
##add_library_trace( lst, 'kernel32', 'lstrlenW' )
###add_library_trace( lst, 'kernel32', 'LocalUnlock' )
###add_library_trace( lst, 'kernel32', 'LocalLock' )
##add_library_trace( lst, 'kernel32', 'CompareStringW' )
##add_library_trace( lst, 'kernel32', 'FoldStringW' )
##add_library_trace( lst, 'kernel32', 'lstrcmpiW' )
##add_library_trace( lst, 'kernel32', 'GetCurrentProcessId' )
###add_library_trace( lst, 'kernel32', 'GetProcAddress' )
##add_library_trace( lst, 'kernel32', 'lstrcpynW' )
##add_library_trace( lst, 'kernel32', 'LocalSize' )
###add_library_trace( lst, 'kernel32', 'GetLastError' )
###add_library_trace( lst, 'kernel32', 'SetLastError' )
##add_library_trace( lst, 'kernel32', 'WideCharToMultiByte' )
###add_library_trace( lst, 'kernel32', 'LocalReAlloc' )
##add_library_trace( lst, 'kernel32', 'GetModuleHandleA' )
add_library_trace( lst, 'kernel32', 'VirtualAlloc' )
add_library_trace( lst, 'kernel32', 'VirtualAllocEx' )
add_library_trace( lst, 'kernel32', 'VirtualFree' )
add_library_trace( lst, 'kernel32', 'VirtualFreeEx' )
add_library_trace( lst, 'kernel32', 'GlobalAlloc' )
add_library_trace( lst, 'kernel32', 'GlobalFree' )
add_library_trace( lst, 'kernel32', 'LocalAlloc' )
add_library_trace( lst, 'kernel32', 'LocalFree' )

for i in lst:
    out.write( "(fn:0x%x,0x%x,\"%s\")\n" % i )
make_splices( lst, out )
install_splices()
print "Installed %d splices." % len(lst)
release_host_process()
interact(None, locals())
#wait_for_shutdown()
uninstall_splices()
#del splice_list
