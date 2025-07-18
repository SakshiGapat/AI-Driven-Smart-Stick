import RPi.GPIO as GPIO
import time
import pyttsx3

PIR_SENSOR = 22
engine = pyttsx3.init()
engine.setProperty('rate', 150)
engine.setProperty('volume', 3.0)

GPIO.setwarnings(False)
GPIO.setmode(GPIO.BCM)
GPIO.setup(PIR_SENSOR, GPIO.IN)

def speak(message):
    engine.say(message)
    engine.runAndWait()

try:
    speak("Motion detection activated.")
    while True:
        if GPIO.input(PIR_SENSOR):
            print("👀 Motion Detected!")
            speak("Warning! Something approaching you.")
            time.sleep(2)
except KeyboardInterrupt:
    speak("Motion detection stopped.")
    GPIO.cleanup()