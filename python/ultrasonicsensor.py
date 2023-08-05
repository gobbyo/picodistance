from machine import Pin
import time

class ultrasonic:
    triggerpin = 11 #default
    echopin = 12 #default
    speedofsound = const(343) # meters per second
    millimeters = const(0.001)
    ultrasoundlimit = const(3657) #This is the limit of the sensor. Set to 12 feet (in millimeters) based on real world testing.  

    def __init__(self):
        print("create ultrasonic")
        self.setpins(self.triggerpin,self.echopin)
        self.distanceinmillimeters = 0
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

        self.distanceinmillimeters = 0

        if timepassed > 100:
            self.distanceinmillimeters = round((timepassed * self.speedofsound * self.millimeters) / 2)
        else:
            self.distanceinmillimeters = 0
        
        if (self.distanceinmillimeters > self.ultrasoundlimit):
            self.distanceinmillimeters = 0
        
        print("distanceinmillimeters = {0}".format(self.distanceinmillimeters))
        
        self.trig.low()
        
        return self.distanceinmillimeters