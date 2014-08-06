#! /usr/bin/env python
# Adapted from Adafruit's tutorial, found here:
# http://learn.adafruit.com/raspberry-pi-e-mail-notifier-using-leds/python-script
# and charlienewey, found here:
# https://github.com/charlienewey/pi-email-notification-led
# Modified to check the inbox value against an old inbox value

from time import sleep as sleep
import imaplib
import re

# Enter email settings here
username = "test@test.se"
password = "test"
server = "test.se"
server_port = 993

# Script config
check_frequency = 5


# Main

def check_number_of_emails(server, server_port, username, password):
    server = imaplib.IMAP4_SSL(server, server_port)
    server.login(username, password)
    server.select()
    email_list = server.select("Inbox")[1][0].split()
    email = re.sub("[^0-9]", "", str(email_list[0]))
    return email

# Parameter to check if there are more emails in inbox then before

inbox_counter = int(check_number_of_emails(server, server_port, username, password))
old_inbox_counter = inbox_counter

while (True):
    try:
        if  (inbox_counter != old_inbox_counter):
            print("New mail!") #Used for debugging
            print(inbox_counter) #Used for debugging
            print(old_inbox_counter) #Used for debugging
            old_inbox_counter = inbox_counter
        else:
            sleep(check_frequency)
            inbox_counter = int(check_number_of_emails(server, server_port, username, password))
            print("No new mail!") #Used for debugging
            print(inbox_counter) #Used for debugging
            print(old_inbox_counter) #Used for debugging
    except (KeyboardInterrupt, SystemExit):
        # Clean up
        try:
            print("End")
        except RuntimeError:
            pass
        print("Error")
        break
