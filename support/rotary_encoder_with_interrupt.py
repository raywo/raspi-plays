#!/usr/bin/env python
# -*- coding: utf-8 -*-

import RPi.GPIO as GPIO
import time


last_clk_status = 0
current_clk_status = 0


#==============================================================================
# “Private” methods which shouldn’t be called from outside the module.

'''Reads the status of pin A (dt) and pin B (clk) and calls the appropriate
callback.

:param arg1: Pin number which generated the events. (Is ignored.)
'''
def __read_status(arg1):
    global current_clk_status
    global current_dt_status

    current_clk_status = GPIO.input(clk)
    current_dt_status = GPIO.input(dt)

    if current_clk_status == current_dt_status:
        cw_callback()
    if current_clk_status != current_dt_status:
        ccw_callback()


'''Standard callback for clockwise rotation events.

:param arg1: Pin number which generated the events. (Is ignored.)
'''
def __cw_rotation():
    print("Im Uhrzeigersinn gedreht")


'''Standard callback for counter clockwise rotation events.

:param arg1: Pin number which generated the events. (Is ignored.)
'''
def __ccw_rotation():
    print("entgegengesetzt zum Uhrzeigersinn gedreht")


'''Standard callback for button clicked events.

:param arg1: Pin number which generated the events. (Is ignored.)
'''
def __btn_clicked(arg1):
    print("der Knopf wurde gedrückt")


''' Cleans up everything.
'''
def __cleanup():
    GPIO.remove_event_detect(dt)
    GPIO.remove_event_detect(sw)
    GPIO.cleanup()
    print("Rotary cleaned up.")


#==============================================================================
# “Public” methods which represent the api for this module.

'''Sets up the rotary encoder.

:param dt_pin: The BCM pin number for the dt pin (pin A).
:param clk_pin: The BCM pin number for the clk pin (pin B).
:param sw_pin: The BCM pin number for the switch pin.
'''
def setup(dt_pin, clk_pin, sw_pin):
    global clk  # Pin B
    global dt   # Pin A
    global sw

    clk = clk_pin
    dt = dt_pin
    sw = sw_pin

    GPIO.setmode(GPIO.BCM)
    GPIO.setup(clk, GPIO.IN, pull_up_down=GPIO.PUD_UP)
    GPIO.setup(dt, GPIO.IN, pull_up_down=GPIO.PUD_UP)
    GPIO.setup(sw, GPIO.IN, pull_up_down=GPIO.PUD_UP)


'''Starts listening for events on the rotary encoder.
Call this function if you are interested in rotation and click events from this
rotary encoder.

:param cw_callback_func:    The callback which is called when a clockwise
                            rotation is recognized. Leave blank if
                            you don’t need it. A standard callback will be
                            called which prints a message on the screen.
:param ccw_callback_func:   The callback which is called when a counter
                            clockwise rotation is recognized. Leave blank if
                            you don’t need it. A standard callback will be
                            called which prints a message on the screen.
:param btn_callback_func:   The callback which is called when a button click is
                            detected. Leave blank if you don’t need it. A
                            standard callback will be called which prints a
                            message on the screen.
'''
def start_listening(cw_callback_func=__cw_rotation,
                    ccw_callback_func=__ccw_rotation,
                    btn_callback_func=__btn_clicked):
    global cw_callback
    global ccw_callback

    cw_callback = cw_callback_func
    ccw_callback = ccw_callback_func

    # bouncetime is preventing multiple callback for just one event. Within
    # 100 milliseconds everything on this port is ignored. Play with this
    # setting if you getting multiple callback for one click on the rotary
    # enoceder.
    GPIO.add_event_detect(dt, GPIO.FALLING, callback=__read_status, bouncetime=100)
    GPIO.add_event_detect(sw, GPIO.FALLING, callback=btn_callback_func)


'''Stops listening for events on the rotary encoder and cleans everything up.
Call this function if you don’t want to be informed about further events on the
rotary encoder.
'''
def stop_listening():
    __cleanup()
