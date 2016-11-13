#!/usr/bin/env python
# -*- coding: utf-8 -*-

import leds.flowing_serial as flowing
import leds.breathing as breathing

def flow():
    #pins = [ 25, 8, 7, 1, 12, 16, 20, 21 ]
    #flowing.setup(pins)
    flowing.setup(16, 20, 21, 0.8)
    flowing.start_flow()


def breathe():
    pin = 18
    breathing.setup(pin)
    breathing.start_breathing()


if __name__ == '__main__':
    #breathe()
    flow()

    raw_input('Enter drücken zum Beenden')

    flowing.stop_flow()
    #breathing.stop_breathing()
