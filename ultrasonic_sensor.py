import RPi.GPIO as GPIO
import time
import pyttsx3
import threading

TRIG = 23
ECHO = 24

GPIO.setmode(GPIO.BCM)
GPIO.setup(TRIG, GPIO.OUT)
GPIO.setup(ECHO, GPIO.IN)

engine = pyttsx3.init()
engine.setProperty('rate', 175)
engine.setProperty('volume', 3.0)
last_spoken_distance = None

def speak(text):
    threading.Thread(target=lambda: (engine.say(text), engine.runAndWait()), daemon=True).start()

def get_distance():
    GPIO.output(TRIG, True)
    time.sleep(0.00001)
    GPIO.output(TRIG, False)
    start_time, stop_time = time.time(), time.time()
    timeout = time.time() + 0.1
    while GPIO.input(ECHO) == 0:
        start_time = time.time()
        if time.time() > timeout:
            return None
    while GPIO.input(ECHO) == 1:
        stop_time = time.time()
        if time.time() > timeout:
            return None
    elapsed_time = stop_time - start_time
    distance = (elapsed_time * 34300) / 2
    return round(distance, 1)

try:
    speak("Ultrasonic sensor activated.")
    while True:
        distance = get_distance()
        if distance and 2 < distance < 400:
            print(f"📏 Distance: {distance} cm")
            if last_spoken_distance is None or abs(distance - last_spoken_distance) > 5:
                last_spoken_distance = distance
                if distance < 30:
                    speak(f"Warning! Object detected at {distance} centimeters.")
                else:
                    speak(f"Distance is {distance} centimeters.")
        time.sleep(0.5)
except KeyboardInterrupt:
    GPIO.cleanup()
    speak("Measurement stopped. Goodbye.")