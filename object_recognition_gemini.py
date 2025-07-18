import google.generativeai as genai
import requests
import numpy as np
import cv2
import pyttsx3
from PIL import Image

GEMINI_API_KEY = "your_gemini_api_key_here"
ESP32_CAM_URL = "http://192.168.16.225/800x600.jpg"

genai.configure(api_key=GEMINI_API_KEY)
engine = pyttsx3.init()
engine.setProperty("rate", 150)
engine.setProperty('volume', 3.0)

def capture_image():
    try:
        response = requests.get(ESP32_CAM_URL, timeout=5)
        if response.status_code == 200:
            image_array = np.asarray(bytearray(response.content), dtype=np.uint8)
            image = cv2.imdecode(image_array, cv2.IMREAD_COLOR)
            if image is None or image.size == 0:
                return None
            cv2.imwrite("captured.jpg", image)
            print("✅ Image saved as 'captured.jpg'")
            return "captured.jpg"
        else:
            return None
    except Exception as e:
        print(f"❌ Exception: {e}")
        return None

def recognize_objects(image_path):
    try:
        image = Image.open(image_path)
        model = genai.GenerativeModel("gemini-1.5-flash")
        prompt = "List only the names of objects in this image, separated by commas."
        response = model.generate_content([prompt, image])
        return response.text.strip() if hasattr(response, "text") else "❌ No objects detected."
    except Exception as e:
        return f"❌ Error: {e}"

def speak(text):
    engine.say(text)
    engine.runAndWait()

image_path = capture_image()
if image_path:
    result = recognize_objects(image_path)
    print("📢 Detected Objects:", result)
    speak(result)