#!/usr/bin/env python
# -*- coding: utf-8 -*-

import time
import RPi.GPIO as GPIO

# Layout festlegen auf GPIO
GPIO.setmode(GPIO.BCM)

# festlegen auf welchen Pin die LED steckt
led_pin = 18

# LED-Pin auf Output setzen
GPIO.setup(led_pin, GPIO.OUT)

# in einer Endlosschleife die LED blinken lassen
try:
  while 1:
    # ausschalten
    GPIO.output(led_pin, GPIO.LOW)

    # kurz warten
    time.sleep(0.5)

    # anschalten
    GPIO.output(led_pin, GPIO.HIGH)

    # kurz warten
    time.sleep(0.5)
except KeyboardInterrupt:
    pass

# alles wieder aufräumen
GPIO.cleanup
