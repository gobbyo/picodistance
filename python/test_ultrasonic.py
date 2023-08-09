from ultrasonicsensor import ultrasonic
from distancestringtool import distancestring

def main():
    us = ultrasonic()
    distance = distancestring()
    try:
        for i in range(3):
            d = us.getdistancemeasure()
            distance.set(d)
            print("{0}' {1:.2f}\"".format(distance.s_feet, float(distance.s_inches)))
            print("{0}m {1:.2f}cm".format(distance.meters, float(distance.centimeters)))
    except KeyboardInterrupt:
        print("KeyboardInterrupt")
    finally:
        print("shutting down")
        us.__del__()

if __name__ == '__main__':
    main()