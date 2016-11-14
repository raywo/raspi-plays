#!/usr/bin/env python
# -*- coding: utf-8 -*-

import RPi.GPIO as GPIO
import time
import thread
import threading


last_clk_status = 0
current_clk_status = 0
flag = 0

def setup(clk_pin, dt_pin, sw_pin):
    global clk
    global dt
    global sw

    clk = clk_pin
    dt = dt_pin
    sw = sw_pin

    GPIO.setmode(GPIO.BCM)
    GPIO.setup(clk, GPIO.IN)
    GPIO.setup(dt, GPIO.IN)
    GPIO.setup(sw, GPIO.IN, pull_up_down=GPIO.PUD_UP)


def __poll_rotary(stopper):
    global flag
    global last_clk_status
    global current_clk_status

    last_clk_status = GPIO.input(clk)

    while((not GPIO.input(dt) and (not stopper.is_set()))):
        current_clk_status = GPIO.input(clk)
        flag = 1

    if flag == 1:
        flag = 0
        if (last_clk_status == 0) and (current_clk_status == 1):
            cw_callback()
        if (last_clk_status == 1) and (current_clk_status == 0):
            ccw_callback()


def __loop(arg1, stopper):
    while not stopper.is_set():
        __poll_rotary(stopper)


def __cw_rotation():
    print("Im Uhrzeigersinn gedreht")


def __ccw_rotation():
    print("entgegengesetzt zum Uhrzeigersinn gedreht")


def __btn_clicked(arg1):
    print("der Knopf wurde gedrückt")


def __cleanup():
    GPIO.cleanup()
    print("Rotary cleaned up.")


def start_listening(cw_callback_func=__cw_rotation,
                    ccw_callback_func=__ccw_rotation,
                    btn_callback_func=__btn_clicked):
    global stop_event
    global cw_callback
    global ccw_callback

    cw_callback = cw_callback_func
    ccw_callback = ccw_callback_func

    GPIO.add_event_detect(sw, GPIO.FALLING, callback=btn_callback_func)

    stop_event = threading.Event()
    thread.start_new_thread(__loop, (1, stop_event))


def stop_listening():
    stop_event.set()
    time.sleep(0.9)
    __cleanup()
