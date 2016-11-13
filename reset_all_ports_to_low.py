#!/usr/bin/env python
# -*- coding: utf-8 -*-

import RPi.GPIO as GPIO


def setup():
  # Layout festlegen auf physikalische Pins
  GPIO.setmode(GPIO.BCM)

  for pin in range(1, 27):
      GPIO.setup(pin, GPIO.IN)


if __name__ == '__main__':
    setup()
    # alles wieder aufräumen
    GPIO.cleanup()
