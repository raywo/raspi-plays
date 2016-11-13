#!/usr/bin/env python
# -*- coding: utf-8 -*-

import RPi.GPIO as GPIO
import thread
import threading
import time


high      = 50
low       = 0
stepping  = 1
on_time   = 0.25
off_time  = 0.35


def setup(led_pin):
    global pin
    global p

    pin = led_pin

    # Layout festlegen auf BCM-Nummerierung
    GPIO.setmode(GPIO.BCM)

    # „atmende“ LED konfigurieren …
    GPIO.setup(pin, GPIO.OUT)
    # … und PWM starten
    p = GPIO.PWM(pin, 50)
    p.start(0)


def __loop(arg1, stopper):
    while not stopper.is_set():
        for dc in range(low, high + 1, stepping + 1):
            p.ChangeDutyCycle(dc)
            stopper.wait(0.025)

        stopper.wait(on_time)

        for dc in range(high , low - 1, -stepping):
            p.ChangeDutyCycle(dc)
            stopper.wait(0.04)

        stopper.wait(off_time)


def __cleanup():
    p.stop()
    GPIO.cleanup()


def start_breathing():
    global stop_event
    stop_event = threading.Event()
    thread.start_new_thread(__loop, (1, stop_event))


def stop_breathing():
    stop_event.set()
    time.sleep(0.1)
