#!/usr/bin/env python
# -*- coding: utf-8 -*-

import leds.breathing as breathing
from classes.RotaryEncoder import RotaryEncoder
from classes.FlowingLEDs import FlowingLEDs
from classes.ShiftRegister595 import ShiftRegister595

delay = 0.3
stepping = 0.005 # 0.1

def flow():
    global flowing_leds

    shift_register = ShiftRegister595(16, 20, 21)
    flowing_leds = FlowingLEDs(shift_register, delay)
    flowing_leds.start_flow()


def breathe():
    pin = 18
    breathing.setup(pin)
    breathing.start_breathing()


def rotary_enc():
    global rotary
    global delay

    delay = 0
    rotary = RotaryEncoder(19, 26, 13)
    rotary.start_listening(cw_callback_func=__my_cw, ccw_callback_func=__my_ccw)


def __my_cw():
    global delay

    delay = delay + stepping
    print("delay: %f" % delay)
    flowing_leds.set_inbetween_delay(delay)

def __my_ccw():
    global delay
    delay = delay - stepping

    if delay < 0:
        delay = 0

    print("delay: %f" % delay)
    flowing_leds.set_inbetween_delay(delay)


if __name__ == '__main__':
    #breathe()
    flow()
    rotary_enc()

    raw_input('Enter drücken zum Beenden')

    flowing_leds.stop_flow()
    rotary.stop_listening()
    #breathing.stop_breathing()
