#!/usr/bin/env python
# -*- coding: utf-8 -*-

import time
import RPi.GPIO as GPIO


# alles herrichten
# festlegen auf welchen Pin die LED steckt
led_pin   = 18
high      = 50
low       = 0
stepping  = 1
on_time   = 0.25
off_time  = 0.35


def setup():
    global p
    print("Gleich sollte die LED „atmen“. (Mit CTRL + C abbrechen.)")

    # Layout festlegen auf GPIO
    GPIO.setmode(GPIO.BCM)

    # LED-Pin auf Output setzen
    GPIO.setup(led_pin, GPIO.OUT)

    p = GPIO.PWM(led_pin, 50)
    p.start(0)


def loop():
    while True:
        for dc in range(low, high + 1, stepping + 1):
            p.ChangeDutyCycle(dc)
            time.sleep(0.025)

        time.sleep(on_time)

        for dc in range(high , low - 1, -stepping):
            p.ChangeDutyCycle(dc)
            time.sleep(0.04)

        time.sleep(off_time)


def cleanup():
    p.stop()
    GPIO.cleanup()


if __name__ == '__main__':
    setup()
    try:
        loop()
    except KeyboardInterrupt:
        cleanup()
