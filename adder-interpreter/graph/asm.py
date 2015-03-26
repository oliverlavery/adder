data=atandtparse.atandtpreprocess("jmp short +0x18")
tokens=atandtscan.scan(data)
tree=atandtparse.parse(tokens)
x=atandtparse.x86generate(tree)
print x.value