import re
import struct
import json

with open('file_inp.txt') as f:
    dat=f.read()

key=[x[1] for x in re.findall("\'.?\'",dat)]
value=[x.replace('{','').replace('}','').split(', ') for x in re.findall("{.*}",dat)]

print(value)

kw={}
for i in range(len(key)):
    base=b''
    ar=[]
    for byte in value[i]:
        base+=struct.pack('B',int(byte,16))
        ar.append(int(byte,16))
    #kw[key[i]]=str(base)
    kw[key[i]]=ar



print(kw)


with open('out.json','w') as f:
    json.dump(kw,f)