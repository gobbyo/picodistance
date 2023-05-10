from machine import Pin
import time

shutdown = const(600)
waitreps = const(10)
waitonpaint = 0.002
millimeters = const(0.001)
ultrasoundlimit = const(4572) #set to 15 feet (in millimeters) based on the spec sheet.
segnum = [0x3F,0x06,0x5B,0x4F,0x66,0x6D,0x7D,0x07,0x7F,0x67]
speedofsound = const(343) # meters per second

triggerpin = const(11)
echopin = const(12)
conversionbuttonpin = const(15)
frontdistancebuttonpin = const(14)
backdistancebuttonpin = const(13)
frontmeasureLEDpin = const(18)
backmeasureLEDpin = const(19)
frontbuttoncorrection = -10 #millimeters
backbuttoncorrection = 6 #millimeters

twodigitpins = [21,16]
fourdigitpins = [3,2,1,0]

fourlatchpin = const(7) #RCLK
fourclockpin = const(6) #SRCLK
fourdatapin = const(8) #SER
twolatchpin = const(26) #RCLK
twoclockpin = const(27) #SRCLK
twodatapin = const(28) #SER

class distancestringtools(object):

    def __init__(self):
        self.totalmillimeters = 0
        self.millitoinch = 0.0393701
        self.s_meters = "0"
        self.meters = 0
        self.s_centimeters = "0"
        self.centimeters = 0
        self.s_feet = "0"
        self.feet = 0
        self.s_inches = "0"
        self.inches = 0
    
    def set(self, milli):
        if milli > 0:
            self.totalmillimeters = milli
            s = "{0}".format(milli / 1000)
            n = s.split('.')
            self.s_meters = "{0}".format(n[0])
            self.meters = int(n[0])
            self.centimeters = (milli - (self.meters * 1000)) / 10
            self.s_centimeters = "{0}".format(self.centimeters)

            totalinches = float(milli) * self.millitoinch
            s = "{0}".format(totalinches / 12.0)
            n = s.split('.')
            self.s_feet = "{0}".format(n[0])
            self.feet = int(n[0])
            self.inches = float(totalinches - (float(self.feet) * 12.0))
            self.s_inches = "{0}".format(self.inches)
        
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

def getdistancemeasure():
    print("getdistancemeasure")

    try:
        trig = Pin(triggerpin,Pin.OUT)
        echo = Pin(echopin,Pin.IN,Pin.PULL_DOWN)

        receive = 0
        send = 0

        trig.low()
        time.sleep(.002)
        trig.high()
        time.sleep(.002)
        trig.low()
        
        while echo.value() == 0:
            time.sleep(.00001)
        send = time.ticks_us()

        while echo.value() == 1:
            time.sleep(.00001)
        receive = time.ticks_us()

        timepassed = receive - send

        distanceinmillimeters = 0

        if timepassed > 0:
            distanceinmillimeters = round((timepassed * speedofsound * millimeters) / 2)
        
        if (distanceinmillimeters > ultrasoundlimit):
            distanceinmillimeters = 0
        
        print("distanceinmillimeters = {0}".format(distanceinmillimeters))
        
        trig.low()
    finally:
        return distanceinmillimeters

def showbacknumber(segdisp):
    for d in segdisp.twodigits:
        for i in range(6):
            for w in range(waitreps):
                val = 0x01 << i
                segdisp.paintdigit(val,d,segdisp.twolatch,segdisp.twoclock,segdisp.twodata)

def showforwardnumber(segdisp):
    d = 1
    while d >= 0:
        i = 6
        while i >= 0:
            for w in range(waitreps):
                val = 0x01 << i
                segdisp.paintdigit(val,segdisp.twodigits[d],segdisp.twolatch,segdisp.twoclock,segdisp.twodata)
            i -= 1
        d -= 1

def showbackfloat(segdisp):
    for d in segdisp.fourdigits:
        for i in range(6):
            for w in range(waitreps):
                val = 0x01 << i
                segdisp.paintdigit(val,d,segdisp.fourlatch,segdisp.fourclock,segdisp.fourdata)

def showforwardfloat(segdisp):
    d = 3
    while d >= 0:
        i = 6
        while i >= 0:
            for w in range(waitreps):
                val = 0x01 << i
                segdisp.paintdigit(val,segdisp.fourdigits[d],segdisp.fourlatch,segdisp.fourclock,segdisp.fourdata)
            i -= 1
        d -= 1

def startup(segdisp):
    showbacknumber(segdisp)
    showbackfloat(segdisp)
    showforwardfloat(segdisp)
    showforwardnumber(segdisp)

def main():   
    frontdistancebutton=Pin(frontdistancebuttonpin,Pin.IN,Pin.PULL_DOWN)
    backtdistancebutton=Pin(backdistancebuttonpin,Pin.IN,Pin.PULL_DOWN)
    conversionbutton=Pin(conversionbuttonpin,Pin.IN,Pin.PULL_DOWN)
    frontmeasureLED=Pin(frontmeasureLEDpin,Pin.OUT)
    backmeasureLED=Pin(backmeasureLEDpin,Pin.OUT)
    
    display = segdisplays()
    startup(display)

    try:
        prev = d = 0
        distance = distancestringtools()
        distance.set(d)
        t = time.time() + shutdown

        while t > time.time():
            if frontdistancebutton.value():
                t += shutdown
                d = getdistancemeasure() + frontbuttoncorrection
                distance.set(d)
                if(d != prev):
                    showforwardfloat(display)
                    showforwardnumber(display)
                    prev = d
                frontmeasureLED.high()
                backmeasureLED.low()
            if backtdistancebutton.value():
                t += shutdown
                d = getdistancemeasure() + backbuttoncorrection
                distance.set(d)
                if(d != prev):
                    showbacknumber(display)
                    showbackfloat(display)
                    prev = d
                frontmeasureLED.low()
                backmeasureLED.high()

            if conversionbutton.value():
                for w in range(waitreps):
                    display.printnumber(distance.meters)
                    display.printfloat(distance.centimeters)
            else:
               for w in range(waitreps):
                    display.printnumber(distance.feet)
                    display.printfloat(distance.inches)

    finally:
        frontmeasureLED.low()
        backmeasureLED.low()
        conversionbutton.low()
        frontdistancebutton.low()
        display.__del__()

if __name__ == '__main__':
	main()