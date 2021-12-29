from machine import Pin,I2C



class OLED(I2C):
    def __init__(self, scl=Pin(2), sda=Pin(0), freq=200000):
        super().__init__(-1, scl, sda)
        self.init(scl = scl, sda = sda, freq=200000)
        self.i2c_address = 60
        init_command = [0xae,
                        0x00,0x10,
                        0xd5,0x80,
                        0xa8,0x3f,
                        0xd3,0x00,
                        0XB0,
                        0x40,
                        0x8d,0x14,
                        0xa1,
                        0xc8,
                        0xda,0x12,
                        0x81,0xff,
                        0xd9,0xf1,
                        0xdb,0x30,
                        0x20,0x02,
                        0xa4,
                        0xa6,
                        0xaf]
        self.writeto_mem(self.i2c_address, 0x00, bytes([0xae]))
        self.writeto_mem(self.i2c_address, 0x00, bytes([0x8d]))
        self.writeto_mem(self.i2c_address, 0x00, bytes([0x10]))
        self.Clear()
        for i in init_command:
            self.writeto_mem(self.i2c_address, 0x00, bytes([i]))
        
    
    def Clear(self):
        for i in range(8):
            self.writeto_mem(self.i2c_address, 0x00, bytes([0xb0+i]))
            self.writeto_mem(self.i2c_address, 0x00, bytes([0x10]))
            self.writeto_mem(self.i2c_address, 0x00, bytes([0x00]))
            for n in range(128):
                self.writeto_mem(self.i2c_address, 0x40, b'\x00')

                 
    def Full(self,num=0xff):
        for i in range(8):
            self.writeto_mem(self.i2c_address, 0x00, bytes([0xb0+i]))
            self.writeto_mem(self.i2c_address, 0x00, bytes([0x00]))
            self.writeto_mem(self.i2c_address, 0x00, bytes([0x10]))
            for n in range(128):
                self.writeto_mem(self.i2c_address, 0x40, bytes([num]))

                
    def Test(self,data):
         self.writeto_mem(self.i2c_address, 0x00, bytes([data]))
                    
          
    def Char(self, x, y, ch):
        import ASCII_8x16
        c = 0
        y = y+2
        for t in range(2):
            self.writeto_mem(self.i2c_address, 0x00, bytes([0xb0+x]))
            self.writeto_mem(self.i2c_address, 0x00, bytes([y//16+0x10]))
            self.writeto_mem(self.i2c_address, 0x00, bytes([y%16]))
            x=x+1
            for i in range(8):
                self.writeto_mem(self.i2c_address, 0x40, bytes([ASCII_8x16.ASCII_8x16[ord(ch)*16+c-512]]))
                c=c+1

                
    def MiniChar(self, x, y, ch):
        import ASCII_8x6
        y = y+2
        self.writeto_mem(self.i2c_address, 0x00, bytes([0xb0+x]))
        self.writeto_mem(self.i2c_address, 0x00, bytes([y//16+0x10]))
        self.writeto_mem(self.i2c_address, 0x00, bytes([y%16]))
        for i in range(6):
            self.writeto_mem(self.i2c_address, 0x40, bytes([ASCII_8x6.Font6x8[ord(ch)-32][i]]))


    
    def String(self, x, y, buf):
        for i in buf:
            if i == '\0':
                break
            self.Char(x, y, i)
            y = y + 8
            if y>120:
                y = 0
                x = x + 2


    def Chinese(self, x, y, ch):
        import CHS_16x16
        c = 0
        for t in range(2):
            self.writeto_mem(self.i2c_address, 0x00, bytes([0xb0+x]))
            self.writeto_mem(self.i2c_address, 0x00, bytes([y//16+0x10]))
            self.writeto_mem(self.i2c_address, 0x00, bytes([y%16]))
            x=x+1
            for i in range(16):
                self.writeto_mem(self.i2c_address, 0x40, bytes([CHS_16x16.GB_16[ch*32+c]]))
                c=c+1
    
    def Pic(self):
        import PIC
        for t in range(8):
            self.writeto_mem(self.i2c_address, 0x00, bytes([0xb0+t]))
            self.writeto_mem(self.i2c_address, 0x00, bytes([0x10]))
            self.writeto_mem(self.i2c_address, 0x00, bytes([0x02]))
            for i in range(128):
                self.writeto_mem(self.i2c_address, 0x40, bytes([PIC.PIC_128x64[i+t*128]]))

