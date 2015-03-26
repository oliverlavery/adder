#!/usr/bin/env python

"""
x86 opcode list
"""
    
TODO="""
Write test-suite
"""

import re
x86args={}

#wee little function for printing strings nicely
def hexprint(s):
    tmp=""
    for c in s:
        tmp+="[0x%2.2x]"%ord(c)
    return tmp


def dInt(sint):
    """
    Turns sint into an int, hopefully
    python's int() doesn't handle negatives with base 0 well
    """
    s=str(sint)
    if s[0:2]=="0x":
        return int(s,0)
    else:
        return int(s)

reglist=["%eax","%ecx","%edx","%ebx","%esp","%ebp","%esi","%edi"]
reglist2=["%ax","%cx","%dx","%bx","%sp","%bp","%si","%di"]
reglist3=["%al","%cl","%dl","%bl","%ah","%ch","%dh","%bh"]

allshortregs=reglist2+reglist3

regpos={}
i=0
for r in reglist:
        regpos[r]=i
        i+=1

i=0        
for r in reglist2:
        regpos[r]=i
        i+=1
        
i=0        
for r in reglist3:
        regpos[r]=i
        i+=1

regpos["needsib"]=4
regpos["disp32"]=5

def opc(op,oplist):
        if op in x86args:
                pass
        else:
                x86args[op]=[]
        x86args[op].append(oplist)                

def getAllMnemonics():
    return x86args.keys()

#format is ([arglist],opcode,column,argsize) 
#valid values for column are "" (for n/a), r (for by dest register), and 0-7 for hardcoded

#the ss bits from a scale factor
ssfromscale={}
ssfromscale[1]=0
ssfromscale[2]=1
ssfromscale[4]=2
ssfromscale[8]=3


#int to intelordered string conversion
def intel_order(myint):
    #struct.pack is non-intuitive for non-python programers, which is why I do this sort of thing.
    #it's for people who wish they were using perl, imo. <LH@$! :>
    str=""
    a=chr(myint % 256)
    myint=myint >> 8
    b=chr(myint % 256)
    myint=myint >> 8
    c=chr(myint % 256)
    myint=myint >> 8
    d=chr(myint % 256)
    
    str+="%c%c%c%c" % (a,b,c,d)
    return str

def intel_byte(myint):
    #used to make negative numbers work as a byte
    if myint<0:
        tmp=chr(256-abs(myint))
    else:
        tmp=chr(myint)
    return tmp

def intel_2byte(myint):
    #used to do 2 byte "words"
    a=chr(myint % 256)
    myint=myint >> 8
    b=chr(myint % 256)
    str="%c%c"%(a,b)
    return str

def IsInt( str ):
   """
   Checks for integer, hex or no
   """
   try:
      num = int(str,0)
      return 1
   except ValueError:
      return 0

class needLongCall(Exception): pass
    

class x86mnemonic:
    def __init__(self,arglist,opcode,column,columnloc,argsize,effectiveaddressloc,needprefix=1):
        self.arglist=arglist
        self.opcode=opcode
        self.column=column
        self.columnloc=columnloc
        self.argsize=argsize
        self.prepend="" #set if we encounter %fs: in a register expression
        #effectiveaddress is the index into the arglist for the modrm row
        self.effectiveaddressloc=effectiveaddressloc
        self.needprefix=needprefix

    def get(self,valuelist,context=None):
        tmp=""
        self.prepend=""
        self.modrm=self.getModRM(valuelist,context)
        #print "modrm=%s"%hexprint(self.modrm)
        self.argument=self.getArgument(valuelist,context)
        #print "Arg=%s"%hexprint(self.argument)

        tmp+=self.opcode
        #print "OPCODE=%s"%hexprint(self.opcode)
        tmp+=self.modrm
        tmp+=self.argument
        tmp=self.prepend+tmp
        return tmp
    
    
    def getModRM(self,valuelist,context=None):
        #print "Inside getModRM Valuelist=%s"%valuelist
        column=self.column
        if column=="":
            #we don't need a ModRM byte
            return ""
        if column=="r":
            #get the position of this register in the column list
            #if you get an error here, your columnloc is pointing to a registerexpression...
            additive=regpos[valuelist[self.columnloc]]
        else:
            additive=int(self.column)
        #now we need to find the now
        if self.arglist[self.effectiveaddressloc]=="reg" \
            or self.arglist[self.effectiveaddressloc] in reglist \
            or self.arglist[self.effectiveaddressloc] in reglist2 \
            or self.arglist[self.effectiveaddressloc] in reglist3:
            #print 'Handling reg'
            rp=regpos[valuelist[self.effectiveaddressloc]]
            additive=additive*8
            base=64*3
            row=base+rp
            #print "Row=%2.2x attitive=%d"%(row,additive)
            return chr(row+additive)
        elif self.arglist[self.effectiveaddressloc]=="registerexpression":
            #print "Parsing register expression"
            if context==None:
                print "Cannot get argument for a registerexpression with no context, sorry"
                return ""
                
            registerexpression=valuelist[self.effectiveaddressloc]
            #print "Regexp=%s"%registerexpression
            #a register expression needs to get parsed.
            #you can have label+/-label+/-number(register[,[register,]number])
            #print "Parsing registerexpression: %s"%registerexpression
            newlabels=[]
            
            #add any prefix needed
            if registerexpression["segreg"]=="%fs:":
                if not self.prepend.count("\x64"):
                    self.prepend+="\x64"
                
                    
            #print "reg2=%s scale=%s reg1=%s"%(registerexpression["reg2"],registerexpression["scalefactor"],registerexpression["reg1"])
            if registerexpression["reg2"]!="" or registerexpression["scalefactor"]!=1 \
               or registerexpression["reg1"]=="%esp":
                eaddress="needsib"
            elif IsInt(registerexpression["reg1"]):
                eaddress="disp32"
            else:
                eaddress=registerexpression["reg1"]
                
            for l in registerexpression["labelsandnumbers"]:
                loc=context.getLabel(l)
                #print "Here"
                if loc!=None:
                    #print "Found location %s at %s"%(l,loc)
                    newlabels.append(loc)
                    continue
                try:
                    l=int(l,0)
                    newlabels.append(l)
                except:
                    #print "Could not find %s as a label or number!"%l
                    context.addToRedoList(l,self.argsize)
                    ##TODO WE NEED TO CALCULATE THIS VALUE BETTER!
                    #+1 for modrm byte
                    oplen=len(self.prepend)+self.argsize+1 
                    if eaddress=="needsib":
                        oplen+=1
                    return "\x90"*(oplen)


            leftresult=0
            i=0
            for l in newlabels:
                if registerexpression["additives"][i]=="+":
#                    print 'pos '+ str(l)
                    leftresult+=l
                else:
                    print 'neg '+ str(l)
                    leftresult+=l
                i+=1
                    
            #print "Result=%s"%leftresult
            
            if leftresult==0:
                modbits=0
                #special case for ebp here
                if registerexpression["reg1"]=="%ebp":
                    addrarg=chr(0)
                else:
                    addrarg=""
            elif abs(leftresult)<128:
                #we are a 8 bit displacement
                modbits=1
                #handle negatives here
                if leftresult<0:
                    addrarg=chr(128-abs(leftresult))
                else:
                    addrarg=chr(leftresult)
            else:
                #32 bit displacement
                modbits=2
                addrarg=intel_order(leftresult)
                
                
            #now we have the rmbits and the modbits
            rmbits=regpos[eaddress]
            modrm=chr((modbits<<6)+(additive<<3)+rmbits)
            #print "ModRM Byte=%s"%hexprint(modrm)
            if eaddress=="needsib":
                ss=ssfromscale[dInt(registerexpression["scalefactor"])]
                if registerexpression["scalefactor"]!=1 and registerexpression["reg2"]=="":
                    basebits = 5
                    indexbits=regpos[registerexpression["reg1"]]
                else:
                    if registerexpression["reg2"]=="%esp":
                        print "ERROR: esp is not allowed to be a index register!"
                    basebits=regpos[registerexpression["reg1"]]
                    if registerexpression["reg2"]=="":
                        #we are (esp)
                        indexbits=4
                    else:
                        indexbits=regpos[registerexpression["reg2"]]
                sib=chr((ss<<6)+(indexbits<<3)+basebits)
            elif eaddress=="disp32":
                addrarg=intel_order(int(registerexpression["reg1"],0))
                sib=""
            else:
                sib=""
            return modrm+sib+addrarg
            
        elif self.arglist[self.effectiveaddressloc]=="constant":
            #movl 1,($1)
            #print "Constant location detected in a register expression."
            return "\x05"+intel_order(valuelist[self.effectiveaddressloc])
        else:
            print "ERROR: Was not able to produce a modrm for %s"%self.arglist[self.effectiveaddressloc]
            return ""
        print "How did I get here? effiective address is %s"%(self.arglist[self.effectiveaddressloc])
        return ""
                    
    def getArgument(self,valuelist,context=None):
        i=0
        tmp=""
        #print "constant getargument"
        for a in self.arglist:
            if a not in ["constant","constant8"]:
                i+=1
                continue
            if self.argsize == 4:
                #32 bit contant
                tmp+=intel_order(int(str(valuelist[i]),0))
            if self.argsize == 1:
                #8 bit constant
                #print "Value: %s"%valuelist[i]
                tmp+=intel_byte(int(str(valuelist[i]),0))
            if self.argsize == 2:
                #word size, odd.
                tmp+=intel_2byte(int(str(valuelist[i]),0))
                if self.needprefix and not self.prepend.count("\x66"):
                    self.prepend=chr(0x66)
            i+=1

        #we need to add the 16 bit prefix if we are doing a mov for a word ptr (16 bits..)
        for a in valuelist:
            if a in reglist2:
                if self.needprefix and not self.prepend.count("\x66"):
                    self.prepend=chr(0x66)

        return tmp
                                            
class call(x86mnemonic):
    #calls and jumps are annoying
        
    def __init__(self,arglist,shortopcode,shortargsize,longopcode,longargsize,column,columnloc,effectiveaddressloc):
        #we default to short.
        x86mnemonic.__init__(self,arglist,shortopcode,column,columnloc,shortargsize,effectiveaddressloc)
        self.shortopcode=shortopcode
        self.shortargsize=shortargsize
        self.longopcode=longopcode
        self.longargsize=longargsize
        self.debug=0
        
    
    def getArgument(self,valuelist,context=None):
        """
        our argument is a label ("name") so we need to check to see if it is resolved.
        If it IS resolved, our job is simple
        If it IS NOT resolved, our job is quite complex
        In this, we handle single labels, not register expressions with labels.
        """
        #print "***Self.argsize=%d"%self.argsize        
        #print "self.arglist[0]=%s"%self.arglist[0]

        if context==None:
            print "Cannot get argument for a call with no context, sorry"
            return None
        #increment the context's call number
        context.inccall()
        #here we adjust in case we need a long call and we know it
        if context.needlongcall():
            self.argsize=self.longargsize
            self.opcode=self.longopcode
        else:
            self.argsize=self.shortargsize
            self.opcode=self.shortopcode
 
        if self.arglist[0] in ["constant","constant8"]:
            if self.argsize==4:
                return intel_order(dInt(valuelist[0]))
        
            if self.argsize==1:
                #print "valuelist[0]=%s"%valuelist[0]
                v=dInt(valuelist[0])
                a=abs(v)
                if a>128:
                    raise needLongCall
                return intel_byte(v)
                  
            
        if self.arglist[0]=="name":
            l=valuelist[0]
            if not context.isLabelDefined(l):
                #add 1 for sib
                length=self.argsize
                context.addToRedoList(l,length)
                #return some filler nops
                if self.debug:
                    print "Label %s was not defined! Argsize=%d"%(l,self.argsize)
                return "\x90"*(length) 
            
            #if we got here, all our labels are defined
            #get location of current instruction
            addr=context.getLabel("./")+len(self.opcode)+len(self.modrm)+self.argsize
            #calls and jumps
            dest=context.getLabel(l)
            delta=dest-addr
            if self.argsize==1:
                a=abs(delta)
                if self.debug:
                    print "A=%d"%a
                if a>128:
                    if self.debug:
                        print "I need a long call!"
                    raise needLongCall
                
            #return 4 bytes in intel order
            if self.debug:
                print "jmp/call found to %s. current=%d dst=%d delta=%d"%(l,addr,dest,delta)
            if self.argsize==4:
                d= intel_order(delta)
                if self.debug:
                    if l=="exitthread":
                        print "VL=%s"%valuelist
                        print "d=%s"%hexprint(d)
                return d
            else:
                #we are a short call or short jmp
                return intel_byte(delta)
        
        if self.arglist[0]=="registerexpression":
            #we handle this as a ModRM
            return ""
        if self.arglist[0]=="reg":
            #we handle this as a ModRM
            return ""
#END CALL FUNCTION





opc("add",x86mnemonic(['constant', '%al'],"\x04","",None,1,-1))
opc("addb",x86mnemonic(['constant', '%al'],"\x04","",None,1,-1))
opc("add",x86mnemonic(['constant', '%eax'],"\x05","",None,4,-1))
opc("addl",x86mnemonic(['constant', '%eax'],"\x05","",None,4,-1))

opc("add",x86mnemonic(['constant', 'reg'],"\x81","0",None,4,1))
opc("add",x86mnemonic(['constant', 'registerexpression'],"\x81","0",None,4,1))
opc("addl",x86mnemonic(['constant', 'reg'],"\x81","0",None,4,1))
opc("addl",x86mnemonic(['constant', 'registerexpression'],"\x81","0",None,4,1))

opc("add",x86mnemonic(['constant8', 'reg'],"\x83","0",None,1,1))
opc("addb",x86mnemonic(['constant8', 'registerexpression'],"\x83","0",None,1,1))
opc("add",x86mnemonic(["registerexpression","reg"],"\x03","r",1,4,0))
opc("add",x86mnemonic(["reg","registerexpression"],"\x01","r",0,4,1))
opc("addl",x86mnemonic(["registerexpression","reg"],"\x03","r",1,4,0))
opc("addl",x86mnemonic(["reg","reg"],"\x03","r",1,4,0))
opc("add",x86mnemonic(["reg","reg"],"\x03","r",1,4,0))
opc("addl",x86mnemonic(["reg","registerexpression"],"\x01","r",0,4,1))
for r in allshortregs:
    opc("addb",x86mnemonic(["registerexpression",r],"\x02","r",1,4,0))

#SUB        
opc("sub",x86mnemonic(['constant','%al'],"\x2c","",None,1,-1))
opc("sub",x86mnemonic(['constant','%eax'],"\x2d","",None,4,-1))
opc("sub",x86mnemonic(['constant','reg'],"\x81","5",1,4,1))
opc("subl",x86mnemonic(['constant','reg'],"\x81","5",1,4,1))
opc("sub",x86mnemonic(['constant8','reg'],"\x83","5",1,1,1))
opc("sub",x86mnemonic(["reg","reg"],"\x2b","r",1,4,0))
opc("subl",x86mnemonic(["reg","reg"],"\x2b","r",1,4,0))

#CALL
opc("call",call(['name'],"\xe8",4,"\xe8",4,"",None,-1))
opc("call",call(['constant'],"\xe8",4,"\xe8",4,"",None,-1))

opc("call",call(['registerexpression'],"\xff",4,"\xff",4,"2",None,0))
opc("call",call(['reg'],"\xff",1,"\xff",1,"2",4,0))

for r in reglist:
    opc("pop",x86mnemonic([r],chr(0x58+regpos[r]),"",None,0,-1))
    opc("popl",x86mnemonic([r],chr(0x58+regpos[r]),"",None,0,-1))
    opc("push",x86mnemonic([r],chr(0x50+regpos[r]),"",None,0,-1))
    opc("pushl",x86mnemonic([r],chr(0x50+regpos[r]),"",None,0,-1))


opc("push",x86mnemonic(["constant"],chr(0x68),"",None,4,-1))
opc("pushl",x86mnemonic(["constant"],chr(0x68),"",None,4,-1))
opc("pushl",x86mnemonic(["constant8"],chr(0x6a),"",None,1,-1))
opc("push",x86mnemonic(["constant8"],chr(0x6a),"",None,1,-1))
opc("pushl",x86mnemonic(["registerexpression"],chr(0xff),"6",None,4,0))


for r in reglist:
    opc("mov",x86mnemonic(["constant",r],chr(0xb8+regpos[r]),"",None,4,1))
    opc("movl",x86mnemonic(["constant",r],chr(0xb8+regpos[r]),"",None,4,1))

for r in reglist2:
    opc("movw",x86mnemonic(["constant",r],chr(0xb8+regpos[r]),"",None,2,1))

for r in allshortregs:
    opc("movb",x86mnemonic(["constant8",r],chr(0xb0+regpos[r]),"",None,1,1))
    opc("mov",x86mnemonic(["constant8",r],chr(0xb0+regpos[r]),"",None,1,1))

opc("mov",x86mnemonic(["constant","reg"],chr(0xc7),"0",None,4,1))
opc("movl",x86mnemonic(["constant","reg"],chr(0xc7),"0",None,4,1))
opc("mov",x86mnemonic(["constant","registerexpression"],chr(0xc7),"0",None,4,1))
opc("movl",x86mnemonic(["constant","registerexpression"],chr(0xc7),"0",None,4,1))
for r in reglist:
    for r2 in reglist:
        opc("mov",x86mnemonic([r,r2],chr(0x8b),"r",1,4,0))
        opc("movl",x86mnemonic([r,r2],chr(0x8b),"r",1,4,0))
    
    opc("mov",x86mnemonic(["registerexpression",r],chr(0x8b),"r",1,4,0))
    opc("movl",x86mnemonic(["registerexpression",r],chr(0x8b),"r",1,4,0))
    opc("mov",x86mnemonic([r,"registerexpression"],chr(0x89),"r",0,4,1))
    opc("movl",x86mnemonic([r,"registerexpression"],chr(0x89),"r",0,4,1))

    #for 16 bit movs
    #opc("mov",x86mnemonic(["registerexpression",r],chr(0x8b),"r",0,2,1))
    opc("movw",x86mnemonic(["registerexpression",r],chr(0x8b),"r",1,2,0))

opc("mov",x86mnemonic(["registerexpression","reg"],chr(0x8b),"r",1,4,0))

#for r in reglist2:
#    opc("movw",x86mnemonic(["constant",r],chr(0xb8+regpos[r]),"",0,2,1))
#    opc("movw",x86mnemonic(["constant8",r],chr(0xb8+regpos[r]),"",0,2,1))

for r in reglist3:
    for r2 in reglist3:
        opc("mov",x86mnemonic([r2,r],chr(0x8a),"r",0,1,1))
        opc("movb",x86mnemonic([r2,r],chr(0x8a),"r",0,1,1))
        #what about b3?
        #opc("movb",x86mnemonic(["constant8",r2],chr(0xc6),"0",None,1,1))

    opc("mov",x86mnemonic(["constant8",r],chr(0xc6),"0",None,1,1))
    #What about 0xb0?
    #opc("movb",x86mnemonic(["constant8",r],chr(0xc6),"0",None,1,1))
    #opc("movb",x86mnemonic(["constant8",r],chr(0xb0+regpos[r]),"",None,1,1))
    opc("mov",x86mnemonic(["constant8","registerexpression"],chr(0xc6),"0",None,1,1))
    opc("movb",x86mnemonic(["constant8","registerexpression"],chr(0xc6),"0",None,1,1))
    opc("mov",x86mnemonic(["registerexpression",r],chr(0x8a),"r",1,1,0))
    opc("movb",x86mnemonic(["registerexpression",r],chr(0x8a),"r",1,1,0))
    opc("mov",x86mnemonic([r,"registerexpression"],chr(0x88),"r",0,1,1))
    opc("movb",x86mnemonic([r,"registerexpression"],chr(0x88),"r",0,1,1))

opc("lea",x86mnemonic(["registerexpression","reg"],chr(0x8d),"r",1,4,0))
opc("leal",x86mnemonic(["registerexpression","reg"],chr(0x8d),"r",1,4,0))

#How to add a new instruction to this list
#1. Go to the intel reference for x86 and find the page with the instruction on it - probably best
#   is to just binary search, rather than using find functionality, although that also works
#2. If the instruction looks like 90+rd or has named registers in it (like EAX)
#   then you have to special case them. 
#3. for a /r you use "r" as the register, and the register column location in the argument list
#   needs to be put next
#   Put whatever the memory address argument is as the OTHER argument (i.e. if you have "r",1,whatever,X
#   then X must be 0, and if you have "r",0, then X is 1.
#4. for a /[0-9] you do the same, but hardcode the number instead of r. Column location is None.
#5. If you don't need a second byte, then just use "" for the column
#6. Ignore the 16 bit operations

for r in reglist:
    opc("xchg",x86mnemonic(["reg","%eax"],chr(0x90+regpos[r]),"",0,2,1))
    opc("xchg",x86mnemonic(["%eax","reg"],chr(0x90+regpos[r]),"",0,2,1))

for r in allshortregs:
    opc("xchg",x86mnemonic(["registerexpression",r],chr(0x86),"r",1,2,0))
    opc("xchg",x86mnemonic([r,"registerexpression"],chr(0x86),"r",0,2,1))

opc("xchg",x86mnemonic(["reg","registerexpression"],chr(0x87),"r",0,2,1))
opc("xchg",x86mnemonic(["registerexpression","reg"],chr(0x87),"r",1,2,0))
opc("xchg",x86mnemonic(["reg","reg"],chr(0x87),"r",0,2,1))

#if int 3, then we need cc opcode with no arg- - not handled properly here.
#Probably have to hardcode a check for the constant itself. That would suck,
#so you'll just have to use int3 instead
opc("int",x86mnemonic(["constant8"],chr(0xcd),"",0,1,1))
opc("int3",x86mnemonic([],chr(0xcc),"",None,0,-1))

opc("cmp",x86mnemonic(["constant8","%al"],chr(0x3c),"",None,1,-1))
opc("cmpb",x86mnemonic(["constant8","%al"],chr(0x3c),"",None,1,-1))
opc("cmp",x86mnemonic(["constant","%eax"],chr(0x3d),"",None,1,-1))
opc("cmpl",x86mnemonic(["constant","%eax"],chr(0x3d),"",None,4,-1))
opc("cmpw",x86mnemonic(["constant","%eax"],chr(0x3d),"",None,2,-1))

opc("cmp",x86mnemonic(["constant8","registerexpression"],chr(0x80),"7",None,1,1))
opc("cmpb",x86mnemonic(["constant8","registerexpression"],chr(0x80),"7",None,1,1))

for r in allshortregs:
    opc("cmp",x86mnemonic(["constant8",r],chr(0x80),"7",None,1,1))
    opc("cmpb",x86mnemonic(["constant8",r],chr(0x80),"7",None,1,1))

    opc("cmp",x86mnemonic(["registerexpression",r],chr(0x38),"r",1,1,0))
    opc("cmpb",x86mnemonic(["registerexpression",r],chr(0x38),"r",1,1,0))
    opc("cmpb",x86mnemonic(["reg",r],chr(0x38),"r",0,1,1))
    opc("cmp",x86mnemonic([r,"registerexpression"],chr(0x3a),"r",0,1,1))
    opc("cmpb",x86mnemonic([r,"registerexpression"],chr(0x3a),"r",0,1,1))
    #TODO: CHECK THIS:
    for r2 in allshortregs:
        opc("cmpb",x86mnemonic([r,r2],chr(0x3a),"r",1,1,0))
    
opc("cmp",x86mnemonic(["constant8","reg"],chr(0x83),"7",None,1,1))
opc("cmpl",x86mnemonic(["constant8","reg"],chr(0x83),"7",None,1,1))
opc("cmp",x86mnemonic(["constant8","registerexpression"],chr(0x83),"7",None,1,1))

opc("cmp",x86mnemonic(["constant","reg"],chr(0x81),"7",None,4,1))
opc("cmpl",x86mnemonic(["constant","reg"],chr(0x81),"7",None,4,1))
opc("cmpw",x86mnemonic(["constant","reg"],chr(0x81),"7",None,2,1))
opc("cmp",x86mnemonic(["constant","registerexpression"],chr(0x81),"7",None,4,1))
opc("cmpl",x86mnemonic(["constant","registerexpression"],chr(0x81),"7",None,4,1))
opc("cmpw",x86mnemonic(["constant","registerexpression"],chr(0x81),"7",None,2,1))

opc("cmp",x86mnemonic(["reg","registerexpression"],chr(0x39),"r",0,4,1))
opc("cmp",x86mnemonic(["reg","reg"],chr(0x39),"r",0,4,1))
opc("cmpl",x86mnemonic(["reg","registerexpression"],chr(0x39),"r",0,4,1))
opc("cmpl",x86mnemonic(["reg","reg"],chr(0x39),"r",0,4,1))
opc("cmpw",x86mnemonic(["reg","registerexpression"],chr(0x39),"r",0,4,1))

opc("cmp",x86mnemonic(["registerexpression","reg"],chr(0x3b),"r",1,4,0))
opc("cmpl",x86mnemonic(["registerexpression","reg"],chr(0x3b),"r",1,4,0))
opc("cmpw",x86mnemonic(["registerexpression","reg"],chr(0x3b),"r",1,4,0))

#All the jumps. Sheesh
        
opc("ja",call(["constant"],chr(0x77),1,"\x0f\x87",4,"",None,-4))
opc("jae",call(["constant"],chr(0x73),1,"\x0f\x83",4,"",None,-4))
opc("jb",call(["constant"],chr(0x72),1,"\x0f\x82",4,"",None,-4))
opc("jbe",call(["constant"],chr(0x76),1,"\x0f\x86",4,"",None,-4))
opc("jcxz",call(["constant"],chr(0xe3),1,chr(0xe3),1,"",None,-4))
opc("jecxz",call(["constant"],chr(0xe3),1,chr(0xe3),1,"",None,-4))
opc("jc",call(["constant"],chr(0x72),1,"\x0f\x82",4,"",None,-4))
opc("je",call(["constant"],chr(0x74),1,"\x0f\x84",4,"",None,-4))
opc("jg",call(["constant"],chr(0x7f),1,"\x0f\x8f",4,"",None,-4))
opc("jge",call(["constant"],chr(0x7d),1,"\x0f\x8d",4,"",None,-4))
opc("jl",call(["constant"],chr(0x7c),1,"\x0f\x8c",4,"",None,-4))
opc("jle",call(["constant"],chr(0x7e),1,"\x0f\x8e",4,"",None,-4))
opc("jna",call(["constant"],chr(0x76),1,"\x0f\x86",4,"",None,-4))
opc("jnae",call(["constant"],chr(0x72),1,"\x0f\x82",4,"",None,-4))
opc("jnb",call(["constant"],chr(0x73),1,"\x0f\x83",4,"",None,-4))
opc("jnbe",call(["constant"],chr(0x77),1,"\x0f\x87",4,"",None,-4))
opc("jnc",call(["constant"],chr(0x73),1,"\x0f\x83",4,"",None,-4))
opc("jne",call(["constant"],chr(0x75),1,"\x0f\x85",4,"",None,-4))
opc("jng",call(["constant"],chr(0x7e),1,"\x0f\x8e",4,"",None,-4))
opc("jnge",call(["constant"],chr(0x7c),1,"\x0f\x8c",4,"",None,-4))
opc("jnl",call(["constant"],chr(0x7d),1,"\x0f\x8d",4,"",None,-4))
opc("jnle",call(["constant"],chr(0x7f),1,"\x0f\x8f",4,"",None,-4))
opc("jno",call(["constant"],chr(0x71),1,"\x0f\x84",4,"",None,-4))
opc("jnp",call(["constant"],chr(0x7b),1,"\x0f\x8b",4,"",None,-4))
opc("jns",call(["constant"],chr(0x79),1,"\x0f\x89",4,"",None,-4))
opc("jnz",call(["constant"],chr(0x75),1,"\x0f\x85",4,"",None,-4))
opc("jo",call(["constant"],chr(0x70),1,"\x0f\x80",4,"",None,-4))
opc("jp",call(["constant"],chr(0x7a),1,"\x0f\x8a",4,"",None,-4))
opc("jpe",call(["constant"],chr(0x7a),1,"\x0f\x8a",4,"",None,-4))
opc("jpo",call(["constant"],chr(0x7b),1,"\x0f\x8b",4,"",None,-4))
opc("js",call(["constant"],chr(0x78),1,"\x0f\x88",4,"",None,-4))
opc("jz",call(["constant"],chr(0x74),1,"\x0f\x84",4,"",None,-4))


opc("ja",call(["name"],chr(0x77),1,"\x0f\x87",4,"",None,-4))
opc("jae",call(["name"],chr(0x73),1,"\x0f\x83",4,"",None,-4))
opc("jb",call(["name"],chr(0x72),1,"\x0f\x82",4,"",None,-4))
opc("jbe",call(["name"],chr(0x76),1,"\x0f\x86",4,"",None,-4))
opc("jcxz",call(["name"],chr(0xe3),1,chr(0xe3),1,"",None,-4))
opc("jecxz",call(["name"],chr(0xe3),1,chr(0xe3),1,"",None,-4))
opc("jc",call(["name"],chr(0x72),1,"\x0f\x82",4,"",None,-4))
opc("je",call(["name"],chr(0x74),1,"\x0f\x84",4,"",None,-4))
opc("jg",call(["name"],chr(0x7f),1,"\x0f\x8f",4,"",None,-4))
opc("jge",call(["name"],chr(0x7d),1,"\x0f\x8d",4,"",None,-4))
opc("jl",call(["name"],chr(0x7c),1,"\x0f\x8c",4,"",None,-4))
opc("jle",call(["name"],chr(0x7e),1,"\x0f\x8e",4,"",None,-4))
opc("jna",call(["name"],chr(0x76),1,"\x0f\x86",4,"",None,-4))
opc("jnae",call(["name"],chr(0x72),1,"\x0f\x82",4,"",None,-4))
opc("jnb",call(["name"],chr(0x73),1,"\x0f\x83",4,"",None,-4))
opc("jnbe",call(["name"],chr(0x77),1,"\x0f\x87",4,"",None,-4))
opc("jnc",call(["name"],chr(0x73),1,"\x0f\x83",4,"",None,-4))
opc("jne",call(["name"],chr(0x75),1,"\x0f\x85",4,"",None,-4))
opc("jng",call(["name"],chr(0x7e),1,"\x0f\x8e",4,"",None,-4))
opc("jnge",call(["name"],chr(0x7c),1,"\x0f\x8c",4,"",None,-4))
opc("jnl",call(["name"],chr(0x7d),1,"\x0f\x8d",4,"",None,-4))
opc("jnle",call(["name"],chr(0x7f),1,"\x0f\x8f",4,"",None,-4))
opc("jno",call(["name"],chr(0x71),1,"\x0f\x84",4,"",None,-4))
opc("jnp",call(["name"],chr(0x7b),1,"\x0f\x8b",4,"",None,-4))
opc("jns",call(["name"],chr(0x79),1,"\x0f\x89",4,"",None,-4))
opc("jnz",call(["name"],chr(0x75),1,"\x0f\x85",4,"",None,-4))
opc("jo",call(["name"],chr(0x70),1,"\x0f\x80",4,"",None,-4))
opc("jp",call(["name"],chr(0x7a),1,"\x0f\x8a",4,"",None,-4))
opc("jpe",call(["name"],chr(0x7a),1,"\x0f\x8a",4,"",None,-4))
opc("jpo",call(["name"],chr(0x7b),1,"\x0f\x8b",4,"",None,-4))
opc("js",call(["name"],chr(0x78),1,"\x0f\x88",4,"",None,-4))
opc("jz",call(["name"],chr(0x74),1,"\x0f\x84",4,"",None,-4))

opc("jmp",call(["constant"],"\xeb",1,"\xe9",4,"",None,-4))
opc("jmp",call(["name"],"\xeb",1,"\xe9",4,"",None,-4))

opc("jmp",call(["registerexpression"],"\xff",4,"\xff",4,"4",None,0))
opc("jmp",call(["reg"],"\xff",4,"\xff",4,"4",None,0))



#RET
opc("ret",x86mnemonic([],chr(0xc3),"",0,0,-1))
opc("farret",x86mnemonic([],chr(0xcb),"",0,0,-1))
opc("ret",x86mnemonic(["constant"],chr(0xc2),"",0,2,-1,needprefix=0))
opc("farret",x86mnemonic(["constant"],chr(0xca),"",0,2,-1,needprefix=0))

#TEST
opc("test",x86mnemonic(["constant8","%al"],chr(0xa8),"",None,1,-1))
opc("test",x86mnemonic(["constant","%eax"],chr(0xa9),"",None,4,-1))
opc("test",x86mnemonic(["constant8","registerexpression"],chr(0xf6),"0",None,1,-1))
opc("test",x86mnemonic(["constant","registerexpression"],chr(0xf7),"0",None,1,-1))
for r in allshortregs:
    opc("test",x86mnemonic([r,"registerexpression"],chr(0x84),"r",0,1,1))
    for r2 in allshortregs:
        opc("test",x86mnemonic([r,r2],chr(0x84),"r",0,1,1))
opc("test",x86mnemonic(["reg","registerexpression"],chr(0x85),"r",0,1,1))
opc("test",x86mnemonic(["reg","reg"],chr(0x85),"r",0,1,1))

#XOR
opc("xor", x86mnemonic(["constant8","%al"],chr(0x34),"",None,1,-1))
opc("xorb", x86mnemonic(["constant8","%al"],chr(0x34),"",None,1,-1))
opc("xor", x86mnemonic(["constant","%eax"],chr(0x35),"",None,4,-1))
opc("xorl", x86mnemonic(["constant","%eax"],chr(0x35),"",None,4,-1))
opc("xorb", x86mnemonic(["constant8","registerexpression"],chr(0x80),"6",None,1,-1))
opc("xor", x86mnemonic(["constant","registerexpression"],chr(0x81),"6",None,4,-1))
opc("xorl", x86mnemonic(["constant","registerexpression"],chr(0x81),"6",None,4,-1))
opc("xorb", x86mnemonic(["reg","registerexpression"],chr(0x30),"r",0,1,1))
opc("xor", x86mnemonic(["reg","registerexpression"],chr(0x31),"r",0,1,1))
opc("xorl", x86mnemonic(["reg","registerexpression"],chr(0x31),"r",0,4,1))
opc("xorb", x86mnemonic(["registerexpression","reg"],chr(0x32),"r",1,1,0))
opc("xor", x86mnemonic(["registerexpression","reg"],chr(0x33),"r",1,4,0))
opc("xor", x86mnemonic(["reg","reg"],chr(0x33),"r",0,4,1))
opc("xorl", x86mnemonic(["reg","reg"],chr(0x33),"r",0,4,1))
opc("xorl", x86mnemonic(["registerexpression","reg"],chr(0x33),"r",1,4,0))

#SHL
for r in allshortregs:
    opc("shl",  x86mnemonic(["constant8",r],chr(0xc0),"4",None,1,1))
    opc("shr",  x86mnemonic(["constant8",r],chr(0xc0),"5",None,1,1))    
opc("shl",  x86mnemonic(["%cl",r],chr(0xd2),"4",None,1,1))
opc("shr",  x86mnemonic(["%cl",r],chr(0xd2),"5",None,1,1))
opc("shl",  x86mnemonic(["constant8","registerexpression"],chr(0xc1),"4",None,1,1))
opc("shr",  x86mnemonic(["constant8","registerexpression"],chr(0xc1),"5",None,1,1))
opc("shl",  x86mnemonic(["constant8","reg"],chr(0xc1),"4",None,1,1))
opc("shr",  x86mnemonic(["constant8","reg"],chr(0xc1),"5",None,1,1))
opc("shll",  x86mnemonic(["constant8","registerexpression"],chr(0xc1),"4",None,1,1))
opc("shrl",  x86mnemonic(["constant8","registerexpression"],chr(0xc1),"5",None,1,1))
opc("shll",  x86mnemonic(["constant8","reg"],chr(0xc1),"4",None,1,1))
opc("shrl",  x86mnemonic(["constant8","reg"],chr(0xc1),"5",None,1,1))

#OR
opc("or",x86mnemonic(["constant8","%al"],chr(0x0c),"",None,1,-1))
opc("or",x86mnemonic(["constant","%eax"],chr(0x0d),"",None,4,-1))
opc("orb",x86mnemonic(["constant8","registerexpression"],chr(0x80),"1",None,1,1))
opc("orb",x86mnemonic(["constant8","reg"],chr(0x80),"1",None,1,1))
opc("or",x86mnemonic(["constant8","registerexpression"],chr(0x80),"1",None,1,1))
opc("or",x86mnemonic(["constant8","reg"],chr(0x80),"1",None,1,1))


opc("or",x86mnemonic(["constant","registerexpression"],chr(0x81),"1",None,4,1))
opc("orl",x86mnemonic(["constant","registerexpression"],chr(0x81),"1",None,4,1))
opc("or",x86mnemonic(["constant","reg"],chr(0x81),"1",None,4,1))
opc("orl",x86mnemonic(["constant","reg"],chr(0x81),"1",None,4,1))
#sign extended
#opc("or",x86mnemonic(["constant8"."registerexpression"],chr(0x83),"1",None,1,1))
opc("or",x86mnemonic(["reg","registerexpression"],chr(0x09),"r",0,0,1))
opc("or",x86mnemonic(["reg","reg"],chr(0x09),"r",0,0,1))
opc("orl",x86mnemonic(["reg","reg"],chr(0x09),"r",0,0,1))

for r in allshortregs:
    opc("or",x86mnemonic([r,"registerexpression"],chr(0x08),"r",0,0,1))
    opc("or",x86mnemonic(["registerexpression",r],chr(0x0a),"r",1,0,0))

opc("or",x86mnemonic(["registerexpression","reg"],chr(0x0b),"r",1,0,0))

#LOOP
opc("loop",call(["name"],chr(0xe2),1,chr(0xe2),1,"",None,0))
opc("loope",call(["name"],chr(0xe1),1,chr(0xe2),1,"",None,0))
opc("loopz",call(["name"],chr(0xe1),1,chr(0xe2),1,"",None,0))
opc("loopne",call(["name"],chr(0xe0),1,chr(0xe2),1,"",None,0))
opc("loopnz",call(["name"],chr(0xe0),1,chr(0xe2),1,"",None,0))

opc("loop",call(["constant8"],chr(0xe2),1,chr(0xe2),1,"",None,0))
opc("loope",call(["constant8"],chr(0xe1),1,chr(0xe2),1,"",None,0))
opc("loopz",call(["constant8"],chr(0xe1),1,chr(0xe2),1,"",None,0))
opc("loopne",call(["constant8"],chr(0xe0),1,chr(0xe2),1,"",None,0))
opc("loopnz",call(["constant8"],chr(0xe0),1,chr(0xe2),1,"",None,0))

#INC
opc("inc",x86mnemonic(["registerexpression"],chr(0xff),"0",None,0,0))
opc("inc",x86mnemonic(["reg"],chr(0xff),"0",None,0,0))
opc("incl",x86mnemonic(["registerexpression"],chr(0xff),"0",None,0,0))
opc("incl",x86mnemonic(["reg"],chr(0xff),"0",None,0,0))
opc("incb",x86mnemonic(["registerexpression"],chr(0xfe),"0",None,0,0))
for r2 in allshortregs:
    opc("incb",x86mnemonic([r2],chr(0xfe),"0",None,0,0))

for r in reglist:
    opc("inc",x86mnemonic([r],chr(0x40+regpos[r]),"",None,0,0))
    opc("incl",x86mnemonic([r],chr(0x40+regpos[r]),"",None,0,0))
    

#DEC
opc("dec",x86mnemonic(["registerexpression"],chr(0xff),"1",None,0,0))
opc("dec",x86mnemonic(["reg"],chr(0xff),"1",None,0,0))
opc("decl",x86mnemonic(["registerexpression"],chr(0xff),"1",None,0,0))
opc("decl",x86mnemonic(["reg"],chr(0xff),"1",None,0,0))
opc("decb",x86mnemonic(["registerexpression"],chr(0xfe),"1",None,0,0))
for r2 in allshortregs:
    opc("decb",x86mnemonic([r2],chr(0xfe),"1",None,0,0))

for r in reglist:
    opc("dec",x86mnemonic([r],chr(0x48+regpos[r]),"",None,0,0))
    opc("decl",x86mnemonic([r],chr(0x48+regpos[r]),"",None,0,0))
    
#CWD/CDQ page 854
opc("cdq",x86mnemonic([],chr(0x99),"",None,0,0))
opc("cwd",x86mnemonic([],chr(0x99),"",None,0,0))
opc("cdql",x86mnemonic([],chr(0x99),"",None,0,0))
opc("nop",x86mnemonic([],chr(0x90),"",None,0,0))

#AND - Logical And, Page 70
#remember, intel's documentation is backwards...
opc("and",x86mnemonic(["constant8","registerexpression"],chr(0x83),"4",None,0,1))
opc("andb",x86mnemonic(["constant8","registerexpression"],chr(0x83),"4",None,0,1))
opc("and",x86mnemonic(["constant8","reg"],chr(0x83),"4",None,1,1))
opc("andb",x86mnemonic(["constant8","reg"],chr(0x83),"4",None,1,1))

#81 /4 id   AND r/m32,imm32
opc("and",x86mnemonic(["constant","registerexpression"],chr(0x81),"4",None,4,1))
opc("andl",x86mnemonic(["constant","registerexpression"],chr(0x81),"4",None,4,1))
opc("and",x86mnemonic(["constant","reg"],chr(0x81),"4",None,4,1))
opc("andl",x86mnemonic(["constant","reg"],chr(0x81),"4",None,4,1))

opc("and",x86mnemonic(["constant8","%al"],chr(0x24),"",None,1,1))
opc("andb",x86mnemonic(["constant8","%al"],chr(0x24),"",None,1,1))
opc("and",x86mnemonic(["constant","%eax"],chr(0x25),"",None,4,1))
opc("andl",x86mnemonic(["constant","%eax"],chr(0x25),"",None,4,1))

for r2 in allshortregs:
    opc("and",x86mnemonic(["constant8",r2],chr(0x80),"4",None,0,1))
    opc("andb",x86mnemonic(["constant8",r2],chr(0x80),"4",None,0,1))
    opc("and",x86mnemonic([r2,"registerexpression"],chr(0x20),"r",1,0,0))
    opc("andb",x86mnemonic([r2,"registerexpression"],chr(0x20),"r",1,0,0))
# 21/r and r/m32,r32 
opc("and",x86mnemonic(["reg","registerexpression"],chr(0x21),"r",0,1,4))
opc("and",x86mnemonic(["reg","reg"],chr(0x21),"r",0,1,4))
opc("andl",x86mnemonic(["reg","registerexpression"],chr(0x21),"r",0,1,4))
opc("andl",x86mnemonic(["reg","reg"],chr(0x21),"r",0,1,4))

# 23 /r AND r32, r/m32
opc("and",x86mnemonic(["reg","registerexpression"],chr(0x21),"r",0,1,4))
opc("and",x86mnemonic(["reg","reg"],chr(0x21),"r",0,1,4))
opc("andl",x86mnemonic(["reg","registerexpression"],chr(0x21),"r",0,1,4))
opc("andl",x86mnemonic(["reg","reg"],chr(0x21),"r",0,1,4))

#CHECK THIS
for r2 in allshortregs:
    opc("andb",x86mnemonic(["registerexpression",r2],chr(0x22),"r",0,1,4))
    opc("andb",x86mnemonic(["reg",r2],chr(0x22),"r",0,1,4))
    opc("and",x86mnemonic(["registerexpression",r2],chr(0x22),"r",0,1,4))
    opc("and",x86mnemonic(["reg",r2],chr(0x22),"r",0,1,4))

opc("and",x86mnemonic(["reg","registerexpression"],chr(0x21),"r",1,0,4))
opc("and",x86mnemonic(["reg","reg"],chr(0x21),"r",1,0,0))
opc("andl",x86mnemonic(["reg","registerexpression"],chr(0x21),"r",1,0,4))
opc("andl",x86mnemonic(["reg","reg"],chr(0x21),"r",1,0,0))

opc("and",x86mnemonic(["registerexpression","reg"],chr(0x23),"r",1,0,0))

def convertfromintel(opcode, instruction,definition=""):
    """
    Converts the format in intel's pdf to our stuff
    Example:
    >>print convertfromintel("25 id","AND EAX,imm32")
    opc("AND",x86mnemonic(["constant",%eax],chr(0x25),"",None,0,4))

    
    """
    words=opcode.split(" ")
    op="chr(0x%s)"%words[0]
    words=words[1:]
    for w in words:
        if not w[0].isupper():
            #time to move on to next step
            break
        op+="+chr(%s)"%w
        words=words[1:]
    #now we're looking at either nothing
    #or at /r 
    #or at /4 id
    columnloc=0
    if len(words)>0:
        #we do have a register or argument
        if words[0][0]=="/":
            #we have a register column (number or r)
            column="\"%s\""%words[0][1]
            words=words[1:]
        else:
            column="\"\""
            columnloc="None"

    argsize=0
    if len(words)>0:
        #we do have a argument
        dic={"b":1,"w":2,"d":4}
        argsize=dic[words[0][1]]
        
    
    #now we need to parse the instruction
    words=instruction.split(" ")
    name=words[0].lower()
    words=words[1:]
    prefix=""
    arglist=[]
    if len(words)>0:
        argloc=0
        currloc=0
        #we have arguments
        words=words[0].split(",")
        args=[]
        for w in words:
            if w.count("/"):
                #we don't treat r/m8 and r/m32 differently...bug?
                arg="\"registerexpression\""
                argloc=currloc
            elif w=="r8":
                arg="r"
                prefix="for r in allshortregs:\n    "
            elif w=="r32":
                arg="\"reg\""
            elif w=="imm8":
                arg="\"constant8\""
            elif w=="imm32":
                arg="\"constant\""
            else:
                arg="%"+w.lower()
            args+=[arg]
        #intel has it backwards...
        args.reverse() 
        arglist=",".join(args)

    if argloc==0 and columnloc==0:
        columnloc=1

    ret=prefix+"opc(\"%s\",x86mnemonic([%s],%s,%s,%s,%s,%s)) %s"%(name,arglist,op,column,columnloc,argsize,argloc,"#"+definition)
    return ret

if __name__=="__main__":
    print convertfromintel("25 id","AND EAX,imm32")
    print convertfromintel("23 /r","AND r32,r/m32")
    print convertfromintel("20 /r","AND r/m8,r8")
    l=getAllMnemonics()
    l.sort()
    l.reverse()
    print "r'%s'"%"|".join(l)
    