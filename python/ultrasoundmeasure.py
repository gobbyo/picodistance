from machine import Pin, PWM
import time

triggerpin = const(11)
echopin = const(12)

millimeters = const(0.001)
ultrasoundlimit = const(3657) #set max to 12 feet (in millimeters)
speedofsound = const(343) # meters per second
led_value = const(20)      # 20% brightness

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

def getdistancemeasure():
    print("getdistancemeasure")

    trig = Pin(triggerpin,Pin.OUT)
    echo = Pin(echopin,Pin.IN,Pin.PULL_DOWN)

    receive = 0
    send = 0

    
    #while echo.value() == 0:      
    trig.low()
    time.sleep_us(2)
    trig.high()
    time.sleep_us(5)
    trig.low()

    while echo.value() == 0:
        send = time.ticks_us()

    while echo.value() == 1:
        receive = time.ticks_us()

    timepassed = receive - send

    distanceinmillimeters = round((timepassed * speedofsound * millimeters) / 2)
    
    print("distanceinmillimeters = {0}".format(distanceinmillimeters))
    
    if distanceinmillimeters > ultrasoundlimit:
        distanceinmillimeters = 0
    
    trig.low()

    return distanceinmillimeters

def main():

    try:
        dt = distancestringtools()
        for i in range(3):
            dt.set(getdistancemeasure())
            print("feet={0} inches={1}".format(dt.feet, dt.inches))
            print("meters={0} centimeters={1}".format(dt.meters, dt.centimeters))
            time.sleep(2)
        
    finally:
        print("Finished")


if __name__ == '__main__':
	main()