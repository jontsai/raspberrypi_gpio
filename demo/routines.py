from time import sleep
import random
import threading

class BaseRPiRoutine(threading.Thread):
    def __init__(self, agent, *args, **kwargs):
        #threading.Thread.__init__(self, *args, **kwargs)
        super(BaseRPiRoutine, self).__init__(*args, **kwargs)
        # set daemon thread flag
        # allows entire Python program to exit when only daemon threads are left
        self.daemon = True
        self.agent = agent # store reference to RPiAgent
        self.pins = agent.pins

    def run(self):
        self.pins.reset()
        self.routine()

    def settings(self, setting_name, new_value=None):
        """Set or retrieve routine setting value stored in RPiAgent
        """
        routine_settings = self.agent.routine_settings.get(self.__class__.__name__, None)
        if routine_settings:
            if new_value:
                routine_settings[setting_name] = new_value
            setting_value = routine_settings.get(setting_name)
        else:
            setting_value = None
        return setting_value

    def signal(self, channel):
        """Being notified of input received from upstream
        """
        pass

class LedCycleRPiRoutine(BaseRPiRoutine):
    def routine(self):
        pins = self.pins
        pins.register(pins.IN[0], lambda channel: self.speed_up())
        pins.register(pins.IN[1], lambda channel: self.slow_down())
        for x in xrange(6):
            pins.led_on(pins.OUT[x])
            sleep(self.settings('cycle_delay'))
            pins.led_off(pins.OUT[x])
        pins.deregister(pins.IN[0])
        pins.deregister(pins.IN[1])

    def speed_up(self):
        cycle_delay_min = self.settings('cycle_delay_min')
        cycle_delay_step = self.settings('cycle_delay_step')
        cycle_delay = self.settings('cycle_delay')
        cycle_delay = max(cycle_delay_min, cycle_delay - cycle_delay_step)
        self.settings('cycle_delay', cycle_delay)
        print 'Sped up, cycle delay: %2f' % cycle_delay

    def slow_down(self):
        cycle_delay_max = self.settings('cycle_delay_max')
        cycle_delay_step = self.settings('cycle_delay_step')
        cycle_delay = self.settings('cycle_delay')
        cycle_delay = min(cycle_delay_max, cycle_delay + cycle_delay_step)
        self.settings('cycle_delay', cycle_delay)
        print 'Slowed down, cycle delay: %2f' % cycle_delay

class TwinklingLedRPiRoutine(BaseRPiRoutine):
    def routine(self):
        """Twinkle lights on and off randomly
        """
        pins = self.pins
        lights_on = []
        for x in xrange(6):
            if random.choice([True, False]):
                lights_on.append(pins.OUT[x])
        for light in lights_on:
            pins.led_on(light)
        delay = self.settings('max_delay') * random.random()
        sleep(delay)
        for light in lights_on:
            pins.led_off(light)

class BinaryCountLedRPiRoutine(BaseRPiRoutine):
    def routine(self):
        """With 6 LEDs, counts from 0 to 2^6 -1 (63)
        """
        pins = self.pins
        for n in xrange(2**6):
            bits = self.num_to_bit_array(n)
            for k in xrange(len(bits)):
                if bits[k]:
                    pins.led_on(pins.OUT[k])
            sleep(self.settings('delay'))
            for k in xrange(len(bits)):
                if bits[k]:
                    pins.led_off(pins.OUT[k])

    def num_to_bit_array(self, n):
        """Translates a number into a bit array
        0 = [0, 0, 0, 0, 0, 0]
        1 = [1, 0, 0, 0, 0, 0]
        2 = [0, 1, 0, 0, 0, 0]
        3 = [1, 1, 0, 0, 0, 0]
        4 = [0, 0, 1, 0, 0, 0]
        ...
        62 = [0, 1, 1, 1, 1, 1]
        63 = [1, 1, 1, 1, 1, 1]
        """
        bits = []
        for x in xrange(6):
            bits.append(n % 2 == 1)
            n >>= 1
        return bits

class ButtonControlSetsRPiRoutine(BaseRPiRoutine):
    def routine(self):
        pins = self.pins
        in0 = pins.input(pins.IN[0])
        in1 = pins.input(pins.IN[1])

        # first set of triplets
        pins.led(pins.OUT[0], on=in0)
        pins.led(pins.OUT[1], on=in0)
        pins.led(pins.OUT[2], on=in0)

        # second set of triplets
        pins.led(pins.OUT[3], on=in1)
        pins.led(pins.OUT[4], on=in1)
        pins.led(pins.OUT[5], on=in1)

ROUTINE_CLASSES = [
    LedCycleRPiRoutine,
    TwinklingLedRPiRoutine,
    BinaryCountLedRPiRoutine,
    ButtonControlSetsRPiRoutine,
]

def get_random_routine():
    routine_class = random.choice(ROUTINE_CLASSES)
    return routine_class

def get_routine_n(index):
    routine_class = ROUTINE_CLASSES[index % len(ROUTINE_CLASSES)]
    return routine_class
