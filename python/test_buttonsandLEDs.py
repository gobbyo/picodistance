from buttonswitches import buttonswitches

def main():
    # Create an instance of the buttonswitches class
    btns = buttonswitches()
    try:
        prev = "feet"
        while True:
            if btns.onFrontBtnPressed():
                print("front button pressed")
            if btns.onBackBtnPressed():
                print("back button pressed")
            if btns.inMeters():
                if prev == "feet":
                    print("meters")
                    prev = "meters"
            else:
                if prev == "meters":
                    print("feet")
                    prev = "feet"
    except KeyboardInterrupt:
        print("KeyboardInterrupt")
    finally:
        print("shutting down")
        btns.__del__()

if __name__ == '__main__':
    main()