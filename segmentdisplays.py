from machine import Pin
import time

#   4 digit 7 segmented LED
#
#       digit 1        digit 2        digit 3        digit 4
#        _a_            _a_            _a_            _a_
#     f |_g_| b      f |_g_| b      f |_g_| b      f |_g_| b
#     e |___| c _h   e |___| c _h   e |___| c _h   e |___| c _h
#         d              d              d              d
#
# num   hgfe dcba   hex
#
# 0 = 	0011 1111   0x3F
# 1 =	0000 0110   0x06
# 2 =	0101 1011   0x5B
# 3 =	0100 1111   0x4F
# 4 =	0110 0110   0x66
# 5 =	0110 1101   0x6D
# 6 =	0111 1101   0x7D
# 7 =	0000 0111   0x07
# 8 =   0111 1111   0x7F
# 9 =   0110 0111   0x67

class segdisplays:
    waitreps = 10
    waitonpaint = 0.002
    segnum = [0x3F,0x06,0x5B,0x4F,0x66,0x6D,0x7D,0x07,0x7F,0x67]
    #2 and 4 digit display pins
    twodigitpins = [21,16]
    fourdigitpins = [3,2,1,0]
    #shift register pins
    fourlatchpin = const(7) #RCLK default
    fourclockpin = const(6) #SRCLK default
    fourdatapin = const(8) #SER default
    twolatchpin = const(26) #RCLK default
    twoclockpin = const(27) #SRCLK default
    twodatapin = const(28) #SER default

    def __init__(self):
        self.twodigits = []
        self.fourdigits = []
        self.setdigitpins(self.twodigitpins,self.fourdigitpins)  
        self.setregisterpins(self.twolatchpin,self.twoclockpin,self.twodatapin,self.fourlatchpin,self.fourclockpin,self.fourdatapin)
    
    def setdigitpins(self,two_digits,four_digits):
        self.twodigits = []
        for d in two_digits:
            pin = Pin(d, Pin.OUT)
            pin.high()
            self.twodigits.append(pin)
        
        self.fourdigits = []
        for d in four_digits:
            pin = Pin(d, Pin.OUT)
            pin.high()
            self.fourdigits.append(pin)
            
    def setregisterpins(self,two_latch,two_clock,two_data,four_latch,four_clock,four_data):
        self.fourlatch = Pin(four_latch, Pin.OUT)
        self.fourclock = Pin(four_clock, Pin.OUT)
        self.fourdata = Pin(four_data, Pin.OUT)
        self.twolatch = Pin(two_latch, Pin.OUT)
        self.twoclock = Pin(two_clock, Pin.OUT)
        self.twodata = Pin(two_data, Pin.OUT)
    
    def __del__(self):
        for t in self.twodigits:
            self.setregister(0,self.twolatch,self.twoclock,self.twodata)
            t.low()
        for f in self.fourdigits:
            self.setregister(0,self.fourlatch,self.fourclock,self.fourdata)
            f.low()

    def getArray(self,val):
        a = [0,0,0,0,0,0,0,0]
        i = 0
        for s in a:
            a[i] = (val & (0x01 << i)) >> i
            i += 1
        return a

    def setregister(self,val,latch,clock,data):
        input = [0,0,0,0,0,0,0,0]
        #open latch for data
        clock.low()
        latch.low()
        clock.high()

        input = self.getArray(val)

        #load data in register
        for i in range(7, -1, -1):
            clock.low()
            if input[i] == 1:
                data.high()
            else:
                data.low()
            clock.high()

        #close latch for data
        clock.low()
        latch.high()
        clock.high()

    def paintdigit(self,val,digit,latch,clock,data):
        digit.low()
        #display the value
        self.setregister(val,latch,clock,data)
        #wait to see it
        time.sleep(self.waitonpaint)
        #clear the display
        self.setregister(0,latch,clock,data)
        digit.high()

    def printnumber(self,d):
        if d < 99:
            num = "{0}".format(d)
            d = len(self.twodigits)-1
            i = len(num)-1
            while i >= 0 & d >= 0:
                if(num[i].isdigit()):
                    val = self.segnum[int(num[i])]
                    self.paintdigit(val,self.twodigits[d],self.twolatch,self.twoclock,self.twodata)
                    d -= 1
                i -= 1

    def printfloat(self,f):
        if f < 100: 
            num = "{:.2f}".format(f)
            i = len(num)-1
            decimal = False
            d = 3
            while i >= 0 & d >= 0:
                if(num[i].isdigit()):
                    val = self.segnum[int(num[i])]
                    if decimal:
                        val |= 0x01 << 7
                        decimal = False
                    self.paintdigit(val,self.fourdigits[d],self.fourlatch,self.fourclock,self.fourdata)
                    d -= 1
                else:
                    decimal = True
                i -= 1
    
    def showbacknumber(self):
        for d in self.twodigits:
            for i in range(6):
                for w in range(self.waitreps/4):
                    val = 0x01 << i
                    self.paintdigit(val,d,self.twolatch,self.twoclock,self.twodata)

    def showforwardnumber(self):
        d = 1
        while d >= 0:
            i = 6
            while i >= 0:
                for w in range(self.waitreps/4):
                    val = 0x01 << i
                    self.paintdigit(val,self.twodigits[d],self.twolatch,self.twoclock,self.twodata)
                i -= 1
            d -= 1

    def showbackfloat(self):
        for d in self.fourdigits:
            for i in range(6):
                for w in range(self.waitreps/4):
                    val = 0x01 << i
                    self.paintdigit(val,d,self.fourlatch,self.fourclock,self.fourdata)

    def showforwardfloat(self):
        d = 3
        while d >= 0:
            i = 6
            while i >= 0:
                for w in range(self.waitreps/4):
                    val = 0x01 << i
                    self.paintdigit(val,self.fourdigits[d],self.fourlatch,self.fourclock,self.fourdata)
                i -= 1
            d -= 1

    def backnumberOneSegonly(self, startval):
        print("showbacknumberOneSegonly")
        a = len(self.twodigits)-1
        while a > 0:
            d = self.twodigits[a]
            for v in range(6):
                i = startval
                for i in range(self.waitreps/4):
                    val = 0x01 << i
                    d.low()
                    self.setregister(val,self.twolatch,self.twoclock,self.twodata)
                    time.sleep(self.waitonpaint)
                    self.setregister(0,self.twolatch,self.twoclock,self.twodata)
                    d.high()
    
    def forwardnumberOneSegonly(self):
        val = 0
        for d in self.twodigits:
            for v in range(6):
                for i in range(self.waitreps/4):
                    val = 0x01 << i
                    d.low()
                    self.setregister(val,self.twolatch,self.twoclock,self.twodata)
                    time.sleep(self.waitonpaint)
                    self.setregister(0,self.twolatch,self.twoclock,self.twodata)
                    d.high()
    
    def backfloatOneSegonly(self):
        val = 0
        a = len(self.twodigits)-1
        while a > 0:
            d = self.twodigits[a]
            for v in range(6):
                for i in range(self.waitreps/4):
                    val = 0x01 << i
                    d.low()
                    self.setregister(val,self.fourlatch,self.fourclock,self.fourdata)
                    time.sleep(self.waitonpaint)
                    self.setregister(0,self.fourlatch,self.fourclock,self.fourdata)
                    d.high()
    
    def backfloatOneSegonly(self):
        val = 0
        for d in self.twodigits:
            for v in range(6):
                for i in range(self.waitreps/4):
                    val = 0x01 << i
                    d.low()
                    self.setregister(val,self.fourlatch,self.fourclock,self.fourdata)
                    time.sleep(self.waitonpaint)
                    self.setregister(0,self.fourlatch,self.fourclock,self.fourdata)
                    d.high()

    def startup(self):
        self.showbacknumber()
        self.showbackfloat()
        self.showforwardfloat()
        self.showforwardnumber()