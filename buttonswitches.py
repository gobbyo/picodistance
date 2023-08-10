from machine import Pin, PWM

class buttonswitches(object):
    backdistancebuttonpin = 13
    conversionbuttonpin = 14
    frontdistancebuttonpin = 15
    frontmeasureLEDpin = 18
    backmeasureLEDpin = 19
    led_value = 5      # 5% brightness

    def __init__(self):
        self.frontdistancebutton=Pin(self.frontdistancebuttonpin,Pin.IN,Pin.PULL_DOWN)
        self.backdistancebutton=Pin(self.backdistancebuttonpin,Pin.IN,Pin.PULL_DOWN)
        self.conversionbutton=Pin(self.conversionbuttonpin,Pin.IN,Pin.PULL_DOWN)
        self.frontmeasureLED=PWM(Pin(self.frontmeasureLEDpin))
        self.backmeasureLED=PWM(Pin(self.backmeasureLEDpin))
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
                self.frontmeasureLED.duty_u16(int(self.led_value * 500)) 
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
                self.backmeasureLED.duty_u16(int(self.led_value * 500)) 
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