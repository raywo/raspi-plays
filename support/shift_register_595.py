#!/usr/bin/env python
# -*- coding: utf-8 -*-

import time
import RPi.GPIO as GPIO

'''Sets up the 595 pins.

:param sd_pin: The BCM pin number of the data pin.
:param st_cp_pin: The BCM pin number of the st_sp pin.
:param sh_cp_pin: The BCM pin number of the sh_sp pin.
'''
def setup(sd_pin, st_cp_pin, sh_cp_pin):
    global sd
    global st_cp
    global sh_cp

    sd = sd_pin
    st_cp = st_cp_pin
    sh_cp = sh_cp_pin

    # Layout festlegen auf BCM-Nummerierung
    GPIO.setmode(GPIO.BCM)

    # Pins konfigurieren
    GPIO.setup(sd, GPIO.OUT)
    GPIO.setup(st_cp, GPIO.OUT)
    GPIO.setup(sh_cp, GPIO.OUT)
    GPIO.output(sd, GPIO.LOW)
    GPIO.output(st_cp, GPIO.LOW)
    GPIO.output(sh_cp, GPIO.LOW)


'''Cleans up everthing.
'''
def cleanup():
    # Pins ausschalten
    GPIO.output(sd, GPIO.LOW)
    GPIO.output(st_cp, GPIO.LOW)
    GPIO.output(sh_cp, GPIO.LOW)
    GPIO.cleanup()
    print("Shift register cleaned up.")


'''Write data to the shift register of the 595 chip.

:param data: 8 bit of data to be written to the chip.
'''
def serial_write(data):
    for bit in range(0, 8):
        GPIO.output(sd, 0x80 & (data << bit))
        GPIO.output(sh_cp, GPIO.HIGH)
        time.sleep(0.001)
        GPIO.output(sh_cp, GPIO.LOW)


'''Outputs the stored byte in parallel.
'''
def output():
    GPIO.output(st_cp, GPIO.HIGH)
    time.sleep(0.001)
    GPIO.output(st_cp, GPIO.LOW)
