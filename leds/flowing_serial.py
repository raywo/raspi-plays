#!/usr/bin/env python
# -*- coding: utf-8 -*-

import time
import thread
import threading
import RPi.GPIO as GPIO
import support.shift_register_595 as sr595

inbetween_loop_delay = 0.035 # 0.03

pattern = [0x80, 0xC0, 0x40, 0x60, 0x20, 0x30, 0x10, 0x18, 0x08, 0x0C, 0x04, 0x06, 0x02, 0x03, 0x01, 0x00]


def setup(sd_pin, st_cp_pin, sh_cp_pin, delay=0.05):
    global loop_delay
    loop_delay = delay

    sr595.setup(sd_pin, st_cp_pin, sh_cp_pin)


''' Räumt alles wieder auf.
'''
def __cleanup():
    sr595.cleanup()
    print("flowing_serial cleaned up.")


def __ascending_loop(stopper):
    for i in range(len(pattern) - 1, -1, -1):
        if stopper.is_set():
            return

        sr595.serial_write(pattern[i])
        sr595.output()
        stopper.wait(inbetween_loop_delay)


def __descending_loop(stopper):
    for i in range(0, len(pattern), 1):
        if stopper.is_set():
            return

        sr595.serial_write(pattern[i])
        sr595.output()
        stopper.wait(inbetween_loop_delay)


def __loop(arg1, stopper):
    while not stopper.is_set():
        __ascending_loop(stopper)
        __descending_loop(stopper)
        stopper.wait(loop_delay)

    __cleanup()


def start_flow():
    global stop_event
    stop_event = threading.Event()
    thread.start_new_thread(__loop, (1, stop_event))


def stop_flow():
    stop_event.set()
    time.sleep(0.1)
