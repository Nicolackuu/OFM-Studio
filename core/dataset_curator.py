import os
import shutil
from pathlib import Path
from typing import List
import subprocess
import sys

from core.utils import print_info, print_success, print_error, print_warning, Colors, clear_screen

class DatasetCurator:
    def __init__(self, raw_dir: Path, approved_dir: Path):
        self.raw_dir = raw_dir
        self.approved_dir = approved_dir
        self.approved_dir.mkdir(parents=True, exist_ok=True)
        
        self.stats = {
            'total': 0,
            'approved': 0,
            'rejected': 0,
            'skipped': 0
        }
    
    def _open_image(self, image_path: Path):
        try:
            if os.name == 'nt':
                os.startfile(image_path)
            elif sys.platform == 'darwin':
                subprocess.call(('open', image_path))
            else:
                subprocess.call(('xdg-open', image_path))
        except Exception as e:
            print_warning(f"Could not auto-open image: {e}")
    
    def review_images(self, image_files: List[Path]) -> bool:
        if not image_files:
            print_error("No images to review")
            return False
        
        self.stats['total'] = len(image_files)
        
        print(f"\n{Colors.CYAN}{'=' * 60}")
        print(f"  DATASET CURATION - REVIEW MODE")
        print(f"{'=' * 60}{Colors.RESET}")
        print(f"Total images: {len(image_files)}")
        print(f"\n{Colors.YELLOW}CONTROLS:{Colors.RESET}")
        print(f"  [Enter] or [O] = APPROVE (Keep for dataset)")
        print(f"  [X] or [N] = REJECT (Delete)")
        print(f"  [S] = SKIP (Keep in RAW, don't approve)")
        print(f"  [Q] = QUIT curation\n")
        
        input(f"{Colors.CYAN}Press Enter to start review...{Colors.RESET}")
        
        for idx, image_path in enumerate(image_files, 1):
            clear_screen()
            
            print(f"{Colors.CYAN}{'=' * 60}")
            print(f"  IMAGE {idx}/{len(image_files)}")
            print(f"{'=' * 60}{Colors.RESET}")
            print(f"File: {image_path.name}")
            print(f"Size: {image_path.stat().st_size / 1024:.1f} KB")
            print(f"\nProgress: {Colors.GREEN}{self.stats['approved']} approved{Colors.RESET} | "
                  f"{Colors.RED}{self.stats['rejected']} rejected{Colors.RESET} | "
                  f"{Colors.YELLOW}{self.stats['skipped']} skipped{Colors.RESET}\n")
            
            self._open_image(image_path)
            
            while True:
                choice = input(f"{Colors.YELLOW}[Enter/O] Approve | [X/N] Reject | [S] Skip | [Q] Quit > {Colors.RESET}").strip().upper()
                
                if choice in ['', 'O']:
                    try:
                        new_name = f"dataset_{self.stats['approved'] + 1:03d}{image_path.suffix}"
                        dest_path = self.approved_dir / new_name
                        shutil.copy2(image_path, dest_path)
                        self.stats['approved'] += 1
                        print_success(f"✓ Approved → {new_name}")
                        break
                    except Exception as e:
                        print_error(f"Failed to approve: {e}")
                        break
                
                elif choice in ['X', 'N']:
                    try:
                        image_path.unlink()
                        self.stats['rejected'] += 1
                        print_error(f"✗ Rejected and deleted")
                        break
                    except Exception as e:
                        print_error(f"Failed to delete: {e}")
                        break
                
                elif choice == 'S':
                    self.stats['skipped'] += 1
                    print_warning(f"⊘ Skipped (kept in RAW)")
                    break
                
                elif choice == 'Q':
                    print_warning("\nCuration interrupted by user")
                    self._print_final_stats()
                    return False
                
                else:
                    print_error("Invalid choice. Use Enter/O/X/N/S/Q")
        
        self._print_final_stats()
        return True
    
    def _print_final_stats(self):
        print(f"\n{Colors.CYAN}{'=' * 60}")
        print(f"  CURATION COMPLETE")
        print(f"{'=' * 60}{Colors.RESET}")
        print(f"Total Reviewed: {self.stats['total']}")
        print(f"Approved: {Colors.GREEN}{self.stats['approved']}{Colors.RESET} → {self.approved_dir}")
        print(f"Rejected: {Colors.RED}{self.stats['rejected']}{Colors.RESET} (deleted)")
        print(f"Skipped: {Colors.YELLOW}{self.stats['skipped']}{Colors.RESET} (kept in RAW)")
        
        if self.stats['approved'] > 0:
            print(f"\n{Colors.GREEN}✓ Dataset ready for face swap!{Colors.RESET}")
        else:
            print(f"\n{Colors.YELLOW}⚠ No images approved. Run curation again or adjust selection.{Colors.RESET}")
