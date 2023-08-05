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

waitreps = 10
waitonpaint = 0.004
# The variable below can be any number of digits for a 7 segment display. 
# For example, a 2 digit 7 segment display is digitpins=[1,0], four digit 7 segment display is digitpins=[3,2,1,0], etc.
fourdigitpins = [3,2,1,0]
segnum = [0x3F,0x06,0x5B,0x4F,0x66,0x6D,0x7D,0x07,0x7F,0x67]
fourlatchpin = const(7) #RCLK
fourclockpin = const(6) #SRCLK
fourdatapin = const(8) #SER

twodigitpins = [21,16]
twoclockpin = const(27) #SRCLK
twodatapin = const(28) #SER
twolatchpin = const(26) #RCLK

class segdisplays:
    def __init__(self):
        self.twodigits = []
        for d in twodigitpins:
            pin = Pin(d, Pin.OUT)
            pin.high()
            self.twodigits.append(pin)
        self. fourdigits = []

        for d in fourdigitpins:
            pin = Pin(d, Pin.OUT)
            pin.high()
            self.fourdigits.append(pin)
        
        self.fourlatch = Pin(fourlatchpin, Pin.OUT)
        self.fourclock = Pin(fourclockpin, Pin.OUT)
        self.fourdata = Pin(fourdatapin, Pin.OUT)
            
        self.twolatch = Pin(twolatchpin, Pin.OUT)
        self.twoclock = Pin(twoclockpin, Pin.OUT)
        self.twodata = Pin(twodatapin, Pin.OUT)
    
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
        time.sleep(waitonpaint)
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
                    val = segnum[int(num[i])]
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
                    val = segnum[int(num[i])]
                    if decimal:
                        val |= 0x01 << 7
                        decimal = False
                    self.paintdigit(val,self.fourdigits[d],self.fourlatch,self.fourclock,self.fourdata)
                    d -= 1
                else:
                    decimal = True
                i -= 1

def showbacknumber(segdisp):
    d = 0
    while d <= 1:
        print("showbacknumber paintdigit {0}".format(d))
        for i in range(6):
            val = 0
            for w in range(waitreps):
                val = 0x01 << i
                segdisp.paintdigit(val,segdisp.twodigits[d],segdisp.twolatch,segdisp.twoclock,segdisp.twodata)
        d += 1

def showbacknumberOneSegonly(segdisp, val):
    d = 0
    while d <= 1:
        print("showbacknumberGonly paintdigit {0}".format(d))
        for w in range(waitreps):
            segdisp.paintdigit(val,segdisp.twodigits[d],segdisp.twolatch,segdisp.twoclock,segdisp.twodata)
        d += 1

def showforwardnumber(segdisp):
    d = 1
    while d >= 0:
        print("showforwardnumber paintdigit {0}".format(d))
        i = 5
        while i >= 0:
            val = 0
            for w in range(waitreps):
                val = 0x01 << i
                segdisp.paintdigit(val,segdisp.twodigits[d],segdisp.twolatch,segdisp.twoclock,segdisp.twodata)
            i -= 1
        d -= 1

def showforwardnumberOneSegonly(segdisp, val):
    d = 1
    while d >= 0:
        print("showforwardnumberGonly paintdigit {0}".format(d))
        for w in range(waitreps):
            segdisp.paintdigit(val,segdisp.twodigits[d],segdisp.twolatch,segdisp.twoclock,segdisp.twodata)
        d -= 1

def showbackfloat(segdisp):
    for d in segdisp.fourdigits:
        for i in range(6):
            val = 0
            for w in range(waitreps):
                val = 0x01 << i
                segdisp.paintdigit(val,d,segdisp.fourlatch,segdisp.fourclock,segdisp.fourdata)

def showbackfloatOneSegonly(segdisp, val):
    for d in segdisp.fourdigits:
            for w in range(waitreps):
                segdisp.paintdigit(val,d,segdisp.fourlatch,segdisp.fourclock,segdisp.fourdata)

def showforwardfloat(segdisp):
    d = 3
    while d >= 0:
        i = 5
        while i >= 0:
            val = 0
            for w in range(waitreps):
                val = 0x01 << i
                segdisp.paintdigit(val,segdisp.fourdigits[d],segdisp.fourlatch,segdisp.fourclock,segdisp.fourdata)
            i -= 1
        d -= 1

def showforwardfloatOneSegonly(segdisp, val):
    d = 3
    while d >= 0:
        for w in range(waitreps):
            segdisp.paintdigit(val,segdisp.fourdigits[d],segdisp.fourlatch,segdisp.fourclock,segdisp.fourdata)
        d -= 1

def main():
    segdisp = segdisplays()
    try:
        print("circuit test...")
        showbacknumberOneSegonly(segdisp, 0x01 << 7)
        showbackfloatOneSegonly(segdisp, 0x01 << 7)
        showforwardfloatOneSegonly(segdisp, 0x01 << 7)
        showforwardnumberOneSegonly(segdisp, 0x01 << 7)

        showbacknumber(segdisp)
        showbackfloat(segdisp)
        showforwardfloat(segdisp)
        showforwardnumber(segdisp)

        showbacknumberOneSegonly(segdisp, 0x01 << 6)
        showbackfloatOneSegonly(segdisp, 0x01 << 6)
        showforwardfloatOneSegonly(segdisp, 0x01 << 6)
        showforwardnumberOneSegonly(segdisp, 0x01 << 6)
    finally:
        print("test finished")

if __name__ == '__main__':
	main()