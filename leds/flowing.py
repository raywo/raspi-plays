#!/usr/bin/env python
# -*- coding: utf-8 -*-

import time
import thread
import threading
import RPi.GPIO as GPIO

inbetween_loop_delay = 0.03

def setup(led_pins, delay=0.05):
    global pins
    global loop_delay

    pins = led_pins
    loop_delay = delay

    # Layout festlegen auf BCM-Nummerierung
    GPIO.setmode(GPIO.BCM)

    # Pins für Lauflicht konfigurieren
    for pin in pins:
      GPIO.setup(pin, GPIO.OUT)
      GPIO.output(pin, GPIO.HIGH)


'''Start the loop from pins[0] to pins[length-1].

The stopper variable is use to determine, whether the loop should be
canceled or not.
'''
def __ascending_loop(stopper):
    for i in range(0, len(pins)):
        if stopper.is_set():
            return

        GPIO.output(pins[i], GPIO.LOW)

        if i + 1 < len(pins):
            stopper.wait(inbetween_loop_delay)
            GPIO.output(pins[i + 1], GPIO.LOW)
            stopper.wait(inbetween_loop_delay)
            GPIO.output(pins[i], GPIO.HIGH)

        stopper.wait(loop_delay)


def __descending_loop(stopper):
    for i in range(len(pins) - 1, -1, -1):
        if stopper.is_set():
            return

        if i - 1 >= 0:
            stopper.wait(inbetween_loop_delay)
            GPIO.output(pins[i - 1], GPIO.LOW)
            stopper.wait(inbetween_loop_delay)
            GPIO.output(pins[i], GPIO.HIGH)

        stopper.wait(loop_delay)


def __loop(arg1, stopper):
    while(not stopper.is_set()):
        __ascending_loop(stopper)
        __descending_loop(stopper)

    __cleanup()


def __cleanup():
    GPIO.cleanup()


def start_flow():
    global stop_event
    stop_event = threading.Event()
    thread.start_new_thread(__loop, (1, stop_event))


def stop_flow():
    stop_event.set()
    time.sleep(0.1)
