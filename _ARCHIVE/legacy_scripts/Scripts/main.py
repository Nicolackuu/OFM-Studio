import os
import time
from config import CONFIG_PARAMS, CYAN, GREEN, YELLOW, RED, RESET
from data_bank import random_casting, get_prompt_text, CHAR_DNA
from core_engine import init_client, generate_image

def change_aspect_ratio():
    print(f"\n{YELLOW}--- CHOIX DU FORMAT (RATIO) ---{RESET}")
    print("1. 16:9 (Cinéma) - Idéal pour les bandes larges")
    print("2. 3:2  (Photo Pro) - LE MEILLEUR pour les visages (Plus haut)")
    print("3. 1:1  (Carré) - Format Instagram")
    print("4. 3:4  (Portrait) - Très haute qualité")
    
    c = input("> Choix : ")
    if c == "1":
        CONFIG_PARAMS['aspect_ratio'] = "16:9"
    elif c == "2":
        CONFIG_PARAMS['aspect_ratio'] = "3:2"
    elif c == "3":
        CONFIG_PARAMS['aspect_ratio'] = "1:1"
    elif c == "4":
        CONFIG_PARAMS['aspect_ratio'] = "3:4"
    print(f"{GREEN}Ratio réglé sur : {CONFIG_PARAMS['aspect_ratio']}{RESET}")

def change_resolution():
    print(f"\n{YELLOW}--- CHOIX DE LA RÉSOLUTION ---{RESET}")
    print("1. 1K (Standard) - Rapide")
    print("2. 2K (Haute Qualité) - Recommandé ⭐")
    print("3. 4K (Ultra HD) - Maximum de détails (Plus lent)")
    
    c = input("> Choix : ")
    if c == "1":
        CONFIG_PARAMS['image_size'] = "1K"
    elif c == "2":
        CONFIG_PARAMS['image_size'] = "2K"
    elif c == "3":
        CONFIG_PARAMS['image_size'] = "4K"
    print(f"{GREEN}Résolution réglée sur : {CONFIG_PARAMS['image_size']}{RESET}")

def main():
    init_client()
    os.system('cls' if os.name == 'nt' else 'clear')
    print(f"{CYAN}=== GEMINI STUDIO V16 (MODULAR + 2K/4K SUPPORT) ==={RESET}")
    print(f"Ratio Actuel : {CONFIG_PARAMS['aspect_ratio']}")
    print(f"Résolution : {CONFIG_PARAMS['image_size']}")

    while True:
        print(f"\n{YELLOW}--- MENU ---{RESET}")
        print(f"{CYAN}[0] 🎰 SLOT MACHINE (Nouveau Modèle){RESET}")
        print(f"{CYAN}[R] 📐 CHANGER LE RATIO (Actuel: {CONFIG_PARAMS['aspect_ratio']}){RESET}")
        print(f"{CYAN}[Q] 🎬 CHANGER LA RÉSOLUTION (Actuel: {CONFIG_PARAMS['image_size']}){RESET}")
        print("1. PHASE 1 : Foundation")
        print("2. PHASE 2 : Structure")
        print("3. PHASE 3 : Dynamics")
        print(f"X. Quitter")
        
        choice = input(f"> Choix : ").strip().upper()
        if choice == "X":
            break
        
        if choice == "0":
            random_casting()
            continue
            
        if choice == "R":
            change_aspect_ratio()
            continue
        
        if choice == "Q":
            change_resolution()
            continue

        if choice not in ["1", "2", "3"]:
            continue
        
        if not CHAR_DNA:
            random_casting()

        prompt = get_prompt_text(choice)
        reference_image_path = None
        
        if choice in ["2", "3"]:
            print(f"\n{CYAN}Glisse l'image de référence ici :{RESET}")
            reference_image_path = input(f"> ").strip('"')

        while True:
            last_saved_path = generate_image(prompt, reference_image_path, choice)
            
            if last_saved_path and os.path.exists(last_saved_path):
                action = input(f"{CYAN}[G]arder ou [R]efaire ? > {RESET}").upper()
                if action == "R":
                    try:
                        time.sleep(0.5)
                        os.remove(last_saved_path)
                        print(f"{RED}Supprimé. Relance...{RESET}")
                        continue
                    except:
                        pass
                else:
                    print(f"{GREEN}Validé.{RESET}")
                    break
            else:
                if input("Réessayer ? (O/N) > ").upper() != "O":
                    break

if __name__ == "__main__":
    main()
