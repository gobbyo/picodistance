from machine import Pin, PWM
import time

shutdown = const(30)

led_value = const(20)      # 20% brightness
conversionbuttonpin = const(15)
frontdistancebuttonpin = const(14)
backdistancebuttonpin = const(13)
frontmeasureLEDpin = const(18)
backmeasureLEDpin = const(19)

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
                print("front distance on")
                self.frontmeasureLED.freq(1000)      # Set the frequency value
                self.frontmeasureLED.duty_u16(int(led_value * 500)) 
                print("back distance off")
                self.backmeasureLED.duty_u16(int(0))
                changed = True
        return changed

    def onBackBtnPressed(self):
        changed = False        
        backcurrentvalue = self.backdistancebutton.value()
        if backcurrentvalue != self.backlastvalue:
            self.backlastvalue = backcurrentvalue
            if backcurrentvalue == 1:
                print("back distance on")
                self.backmeasureLED.freq(1000)      # Set the frequency value
                self.backmeasureLED.duty_u16(int(led_value * 500)) 
                print("front distance off")
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

    try:
        t = time.time() + shutdown

        while t > time.time():
            switches.onFrontBtnPressed()
            switches.onBackBtnPressed()
            switches.inMeters()
    finally:
        print("gracefully exiting program")
        switches.__del__()

if __name__ == '__main__':
	main()