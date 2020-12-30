import struct
import fcntl
import delay
import json


class SSD1306:
    ADDR=0x78//2
    
    def __init__(self,fdev):
        f=open(fdev,'wb',buffer=0)
        
        self.f=f
        self.x=0
        self.y=0

        with open('font.json') as f:
            self.font=json.load(f)
        
        stat


    def init(self):
        self.power_on()

        cmd=b'\x80\xb0\x80\x00\x80\x10\x40'
        self.f.write(cmd)

        cmd=b'\x00\xa8\x3f\x00'
        self.f.write(cmd)

        cmd=b'\x00\xd5\xf0'
        self.f.write(cmd)

        cmd=b'\x80\x40\x00\x8d\x14'
        self.f.write(cmd)

        cmd=b'\x00\x20\x02'
        self.f.write(cmd)

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

        delay.sleep(0.01)
        cmd=b'\x80\xaf'
        self.f.write(cmd)


        cmd=b'\x00\x20\x02'
        self.f.write(cmd)

        cmd=b'\x00\xd5\xf0'
        self.f.write(cmd)

        cmd=b'\x00\xd5\xf0'
        self.f.write(cmd)

        self.contrst(80)

    def contrst(self,val):
        cmd=b'\x00\x81'+struct.pack('B')
        return self.f.write(cmd)
         
    def power_on(self):
        cmd=b'\x80\xaf'
        return self.f.write(cmd)

    def power_off(self):
        cmd=b'\x80\xae'
        return self.f.write(cmd)      


    def gotoxy(self,x,y):
        self.x=x//8
        self.y=y//128

    def stdout(self,val):        
        pass

