import sys, os, time, difflib, optparse, re
functions = []
calls = []
root_strings = []
range_top = None
range_bottom = None

nodenumber = 0
clusternumber = 0

class fn_call:
    def __init__( self, addr, caller):
        global nodenumber
        self.addr = addr
        self.caller = caller
        self.name = "node" + str(nodenumber)
        nodenumber += 1
        self.parent = find_function( caller )
        #assert( self.parent != None )
        self.fn = find_function( addr )
        self.label = self.fn[2]
        self.childstr = ""
        assert( self.fn != None )
        
def find_function( addr ):
    for i in functions:
        if ( addr >= i[0] and addr < i[1] ):
            return i

def read_input( f ):
    global functions
    s = f.readline()
    while (s):
        m = re.match(r'\s*\(call:\s*(0x[0-9a-fA-F]+)\s*,\s*(0x[0-9a-fA-F]+)\s*,\s*([0-9]+)\s*\)\s*', s)
        if m == None:
            m = re.match(r'\s*\(fn:\s*(0x[0-9a-fA-F]+)\s*,\s*(0x[0-9a-fA-F]+)\s*,\"(.*)\"\)\s*', s)
            if ( m == None ):
                return 
            functions.append( ( eval(m.group(1)), eval(m.group(2)), m.group(3) ) )
        else:
            # cheesy way to parse hex digits
            addr = eval(m.group(1))
            caller = eval(m.group(2))
            thread = int(m.group(3))
            calls.append( fn_call( addr, caller ) )
        s=f.readline()

def within_target_range( addr ):
    global range_top, range_bottom
    
    if range_top != None and range_bottom != None:
        if addr >= range_top and addr < range_bottom:
            return True
        else:
            return False
    return True
    

def write_root_node( call ):
    global clusternumber
    global nodenumber
    s = ""
    if ( within_target_range( call.addr ) or call.parent != None and within_target_range( call.parent[0] ) ):
        if len(call.childstr) > 0:
            s +=  "subgraph cluster%d {\n" % clusternumber
            clusternumber += 1
            s += call.childstr
            s += "}\n"

        s +=  call.name + "[label = \"%s\"];\n" % call.label
        if call.parent == None:
            s += "entry%d [label = \"0x%x\",style=dotted];\nentry%d -> %s [style=dotted]\n" % ( nodenumber, call.caller, nodenumber, call.name )
        else:
            s += "entry%d [label = \"%s\"];\nentry%d -> %s [label=\"0x%x\", fontsize=10]\n" % ( nodenumber, call.parent[2], nodenumber, call.name, call.caller )        
        nodenumber += 1
        root_strings.append(s) 

def write_child_node( call, parent ):
    s = call.name + "[label = \"%s\"];\n" % call.label 
    s += parent.name + " -> " + call.name + "[ label=\"" + hex(call.caller) + "\", fontsize=10, weight=10]\n"
    parent.childstr = call.childstr + s + parent.childstr

def build_output( i, parent = None ):
    had_children = False
    call = calls[i]
    i += 1
    if ( call.parent ):
        print "node %d 0x%x parent 0x%x" % (i, call.addr, call.parent[0])
    else:
        print "node %d 0x%x parent <none>" % (i, call.addr)
  
    while ( i < len(calls) and calls[i].parent == call.fn ):
        had_children = True
        i = build_output( i, call )
        print "loop" + str(i)
        if (i > len(calls)):
            break
    if ( parent != None ):
        write_child_node( call, parent )
 
    if parent == None and ( had_children or call.parent != None ):
        write_root_node( call )

    return i


usage = "usage: %prog fromfile tofile top_addr bottom_addr"
parser = optparse.OptionParser(usage)
(options, args) = parser.parse_args()

if len(args) == 0:
    parser.print_help()
    sys.exit(1)
if len(args) < 2:
    parser.error("need to specify a fromfile and tofile")

fromname = args[0]
toname = args[1]
fromfile = file( fromname, "r" )
tofile = file( toname, "w+" )

if len(args) == 4:
    range_top = eval(args[2])
    range_bottom = eval(args[3])
    print range_top
    print range_bottom
    
read_input( fromfile )
i = 0
while i < len(calls):
    i = build_output( i )
    
tofile.write("""
digraph G {
fontname="helvetica";
rankdir=LR;
node [shape=record,width=.1,height=.1];
""")
root_strings.reverse()
for s in root_strings:
    tofile.write( s )
tofile.write("}\n")
