import RPi.GPIO as GPIO

def main():
    try:
        cleanup()
        setup()
        driver_loop()
    except KeyboardInterrupt:
        print 'Got KeyboardInterrupt'
    finally:
        print 'Cleaning up...'
        cleanup()

def cleanup():
    GPIO.cleanup()

def setup():
    GPIO.setmode(GPIO.BOARD)
    #GPIO.setwarnings(False)

    GPIO.setup(11, GPIO.IN)
    GPIO.setup(12, GPIO.IN)

    GPIO.setup(13, GPIO.OUT)
    GPIO.setup(15, GPIO.OUT)

def driver_loop():
    print 'Entering driver loop'
    while True:
        if GPIO.input(11):
            GPIO.output(13, False)
        else:
            GPIO.output(13, True)

        if GPIO.input(12):
            GPIO.output(15, False)
        else:
            GPIO.output(15, True)

if __name__ == '__main__':
    main()
