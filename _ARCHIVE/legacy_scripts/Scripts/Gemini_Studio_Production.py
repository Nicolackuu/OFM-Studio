import os
import sys
import time
import subprocess
import random
from datetime import datetime

# ==============================================================================
# 1. CONFIGURATION
# ==============================================================================

GOOGLE_API_KEY = "AIzaSyBNvA1PZp-3ZYRo5Nyewo6gQWFAnMXfzi0"
MODEL_IMAGE = "gemini-3-pro-image-preview"

# Paramètres Studio (AJUSTÉS POUR QUALITÉ MAXIMALE)
# On passe en 3:2 par défaut : C'est plus haut que le 16:9, donc les visages seront plus grands.
CONFIG_PARAMS = {
    "temperature": 0.85,
    "top_p": 0.9,
    "aspect_ratio": "3:2", # <-- LE SECRET : Format Reflex Pro (Plus de pixels en hauteur)
    "image_size": "1K"     # L'API limite souvent ici, mais le ratio 3:2 densifie l'image
}

# Chemins Absolus
BASE_DIR = r"C:\Users\nicol\Desktop\OFM IA"
OUTPUT_DIR = os.path.join(BASE_DIR, "IMAGES", "GENERATED")

if not os.path.exists(OUTPUT_DIR):
    try: os.makedirs(OUTPUT_DIR)
    except: pass

# ==============================================================================
# 2. BANQUE DE DONNÉES "NATURAL BOMBSHELL"
# ==============================================================================

BANK_NATIONALITY = [
    {"fr": "Française (Naturelle)", "en": "French Parisian student, naturally stunning, effortless beauty, minimal makeup aesthetic"},
    {"fr": "Brésilienne (Solaire)", "en": "Brazilian model, golden tan skin, warm undertones, radiant healthy glow, exotic beauty"},
    {"fr": "Russe (Froide)", "en": "Russian elegant beauty, pale porcelain skin, high cheekbones, striking and intense look"},
    {"fr": "Japonaise (Moderne)", "en": "Japanese Tokyo fashionista, flawless skin texture, almond eyes, trendy and cute"},
    {"fr": "Italienne (Intense)", "en": "Italian brunette, olive skin tone, passionate gaze, thick eyebrows, mediterranean charm"},
    {"fr": "Scandinave (Ange)", "en": "Swedish angelic beauty, sun-bleached hair, light skin with pink undertones, ethereal"},
    {"fr": "Américaine (Girl Next Door)", "en": "American girl next door, athletic, healthy flush, bright smile, accessible beauty"},
    {"fr": "Espagnole (Voluptueuse)", "en": "Spanish beauty, sun-kissed skin, expressive features, dark intense eyes"},
    {"fr": "Métisse (Caramel)", "en": "Mixed race goddess, glowing caramel skin, unique striking features, perfect symmetry"}
]

BANK_BODY = [
    {"fr": "Sablier (Courbes Fines)", "en": "Slim hourglass figure, tiny waist, wide hips, soft feminine curves, fit but not muscular"},
    {"fr": "Athlétique (Tonique)", "en": "Toned athletic physique, defined collarbones, flat stomach, healthy fit look"},
    {"fr": "Mannequin (Élancée)", "en": "Tall and slender model physique, long legs, elegant posture, delicate frame"},
    {"fr": "Curvy (Voluptueuse)", "en": "Voluptuous curvy figure, thick thighs, soft tummy, very feminine and attractive"}
]

BANK_FACE_SHAPE = [
    {"fr": "Ovale (Mâchoire définie)", "en": "Symmetrical oval face with a sharp, defined jawline and elegant chin"},
    {"fr": "Cœur (Pommettes hautes)", "en": "Heart-shaped face, high prominent cheekbones, narrowing to a delicate chin"},
    {"fr": "Diamant (Sculpté)", "en": "Diamond face shape, sculpted hollow cheeks, angular features, very photogenic"},
    {"fr": "Rond (Douceur)", "en": "Soft round face shape, full cheeks, youthful and fresh appearance"},
    {"fr": "Carré (Caractère)", "en": "Square face shape with a strong jawline, intense and striking look"}
]

BANK_EYES = [
    {"fr": "Bleu Glace (Limbe Foncé)", "en": "Piercing ice-blue eyes with a dark limbal ring, sharp almond shape, heavy lashes"},
    {"fr": "Vert Émeraude (Chat)", "en": "Vivid emerald green eyes, upturned cat-eye shape, seductive and intense"},
    {"fr": "Noisette Miel (Soleil)", "en": "Warm hazel eyes with golden honey flecks, large round shape, expressive"},
    {"fr": "Brun Noir (Profond)", "en": "Deep dark chocolate eyes, mysterious, soulful, slightly hooded eyelids"},
    {"fr": "Gris Orage (Rare)", "en": "Rare storm-grey eyes, changing with light, melancholic and beautiful"},
    {"fr": "Hétérochromie (Vairons)", "en": "Heterochromia (left eye blue, right eye hazel), extremely unique and hypnotic"}
]

BANK_HAIR = [
    {"fr": "Blond Miel (Wavy)", "en": "Honey blonde hair, long layers, loose natural beach waves, slightly messy texture"},
    {"fr": "Brun Chocolat (Lisse)", "en": "Rich dark chocolate brown hair, waist length, silky straight with a middle part"},
    {"fr": "Roux Cuivré (Naturel)", "en": "Natural copper red hair, voluminous, soft curls catching the light"},
    {"fr": "Noir Jais (Carré)", "en": "Jet black hair, sharp bob cut (chin length), glossy and sleek texture"},
    {"fr": "Châtain Cendré (Balayage)", "en": "Ash brown hair with subtle blonde highlights (balayage), messy bun style with loose strands"},
    {"fr": "Blond Platine (Long)", "en": "Platinum blonde hair, extremely long, straight with curtain bangs framing the face"}
]

BANK_NOSE_LIPS = [
    {"fr": "Nez Fin / Lèvres Pulpeuses", "en": "Small straight button nose and naturally full, plush lips (cupid's bow defined)"},
    {"fr": "Nez Grec / Lèvres Douces", "en": "Elegant straight Grecian nose and soft, balanced rosebud lips"},
    {"fr": "Nez Mignon / Lèvres Larges", "en": "Slightly upturned cute nose and wide smile, prominent lower lip"},
    {"fr": "Nez Aquilin / Bouche Boudeuse", "en": "Slightly aquiline aristocratic nose and pouty, voluminous lips"},
    {"fr": "Nez Naturel / Lèvres Fines", "en": "Natural nose with a slight bump (character) and defined, elegant lips"}
]

BANK_IMPERFECTIONS = [
    {"fr": "Taches de rousseur (Nez)", "en": "A dusting of natural freckles across the bridge of the nose and cheeks (sun-kissed look)"},
    {"fr": "Grain de beauté (Joue Gauche)", "en": "A single, distinct beauty mark on the upper left cheek, adding character"},
    {"fr": "Petite cicatrice (Sourcil Droit)", "en": "A small, faint vertical scar cutting through the right eyebrow (cool gap)"},
    {"fr": "Fossettes (Sourire)", "en": "Deep natural dimples visible on cheeks, adding extreme charm"},
    {"fr": "Grain de beauté (Lèvre)", "en": "A small attractive mole just above the upper lip on the right side (Monroe style)"},
    {"fr": "Dents du bonheur (Léger)", "en": "A very slight, cute gap between the two front teeth (diastema), natural smile"},
    {"fr": "Texture de peau (Réaliste)", "en": "Visible natural skin texture, slight pores on cheeks, not airbrushed, hyper-realistic"}
]

CHAR_DNA = {}

# ==============================================================================
# 3. MOTEUR
# ==============================================================================

try:
    from google import genai
    from google.genai import types
except ImportError:
    os.system("python -m pip install google-genai")
    from google import genai
    from google.genai import types

CYAN, GREEN, YELLOW, RED, RESET = '\033[96m', '\033[92m', '\033[93m', '\033[91m', '\033[0m'
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
        with open(clean_path, "rb") as f: return f.read()
    return None

def save_binary_file(file_path, data):
    with open(file_path, "wb") as f: f.write(data)
    print(f"{GREEN}[SUCCES] Image sauvegardée.{RESET}")

def open_image_auto(path):
    try:
        if os.name == 'nt': os.startfile(path)
        elif sys.platform == 'darwin': subprocess.call(('open', path))
        else: subprocess.call(('xdg-open', path))
    except: pass

def random_casting():
    global CHAR_DNA
    print(f"\n{CYAN}=== 🎰 SLOT MACHINE (MODE NATURAL BOMBSHELL) ==={RESET}")
    
    nat = random.choice(BANK_NATIONALITY)
    body = random.choice(BANK_BODY)
    face = random.choice(BANK_FACE_SHAPE)
    eyes = random.choice(BANK_EYES)
    hair = random.choice(BANK_HAIR)
    nose_lips = random.choice(BANK_NOSE_LIPS)
    imp = random.choice(BANK_IMPERFECTIONS)
    age = str(random.randint(20, 25))

    CHAR_DNA = {
        "AGE": age,
        "EN_FULL": {
            "NATIONALITY": nat['en'],
            "BODY": body['en'],
            "FACE": face['en'],
            "EYES": eyes['en'],
            "HAIR": hair['en'],
            "NOSE_LIPS": nose_lips['en'],
            "IMP": imp['en']
        },
        "DISPLAY": {
            "Nationalité": nat['fr'],
            "Corps": body['fr'],
            "Visage": face['fr'],
            "Yeux": eyes['fr'],
            "Cheveux": hair['fr'],
            "Nez/Levres": nose_lips['fr'],
            "Charme": imp['fr']
        }
    }

    print(f"{YELLOW}✨ NOUVEAU PROFIL GÉNÉRÉ :{RESET}")
    print(f"   🔥 {CHAR_DNA['DISPLAY']['Nationalité']} ({age} ans)")
    print(f"   🍑 {CHAR_DNA['DISPLAY']['Corps']}")
    print(f"   👱‍♀️ {CHAR_DNA['DISPLAY']['Visage']} | {CHAR_DNA['DISPLAY']['Cheveux']}")
    print(f"   👀 {CHAR_DNA['DISPLAY']['Yeux']} | {CHAR_DNA['DISPLAY']['Nez/Levres']}")
    print(f"   💎 {CHAR_DNA['DISPLAY']['Charme']} (Détail qui tue)")
    print(f"{GREEN}--> Profil verrouillé.{RESET}")

def change_aspect_ratio():
    print(f"\n{YELLOW}--- CHOIX DU FORMAT (RATIO) ---{RESET}")
    print("1. 16:9 (Cinéma) - Idéal pour les bandes larges (Défaut Studio)")
    print("2. 3:2  (Photo Pro) - LE MEILLEUR pour les visages (Plus haut)")
    print("3. 1:1  (Carré) - Attention, ça va écraser les 5 têtes")
    print("4. 3:4  (Portrait) - Très haute qualité, mais les 5 têtes seront serrées")
    
    c = input("> Choix : ")
    if c == "1": CONFIG_PARAMS['aspect_ratio'] = "16:9"
    elif c == "2": CONFIG_PARAMS['aspect_ratio'] = "3:2"
    elif c == "3": CONFIG_PARAMS['aspect_ratio'] = "1:1"
    elif c == "4": CONFIG_PARAMS['aspect_ratio'] = "3:4"
    print(f"{GREEN}Ratio réglé sur : {CONFIG_PARAMS['aspect_ratio']}{RESET}")

def get_prompt_text(phase_num):
    if not CHAR_DNA: random_casting()
    dna = CHAR_DNA['EN_FULL']
    age = CHAR_DNA['AGE']

    if phase_num == "1":
        return f"""
### PROFESSIONAL PORTRAIT STUDY: PHASE 1 (FOUNDATION) ###
OBJECTIVE: Create a high-resolution photographic triptych to establish the primary facial structure.
Focus on maximum detail clarity but maintaining extreme attractiveness.
Layout: 3 large frames side-by-side.
Subject: Fictional female model, {age} years old. {dna['NATIONALITY']}.

FRAME 1 (LEFT): Strict 90-degree left profile.
FRAME 2 (CENTER): Dead-center frontal headshot. Neutral expression, symmetrical.
FRAME 3 (RIGHT): Three-quarter view (45 degrees right).

PHOTOREALISM & TEXTURE PROTOCOL:
- Aesthetic: High-end editorial photography, raw but flattering lighting.
- DETAILS: Ultra-sharp focus on iris patterns, natural skin texture with visible pores.
- RESTRICTIONS: NO plastic smoothing, NO AI-blur. Skin must look human.

MODEL SPECIFICS:
- FACE SHAPE: {dna['FACE']}
- EYES: {dna['EYES']}
- HAIR: {dna['HAIR']}
- NOSE & LIPS: {dna['NOSE_LIPS']}
- DISTINCTIVE FEATURES: {dna['IMP']}
- BODY TYPE: {dna['BODY']}
"""
    elif phase_num == "2":
        return f"""
### PROFESSIONAL PORTRAIT STUDY: PHASE 2 (STRUCTURE) ###
REFERENCE MANDATE: Maintain absolute 100% facial identity consistency with the attached image.
Feature to track strictly: {dna['IMP']}.
Layout: Horizontal strip of 5 frames.
FRAME 1: High Angle (Looking down).
FRAME 2: Low Angle (Looking up).
FRAME 3: Frontal recall.
FRAME 4: Right Profile.
FRAME 5: Hairline Focus.
PHOTOREALISM PROTOCOL: Raw but beautiful aesthetic.
"""
    elif phase_num == "3":
        return f"""
### PROFESSIONAL PORTRAIT STUDY: PHASE 3 (DYNAMICS) ###
REFERENCE MANDATE: Maintain absolute 100% facial identity consistency.
Feature to track strictly: {dna['IMP']}.
Layout: Horizontal strip of 5 frames (Emotions).
FRAME 1 (JOY): Wide, genuine smile.
FRAME 2 (INTENSITY): Fierce, focused "baddie" stare.
FRAME 3 (SERENE): Eyes closed gently.
FRAME 4 (SKEPTICAL): One eyebrow raised.
FRAME 5 (SURPRISE): Mouth slightly open, gasp.
"""
    return ""

def main():
    init_client()
    os.system('cls' if os.name == 'nt' else 'clear')
    print(f"{CYAN}=== GEMINI STUDIO V15 (UNRESTRICTED) ==={RESET}")
    print(f"Ratio Actuel : {CONFIG_PARAMS['aspect_ratio']}")

    while True:
        print(f"\n{YELLOW}--- MENU ---")
        print(f"{CYAN}[0] 🎰 SLOT MACHINE (Nouveau Modèle){RESET}")
        print(f"{CYAN}[R] 📐 CHANGER LE RATIO (Actuel: {CONFIG_PARAMS['aspect_ratio']}){RESET}")
        print("1. PHASE 1 : Foundation")
        print("2. PHASE 2 : Structure")
        print("3. PHASE 3 : Dynamics")
        print(f"X. Quitter")
        
        choice = input(f"> Choix : ").strip().upper()
        if choice == "X": break
        
        if choice == "0":
            random_casting()
            continue
            
        if choice == "R":
            change_aspect_ratio()
            continue

        if choice not in ["1", "2", "3"]: continue
        
        if not CHAR_DNA: random_casting()

        prompt = get_prompt_text(choice)
        base_contents = [prompt]
        
        if choice in ["2", "3"]:
            print(f"\n{CYAN}Glisse l'image de référence ici :{RESET}")
            ref_path = input(f"> ").strip('"')
            img_bytes = get_image_bytes(ref_path)
            if img_bytes:
                base_contents.append(types.Part.from_bytes(data=img_bytes, mime_type="image/png"))
            else:
                continue

        while True:
            print(f"\n{CYAN}[ACTION] Création en cours...{RESET}")
            last_saved_path = None
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
                    nat_name = CHAR_DNA['DISPLAY']['Nationalité'].split()[0]
                    filename = f"Phase{choice}_{nat_name}_{timestamp}.png"
                    last_saved_path = os.path.join(OUTPUT_DIR, filename)
                    save_binary_file(last_saved_path, part.inline_data.data)
                    open_image_auto(last_saved_path)
                else:
                    print(f"{RED}Erreur Gen.{RESET}")

            except Exception as e:
                print(f"{RED}[CRASH] {e}{RESET}")

            if last_saved_path and os.path.exists(last_saved_path):
                action = input(f"{CYAN}[G]arder ou [R]efaire ? > {RESET}").upper()
                if action == "R":
                    try:
                        time.sleep(0.5)
                        os.remove(last_saved_path)
                        print(f"{RED}Supprimé. Relance...{RESET}")
                        continue
                    except: pass
                else:
                    print(f"{GREEN}Validé.{RESET}")
                    break 
            else:
                if input("Réessayer ? (O/N) > ").upper() != "O": break

if __name__ == "__main__":
    main()