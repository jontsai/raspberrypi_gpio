from time import sleep

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
    GPIO.setup(13, GPIO.OUT)
    GPIO.setup(15, GPIO.OUT)
    GPIO.setup(16, GPIO.OUT)

def driver_loop():
    print 'Entering driver loop'

    while True:
        print 'Output 13'
        GPIO.output(13, False)
        sleep(1)
        GPIO.output(13, True)
        sleep(1)

        print 'Output 15'
        GPIO.output(15, False)
        sleep(1)
        GPIO.output(15, True)
        sleep(1)

        print 'Output 16'
        GPIO.output(16, False)
        sleep(1)
        GPIO.output(16, True)
        sleep(1)

if __name__ == '__main__':
    main()
