#! /usr/bin/env python
# Blinks an LED when the user's GMail account has mail.
# Adapted from Adafruit's tutorial, found here:
# http://learn.adafruit.com/raspberry-pi-e-mail-notifier-using-leds/python-script


import RPi.GPIO as GPIO
from time import sleep as sleep
import imaplib

# Enter email settings here
username = ""
password = ""
server = ""
port = 1234

# Script config
check_frequency = 60
blink_frequency = 2
gpio_pin = 18


# Main
def check_unread_emails(server, server_port, username, password):
    server = imaplib.IMAP4_SSL(server, server_port)
    server.login(username, password)
    server.select()

    emails = server.search(None, 'UnSeen')[1][0].split()
    emails = filter(lambda email: email != "", emails)

    return len(emails)



# Prepare everything
GPIO.setmode(GPIO.BCM)
GPIO.setup(gpio_pin, GPIO.OUT)

while (True):
    try:
        if int(check_unread_emails(server, port, username, password)) > 0:
            led_on = True
            for i in range(check_frequency / blink_frequency):
                GPIO.output(gpio_pin, led_on)
                led_on = not led_on
                sleep(1.0 / blink_frequency)
        else:
            GPIO.output(gpio_pin, False)
            sleep(check_frequency)

    except (KeyboardInterrupt, SystemExit):
        # Clean up - set output to false and release pin
        try:
            GPIO.output(gpio_pin, False)
        except RuntimeError:
            pass
        GPIO.cleanup()
        break
