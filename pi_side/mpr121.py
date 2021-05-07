#!/usr/bin/python



import struct
import fcntl
import json



class MPR121:
    def __init__(self,dev='/dev/i2c-1',slave_addr='0xa5',mask={'0':1,'1':2,'2':4,'3':8,'4':16,'5':32,'6':64,'7':128,'8':256,'9':512,'10':1024,'11':2048})
        self.f=open(dev,'w+b')
        fcntl.ioctl(self.f.fileno(),int("0x0703",base=16),int(slave_addr,base=16)
        with open('config.json') as f:
            self.config_array=json.load(f)
        self.config()
        self.mask=mask


    def config(self):
        for val in self.config_array:
            cmd=struct.pack('BB',val[0],val[1])
            self.f.write(cmd)
    
    def __call__(self):
        dat=self.f.read(2)
        val=struct.unpack("H",dat)
        out=[]
        for sym,mask in self.mask.items():
            if val&mask:
                out.append(sym)
        return out




    
