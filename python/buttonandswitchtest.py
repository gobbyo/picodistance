from machine import Pin
import time

shutdown = const(30)
conversionbuttonpin = const(15)
frontdistancebuttonpin = const(14)
backdistancebuttonpin = const(13)


def main():   

    frontdistancebutton=Pin(frontdistancebuttonpin,Pin.IN,Pin.PULL_DOWN)
    backdistancebutton=Pin(backdistancebuttonpin,Pin.IN,Pin.PULL_DOWN)
    conversionbutton=Pin(conversionbuttonpin,Pin.IN,Pin.PULL_DOWN)

    try:
        t = time.time() + shutdown
        backlastvalue = 0
        backcurrentvalue = 0
        frontlastvalue = 0
        frontcurrentvalue = 0
        convlastvalue = 0
        convcurrentvalue = 0

        while t > time.time():
            frontcurrentvalue = frontdistancebutton.value()
            if frontcurrentvalue != frontlastvalue:
                frontlastvalue = frontcurrentvalue
                if frontcurrentvalue == 1:
                    print("front distance button pressed")
                else:
                    print("front distance button released")

            backcurrentvalue = backdistancebutton.value()
            if backcurrentvalue != backlastvalue:
                backlastvalue = backcurrentvalue
                if backcurrentvalue == 1:
                    print("back distance button pressed")
                else:
                    print("back distance button released")
            
            convcurrentvalue = conversionbutton.value()
            if convcurrentvalue != convlastvalue:
                convlastvalue = convcurrentvalue
                if convcurrentvalue == 1:
                    print("meters")
                else:
                    print("feet")


    finally:
        print("exiting program")

if __name__ == '__main__':
	main()