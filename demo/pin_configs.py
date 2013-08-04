import RPi.GPIO as GPIO

from gpio_map_board import *

class BaseRPiPinConfig(object):
    def __init__(self, cleanup=False):
        self.registered_channels = {}
        self.defaults = {}
        if cleanup:
            self.cleanup()
        self._setup_pins()

    def cleanup(self):
        """Cleanup GPIO settings
        """
        for channel in self.registered_channels.keys():
            del self.registered_channels[channel]
        GPIO.cleanup()

    def _setup_pins(self):
        self.IN = []
        self.OUT = []

        GPIO.setmode(GPIO.BOARD)
        #GPIO.setwarnings(False)

        inputs = self.get_inputs()
        for channel in inputs:
            GPIO.setup(channel, GPIO.IN)
            self.IN.append(channel)

        outputs = self.get_outputs()
        for (channel, default,) in outputs:
            # per https://code.google.com/p/raspberry-gpio-python/wiki/BasicUsage
            self.defaults[channel] = default
            GPIO.setup(channel, GPIO.OUT, initial=default)
            self.OUT.append(channel)

    def get_inputs(self):
        inputs = []
        return inputs

    def get_outputs(self):
        outputs = []
        return outputs

    def reset(self):
        """Resets all output pins to default value
        """
        for channel, default in self.defaults.items():
            GPIO.output(channel, default)

    def input(self, channel):
        """Check GPIO.input for `channel`
        """
        signal = GPIO.input(channel) == GPIO.HIGH
        return signal

    def pwm(self, channel, frequency):
        pwm = GPIO.PWM(channel, frequency)
        return pwm

    def register(self, channel, callback, bouncetime=200):
        return
        """Adds a callback on event

        `bouncetime` milliseconds

        Switch debounce technique
        https://code.google.com/p/raspberry-gpio-python/wiki/Inputs#Switch_debounce
        """
        if channel not in self.registered_channels:
            # add the event detection and callback separately
            #GPIO.add_event_detect(channel, GPIO.RISING, callback=callback, bouncetime=bouncetime)
            GPIO.remove_event_detect(channel)
            GPIO.add_event_detect(channel, GPIO.RISING)
            self.registered_channels[channel] = {}
        channel_callbacks = self.registered_channels[channel]
        if callback not in channel_callbacks:
            # limit adding a particular callback function on a particular channel to one time
            channel_callbacks[callback] = True
            GPIO.add_event_callback(channel, callback, bouncetime=bouncetime)

    def deregister(self, channel):
        if channel in self.registered_channels:
            GPIO.remove_event_detect(channel)
            del self.registered_channels[channel]

class SwitchLedRPiPinConfig(BaseRPiPinConfig):
    def get_inputs(self):
        inputs = [
            GP0,
            GP1,
        ]
        return inputs

    def get_outputs(self):
        output_channels = [
            GP2,
            GP3,
            GP4,
            GP5,
            GP6,
            GP7,
        ]
        outputs = [(channel, GPIO.HIGH,) for channel in output_channels]
        return outputs

    def led(self, channel, on=True):
        """Turns an LED on or off at GPIO `channel`

        on = high
        off = low
        """
        is_high = not(on)
        GPIO.output(channel, is_high)

    def led_on(self, channel):
        self.led(channel, on=True)

    def led_off(self, channel):
        self.led(channel, on=False)
