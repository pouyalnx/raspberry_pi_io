#!/usr/bin/python
from sys import argv
fin=argv[1]

#version 2 solve
#f_part=fin.split('.')
#fout=f_part[0]+".oled"
fout=argv[2]



th=int(argv[3])

####################################################################
from struct import pack
def image_converter(image,th=140):
    (X,Y)=image.size
    x=0
    mask=0
    pos=0
    l=X*Y
    dat=b''
    buf=[0 for z in range(X)]
    while pos!=l:
        v=(image[pos][0]+image[pos][1]+image[pos][2])/3
        sig=(0,1)[v>th]
        buf[x]|=sig<<mask
        pos+=1
        x+=1
        if x==X:
            mask+=1
            if mask==8: #for that each row max have eiht byte
                mask=0
                for val in buf:
                    dat+=pack('B',val)
                buf=[0 for z in range(X)]
            x=0

    return dat
####################################################################


from PIL import Image
f=open(fin,'rb')
i=Image.open(f)
dat=image_converter(i.getdata(),th)
with open(fout,'wb') as f:
    f.write(dat)



