from buttonsandLEDs import buttonswitches

def main():
    # Create an instance of the buttonswitches class
    btns = buttonswitches()
    try:
        while True:
            if btns.onFrontBtnPressed():
                print("front button pressed")
            if btns.onBackBtnPressed():
                print("back button pressed")
            if btns.inMeters():
                print("meters")
            else:
                print("feet")
    except KeyboardInterrupt:
        print("KeyboardInterrupt")
    finally:
        print("shutting down")
        btns.__del__()

if __name__ == '__main__':
    main()