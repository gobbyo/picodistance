from machine import Pin, PWM
import time

shutdown = const(30)

led_value = const(20)      # 20% brightness
backdistancebuttonpin = const(13)
conversionbuttonpin = const(14)
frontdistancebuttonpin = const(15)
frontmeasureLEDpin = const(18)
backmeasureLEDpin = const(19)
laser1pin = const(4)
laser2pin = const(5)

class diodeLasers(object):
    def __init__(self):
        self.laser1 = Pin(laser1pin,Pin.OUT)
        self.laser2 = Pin(laser2pin,Pin.OUT)
    def on(self):
        self.laser1.high()
        self.laser2.high()
    def off(self):
        print("turning off lasers")
        self.laser1.low()
        self.laser2.low()
    
    def __del__(self):
        self.off()

class buttonswitches(object):
    def __init__(self):
        self.frontdistancebutton=Pin(frontdistancebuttonpin,Pin.IN,Pin.PULL_DOWN)
        self.backdistancebutton=Pin(backdistancebuttonpin,Pin.IN,Pin.PULL_DOWN)
        self.conversionbutton=Pin(conversionbuttonpin,Pin.IN,Pin.PULL_DOWN)
        self.frontmeasureLED=PWM(Pin(frontmeasureLEDpin))
        self.backmeasureLED=PWM(Pin(backmeasureLEDpin))
        self.backlastvalue = 0
        self.frontlastvalue = 0
        self.convlastvalue = 0
    
    def onFrontBtnPressed(self):
        changed = False
        frontcurrentvalue = self.frontdistancebutton.value()
        if frontcurrentvalue != self.frontlastvalue:
            self.frontlastvalue = frontcurrentvalue
            if frontcurrentvalue == 1:
                self.frontmeasureLED.freq(1000)      # Set the frequency value
                self.frontmeasureLED.duty_u16(int(led_value * 500)) 
                self.backmeasureLED.duty_u16(int(0))
                changed = True
        return changed

    def onBackBtnPressed(self):
        changed = False        
        backcurrentvalue = self.backdistancebutton.value()
        if backcurrentvalue != self.backlastvalue:
            self.backlastvalue = backcurrentvalue
            if backcurrentvalue == 1:
                self.backmeasureLED.freq(1000)      # Set the frequency value
                self.backmeasureLED.duty_u16(int(led_value * 500)) 
                self.frontmeasureLED.duty_u16(int(0))
                changed = True
        return changed
    
    def inMeters(self):
        convcurrentvalue = self.conversionbutton.value()
        if convcurrentvalue != self.convlastvalue:
            self.convlastvalue = convcurrentvalue
            if convcurrentvalue == 1:
                print("meters")
            else:
                print("feet")
        return self.convlastvalue
    
    def __del__(self):
        print("turning off LEDs")
        self.frontmeasureLED.duty_u16(int(0))
        self.backmeasureLED.duty_u16(int(0))
        
def main():   
    print("button switch test")
    switches = buttonswitches()
    lasers = diodeLasers()

    try:
        t = time.time() + shutdown
        
        while t > time.time():
            if switches.onFrontBtnPressed():
                print("onFrontBtnPressed")
            if switches.onBackBtnPressed():
                print("onBackBtnPressed")
            if switches.inMeters():
                lasers.laser1.off()
                lasers.laser2.on()
            else:
                lasers.laser1.on()
                lasers.laser2.off()
    finally:
        print("gracefully exiting program")
        lasers.__del__()
        switches.__del__()

if __name__ == '__main__':
	main()