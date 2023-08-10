from machine import Pin

class diodeLaser(object):
    laser1pin = 4 #default
    laser2pin = 5 #default

    def __init__(self):
        print("create lasers")
        self.setpins(self.laser1pin,self.laser2pin)
    def setpins(self,laser1_pin, laser2_pin):
        self.laser1 = Pin(laser1_pin,Pin.OUT)
        self.laser2 = Pin(laser2_pin,Pin.OUT)
    def on(self):
        self.laser1.high()
        self.laser2.high()
    def off(self):
        print("turning off lasers")
        self.laser1.low()
        self.laser2.low()
    
    def __del__(self):
        print("delete lasers")
        self.off()