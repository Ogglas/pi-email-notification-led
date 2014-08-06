#! /usr/bin/env python
# Blinks an LED when the user's GMail account has mail.
# Adapted from Adafruit's tutorial, found here:
# http://learn.adafruit.com/raspberry-pi-e-mail-notifier-using-leds/python-script


from time import sleep as sleep
import imaplib
import re
import RPi.GPIO as GPIO
from socket import gaierror as gaierror
import configparser
import logging
import argparse

#Set up argument parsing
parser = argparse.ArgumentParser(description="Runs a process which checks for mail through the IMAP protocol (using SSL)")
parser.add_argument("--loglevel", "-l", help="Specify logging level. [CRITICAL ERROR WARNING INFO DEBUG NOTSET]", default="INFO")
parser.add_argument("--config-path", "-c", help="Location of configuration file", default="email_settings.cfg")
 
args = parser.parse_args()
loglevelarg = args.loglevel.upper()
cfg_file_path = args.config_path
 
if (loglevelarg == "CRITICAL"):
    loglevel = 50
elif (loglevelarg == "ERROR"):
    loglevel = 40
elif (loglevelarg == "WARNING"):
    loglevel = 30
elif (loglevelarg == "INFO"):
    loglevel = 20
elif (loglevelarg == "DEBUG"):
    loglevel = 10
elif (loglevelarg == "NOTSET"):
    loglevel = 0
else:
    loglevel = 20

#Set up logging
logging.basicConfig(format='[%(asctime)s] %(levelname)s: %(message)s', level=loglevel,
                    datefmt='%Y-%m-%d %H:%M:%S')
 
logging.info("Logging started")

#Set up configparser
cfg = configparser.ConfigParser()
logging.info("Reading configuration file from path: %s", cfg_file_path)
cfg.read(cfg_file_path)
try:
    login_cfg = cfg["login"]
except:
    logging.error("Configuration file: %s not found", cfg_file_path)
    exit(1)

username = login_cfg["username"]
password = login_cfg["password"]
server = login_cfg["server"]
server_port = int(login_cfg["server_port"])

# Script config
check_frequency = 5
lamp_time_on = 30
gpio_pin = 17
GPIO.setmode(GPIO.BCM)
GPIO.setup(gpio_pin, GPIO.OUT)

# Main
def check_number_of_emails(server, server_port, username, password):
    logging.debug("Logging in to server: %s port: %s with username: %s", server, server_port, username)
    try:
        server = imaplib.IMAP4_SSL(server, server_port)
    except gaierror:
        logging.error("Couldn't connect to server %s with port %s",server, server_port)
        exit(1)
    try:
        server.login(username, password)
    except:
        #logging.error(sys.exc_info()[1])
        logging.error("Couldn't login to server %s with username %s",server, username)
        exit(1)
    logging.info("Connected to server, checking for emails")
    server.select()
    email_list = server.select("Inbox")[1][0].split()
    email = re.sub("[^0-9]", "", str(email_list[0]))
    return email

# Parameters to check if there are more emails in inbox then before
inbox_counter = int(check_number_of_emails(server, server_port, username, password))
old_inbox_counter = inbox_counter

while (True):
    try:
        if  (inbox_counter != old_inbox_counter):
            logging.debug("New email!")
            logging.debug("inbox_counter = " + str(inbox_counter))
            logging.debug("old_inbox_counter = " + str(old_inbox_counter))
            GPIO.output(gpio_pin, False)
            sleep(lamp_time_on * (inbox_counter - old_inbox_counter))
            old_inbox_counter = inbox_counter
        else:
            sleep(check_frequency)
            inbox_counter = int(check_number_of_emails(server, server_port, username, password))
            logging.debug("No new email!")
            logging.debug("inbox_counter = " + str(inbox_counter))
            logging.debug("old_inbox_counter = " + str(old_inbox_counter))
            GPIO.output(gpio_pin, True)
    except (KeyboardInterrupt, SystemExit):
        # Clean up
        try:
            print("End")
        except RuntimeError:
            pass
        print("Good bye!")
        break
