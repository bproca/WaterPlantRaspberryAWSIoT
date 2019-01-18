#!/usr/bin/env python

import RPi.GPIO as GPIO
import time
#import publisher
import Adafruit_ADS1x15

RelayPin = 11
MAX_VALUE_ADC = 32768

adc = Adafruit_ADS1x15.ADS1115()

def setup():
    GPIO.setmode(GPIO.BOARD)
    GPIO.setup(RelayPin, GPIO.OUT)
    GPIO.output(RelayPin, GPIO.HIGH)
    setup_adc()

def setup_adc():
    # Create an ADS1115 ADC (16-bit) instance
    adc.start_adc_comparator(0,  # Channel number
                             20000, 5000,  # High threshold value, low threshold value
                             active_low=True, traditional=True, latching=False,
                             num_readings=1, gain=1)

def destroy():
    GPIO.cleanup()
    GPIO.output(RelayPin, GPIO.HIGH)
    adc.stop_adc()

def loop():
    while True:
        time.sleep(2)
        value = read_adc_value()
        moisture = value * 100 / MAX_VALUE_ADC
        print 'analog value: %03d  moisture: %d' %(value, moisture)

def read_adc_value():
    return MAX_VALUE_ADC - adc.get_last_result()

if __name__ == '__main__':
    try:
        publisher.setup()
        setup()
        loop()
    except KeyboardInterrupt:
        destroy()


