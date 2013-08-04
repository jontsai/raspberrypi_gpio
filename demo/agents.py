from time import sleep
import threading

from pin_configs import BaseRPiPinConfig
from pin_configs import SwitchLedRPiPinConfig
from routines import get_random_routine
from routines import get_routine_n
from settings import DEFAULT_ROUTINE_SETTINGS

CYCLE_SLEEP_DURATION = 10 # milliseconds
ROUTINE_ROTATION_DURATION = 15000 # milliseconds

class BaseRPiAgent(threading.Thread):
    def __init__(self, pin_config=None, *args, **kwargs):
        #threading.Thread.__init__(self, *args, **kwargs)
        super(BaseRPiAgent, self).__init__(*args, **kwargs)
        self.pins = BaseRPiPinConfig(cleanup=True) if pin_config is None else pin_config
        self.should_run = True
        self.routine = None
        self.set_routine_settings()
        self.running_time = 0

    def set_routine_settings(self):
        """Initialize routine settings to defaults
        """
        self.routine_settings = DEFAULT_ROUTINE_SETTINGS

    def run(self):
        print 'Running %s' % (self.__class__.__name__,)
        while self.should_run:
            self.execute_routine()
            # CYCLE_SLEEP_DURATION expresed in milliseconds to prevent rounding errors
            sleep(CYCLE_SLEEP_DURATION / 1000.)
            self.running_time += CYCLE_SLEEP_DURATION

    def get_routine(self):
        routine = self.routine if hasattr(self, 'routine') else None
        return routine

    def execute_routine(self):
        """Abstract method
        """
        pass

    def terminate(self):
        self.should_run = False
        # routine = self.get_routine()
        # if routine:
        #     while False and routine.is_alive():
        #         print 'Waiting for children threads to die...'
        #         sleep(1)
        print 'Cleaning up...'
        self.pins.cleanup()

class DemoRPiAgent(BaseRPiAgent):
    def __init__(self, *args, **kwargs):
        pin_config = SwitchLedRPiPinConfig(cleanup=True)
        pins = pin_config
        super(DemoRPiAgent, self).__init__(pin_config=pin_config, *args, **kwargs)
        self.current_routine_index = 0
        self.switch_current_routine(index=self.current_routine_index)
        self.button_sequence = []
        self.button_pattern_routines = (
            ([pins.IN[0], pins.IN[1], pins.IN[0], pins.IN[1]],
             self.switch_current_routine,)
        )

    def handle_button_pressed(self, channel):
        # store/update the button press to the button sequence
        self.button_sequence.append(channel)
        self.check_sequence()

    def check_sequence(self):
        """Checks for a matched button sequence
        If there is a match, kicks off the matched button sequence routine

        We are using this technique since the techniques for detecting combination button presses are limited
        Detecting combination button presses only gives us 2^B states, where B is the number of buttons
        However, with this technique, we can have infinitely long sequences and infinitely many distinct commands
        """
        sequence = self.button_sequence
        # if a matched sequence is found, kick off the button routine
        for pattern, button_routine in self.button_pattern_routines:
            while len(pattern) >= len(sequence):
                if pattern[:len(sequence)] == sequence:
                    # compare slices/subsequences to see if there is a match
                    button_routine()
                    break
                else:
                    # shorten the pattern
                    pattern = pattern[1:]

    def execute_routine(self):
        pins = self.pins
        pins.register(pins.IN[0], self.handle_button_pressed)
        pins.register(pins.IN[1], self.handle_button_pressed)

        if self.running_time > 0 and self.running_time % ROUTINE_ROTATION_DURATION == 0:
            # change routines every so often
            print 'Demo running time: %ss' % (self.running_time / 1000.)
            self.switch_current_routine()

        if not hasattr(self, 'routine') or self.routine is None:
            # no routine set, so set one
            routine = self.current_routine_class(self)
            routine.start()
            self.routine = routine
        else:
            # there is a routine
            routine = self.routine
            if routine.is_alive():
                # wait for routine to finish running
                pass
            else:
                self.routine = None

    def switch_current_routine(self, index=None, random=False):
        print 'Switching routines...'
        if random:
            routine_class = get_random_routine()
        else:
            if index is None:
                # get the next one
                index = self.current_routine_index + 1
            self.current_routine_index = index
            routine_class = get_routine_n(index)
        self.current_routine_class = routine_class
        print 'Current routine: %s' % routine_class.__name__
        return routine_class
