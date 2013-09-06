#! /usr/bin/env python
# Blinks an LED when the user's GMail account has mail.
# Adapted from Adafruit's tutorial, found here:
# http://learn.adafruit.com/raspberry-pi-e-mail-notifier-using-leds/python-script


import RPi.GPIO as GPIO
from time import sleep as sleep
import feedparser


# Set up your account here
username = ""
password = ""

# Configure the application's settings here
check_frequency = 60
blink_frequency = 2
gpio_pin = 18


# Prepare everything
GPIO.setmode(GPIO.BCM)
GPIO.setup(gpio_pin, GPIO.OUT)
url = "https://" + username + ":" + password + "@mail.google.com/mail/feed/atom"

while (True):
    try:
        if int(feedparser.parse(url)["feed"]["fullcount"]) > 0:
            led_on = True
            for i in range(check_frequency / blink_frequency):
                GPIO.output(gpio_pin, led_on)
                led_on = not led_on
                sleep(1.0 / blink_frequency)
        else:
            GPIO.output(gpio_pin, False)

    except KeyboardInterrupt:
        # Clean up - set output to false and release pin
        try:
            GPIO.output(gpio_pin, False)
        except RuntimeError:
            pass

        GPIO.cleanup()
        break
