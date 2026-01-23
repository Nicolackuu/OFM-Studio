import os
import sys
import subprocess
from datetime import datetime

try:
    from google import genai
    from google.genai import types
except ImportError:
    os.system("python -m pip install google-genai")
    from google import genai
    from google.genai import types

from config import GOOGLE_API_KEY, MODEL_IMAGE, CONFIG_PARAMS, OUTPUT_DIR, CYAN, GREEN, RED, RESET
from data_bank import CHAR_DNA

client = None

def init_client():
    global client
    try:
        client = genai.Client(api_key=GOOGLE_API_KEY)
    except:
        print(f"{RED}Erreur Clé API{RESET}")

def get_image_bytes(file_path):
    clean_path = file_path.strip('"')
    if not os.path.exists(clean_path):
        clean_path = os.path.join(OUTPUT_DIR, os.path.basename(clean_path))
    if os.path.exists(clean_path):
        with open(clean_path, "rb") as f:
            return f.read()
    return None

def save_binary_file(file_path, data):
    with open(file_path, "wb") as f:
        f.write(data)
    print(f"{GREEN}[SUCCES] Image sauvegardée.{RESET}")

def open_image_auto(path):
    try:
        if os.name == 'nt':
            os.startfile(path)
        elif sys.platform == 'darwin':
            subprocess.call(('open', path))
        else:
            subprocess.call(('xdg-open', path))
    except:
        pass

def generate_image(prompt, reference_image_path=None, phase_choice="1"):
    if not client:
        print(f"{RED}Client non initialisé{RESET}")
        return None
    
    base_contents = [prompt]
    
    if reference_image_path:
        img_bytes = get_image_bytes(reference_image_path)
        if img_bytes:
            base_contents.append(types.Part.from_bytes(data=img_bytes, mime_type="image/png"))
        else:
            print(f"{RED}Impossible de charger l'image de référence{RESET}")
            return None
    
    print(f"\n{CYAN}[ACTION] Création en cours (Résolution: {CONFIG_PARAMS['image_size']})...{RESET}")
    
    try:
        response = client.models.generate_content(
            model=MODEL_IMAGE,
            contents=base_contents,
            config=types.GenerateContentConfig(
                temperature=CONFIG_PARAMS['temperature'],
                top_p=CONFIG_PARAMS['top_p'],
                response_modalities=["IMAGE"],
                image_config=types.ImageConfig(
                    image_size=CONFIG_PARAMS['image_size'],
                    aspect_ratio=CONFIG_PARAMS['aspect_ratio']
                )
            )
        )

        if response.candidates and response.candidates[0].content.parts[0].inline_data:
            part = response.candidates[0].content.parts[0]
            timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
            nat_name = CHAR_DNA['DISPLAY']['Nationalité'].split()[0] if CHAR_DNA else "Model"
            filename = f"Phase{phase_choice}_{nat_name}_{CONFIG_PARAMS['image_size']}_{timestamp}.png"
            file_path = os.path.join(OUTPUT_DIR, filename)
            save_binary_file(file_path, part.inline_data.data)
            open_image_auto(file_path)
            return file_path
        else:
            print(f"{RED}Erreur Gen.{RESET}")
            return None

    except Exception as e:
        print(f"{RED}[CRASH] {e}{RESET}")
        return None
