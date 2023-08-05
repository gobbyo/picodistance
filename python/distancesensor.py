from distancestringtool import distancestring
from buttonswitches import buttonswitches
from ultrasonicsensor import ultrasonic
from segmentdisplays import segdisplays
from diodeLasers import diodeLaser

frontbuttoncorrection = -12 #millimeters
backbuttoncorrection = 40 #millimeters

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
                d = us.getdistancemeasure()
                d += frontbuttoncorrection
                distance.set(d)
                if(d != prev):
                    display.showforwardfloat()
                    display.showforwardnumber()
                    prev = d

            if switches.onBackBtnPressed():
                d = us.getdistancemeasure()
                if d > 0:
                    d += backbuttoncorrection
                distance.set(d)
                if(d != prev):
                    display.showbacknumber()
                    display.showbackfloat()
                    prev = d

            if switches.inMeters():
                for w in range(display.waitreps):
                    display.printnumber(distance.meters)
                    display.printfloat(distance.centimeters)
            else:
               for w in range(display.waitreps):
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