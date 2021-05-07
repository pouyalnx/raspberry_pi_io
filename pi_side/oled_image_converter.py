from PIL import Image


fname='wallpapersden.com_girl-model-fog_2560x1440.jpg'
f=open(fname,'rb')
i=Image.open(f)

size=(128,64)
i2=i.resize(size)
#i2.save('new '+fname)


i3=i2.convert('P')
#i3.save('new1.bmp')


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
        sig=(0,1)[image[pos]>th]
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


dat=image_converter(i3.getdata())
with open('pat.oled','wb') as f:
    f.write(dat)

