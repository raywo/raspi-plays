#!/usr/bin/env python
# -*- coding: utf-8 -*-

import RPi.GPIO as GPIO

def setup(pin_bcm_no):
  # Layout festlegen auf GPIO
  GPIO.setmode(GPIO.BCM)

  # LED-Pin auf Output setzen
  GPIO.setup(pin_bcm_no, GPIO.OUT)


# alles herrichten
# festlegen auf welchen Pin die LED steckt
led_pin = 18
setup(led_pin)

# LED ausschalten
GPIO.output(led_pin, GPIO.LOW)

# alles wieder aufräumen
GPIO.cleanup()
