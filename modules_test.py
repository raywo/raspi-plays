#!/usr/bin/env python
# -*- coding: utf-8 -*-

import leds.flowing_serial as flowing
import leds.breathing as breathing
import support.rotary_encoder_with_interrupt as rotary

counter = 0

def flow():
    #pins = [ 25, 8, 7, 1, 12, 16, 20, 21 ]
    #flowing.setup(pins)
    flowing.setup(16, 20, 21, 0.8)
    flowing.start_flow()


def breathe():
    pin = 18
    breathing.setup(pin)
    breathing.start_breathing()


def rotary_enc():
    rotary.setup(19, 26, 13)
    rotary.start_listening(cw_callback_func=__my_cw, ccw_callback_func=__my_ccw)


def __my_cw():
    global counter
    counter = counter + 1
    print("counter: %d" % counter)

def __my_ccw():
    global counter
    counter = counter - 1
    print("counter: %d" % counter)


if __name__ == '__main__':
    #breathe()
    #flow()
    rotary_enc()

    raw_input('Enter drücken zum Beenden')

    #flowing.stop_flow()
    rotary.stop_listening()
    #breathing.stop_breathing()
