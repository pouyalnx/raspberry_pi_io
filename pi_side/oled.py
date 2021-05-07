#oled ssd1306 dirver for 128*64 lcd
#based on linux /dev/i2c
#pya 2020/covid19 days
#this driver limited on using one chip at the time never tested for more than one

from fcntl import ioctl
from struct import pack
from time import sleep


class Oled:
    I2C_ADDR=0X78//2
    PAGE=8
    COLUMN=128

    def __init__(self,fdev='/dev/i2c-1',font={}):
        self.page=0
        self.column=0
        self.f=open(fdev,'wb',buffering=0)
        self.font={}
        ioctl(self.f,0x703,self.I2C_ADDR)        
        super().__init__()
        self.hwinit()

    def on(self):
        cmd=b'\x80\xaf'
        return self.f.write(cmd)        

    def off(self):
        cmd=b'\x80\xae'
        return self.f.write(cmd)   

    def contrast(self,val):
        cmd=b'\x00\x81'+pack('B',val%256)
        return self.f.write(cmd)


    def gotoxy(self,page=0,column=0):
        #for page addressing mode
        self.page=page%self.PAGE
        self.column=column%self.COLUMN

    def updatexy(self,dcolumn=0):
        #for page addressing mode
        column=dcolumn+self.column
        self.gotoxy(self.page+column//self.COLUMN,column%self.COLUMN)

    def putb(self,b):
        #for page addressing mode
        ps=0
        pe=0
        l=len(b)
        while pe!=l:
            ps=pe
            pe+=min(self.COLUMN-self.column,l-pe)
            c=pack("BBBBBBB",0x80,0xb0|self.x,0x80,self.y&0xf,0x80,0x10|((self.y>>4)&0xf),0x40)
            self.f.write(c+b[ps:pe])
            self.updatexy(pe-ps)
        return pe

    def putc(self,c):
        #for page addressing mode
        if c in self.font:
            self.putb(self.font[c])


    def __call__(self,data):
        if self.memory_addressing_mode==2:
            for ch in data:
                self.putc(ch)
        else:
            self.f.write(b'\x40'+data)




    def set_memory_addressing_mode(self,mode):
        #mode 0 horzental mode 1 vertical mode in this modes use 0x21 and 0x22 for addressing 
        #mode 2 page mode in this mode use b0-b7 and 00-0f and 10-0f for page addressing
        self.memory_addressing_mode=mode&3
        c=pack('BBB',0x00,0x20,mode&3)
        self.f.write(c)
        if self.memory_addressing_mode==2:
            self.gotoxy()
        else:
            self.set_column_page_address()


    def set_column_page_address(self,ps=0,pe=7,cs=0,ce=127):
        #in 0/1 mode this select window for send data from buffers this mode good for showing images

        self.column_start=cs%self.COLUMN
        self.column_end=ce%self.COLUMN

        self.page_start=ps%self.PAGE
        self.page_end=pe%self.PAGE

        c=c=pack('BBBB',0x00,0x21,self.column_start,self.column_end)
        self.f.write(c)

        c=c=pack('BBBB',0x00,0x22,self.page_start,self.page_end)
        self.f.write(c)



    def hwinit(self):
        self.on()

        cmd=b'\x80\xb0\x80\x00\x80\x10\x40'
        self.f.write(cmd)

        cmd=b'\x00\xa8\x3f\x00'
        self.f.write(cmd)

        cmd=b'\x00\xd5\xf0'
        self.f.write(cmd)

        cmd=b'\x80\x40\x00\x8d\x14'
        self.f.write(cmd)

        self.set_memory_addressing_mode(2)

        cmd=b'\x80\xa6\x80\xa4\x80\xa1\x80\xc8'
        self.f.write(cmd)

        cmd=b'\x00\xda\x12'
        self.f.write(cmd)

        cmd=b'\x00\xd9\xf1'
        self.f.write(cmd)

        cmd=b'\x00\xdb\x40'
        self.f.write(cmd)

        cmd=b'\x00\xd5\xf0'
        self.f.write(cmd)

        sleep(0.01)

        self.on()


        self.set_memory_addressing_mode(2)

        cmd=b'\x00\xd5\xf0'
        self.f.write(cmd)

        cmd=b'\x00\xd5\xf0'
        self.f.write(cmd)

        self.contrast(80)    




if __name__=="__main__":
    #test case for verify it work good
    lcd=Oled()




#idea--->
#u can use linear addrssing mode software see every coloum and row as single pos that can be in range 0-X*Y
#font are saved as dict in app that for each char we have a word
#for another versions use another model of show for example ram based 


def image_converter(image,th=125):
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
                    val=0
            x=0

    return dat













