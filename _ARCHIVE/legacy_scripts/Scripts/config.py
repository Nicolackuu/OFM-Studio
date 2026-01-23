import os

GOOGLE_API_KEY = "AIzaSyBNvA1PZp-3ZYRo5Nyewo6gQWFAnMXfzi0"
MODEL_IMAGE = "gemini-3-pro-image-preview"

CONFIG_PARAMS = {
    "temperature": 0.85,
    "top_p": 0.9,
    "aspect_ratio": "3:2",
    "image_size": "2K"
}

BASE_DIR = r"C:\Users\nicol\Desktop\OFM IA"
OUTPUT_DIR = os.path.join(BASE_DIR, "IMAGES", "GENERATED")

if not os.path.exists(OUTPUT_DIR):
    try:
        os.makedirs(OUTPUT_DIR)
    except:
        pass

CYAN = '\033[96m'
GREEN = '\033[92m'
YELLOW = '\033[93m'
RED = '\033[91m'
RESET = '\033[0m'
