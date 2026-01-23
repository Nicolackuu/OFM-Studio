#!/usr/bin/env python3
import os
import time
from pathlib import Path
from datetime import datetime

from core.config import Config
from core.utils import (
    print_banner, print_info, print_success, print_error,
    get_user_choice, confirm_action, Colors
)
from core.gemini_engine import GeminiEngine

try:
    from google import genai
    from google.genai import types
except ImportError:
    os.system("python -m pip install google-genai")
    from google import genai
    from google.genai import types

class FaceSwapStudio:
    def __init__(self):
        self.engine = GeminiEngine()
        self.engine.update_config(aspect_ratio="16:9", image_size="2K")
        
        self.character_dna = {
            "AGE": "22",
            "FACE_SHAPE": "Oval with high cheekbones and a sharp defined jawline",
            "EYES": "Almond-shaped, icy blue, sharp gaze",
            "HAIR": "Platinum blonde, waist-length, loose beach waves, messy texture",
            "NOSE_LIPS": "Small straight nose, full plump lips, natural cupid's bow",
            "FEATURES": "Small beauty mark under the left eye, light freckles across the nose bridge"
        }
    
    def get_prompt(self, phase: str) -> str:
        if phase == "1":
            return f"""
### PROFESSIONAL PORTRAIT STUDY: PHASE 1 (FOUNDATION) ###
OBJECTIVE: High-resolution photographic triptych (3 frames horizontal).
Subject: Fictional female model, {self.character_dna['AGE']} years old.
FRAME 1: Left profile. FRAME 2: Frontal neutral. FRAME 3: 3/4 view.
AESTHETIC: Raw 35mm film, 85mm lens f/8.
DETAILS: {self.character_dna['FACE_SHAPE']}, {self.character_dna['EYES']}, {self.character_dna['HAIR']}, {self.character_dna['FEATURES']}.
NO FILTERS.
"""
        elif phase == "2":
            return f"""
### PROFESSIONAL PORTRAIT STUDY: PHASE 2 (STRUCTURE) ###
REFERENCE MANDATE: 100% identity consistency with reference.
Subject: {self.character_dna['AGE']}yo, {self.character_dna['HAIR']}.
LAYOUT: 5 frames horizontal strip.
ANGLES: High angle, Low angle, Frontal recall, Right Profile, Hairline/Crown.
AESTHETIC: Raw 35mm film.
"""
        elif phase == "3":
            return f"""
### PROFESSIONAL PORTRAIT STUDY: PHASE 3 (DYNAMICS) ###
REFERENCE MANDATE: 100% identity consistency with reference.
LAYOUT: 5 frames horizontal strip focusing on EMOTIONS.
EXPRESSIONS: Joy (Smile), Intensity (Fierce), Serene (Closed eyes), Skeptical (Smirk), Surprise (Gasp).
AESTHETIC: Raw 35mm film.
"""
        return ""
    
    def run_phase(self, phase: str):
        prompt = self.get_prompt(phase)
        reference_image_path = None
        
        if phase in ["2", "3"]:
            print(f"\n{Colors.CYAN}Drag and drop the reference image (from previous phase):{Colors.RESET}")
            reference_image_path = input(f"> ").strip('"')
            
            if not reference_image_path or not Path(reference_image_path).exists():
                print_error("Invalid reference image path")
                return
        
        while True:
            last_saved_path = self.engine.generate_image(
                prompt=prompt,
                reference_image_path=reference_image_path,
                phase=phase,
                character_name="FaceSwap"
            )
            
            if last_saved_path and last_saved_path.exists():
                print(f"\n{Colors.YELLOW}--- DECISION ---{Colors.RESET}")
                print(f"Image: {last_saved_path.name}")
                
                action = get_user_choice("[K]eep or [R]edo? > ", ["K", "R"])
                
                if action == "R":
                    try:
                        time.sleep(0.5)
                        last_saved_path.unlink()
                        print_error("Deleted. Regenerating...")
                        continue
                    except Exception as e:
                        print_error(f"Could not delete: {e}")
                else:
                    print_success("Image validated!")
                    break
            else:
                if not confirm_action("Retry?"):
                    break
    
    def run(self):
        print_banner("FACE SWAP STUDIO", "Consistent Character Generation")
        
        print(f"{Colors.YELLOW}Character DNA:{Colors.RESET}")
        print(f"  • Age: {self.character_dna['AGE']}")
        print(f"  • Face: {self.character_dna['FACE_SHAPE']}")
        print(f"  • Eyes: {self.character_dna['EYES']}")
        print(f"  • Hair: {self.character_dna['HAIR']}")
        print(f"  • Features: {self.character_dna['FEATURES']}\n")
        
        while True:
            print(f"{Colors.CYAN}{'─' * 60}")
            print(f"  PHASE MENU")
            print(f"{'─' * 60}{Colors.RESET}")
            print(f"{Colors.BOLD}[1]{Colors.RESET} Phase 1: Foundation (3 angles)")
            print(f"{Colors.BOLD}[2]{Colors.RESET} Phase 2: Structure (5 angles, needs reference)")
            print(f"{Colors.BOLD}[3]{Colors.RESET} Phase 3: Dynamics (5 emotions, needs reference)")
            print(f"{Colors.BOLD}[X]{Colors.RESET} Exit")
            
            choice = input(f"\n{Colors.YELLOW}> Choice: {Colors.RESET}").strip().upper()
            
            if choice == "X":
                print_success("Goodbye!")
                break
            elif choice in ["1", "2", "3"]:
                self.run_phase(choice)
            else:
                print_error("Invalid choice")

def main():
    try:
        studio = FaceSwapStudio()
        studio.run()
    except KeyboardInterrupt:
        print(f"\n{Colors.YELLOW}Interrupted by user{Colors.RESET}")
    except Exception as e:
        print_error(f"Fatal error: {e}")
        raise

if __name__ == "__main__":
    main()
