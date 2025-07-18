import RPi.GPIO as GPIO
import time
import pyttsx3

WATER_SENSOR = 25

GPIO.setwarnings(False)
GPIO.setmode(GPIO.BCM)
GPIO.setup(WATER_SENSOR, GPIO.IN)

engine = pyttsx3.init()
engine.setProperty('rate', 150)
engine.setProperty('volume', 3.0)

last_state = None

def speak(message):
    engine.say(message)
    engine.runAndWait()

try:
    while True:
        water_detected = GPIO.input(WATER_SENSOR)
        if water_detected == GPIO.HIGH and last_state != "WATER":
            print("💧 Water Detected!")
            speak("Warning! Water detected.")
            last_state = "WATER"
        elif water_detected == GPIO.LOW and last_state != "NO_WATER":
            print("✅ No water detected.")
            speak("It is safe to move.")
            last_state = "NO_WATER"
        time.sleep(2)
except KeyboardInterrupt:
    GPIO.cleanup()
    print("🚀 Program Terminated.")