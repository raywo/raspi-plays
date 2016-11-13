#!/usr/bin/env python
# -*- coding: utf-8 -*-

import RPi.GPIO as GPIO
import time

# Output-Pins festlegen
sd_pin = 16
st_cp_pin = 20
sh_cp_pin = 21

#=========================================
# Muster für eine geschaltete Zeile
#rows = [ 0x01, 0x02, 0x04, 0x08, 0x10, 0x20, 0x40, 0x80 ]
#cols = [ 0x00, 0x00, 0x00, 0x00, 0x00, 0x00, 0x00, 0x00 ]
# Muster für eine geschaltete Spalte
rows = [ 0xFF, 0xFF, 0xFF, 0xFF, 0xFF, 0xFF, 0xFF, 0xFF ]
cols = [ 0xFE, 0xFD, 0xFB, 0xF7, 0xEF, 0xDF, 0xBF, 0x7F ]

def setup():
  # Layout festlegen auf BCM
  GPIO.setmode(GPIO.BCM)
  # Pins auf Output setzen
  GPIO.setup(sd_pin, GPIO.OUT)
  GPIO.setup(st_cp_pin, GPIO.OUT)
  GPIO.setup(sh_cp_pin, GPIO.OUT)
  # Pins ausschalten
  GPIO.output(sd_pin, GPIO.LOW)
  GPIO.output(st_cp_pin, GPIO.LOW)
  GPIO.output(sh_cp_pin, GPIO.LOW)


# Räumt alles wieder auf.
def destroy():
    # Pins ausschalten
    GPIO.output(sd_pin, GPIO.LOW)
    GPIO.output(st_cp_pin, GPIO.LOW)
    GPIO.output(sh_cp_pin, GPIO.LOW)
    GPIO.cleanup()


# Schreibt die Daten in die Chips.
def write_to_chip(data):
    for bit in range(0, 8):
        GPIO.output(sd_pin, 0x80 & (data << bit))
        GPIO.output(sh_cp_pin, GPIO.HIGH)
        time.sleep(0.001)
        GPIO.output(sh_cp_pin, GPIO.LOW)


# Schreibt die Daten aus den Chips auf die Dot-Matrix.
def output_to_matrix():
    GPIO.output(st_cp_pin, GPIO.HIGH)
    time.sleep(0.001)
    GPIO.output(st_cp_pin, GPIO.LOW)


# Die Hauptschleife des Programms
def loop():
    while True:
        for i in range(0, len(cols)):
            write_to_chip(rows[i])
            write_to_chip(cols[i])
            output_to_matrix()
            raw_input("weiter")
            time.sleep(0.1)

        for i in range(len(cols)-1, -1, -1):
            write_to_chip(rows[i])
            write_to_chip(cols[i])
            output_to_matrix()
            time.sleep(0.1)


# Das Programm startet hier.
if __name__ == '__main__':
    setup()
    try:
        loop()
    except KeyboardInterrupt:
        destroy()
