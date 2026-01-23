import os
from pathlib import Path
from typing import Optional, List
import time

try:
    import instaloader
except ImportError:
    os.system("python -m pip install instaloader")
    import instaloader

from core.config import Config
from core.utils import print_info, print_success, print_error, print_warning, Colors

class DatasetScraper:
    def __init__(self, output_dir: Path):
        self.output_dir = output_dir
        self.output_dir.mkdir(parents=True, exist_ok=True)
        self.loader = self._initialize_loader()
        self.stats = {
            'posts_processed': 0,
            'photos_downloaded': 0,
            'videos_skipped': 0,
            'carousels_found': 0,
            'errors': 0
        }
    
    def _initialize_loader(self):
        loader = instaloader.Instaloader(
            download_pictures=True,
            download_videos=False,
            download_video_thumbnails=False,
            download_geotags=False,
            download_comments=False,
            save_metadata=False,
            compress_json=False,
            post_metadata_txt_pattern='',
            max_connection_attempts=5,
            user_agent="Instagram 269.0.0.18.75 Android (26/8.0.0; 480dpi; 1080x1920; Samsung; SM-G930F; herolte; samsungexynos8890; en_US; 418491484)"
        )
        
        try:
            loader.context._session.cookies.set('sessionid', Config.INSTAGRAM_SESSION_ID, domain='.instagram.com')
            loader.context.username = Config.INSTAGRAM_USERNAME
            print_success("Instagram session authenticated")
        except Exception as e:
            print_error(f"Authentication failed: {e}")
            
        return loader
    
    def download_photos_only(self, username: str, limit: int = 50) -> bool:
        print_info(f"Starting dataset download for @{username}")
        print_warning("MODE: PHOTOS ONLY (Videos and Reels ignored)")
        print_info("CAROUSEL MODE: All images from albums will be downloaded")
        
        os.chdir(self.output_dir)
        
        try:
            profile = instaloader.Profile.from_username(self.loader.context, username)
            
            posts = profile.get_posts()
            seen_shortcodes = set()
            downloaded_count = 0
            
            for post in posts:
                if downloaded_count >= limit:
                    break
                
                if post.shortcode in seen_shortcodes:
                    continue
                seen_shortcodes.add(post.shortcode)
                
                self.stats['posts_processed'] += 1
                
                if post.is_video:
                    self.stats['videos_skipped'] += 1
                    print(f"{Colors.YELLOW}[SKIP]{Colors.RESET} Video/Reel - {post.date_local}")
                    continue
                
                if post.typename == 'GraphSidecar':
                    self.stats['carousels_found'] += 1
                    carousel_count = 0
                    
                    print(f"{Colors.CYAN}[CAROUSEL]{Colors.RESET} Album found - {post.date_local}")
                    
                    try:
                        for node in post.get_sidecar_nodes():
                            if not node.is_video:
                                carousel_count += 1
                                self.stats['photos_downloaded'] += 1
                        
                        self.loader.download_post(post, target=username)
                        downloaded_count += 1
                        print(f"{Colors.GREEN}  → Downloaded {carousel_count} photos from carousel{Colors.RESET}")
                        
                    except Exception as e:
                        self.stats['errors'] += 1
                        print_error(f"  Carousel error: {e}")
                
                else:
                    try:
                        self.loader.download_post(post, target=username)
                        downloaded_count += 1
                        self.stats['photos_downloaded'] += 1
                        print(f"{Colors.GREEN}[{downloaded_count}/{limit}]{Colors.RESET} Photo - {post.date_local}")
                        
                    except Exception as e:
                        self.stats['errors'] += 1
                        print_error(f"Download error: {e}")
            
            self._print_stats()
            return True
            
        except Exception as e:
            print_error(f"Profile download failed: {e}")
            return False
    
    def _print_stats(self):
        print(f"\n{Colors.CYAN}{'=' * 60}")
        print(f"  DOWNLOAD STATISTICS")
        print(f"{'=' * 60}{Colors.RESET}")
        print(f"Posts Processed: {self.stats['posts_processed']}")
        print(f"Photos Downloaded: {Colors.GREEN}{self.stats['photos_downloaded']}{Colors.RESET}")
        print(f"Carousels Found: {self.stats['carousels_found']}")
        print(f"Videos Skipped: {Colors.YELLOW}{self.stats['videos_skipped']}{Colors.RESET}")
        print(f"Errors: {Colors.RED}{self.stats['errors']}{Colors.RESET}\n")
    
    def organize_files(self, username: str) -> List[Path]:
        account_dir = self.output_dir / username
        if not account_dir.exists():
            return []
        
        for f in account_dir.glob("*.txt"):
            try:
                f.unlink()
            except:
                pass
        
        for f in account_dir.glob("*.json.xz"):
            try:
                f.unlink()
            except:
                pass
        
        # Renommer les images systématiquement
        self.rename_images(username)
        
        image_files = []
        for ext in ['.jpg', '.jpeg', '.png', '.webp']:
            image_files.extend(account_dir.glob(f"*{ext}"))
        
        image_files.sort(key=lambda x: x.stat().st_mtime, reverse=True)
        
        print_success(f"Found {len(image_files)} images")
        return image_files
    
    def rename_images(self, username: str):
        """Standardisation: renomme les images de 1 à n dans leur dossier RAW respectif"""
        account_dir = self.output_dir / username
        if not account_dir.exists():
            return
        
        print_info(f"Standardisation du scraper: renommage des images de 1 à n pour {username}")
        
        # Lister toutes les images avec leurs extensions
        image_files = []
        for ext in ['.jpg', '.jpeg', '.png', '.webp']:
            image_files.extend(account_dir.glob(f"*{ext}"))
        
        # Trier par date de modification pour avoir un ordre cohérent
        image_files.sort(key=lambda x: x.stat().st_mtime)
        
        # Renommer chaque image de 1 à n
        renamed_count = 0
        for i, old_path in enumerate(image_files, 1):
            # Conserver l'extension d'origine
            extension = old_path.suffix.lower()
            new_name = f"{i}{extension}"
            new_path = account_dir / new_name
            
            try:
                # Éviter de renommer si le fichier existe déjà avec le bon nom
                if old_path != new_path:
                    old_path.rename(new_path)
                    renamed_count += 1
                    print(f"  → {old_path.name} -> {new_name}")
            except Exception as e:
                print_error(f"Failed to rename {old_path.name}: {e}")
        
        print_success(f"Standardisation terminée: {renamed_count} images renommées de 1.{extension} à {len(image_files)}.{extension}")
        print_info(f"Les images sont maintenant prêtes pour la curation facile")
