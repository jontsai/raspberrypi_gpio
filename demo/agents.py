from time import sleep
import threading

from pin_configs import BaseRPiPinConfig
from pin_configs import SwitchLedRPiPinConfig
from routines import get_random_routine
from routines import get_routine_n
from settings import DEFAULT_ROUTINE_SETTINGS

class BaseRPiAgent(threading.Thread):
    def __init__(self, pin_config=None, *args, **kwargs):
        #threading.Thread.__init__(self, *args, **kwargs)
        super(BaseRPiAgent, self).__init__(*args, **kwargs)
        self.pins = BaseRPiPinConfig(cleanup=True) if pin_config is None else pin_config
        self.should_run = True
        self.routine = None
        self.set_routine_settings()

    def set_routine_settings(self):
        """Initialize routine settings to defaults
        """
        self.routine_settings = DEFAULT_ROUTINE_SETTINGS

    def run(self):
        print 'Running %s' % (self.__class__.__name__,)
        while self.should_run:
            self.execute_routine()
            sleep(0.01) # sleep for 10 milliseconds

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
        super(DemoRPiAgent, self).__init__(pin_config=pin_config, *args, **kwargs)
        self.current_routine_index = 0
        self.switch_current_routine(index=self.current_routine_index)

    def execute_routine(self):
        pins = self.pins
        # def callback(x):
        #     if pins.input(pins.IN[0]) and pins.input(pins.IN[1]):
        #         self.switch_current_routine()
        # pins.register(pins.IN[0], callback, bouncetime=200)
        if pins.input(pins.IN[0]) and pins.input(pins.IN[1]):
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
