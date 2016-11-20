#!/usr/bin/env python
# -*- coding: utf-8 -*-

import RPi.GPIO as GPIO
import time


class RotaryEncoder:

    '''Sets up the rotary encoder.

    :param dt_pin: The BCM pin number for the dt pin (pin A).
    :param clk_pin: The BCM pin number for the clk pin (pin B).
    :param sw_pin: The BCM pin number for the switch pin.
    '''
    def __init__(self, dt_pin, clk_pin, sw_pin):
        self.__current_clk_status = 0

        self.__dt_pin = dt_pin
        self.__clk_pin = clk_pin
        self.__sw_pin = sw_pin

        GPIO.setmode(GPIO.BCM)
        GPIO.setup(self.__clk_pin, GPIO.IN, pull_up_down=GPIO.PUD_UP)
        GPIO.setup(self.__dt_pin, GPIO.IN, pull_up_down=GPIO.PUD_UP)
        GPIO.setup(self.__sw_pin, GPIO.IN, pull_up_down=GPIO.PUD_UP)


    #==============================================================================
    # “Private” methods which shouldn’t be called from outside the module.

    '''Reads the status of pin A (dt) and pin B (clk) and calls the appropriate
    callback.

    :param arg1: Pin number which generated the events. (Is ignored.)
    '''
    def __read_status(self, arg1):
        self.__current_clk_status = GPIO.input(self.__clk_pin)
        current_dt_status = GPIO.input(self.__dt_pin)

        if self.__current_clk_status == current_dt_status:
            self.cw_callback()
        if self.__current_clk_status != current_dt_status:
            self.ccw_callback()


    '''Standard callback for clockwise rotation events.

    :param arg1: Pin number which generated the events. (Is ignored.)
    '''
    def __cw_rotation(self):
        print("clockwise rotation")


    '''Standard callback for counter clockwise rotation events.

    :param arg1: Pin number which generated the events. (Is ignored.)
    '''
    def __ccw_rotation(self):
        print("counterclockwise rotation")


    '''Standard callback for button clicked events.

    :param arg1: Pin number which generated the events. (Is ignored.)
    '''
    def __btn_clicked(self, arg1):
        print("button pressed")


    ''' Cleans up everything.
    '''
    def __cleanup(self):
        GPIO.remove_event_detect(self.__dt_pin)
        GPIO.remove_event_detect(self.__sw_pin)
        print("RotaryEncoder cleaned up.")


    #==============================================================================
    # “Public” methods which represent the api for this module.

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
    def start_listening(self,
                        cw_callback_func=__cw_rotation,
                        ccw_callback_func=__ccw_rotation,
                        btn_callback_func=__btn_clicked):
        self.cw_callback = cw_callback_func
        self.ccw_callback = ccw_callback_func

        # bouncetime is preventing multiple callback for just one event. Within
        # 100 milliseconds everything on this port is ignored. Play with this
        # setting if you getting multiple callback for one click on the rotary
        # enoceder.
        GPIO.add_event_detect(self.__dt_pin, GPIO.FALLING, callback=self.__read_status, bouncetime=100)
        GPIO.add_event_detect(self.__sw_pin, GPIO.FALLING, callback=btn_callback_func)


    '''Stops listening for events on the rotary encoder and cleans everything up.
    Call this function if you don’t want to be informed about further events on the
    rotary encoder.
    '''
    def stop_listening(self):
        self.__cleanup()
