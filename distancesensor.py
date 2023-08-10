from machine import Pin
from distancestringtool import distancestring
from buttonswitches import buttonswitches
from diodeLasers import diodeLaser
import time

waitreps = const(10)
waitonpaint = 0.002
millimeters = const(0.001)
ultrasoundlimit = const(3657) #set to 12 feet (in millimeters) based on real world testing.
segnum = [0x3F,0x06,0x5B,0x4F,0x66,0x6D,0x7D,0x07,0x7F,0x67]
speedofsound = const(343) # meters per second



frontbuttoncorrection = -12 #millimeters
backbuttoncorrection = 40 #millimeters

twodigitpins = [21,16]
fourdigitpins = [3,2,1,0]

fourlatchpin = const(7) #RCLK
fourclockpin = const(6) #SRCLK
fourdatapin = const(8) #SER
twolatchpin = const(26) #RCLK
twoclockpin = const(27) #SRCLK
twodatapin = const(28) #SER

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
    
    def showbacknumber(self):
        for d in self.twodigits:
            for i in range(6):
                for w in range(waitreps/4):
                    val = 0x01 << i
                    self.paintdigit(val,d,self.twolatch,self.twoclock,self.twodata)

    def showforwardnumber(self):
        d = 1
        while d >= 0:
            i = 6
            while i >= 0:
                for w in range(waitreps/4):
                    val = 0x01 << i
                    self.paintdigit(val,self.twodigits[d],self.twolatch,self.twoclock,self.twodata)
                i -= 1
            d -= 1

    def showbackfloat(self):
        for d in self.fourdigits:
            for i in range(6):
                for w in range(waitreps/4):
                    val = 0x01 << i
                    self.paintdigit(val,d,self.fourlatch,self.fourclock,self.fourdata)

    def showforwardfloat(self):
        d = 3
        while d >= 0:
            i = 6
            while i >= 0:
                for w in range(waitreps/4):
                    val = 0x01 << i
                    self.paintdigit(val,self.fourdigits[d],self.fourlatch,self.fourclock,self.fourdata)
                i -= 1
            d -= 1
    
    def startup(self):
        self.showbacknumber()
        self.showbackfloat()
        self.showforwardfloat()
        self.showforwardnumber()
        
class ultrasonic:
    triggerpin = 11
    echopin = 12

    def __init__(self):
        print("create ultrasonic")
        self.setpins(triggerpin,echopin)
    def setpins(self,trigger_pin, echo_pin):
        print("setpins ultrasonic")
        self.trig = Pin(trigger_pin,Pin.OUT)
        self.echo = Pin(echo_pin,Pin.IN,Pin.PULL_DOWN)
    def __del__(self):
        print("delete ultrasonic")
        self.trig.low()
        self.echo.low()

    def getdistancemeasure(self):
        print("getdistancemeasure")

        try:
            receive = 0
            send = 0

            self.trig.low()
            time.sleep(.002)
            self.trig.high()
            time.sleep(.002)
            self.trig.low()
            
            i = 0
            while self.echo.value() == 0:
                time.sleep(.00001)
            send = time.ticks_us()

            while self.echo.value() == 1:
                time.sleep(.00001)
            receive = time.ticks_us()

            timepassed = receive - send

            distanceinmillimeters = 0

            if timepassed > 100:
                distanceinmillimeters = round((timepassed * speedofsound * millimeters) / 2)
            else:
                distanceinmillimeters = 0
            
            if (distanceinmillimeters > ultrasoundlimit):
                distanceinmillimeters = 0
            
            print("distanceinmillimeters = {0}".format(distanceinmillimeters))
            
            self.trig.low()
        finally:
            return distanceinmillimeters

def main():   
    display = segdisplays()
    display.startup()
    switches = buttonswitches()
    lasers = diodeLaser()
    us = ultrasonic()

    try:
        prev = d = 0
        distance = distancestring()
        distance.set(d)
        lasers.on()

        while not (switches.frontdistancebutton.value() and switches.backdistancebutton.value()):
            if switches.onFrontBtnPressed():
                d = us.getdistancemeasure() + frontbuttoncorrection
                distance.set(d)
                if(d != prev):
                    display.showforwardfloat()
                    display.showforwardnumber()
                    prev = d

            if switches.onBackBtnPressed():
                d = us.getdistancemeasure() + backbuttoncorrection
                distance.set(d)
                if(d != prev):
                    display.showbacknumber()
                    display.showbackfloat()
                    prev = d

            if switches.inMeters():
                for w in range(waitreps):
                    display.printnumber(distance.meters)
                    display.printfloat(distance.centimeters)
            else:
               for w in range(waitreps):
                    display.printnumber(distance.feet)
                    display.printfloat(distance.inches)
    except KeyboardInterrupt:
        print("KeyboardInterrupt")
    finally:
        print("shutting down")
        lasers.off()
        display.__del__()
        switches.__del__()
        us.__del__()

if __name__ == '__main__':
	main()