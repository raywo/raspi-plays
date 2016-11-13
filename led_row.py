#!/usr/bin/env python
# -*- coding: utf-8 -*-

import RPi.GPIO as GPIO
import time

led_pins = [ 25, 8, 7, 1, 12, 16, 20, 21 ]
sleep_time_1 = 0.03
sleep_time_2 = 0.05


def setup():
  # Layout festlegen auf BCM-Nummerierung
  GPIO.setmode(GPIO.BCM)

  for pin in led_pins:
      GPIO.setup(pin, GPIO.OUT)
      GPIO.output(pin, GPIO.HIGH)


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


def cleanup():
    # alles wieder aufräumen
    GPIO.cleanup()


def loop():
    while True:
        right_loop()
        left_loop()


if __name__ == '__main__':
    setup()

    try:
        loop()
    except KeyboardInterrupt:
        cleanup()
