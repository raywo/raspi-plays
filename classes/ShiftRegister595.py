#!/usr/bin/env python
# -*- coding: utf-8 -*-

import time
import RPi.GPIO as GPIO


class ShiftRegister595:

    def __init__(self, sd_pin, st_cp_pin, sh_cp_pin):
        self.__sd_pin = sd_pin
        self.__st_cp_pin = st_cp_pin
        self.__sh_cp_pin = sh_cp_pin

        # set pin numbering
        GPIO.setmode(GPIO.BCM)

        # Configure pins to output and set them to low in order to have a
        # fixed starting point.
        GPIO.setup(self.__sd_pin, GPIO.OUT)
        GPIO.setup(self.__st_cp_pin, GPIO.OUT)
        GPIO.setup(self.__sh_cp_pin, GPIO.OUT)
        GPIO.output(self.__sd_pin, GPIO.LOW)
        GPIO.output(self.__st_cp_pin, GPIO.LOW)
        GPIO.output(self.__sh_cp_pin, GPIO.LOW)


    '''Cleans up everthing by setting the used pins to low.
    '''
    def cleanup(self):
        GPIO.output(self.__sd_pin, GPIO.LOW)
        GPIO.output(self.__st_cp_pin, GPIO.LOW)
        GPIO.output(self.__sh_cp_pin, GPIO.LOW)
        print("Shift register cleaned up.")


    '''Write data to the shift register of the 595 chip.

    :param data: 8 bit of data to be written to the chip.
    '''
    def serial_write(self, data):
        for bit in range(0, 8):
            GPIO.output(self.__sd_pin, 0x80 & (data << bit))
            GPIO.output(self.__sh_cp_pin, GPIO.HIGH)
            time.sleep(0.001)
            GPIO.output(self.__sh_cp_pin, GPIO.LOW)


    '''Outputs the stored byte in parallel.
    '''
    def output(self):
        GPIO.output(self.__st_cp_pin, GPIO.HIGH)
        time.sleep(0.001)
        GPIO.output(self.__st_cp_pin, GPIO.LOW)
