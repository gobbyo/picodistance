from machine import Pin
import time

millimeters = const(0.001)
ultrasoundlimit = const(4572) #millimeters
wait = const(10)
multiplex = .004
segnum = [0x3F,0x06,0x5B,0x4F,0x66,0x6D,0x7D,0x07,0x7F,0x67]
speedofsound = const(343) # meters per second

triggerpin = const(13)
echopin = const(12)
conversionbuttonpin = const(15)
frontdistancebuttonpin = const(14)

class distancemeasure(object):

    def __init__(self):
        self.trig = Pin(triggerpin,Pin.OUT)
        self.echo = Pin(echopin,Pin.IN,Pin.PULL_DOWN)
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
    
    def _set(self, milli):
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

    def getdistancemeasure(self):
        receive = 0
        send = 0

        self.trig.low()
        time.sleep_us(2)
        self.trig.high()
        time.sleep_us(5)
        self.trig.low()
        
        while self.echo.value() == 0:
            pass
        send = time.ticks_us()
        while self.echo.value() == 1:
            pass
        receive = time.ticks_us()

        timepassed = receive - send
        distanceinmillimeters = round((timepassed * speedofsound * millimeters) / 2)
        if distanceinmillimeters > ultrasoundlimit:
            distanceinmillimeters = 0
        
        self.trig.low()

        self._set(distanceinmillimeters)

class displaydistance(object):

    def __init__(self):
        self.twodigits =        [16,21]
        self.twodigitpins =     [26,17,18,20,19,22,28,27]
        #twopinout   =          [a, b, c, d, e, f, g, dot]
        self.fourdigits =       [6,9,10,5]
        self.fourdigitpins =    [7,11,3,1,0,8,4,2]
        #fourpinout   =         [a,b,c,d,e,f,g,dot]

        for d in self.fourdigits:
            pin = Pin(d, Pin.OUT)
            pin.high()
        
    def __del__(self):
        for d in self.twodigits:
            pin = Pin(d, Pin.OUT)
            pin.low()
        for d in self.fourdigits:
            pin = Pin(d, Pin.OUT)
            pin.low()
        for n in self.twodigitpins:
            pin = Pin(n, Pin.OUT)
            pin.low()
        for n in self.fourdigitpins:
            pin = Pin(n, Pin.OUT)
            pin.low()

    def paintnumber(self, val, digit, pins):
        digitpin = Pin(digit, Pin.OUT)
        digitpin.low()

        i = 0
        for p in pins:
            pin = Pin(p, Pin.OUT)
            if ((val & (0x01 << i)) >> i) == 1:
                pin.high()
            else:
                pin.low()
            i += 1
        
        time.sleep(multiplex)

        digitpin.high()

    def printnumber(self, n):
        for d in self.twodigits:
            pin = Pin(d, Pin.OUT)
            pin.high()

        num = "{0}".format(n)
        i = len(num)-1
        d = 1

        while i >= 0 & d >= 0:
            val = segnum[int(num[i])]
            self.paintnumber(val, self.twodigits[d], self.twodigitpins)
            i -= 1
            d -= 1

    def printfloat(self, f):
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
                    self.paintnumber(val, self.fourdigits[d], self.fourdigitpins)
                    d -= 1
                else:
                    decimal = True
                i -= 1

def main():   

    frontdistancebutton=Pin(frontdistancebuttonpin,Pin.IN,Pin.PULL_DOWN)
    conversionbutton=Pin(conversionbuttonpin,Pin.IN,Pin.PULL_DOWN)
    display = displaydistance()

    try:
        distance = distancemeasure()

        while True:
            if frontdistancebutton.value():
                distance.getdistancemeasure()

            if conversionbutton.value():              
                for w in range(wait):
                    display.printnumber(distance.meters)
                    display.printfloat(distance.centimeters)
            else:
               for w in range(wait):
                    display.printnumber(distance.feet)
                    display.printfloat(distance.inches)

            if frontdistancebutton.value():
                if conversionbutton.value():
                    break
    finally:
        conversionbutton.low()
        frontdistancebutton.low()
        display.__del__()

if __name__ == '__main__':
	main()