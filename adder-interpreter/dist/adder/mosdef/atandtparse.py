#!/usr/bin/env python


"""
atandtparse.py

Copyright Dave Aitel 2003
"""
import sys
sys.setrecursionlimit (sys.getrecursionlimit()*2)


VERSION="1.0"

TODO="""

.db

TEST IT ALL

"""

from spark import GenericParser
from spark import GenericASTBuilder
from spark import GenericASTTraversal

from ast import AST

from x86opcodes import x86args
from x86opcodes import intel_order
from x86opcodes import needLongCall

nonterminal = GenericASTBuilder.nonterminal
foldtree = lambda n: getattr(n,'attr',0) or ''.join(map(foldtree,n._kids))

#wee little function for printing strings nicely
def hexprint(s):
    tmp=""
    for c in s:
        tmp+="[0x%2.2x]"%ord(c)
    return tmp

#overwrites a string in place...hard to do in python
def stroverwrite(instring,overwritestring,offset):
    head=instring[:offset]
    #print head
    tail=instring[offset+len(overwritestring):]
    #print tail
    result=head+overwritestring+tail
    return result


def isbyte(anint):
    """
    tests if this int fits into a byte
    """
    if anint>=0 and anint<=256:
        return 1
    if anint<0 and anint>=-128:
        return 1
    return 0
        

def unslashify(value):
    """
    \r -> 0x0d, etc
    """
    replacements=[["\\r","\r"],["\\n","\n"],["\\\\","\\"],["\\0","\0"]]
    for r in replacements:
        value=value.replace(r[0],r[1])
    return value


def atandtpreprocess(data):
    """
    This function's job is to fix up all the .set's and do any other preprocessing
    """
    import re
    datalines=data.split("\n")
    for line in datalines:
        # allows the asm to have comments after instructions
        if line.count(";") != 0:
                old = line
                #print "line contains comments"
                line,misc = line.split(";")
                data = data.replace(old,line)
        line=line.strip()
        if line[:len(".set")]==".set":
            line2=line[4:]
            name=line2.split(",")[0]
            value=line2.split(",")[1]
            name=name.strip()
            value=value.strip()
            #print "Name=%s Value=%s"%(name,value)
            #match a whole word.
            r=re.compile(name+r'([^a-zA-Z0-9])')
            data=data.replace(line,"")
            olddata=data
            #the \1 means replace the last character, so we don't erase it
            data=r.sub(value+r'\1',data)
    
#    print "Returning %s"%data
    return data

    
class attx86parser(GenericASTBuilder):
    def p_start(self, args):
        '''
        file_input ::= file_contents 
        file_contents ::= file_contents stmt 
        file_contents ::= file_contents NEWLINE
        file_contents ::=
        stmt ::= mnemonic argumentlist
        stmt ::= labeldefine
        stmt ::= longdefine number
        stmt ::= asciidefine quotedstring
        stmt ::= bytedefine numberlist
        numberlist ::= number
        numberlist ::= number , numberlist
        labeldefine ::= name :
        argumentlist ::= constant , registerexpression
        argumentlist ::= registerexpression , registerexpression
        argumentlist ::= number
        argumentlist ::= reg
        argumentlist ::= constant , reg
        argumentlist ::= registerexpression , reg
        argumentlist ::= reg , registerexpression
        argumentlist ::= reg , reg
        argumentlist ::= registerexpression
        argumentlist ::= constant
        argumentlist ::= name
        argumentlist ::= 
        registerexpression ::= registerexpressionprefix leftregisterexpression ( rightregisterexpression )
        registerexpressionprefix ::= segreg
        registerexpressionprefix ::= 
        leftregisterexpression ::= - leftcomponent
        leftregisterexpression ::= leftcomponent
        leftregisterexpression ::= leftcomponent - leftcomponent
        leftregisterexpression ::= leftcomponent + leftcomponent
        leftregisterexpression ::= 
        leftcomponent ::= name
        leftcomponent ::= number
        rightregisterexpression ::= reg
        rightregisterexpression ::= reg , reg
        rightregisterexpression ::= reg , reg , number
        rightregisterexpression ::= reg , number
        rightregisterexpression ::= number
        constant ::= $ number
        number ::= hexnumber
        number ::= decnumber
        '''
    
    def typestring(self, token):
        return token.type
    
    def error(self, token):
        raise ValueError("Syntax error at `%s' of type %s (line %s)" % (token.attr, token.type,token.lineno) + "Often this is because the line contains a mnemonic we don't have in our list yet.")
    
def parse(tokens):
    parser = attx86parser(AST,'file_input')
    parsed = parser.parse(tokens)
    return parsed

def showtree(node, depth=0):
    if hasattr(node, 'attr'):
        print "%2d" % depth, " "*depth, '<<'+node.type+'>>',
        try:
            if len(node.attr) > 50:
                print node.attr[:50]+'...'
            else: print node.attr
        except:
            print ""
            #print "Error: attr=%s"%str(node.attr)
    else:
        print "%2d" %depth, "-"*depth, '<<'+node.type+'>>'
        for n in node._kids:
            showtree(n, depth+1)

            
class gastypecheck(GenericASTTraversal):
    """
    Generic GNU Assembler typecheck
    """
    def __init__(self, ast):
        GenericASTTraversal.__init__(self, ast)
        self.postorder()

    def n_reg(self,node):
        #print "Reg is %s"%node.attr
        node.exprType="reg"
        
    def n_registerexpression(self,node):
        #print "Reg expr"
        node.exprType="registerexpressions"
        
    def n_name(self,node):
        node.exprType="name"
        
    def n_constant(self,node):
        node.exprType="constant"

    def n_mnemonic(self,node):
        #print "Mnemonic: %s"%node.attr
        node.exprType="mnemonic"
        
    def n_labeldefine(self,node):
        print "Label Defined: %s"%node[0].attr
        node.exprType="labeldefine"
        
    def n_argumentlist(self,node):
        #construct the argumentlist types
        node.exprType="argumentlist"
        node.argList=[]
        for n in node:
            #just ignore the seperators
            if n.type!=",":
                node.argList.append(n.type)
            
    def n_stmt(self,node):
        if node[0].exprType=="labeldefine":
            #no verification on label definitions
            pass
        elif node[0].exprType=="mnemonic":
            #print "Found mnemonic %s with arguments %s"%(node[0].attr,node[1].argList)
            if not self.validateargs(node[0].attr,node[1].argList):
                raise ValeError("%s is not a valid argument list for %s on line %d"%(node[1].argList,node[0].attr,node[0].lineno))
            
    def validateargs(self,mnemonic,arglist):
        """
        We return 1 by default
        """
        return 1
    
    
class x86typecheck(gastypecheck):
    """
    X86 Gnu Assembler Type Check
    
    """
    
    def __init__(self,ast):
        self.validargs={}
        self.validargs["pop"]=[["reg"]]
        self.validargs["sub"]=[["constant","reg"]]
        self.validargs["call"]=[["name"]]
        self.validargs["movl"]=[['reg', 'reg']]
        self.validargs["subl"]=[['constant', 'reg']]
        self.validargs["mov"]=[['reg', 'reg']]
        self.validargs["lea"]=[['registerexpression', 'reg']]
        self.validargs["push"]=[['reg']]
        self.validargs["xchg"]=[['reg', 'reg']]
        self.validargs["mov"].append(['constant', 'reg'])
        self.validargs["int"]=[['constant']]
        self.validargs["cmpw"]=[['constant', 'registerexpression']]
        self.validargs["jne"]=[['name']]
        self.validargs["cmp"]=[['constant', 'reg']]
        self.validargs["add"]=[['constant', 'reg']]
        self.validargs["movl"].append(['constant', 'registerexpression'])

        gastypecheck.__init__(self,ast)

                    
    def validateargs(self,mnemonic,arglist):
        debug=0
        if debug:
            print "Validating %s %s"%(mnemonic,arglist)
        if self.validargs.has_key(mnemonic):
            args=self.validargs[mnemonic]
        else:
            print "Did not have a valid args list for %s"%mnemonic
            print "self.validargs[\"%s\"]=[%s]"%(mnemonic,arglist)
            return 1
        
        for l in args:
            if l==arglist:
                return 1
        print "Did not find our arglist in the valid args list"
        print "self.validargs[\"%s\"].append(%s)"%(mnemonic,arglist)
        return 0

    
    
class x86generate(GenericASTTraversal):
    """
    Assembles X86 Code
    Repeats some of the work of the validator so we don't need to run validate first necessarally.
    BUGS:
        Assumes 32 bit constants unless explicitly told via mnemonic that it's not 32 bits (eg addb, subb)
    """
    
    def __init__(self, ast):
        self.mnargsDict=x86args
        self.longcalls={}

        
        done=0
        GenericASTTraversal.__init__(self, ast)
        while not done:
            try:
                #print "Trying traversal"
                self.currentMN=""
                self.currentAL=[]
                self.currentVL=[]
                self.tempaddr=None
                self.value=""
                self.calls=0
                self.labels={}
                self.redoDict={}
                self.inredo=0
                self.redocallnum=0
                self.postorder()
                done=1
            except needLongCall:
                #print "New long call at %d"%self.calls
                if self.inredo:
                    self.longcalls[self.redocallnum]=1
                else:
                    self.longcalls[self.calls]=1
                

        #self.value=ast.value

        
        
    def inccall(self):
        if not self.inredo:
            self.calls+=1
        return
    
    def inRedo(self,callnum):
        self.redocallnum=callnum
        self.inredo=1
        return
    
    def outRedo(self):
        self.inredo=0
        return
    
    def needlongcall(self):

        if self.inredo:
            if self.longcalls.has_key(self.redocallnum):
                #print "REDO: %d needs a long call."%self.redocallnum
                return 1
            #print "REDO: %d does not need a long call."%self.redocallnum
            return 0
        elif self.longcalls.has_key(self.calls):
            #print "NORMAL: %d needs a long call."%self.calls
            return 1
        #print "NORMAL: %d does not need a long call."%self.calls
        return 0
        
        
    def addlabel(self,label):
        """
        Adds a label to the current position
        """
        self.labels[label]=self.getLabel("./")
    
    def n_reg(self,node):
        #print "Reg is %s"%node.attr
        node.exprType="reg"
        node.value=node.attr

    def n_longdefine(self,node):
        node.exprType="longdefine"

    def n_asciidefine(self,node):
        node.exprType="asciidefine"
    def n_bytedefine(self,node):
        #numberlist from first arg
        nl=node[0].attr
        for n in nl:
            self.value+=chr(int(n,0))
        
        
    def n_numberlist(self,node):
        node.attr=[]
        if node[0].type=="number":
            node.attr=[node[0].attr]
        else:
            #we have number , numberlist
            node.attr=[node[0].attr]+node[2].attr
            
        
    def n_registerexpressionprefix(self,node):
        node.exprType="segreg"
        if len(node)==1:
            node.segreg=node[0].attr
        else:
            node.segreg=""
            
    def n_segreg(self,node):
        node.exprType="segreg"
        node.value=node.attr
        
    def n_leftcomponent(self,node):
        node.attr=node[0].attr
    
    def n_leftregisterexpression(self,node):
        #generates 2 lists to hold the left side of a register expression
        #one list is for the labels and numbers
        #one list is for the sign of each label or number (+ or -)
        #node.exprType="leftregisterexpression"
        node.labelsandnumbers=[]
        node.additives=[]
        if len(node)==0:
            return
        if node[0].attr!="-":
            node.additives.append("+")
        for n in node:
            #eh? This shouldn't be here, should it?
            #if n.attr == ",":
            #    continue
            if n.attr in ["+","-"]:
                node.additives.append(n.attr)
            else:
                node.labelsandnumbers.append(n.attr)
        
    def n_rightregisterexpression(self,node):
        #need to set up all the register expression variables here for the right side
        node.exprType="rightregisterexpression"
        node.reg1=""
        node.reg2=""
        node.scalefactor=1
        length=len(node)
        node.reg1=node[0].attr
        #print "Length=%d"%length
        if length==5:
            #print "5"
            node.scalefactor=node[4].attr
            node.reg2=node[2].attr
        elif length==3:
            if node[2].exprType=="reg":
                node.reg2=node[2].attr
            else:
                node.scalefactor=node[2].attr
                
    def n_registerexpression(self,node):
        #sets up a dictionary to hold the register expression variables
        #print "Reg expr"
        node.exprType="registerexpression"
        node.regexpressionDict={}
        node.regexpressionDict["labelsandnumbers"]=node[1].labelsandnumbers
        node.regexpressionDict["additives"]=node[1].additives
        node.regexpressionDict["reg1"]=node[3].reg1
        node.regexpressionDict["reg2"]=node[3].reg2
        node.regexpressionDict["scalefactor"]=node[3].scalefactor
        node.regexpressionDict["segreg"]=node[0].segreg
        node.value=node.regexpressionDict
        
    def n_number(self,node):
        node.exprType="number"
        node.attr=node[0].attr
    
    def n_name(self,node):
        node.exprType="name"
        node.value=node.attr
        
    def n_constant(self,node):
        node.exprType="constant"
        node.value=int(node[1][0].attr,0)
        
    def n_argumentlist(self,node):
        #construct the argumentlist types
        node.exprType="argumentlist"
        node.argList=[]
        node.valueList=[]
        for n in node:
            #just ignore the seperators
            if n.type!=",":
                node.argList.append(n.type)
                node.valueList.append(n.value)
                
    def n_mnemonic(self,node):
        #print "Mnemonic: %s"%node.attr
        node.exprType="mnemonic"
    
    def n_labeldefine(self,node):
        #print "Label Defined: %s"%node[0].attr
        node.exprType="labeldefine"    
        #also I need to add this label to the lable list
        if self.isLabelDefined(node[0].attr):
            raise ValueError("ERROR: Duplicate define of label %s"%node[0].attr)
            
        
        self.addlabel(node[0].attr)
        
        #every time a label is defined I need to go through and see if I can fix anything
        #in the redolist
        l=node[0].attr
        if self.redoDict.has_key(l):
            rdict=self.redoDict[l]
            del self.redoDict[l]
            for r in rdict:
                addr=r[0]
                mn=r[1]
                al=r[2]
                vl=r[3]
                length=r[4]
                callnum=r[5]
                #print "Getting a new instruction for %s %s %s"%(mn,al,vl)
                #this will put itself back on the redolist if something else is not defined
                self.tempaddr=addr #+length
                #we store off the self.calls and pretend like we're doing the old instruction now...
                self.inRedo(callnum)
                instr=self.getInstr(mn,al,vl)
                self.outRedo()
                s=self.value[addr:addr+len(instr)]
                s2=s[s.find("\x90"):]
                if s2!="\x90"*(len(s2)):
                    print "WARNING: overwriting bytes that probably need to be there...%s"%hexprint(s)
                    print "WARNING: with these bytes:                                  %s"%hexprint(instr)
                    print "mn=%s vl=%s"%(mn,vl)
                self.value=stroverwrite(self.value,instr,addr)
                #print "Current self.value=%s"%hexprint(self.value)
        #Clear this when we are done
        self.tempaddr=None
        return
            
        

    def n_stmt(self,node):
        if node[0].exprType=="labeldefine":
            #no verification on label definitions
            #need to add this to our labellist
            label=node[0][0].attr
            #print "Label Defined %s at location %d"%(label,len(self.value))
            self.addlabel(label)

        elif node[0].exprType=="mnemonic":
            #print "Found mnemonic %s with arguments %s : %s"%(node[0].attr,
            #                                                  node[1].argList,node[1].valueList)
            mn=node[0].attr.lower()
            argList=node[1].argList
            valueList=node[1].valueList
            self.currentAL=argList
            self.currentVL=valueList
            self.currentMN=mn
            
            instr=self.getInstr(mn,argList,valueList)
            #ADD THIS TO OUR INSTRUCTION STREAM!
            self.value+=instr
            #print "%s is %s"%(mn+str(valueList),hexprint(instr))
        elif node[0].exprType=="asciidefine":
            value=node[1].attr
            #cut the quotes off the ends
            value=value[1:-1]
            value=unslashify(value)
            self.value+=value
        elif node[0].exprType=="longdefine":
            value=int(node[1].attr,0)
            self.value+=intel_order(value)
        else:
            print "I don't know how to handle %s in n_stmt"%node[0].exprType
                
    def isLabelDefined(self,l):
        if l in self.labels:
            return 1
        return 0
        
    def addToRedoList(self,l,length):
        #adds the current instruction to the redo list based on a label
        addr=self.getLabel("./")
        mn=self.currentMN
        vl=self.currentVL
        al=self.currentAL
        calls=self.calls
        if l not in self.redoDict:
            self.redoDict[l]=[]
        self.redoDict[l].append((addr,mn,al,vl,length,calls))
                
                
    def getLabel(self,l):
        if l=="./" and self.tempaddr!=None:
            return self.tempaddr
        if l=="./":
            return len(self.value)
        
        if l not in self.labels:
            return None
        return self.labels[l]

    def getInstr(self,mn,arglist,valuelist):
        """
        gets an instruction from a mnemonic, arglist, and valuelist
        """
        oldarglist=[]
        regbutnotconstantlist=[]
        argList=arglist
        valueList=valuelist
        
        for a in argList:
            oldarglist.append(a)
            regbutnotconstantlist.append(a)
                              

        #first we go through and replace all constants with constant8 if they are small enough
        for i in range(len(argList)):
            if argList[i]=="constant":
                if isbyte(valueList[i]):
                    argList[i]="constant8"

        #ok, now we replace all the registers in the arguments with their actual values
        #this is so we can search for a special argument list that lists actual registers
        regargsL=[]
        for i in range(len(argList)):
            if argList[i]=="reg":
                regargsL.append(valueList[i])
                regbutnotconstantlist[i]=valueList[i]
            else:
                regargsL.append(argList[i])

                
        #print "RegargsL[%s]: %s"%(mn,regargsL)
        args=arglist
        #print "Args[%s]=%s"%(mn,args)
        #print "Values=%s"%(valueList)
        
        if mn not in self.mnargsDict:
            raise ValueError("Unrecognized mnemonic %s!"%mn)
        argsLL=self.mnargsDict[mn]
        found=None
        i=0
        #this little loop goes through and finds which argument list we're using 
        for argsL in argsLL:
            if oldarglist==argsL.arglist:
                if i==0:
                    found=argsL
            if regbutnotconstantlist==argsL.arglist:
                if i==0:
                    found=argsL
                    i=1
            if args==argsL.arglist:
                #print "Found normal arg with constant8 converted"
                if i<3:
                    found=argsL
                    i=2
            if regargsL==argsL.arglist:
                #print "Found regargs"
                #regargs has both the registers and the constants converted, so it
                #is most precice
                found=argsL                    
                i=3

        if found==None:
            raise ValueError( "Did not find an argument list! Some sort of weird error mn=%s args=%s." % (mn,argList) )
        
        #now "found" has the argument list - unless there is an argument with a label
        #that is yet to be defined, we now know everything we need to assemble this instruction
        #if the instruction cannot be assembled now (due to a missing label) then this should
        #(MUST) return some 0x90 padding for itself to fill in later.
        instr=found.get(valueList,context=self)
        return instr
            
            
if __name__=="__main__":
    filename="win32.s"
    try:
        data=open(filename).read()
    except:
        data=open("MOSDEF/"+filename).read()


    data=atandtpreprocess(data)
    import atandtscan
    tokens=atandtscan.scan(data)
    print tokens
    print "-"*50
    tree=parse(tokens)
    #print "-"*50

    #print "-"*50
    #print "Showing tree"
    #showtree(tree)
    #print "-"*50
    
    print "-"*50
    #Typecheck is basically useless since we do real checking when we generate it...
    #print "Doing typecheck"
    #typecheck=x86typecheck(tree)
    #print "-"*50
    print "Doing Generation of Code"
    x=x86generate(tree)
    print "Length of shellcode: %d"%len(x.value)
    print hexprint(x.value)
    
    
    
    
    
    
    
    
    
