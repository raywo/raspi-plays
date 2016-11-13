#!/usr/bin/env python
# -*- coding: utf-8 -*-

import RPi.GPIO as GPIO
import time
import thread

#=====================================================
# Pins für Lauflicht
led_pins = [ 25, 8, 7, 1, 12, 16, 20, 21 ]
sleep_time_1 = 0.03
sleep_time_2 = 0.05
# Einstellungen für „atmende“ LED
led_pin   = 18
high      = 50
low       = 0
stepping  = 1
on_time   = 0.25
off_time  = 0.35
#=====================================================


def setup():
    global p
    # Layout festlegen auf BCM-Nummerierung
    GPIO.setmode(GPIO.BCM)

    # Pins für Lauflicht konfigurieren
    for pin in led_pins:
      GPIO.setup(pin, GPIO.OUT)
      GPIO.output(pin, GPIO.HIGH)

    # „atmende“ LED konfigurieren …
    GPIO.setup(led_pin, GPIO.OUT)
    # … und PWM starten
    p = GPIO.PWM(led_pin, 50)
    p.start(0)


def right_loop():
    for i in range(0, len(led_pins)):
        GPIO.output(led_pins[i], GPIO.LOW)

        if i + 1 < len(led_pins):
            time.sleep(sleep_time_1)
            GPIO.output(led_pins[i + 1], GPIO.LOW)
            time.sleep(sleep_time_1)
            GPIO.output(led_pins[i], GPIO.HIGH)

        time.sleep(sleep_time_2)


def left_loop():
    for i in range(len(led_pins) - 1, -1, -1):
        if i - 1 >= 0:
            time.sleep(sleep_time_1)
            GPIO.output(led_pins[i - 1], GPIO.LOW)
            time.sleep(sleep_time_1)
            GPIO.output(led_pins[i], GPIO.HIGH)

        time.sleep(sleep_time_2)


def breathe_loop(p):
    while True:
        for dc in range(low, high + 1, stepping + 1):
            p.ChangeDutyCycle(dc)
            time.sleep(0.025)

        time.sleep(on_time)

        for dc in range(high , low - 1, -stepping):
            p.ChangeDutyCycle(dc)
            time.sleep(0.04)

        time.sleep(off_time)


def loop():
    while True:
        right_loop()
        left_loop()


def cleanup():
    # alles wieder aufräumen
    p.stop()
    GPIO.cleanup()


if __name__ == '__main__':
    setup()

    try:
        thread.start_new_thread(breathe_loop, (p , ))
        loop()
    except KeyboardInterrupt:
        cleanup()
