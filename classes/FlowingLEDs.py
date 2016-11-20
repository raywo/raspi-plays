#!/usr/bin/env python
# -*- coding: utf-8 -*-

import time
import thread
import threading
import RPi.GPIO as GPIO
from classes.ShiftRegister595 import ShiftRegister595


'''A standard pattern like so:
10000000
11000000
01000000
01100000
and so on.
'''
_pattern = [0x80, 0xC0, 0x40, 0x60, 0x20, 0x30, 0x10, 0x18, 0x08, 0x0C, 0x04, 0x06, 0x02, 0x03, 0x01, 0x00]


'''A class for animation of a band of LEDs.

The speed of the animation is controlled by delay and inbetween_delay. Where
delay determines the delay between switching direction and inbetween_delay
determines the delay between the shifts from one pattern element to the next.
'''
class FlowingLEDs:

    '''Sets up this class.

    :param shift_register:  A reference to a shift_register which is used to
                            enable / disable the single LEDs.
    :param delay: The delay between reversing the direction of the flow.
    :param pattern: A bit pattern which describes which LEDs are on and off per
                    step.
    '''
    def __init__(self, shift_register, delay, pattern=_pattern):
        self.__inbetween_loop_delay = 0.035 # 0.03
        self.__loop_delay = delay
        self.__shift_register = shift_register
        self.__pattern = pattern


    ''' Cleans up everything.
    '''
    def __cleanup(self):
        self.__shift_register.cleanup()
        print("FlowingLEDs cleaned up.")


    def __ascending_loop(self, stopper):
        for i in range(len(self.__pattern) - 1, -1, -1):
            if stopper.is_set():
                return

            self.__shift_register.serial_write(self.__pattern[i])
            self.__shift_register.output()
            stopper.wait(self.__inbetween_loop_delay)


    def __descending_loop(self, stopper):
        for i in range(0, len(self.__pattern), 1):
            if stopper.is_set():
                return

            self.__shift_register.serial_write(self.__pattern[i])
            self.__shift_register.output()
            stopper.wait(self.__inbetween_loop_delay)


    def __loop(self, arg1, stopper):
        while not stopper.is_set():
            self.__ascending_loop(stopper)
            stopper.wait(self.__loop_delay)
            self.__descending_loop(stopper)
            stopper.wait(self.__loop_delay)

        self.__cleanup()


    def set_pattern(self, pattern):
        self.__pattern = pattern


    def set_delay(self, delay):
        self.__loop_delay = delay


    def set_inbetween_delay(self, delay):
        self.__inbetween_loop_delay = delay


    def start_flow(self):
        self.stop_event = threading.Event()
        thread.start_new_thread(self.__loop, (1, self.stop_event))


    def stop_flow(self):
        self.stop_event.set()
        time.sleep(0.1)
