#!/usr/bin/python

from __future__ import print_function
import pickle
import os.path
from googleapiclient.discovery import build
from google_auth_oauthlib.flow import InstalledAppFlow
from google.auth.transport.requests import Request
import RPi.GPIO as GPIO, time

# If modifying these scopes, delete the file token.pickle.
SCOPES = ['https://www.googleapis.com/auth/gmail.readonly']
def GPIOdriver(numMessages):
	servoPin = 17
	GPIO.setwarnings(False)
	GPIO.setmode(GPIO.BCM) # tell the Pi what headers to use
	GPIO.setup(14, GPIO.OUT) # set up LED output
	GPIO.setup(servoPin, GPIO.OUT) # set up servo output
	servo = GPIO.PWM(servoPin, 50) # servoPin has PWM 50Hz
	if (numMessages == 0):
		servo.start(2)
		time.sleep(0.5)
		GPIO.output(14, False)
	elif (numMessages > 0):
		servo.start(12)
		time.sleep(0.5)
		GPIO.output(14, True)
	servo.stop()

def main():
    """Shows basic usage of the Gmail API.
    Lists the user's Gmail labels.
    """
    creds = None

    # The file token.pickle stores the user's access and refresh tokens, and is
    # created automatically when the authorization flow completes for the first
    # time.
    if os.path.exists('/home/pi/projects/gmail_python/token.pickle'):
        with open('/home/pi/projects/gmail_python/token.pickle', 'rb') as token:
            creds = pickle.load(token)
    # If there are no (valid) credentials available, let the user log in.
    if not creds or not creds.valid:
        if creds and creds.expired and creds.refresh_token:
            creds.refresh(Request())
        else:
            flow = InstalledAppFlow.from_client_secrets_file(
                '/home/pi/projects/gmail_python/credentials.json', SCOPES)
            creds = flow.run_local_server(port=0)
        # Save the credentials for the next run
        with open('/home/pi/projects/gmail_python/token.pickle', 'wb') as token:
            pickle.dump(creds, token)

    service = build('gmail', 'v1', credentials=creds)

    # Call the Gmail API
    results = service.users().messages().list(userId='me', labelIds='UNREAD').execute()
    numMessages = results.get('resultSizeEstimate')

    GPIOdriver(numMessages)

if __name__ == '__main__':
    main()
