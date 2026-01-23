#!/usr/bin/env python3
import os
import sys
from pathlib import Path
from typing import Optional

from core.config import Config
from core.utils import (
    print_banner, print_info, print_success, print_error, 
    print_warning, get_user_choice, confirm_action, Colors, clear_screen
)
from core.character_bank import Character
from core.gemini_engine import GeminiEngine, PromptBuilder
from core.dataset_scraper import DatasetScraper
from core.dataset_curator import DatasetCurator
from core.batch_face_swap import BatchFaceSwap

class DatasetFactory:
    def __init__(self):
        self.base_dir = Config.BASE_DIR / "DATASET"
        self.raw_dir = self.base_dir / "RAW"
        self.approved_dir = self.base_dir / "APPROVED"
        self.final_dir = self.base_dir / "FINAL_LORA"
        
        self._ensure_directories()
        
        self.source_face: Optional[Path] = None
        self.current_username: Optional[str] = None
        self.approved_images: list = []
    
    def _ensure_directories(self):
        self.base_dir.mkdir(parents=True, exist_ok=True)
        self.raw_dir.mkdir(parents=True, exist_ok=True)
        self.approved_dir.mkdir(parents=True, exist_ok=True)
        self.final_dir.mkdir(parents=True, exist_ok=True)
    
    def module_1_source_face(self):
        print_banner("MODULE 1: SOURCE FACE SELECTION", "Choose the face for your LoRa dataset")
        
        print(f"{Colors.CYAN}OPTIONS:{Colors.RESET}")
        print(f"[A] Generate NEW face (Phase 1 via Gemini Studio)")
        print(f"[B] Choose EXISTING image from IMAGES/GENERATED")
        print(f"[X] Cancel\n")
        
        choice = get_user_choice("Select option > ", ["A", "B", "X"])
        
        if choice == "X":
            return False
        
        elif choice == "A":
            print_info("\nLaunching Gemini Studio for Phase 1 generation...")
            print_warning("After generation, the image will be automatically selected as source face.\n")
            
            engine = GeminiEngine()
            character = Character()
            character.generate_random()
            character.display()
            
            if not confirm_action("Generate Phase 1 with this character?"):
                return False
            
            prompt = PromptBuilder.build_phase_1(character.dna)
            character_name = character.dna['DISPLAY']['Nationalité'].split()[0]
            
            result_path = engine.generate_image(
                prompt=prompt,
                reference_image_path=None,
                phase="1",
                character_name=character_name
            )
            
            if result_path and result_path.exists():
                self.source_face = result_path
                print_success(f"\n✓ Source face selected: {result_path.name}")
                return True
            else:
                print_error("Failed to generate source face")
                return False
        
        elif choice == "B":
            generated_dir = Config.OUTPUT_DIR
            image_files = []
            for ext in ['.png', '.jpg', '.jpeg']:
                image_files.extend(generated_dir.glob(f"*{ext}"))
            
            if not image_files:
                print_error("No images found in IMAGES/GENERATED")
                return False
            
            image_files.sort(key=lambda x: x.stat().st_mtime, reverse=True)
            
            print(f"\n{Colors.CYAN}AVAILABLE IMAGES (Most recent first):{Colors.RESET}")
            for idx, img in enumerate(image_files[:20], 1):
                size_kb = img.stat().st_size / 1024
                print(f"[{idx:2d}] {img.name} ({size_kb:.1f} KB)")
            
            if len(image_files) > 20:
                print(f"... and {len(image_files) - 20} more")
            
            try:
                selection = int(input(f"\n{Colors.YELLOW}Enter image number > {Colors.RESET}"))
                if 1 <= selection <= min(20, len(image_files)):
                    self.source_face = image_files[selection - 1]
                    print_success(f"✓ Source face selected: {self.source_face.name}")
                    return True
                else:
                    print_error("Invalid selection")
                    return False
            except ValueError:
                print_error("Invalid input")
                return False
    
    def module_2_scraper(self):
        if not self.source_face:
            print_error("No source face selected. Run Module 1 first.")
            return False
        
        print_banner("MODULE 2: INSTAGRAM SCRAPER", "Download photos for dataset (PHOTOS ONLY, ALL CAROUSEL IMAGES)")
        
        print(f"{Colors.GREEN}Source Face: {self.source_face.name}{Colors.RESET}\n")
        
        username = input(f"{Colors.YELLOW}Target Instagram username > {Colors.RESET}").strip()
        if not username:
            print_error("No username provided")
            return False
        
        self.current_username = username
        
        try:
            limit = int(input(f"{Colors.YELLOW}Maximum posts to download (20-50 recommended) > {Colors.RESET}"))
        except ValueError:
            limit = 30
            print_warning(f"Using default limit: {limit}")
        
        print(f"\n{Colors.CYAN}SCRAPER CONFIGURATION:{Colors.RESET}")
        print(f"  • Mode: PHOTOS ONLY")
        print(f"  • Carousels: ALL IMAGES")
        print(f"  • Videos: IGNORED")
        print(f"  • Limit: {limit} posts")
        print(f"  • Output: {self.raw_dir / username}\n")
        
        if not confirm_action("Start download?"):
            return False
        
        scraper = DatasetScraper(self.raw_dir)
        success = scraper.download_photos_only(username, limit)
        
        if success:
            image_files = scraper.organize_files(username)
            if image_files:
                print_success(f"\n✓ Downloaded {len(image_files)} images")
                print_info("Ready for Module 3: Curation")
                return True
        
        return False
    
    def module_3_curation(self):
        if not self.current_username:
            print_error("No dataset downloaded. Run Module 2 first.")
            return False
        
        print_banner("MODULE 3: DATASET CURATION", "Review and approve images for final dataset")
        
        raw_user_dir = self.raw_dir / self.current_username
        if not raw_user_dir.exists():
            print_error(f"Raw directory not found: {raw_user_dir}")
            return False
        
        image_files = []
        for ext in ['.jpg', '.jpeg', '.png']:
            image_files.extend(raw_user_dir.glob(f"*{ext}"))
        
        if not image_files:
            print_error("No images found to curate")
            return False
        
        image_files.sort(key=lambda x: x.stat().st_mtime, reverse=True)
        
        print(f"{Colors.GREEN}Source Face: {self.source_face.name}{Colors.RESET}")
        print(f"Images to Review: {len(image_files)}\n")
        
        print_info("You will review each image and decide:")
        print(f"  {Colors.GREEN}APPROVE{Colors.RESET} = Keep for dataset (high quality, clear body)")
        print(f"  {Colors.RED}REJECT{Colors.RESET} = Delete (blurry, bad pose, etc.)")
        print(f"  {Colors.YELLOW}SKIP{Colors.RESET} = Keep in RAW but don't approve\n")
        
        if not confirm_action("Start curation?"):
            return False
        
        curator = DatasetCurator(raw_user_dir, self.approved_dir)
        success = curator.review_images(image_files)
        
        if success and curator.stats['approved'] > 0:
            approved_files = list(self.approved_dir.glob("dataset_*.png")) + \
                           list(self.approved_dir.glob("dataset_*.jpg")) + \
                           list(self.approved_dir.glob("dataset_*.jpeg"))
            self.approved_images = approved_files
            
            print_success(f"\n✓ {len(self.approved_images)} images approved and ready")
            print_info("Ready for Module 4: Batch Face Swap")
            return True
        
        return False
    
    def module_4_batch_face_swap(self):
        if not self.source_face:
            print_error("No source face selected. Run Module 1 first.")
            return False
        
        if not self.approved_images:
            approved_files = list(self.approved_dir.glob("dataset_*.png")) + \
                           list(self.approved_dir.glob("dataset_*.jpg")) + \
                           list(self.approved_dir.glob("dataset_*.jpeg"))
            
            if not approved_files:
                print_error("No approved images found. Run Module 3 first.")
                return False
            
            self.approved_images = approved_files
        
        print_banner("MODULE 4: BATCH FACE SWAP", "Apply source face to all approved images")
        
        print(f"{Colors.GREEN}Source Face: {self.source_face.name}{Colors.RESET}")
        print(f"Approved Images: {len(self.approved_images)}")
        print(f"Output Directory: {self.final_dir}\n")
        
        print_warning("This will use Gemini API for each image.")
        print_info(f"Estimated time: ~{len(self.approved_images) * 30} seconds\n")
        
        if not confirm_action("Start batch processing?"):
            return False
        
        processor = BatchFaceSwap(self.source_face, self.final_dir)
        success = processor.process_batch(self.approved_images)
        
        if success:
            print(f"\n{Colors.GREEN}{'=' * 60}")
            print(f"  🎉 LORA DATASET COMPLETE!")
            print(f"{'=' * 60}{Colors.RESET}")
            print(f"Location: {self.final_dir}")
            print(f"Images: {processor.stats['success']}")
            print(f"\n{Colors.CYAN}Next steps:{Colors.RESET}")
            print(f"  1. Review the final images in {self.final_dir}")
            print(f"  2. Use these images to train your LoRa model")
            print(f"  3. Recommended: 20-40 high-quality images\n")
            return True
        
        return False
    
    def run(self):
        print_banner("DATASET FACTORY V1.0", "LoRa Training Dataset Production Pipeline")
        
        print(f"{Colors.CYAN}WORKFLOW:{Colors.RESET}")
        print(f"  1. Select source face (generate or choose existing)")
        print(f"  2. Scrape Instagram photos (all carousel images)")
        print(f"  3. Curate images (approve/reject)")
        print(f"  4. Batch face swap (apply source face to all)\n")
        
        print(f"{Colors.YELLOW}OUTPUT:{Colors.RESET} 20-40 high-quality images in DATASET/FINAL_LORA/\n")
        
        while True:
            print(f"{Colors.CYAN}{'─' * 60}")
            print(f"  MAIN MENU")
            print(f"{'─' * 60}{Colors.RESET}")
            
            if self.source_face:
                print(f"{Colors.GREEN}✓ [1] Source Face Selected: {self.source_face.name}{Colors.RESET}")
            else:
                print(f"[1] MODULE 1: Select Source Face")
            
            if self.current_username:
                print(f"{Colors.GREEN}✓ [2] Dataset Downloaded: @{self.current_username}{Colors.RESET}")
            else:
                print(f"[2] MODULE 2: Scrape Instagram Photos")
            
            if self.approved_images:
                print(f"{Colors.GREEN}✓ [3] Images Curated: {len(self.approved_images)} approved{Colors.RESET}")
            else:
                print(f"[3] MODULE 3: Curate Dataset")
            
            print(f"[4] MODULE 4: Batch Face Swap (Production)")
            print(f"[R] Reset (Clear all and start over)")
            print(f"[X] Exit\n")
            
            choice = input(f"{Colors.YELLOW}> Select module: {Colors.RESET}").strip().upper()
            
            if choice == "X":
                print_success("Goodbye!")
                break
            
            elif choice == "1":
                self.module_1_source_face()
            
            elif choice == "2":
                self.module_2_scraper()
            
            elif choice == "3":
                self.module_3_curation()
            
            elif choice == "4":
                self.module_4_batch_face_swap()
            
            elif choice == "R":
                if confirm_action("Reset all progress and start over?"):
                    self.source_face = None
                    self.current_username = None
                    self.approved_images = []
                    print_success("Reset complete")
            
            else:
                print_error("Invalid choice")
            
            input(f"\n{Colors.CYAN}Press Enter to continue...{Colors.RESET}")
            clear_screen()

def main():
    try:
        factory = DatasetFactory()
        factory.run()
    except KeyboardInterrupt:
        print(f"\n{Colors.YELLOW}Interrupted by user{Colors.RESET}")
    except Exception as e:
        print_error(f"Fatal error: {e}")
        import traceback
        traceback.print_exc()

if __name__ == "__main__":
    main()
