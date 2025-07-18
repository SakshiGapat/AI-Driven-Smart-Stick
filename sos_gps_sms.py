import os
import time
from twilio.rest import Client
import RPi.GPIO as GPIO

ACCOUNT_SID = "your_twilio_account_sid"
AUTH_TOKEN = "your_twilio_auth_token"
TWILIO_PHONE_NUMBER = "+12209022334"
TO_PHONE_NUMBER = "+91xxxxxxxxxx"

client = Client(ACCOUNT_SID, AUTH_TOKEN)
SOS_BUTTON = 4

GPIO.setwarnings(False)
GPIO.setmode(GPIO.BCM)
GPIO.setup(SOS_BUTTON, GPIO.IN, pull_up_down=GPIO.PUD_UP)

def get_gps_location():
    return "28.7041,77.1025"

def send_sms():
    location = get_gps_location()
    google_maps_link = f"https://www.google.com/maps?q={location}"
    message_body = f"🚨 Emergency Alert! GPS Location: {google_maps_link}"
    try:
        message = client.messages.create(
            body=message_body,
            from_=TWILIO_PHONE_NUMBER,
            to=TO_PHONE_NUMBER
        )
        print(f"✅ SMS Sent! Message SID: {message.sid}")
    except Exception as e:
        print(f"❌ Twilio Error: {e}")

try:
    while True:
        if GPIO.input(SOS_BUTTON) == GPIO.LOW:
            print("🆘 SOS Button Pressed! Sending alert...")
            send_sms()
            time.sleep(5)
        else:
            print("✅ Waiting for SOS button press...")
        time.sleep(1)
except KeyboardInterrupt:
    GPIO.cleanup()