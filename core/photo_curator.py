"""
Photo Curator - Backend Logic for Image Curation
Handles quality analysis, filtering, and export
"""
from pathlib import Path
from typing import List, Dict, Tuple, Optional
import json
from datetime import datetime
import shutil
from PIL import Image
import cv2
import numpy as np


class QualityAnalyzer:
    """Analyze image quality (blur, resolution, faces)"""
    
    def __init__(self):
        self.face_cascade = None
        try:
            # Try to load OpenCV face detector
            cascade_path = cv2.data.haarcascades + 'haarcascade_frontalface_default.xml'
            self.face_cascade = cv2.CascadeClassifier(cascade_path)
        except:
            pass
    
    def detect_blur(self, image_path: Path) -> float:
        """Calculate blur score using Laplacian variance (0-100, lower = more blur)"""
        try:
            img = cv2.imread(str(image_path), cv2.IMREAD_GRAYSCALE)
            if img is None:
                return 0.0
            
            # Calculate Laplacian variance
            laplacian_var = cv2.Laplacian(img, cv2.CV_64F).var()
            
            # Normalize to 0-100 scale (higher = sharper)
            # Typical sharp images: 500-2000, blurry: 0-100
            normalized = min(100, (laplacian_var / 20))
            return round(normalized, 2)
        
        except Exception as e:
            return 0.0
    
    def detect_faces(self, image_path: Path) -> int:
        """Count number of faces detected"""
        try:
            if self.face_cascade is None:
                return -1  # Face detection not available
            
            img = cv2.imread(str(image_path))
            if img is None:
                return 0
            
            gray = cv2.cvtColor(img, cv2.COLOR_BGR2GRAY)
            faces = self.face_cascade.detectMultiScale(gray, 1.1, 4)
            return len(faces)
        
        except Exception as e:
            return -1
    
    def check_resolution(self, image_path: Path) -> Tuple[int, int]:
        """Get image resolution (width, height)"""
        try:
            with Image.open(image_path) as img:
                return img.size
        except Exception as e:
            return (0, 0)
    
    def calculate_quality_score(self, image_path: Path) -> Dict:
        """Calculate overall quality score"""
        blur_score = self.detect_blur(image_path)
        face_count = self.detect_faces(image_path)
        width, height = self.check_resolution(image_path)
        
        # Calculate overall score (0-100)
        # Weights: blur 40%, resolution 30%, face detection 30%
        blur_weight = blur_score * 0.4
        
        # Resolution score (1024x1024 = 100%)
        res_score = min(100, ((width * height) / (1024 * 1024)) * 100)
        res_weight = res_score * 0.3
        
        # Face score (1 face = 100%, 0 or >1 = 50%)
        face_weight = 100 * 0.3 if face_count == 1 else 50 * 0.3 if face_count >= 0 else 0
        
        overall = blur_weight + res_weight + face_weight
        
        return {
            "blur_score": blur_score,
            "face_count": face_count,
            "resolution": (width, height),
            "resolution_score": res_score,
            "overall_score": round(overall, 2)
        }


class PhotoCurator:
    """Main photo curation backend"""
    
    def __init__(self, dataset_path: Path):
        self.dataset_path = dataset_path
        self.images: List[Path] = []
        self.approved: List[Path] = []
        self.rejected: List[Path] = []
        self.history: List[Tuple[str, Path]] = []
        self.current_index = 0
        self.quality_analyzer = QualityAnalyzer()
        self.quality_cache: Dict[str, Dict] = {}
    
    def load_dataset(self) -> List[Path]:
        """Load all images from dataset directory"""
        if not self.dataset_path.exists():
            return []
        
        extensions = ['.jpg', '.jpeg', '.png', '.webp']
        self.images = []
        
        for ext in extensions:
            self.images.extend(self.dataset_path.glob(f"*{ext}"))
            self.images.extend(self.dataset_path.glob(f"*{ext.upper()}"))
        
        # Sort by name
        self.images = sorted(self.images, key=lambda p: p.name)
        return self.images
    
    def apply_quality_filters(self, 
                             min_resolution: Tuple[int, int] = (512, 512),
                             max_blur_threshold: float = 30.0,
                             require_face: bool = False) -> List[Path]:
        """Filter images by quality criteria"""
        filtered = []
        
        for img_path in self.images:
            # Get or calculate quality
            if str(img_path) not in self.quality_cache:
                self.quality_cache[str(img_path)] = self.quality_analyzer.calculate_quality_score(img_path)
            
            quality = self.quality_cache[str(img_path)]
            
            # Check resolution
            width, height = quality['resolution']
            if width < min_resolution[0] or height < min_resolution[1]:
                continue
            
            # Check blur
            if quality['blur_score'] < max_blur_threshold:
                continue
            
            # Check face
            if require_face and quality['face_count'] != 1:
                continue
            
            filtered.append(img_path)
        
        return filtered
    
    def manual_approve(self, image_path: Path):
        """Manually approve an image"""
        if image_path not in self.approved:
            self.approved.append(image_path)
            self.history.append(("approve", image_path))
            
            # Remove from rejected if present
            if image_path in self.rejected:
                self.rejected.remove(image_path)
    
    def manual_reject(self, image_path: Path):
        """Manually reject an image"""
        if image_path not in self.rejected:
            self.rejected.append(image_path)
            self.history.append(("reject", image_path))
            
            # Remove from approved if present
            if image_path in self.approved:
                self.approved.remove(image_path)
    
    def batch_approve(self, image_paths: List[Path]):
        """Approve multiple images at once"""
        for path in image_paths:
            self.manual_approve(path)
    
    def batch_reject(self, image_paths: List[Path]):
        """Reject multiple images at once"""
        for path in image_paths:
            self.manual_reject(path)
    
    def undo(self) -> bool:
        """Undo last action. Returns True if successful."""
        if not self.history:
            return False
        
        action, image_path = self.history.pop()
        
        if action == "approve" and image_path in self.approved:
            self.approved.remove(image_path)
            return True
        elif action == "reject" and image_path in self.rejected:
            self.rejected.remove(image_path)
            return True
        
        return False
    
    def export_approved(self, 
                       output_dir: Path,
                       format_template: str = "dataset_{idx:03d}",
                       copy_mode: bool = True) -> int:
        """Export approved images to output directory. Returns count of exported files."""
        output_dir.mkdir(parents=True, exist_ok=True)
        
        exported_count = 0
        
        for idx, img_path in enumerate(self.approved, 1):
            # Generate output filename
            ext = img_path.suffix
            output_name = format_template.format(idx=idx) + ext
            output_path = output_dir / output_name
            
            # Copy or move
            if copy_mode:
                shutil.copy2(img_path, output_path)
            else:
                shutil.move(str(img_path), output_path)
            
            exported_count += 1
        
        # Create metadata JSON
        metadata = {
            "export_date": datetime.now().isoformat(),
            "total_exported": exported_count,
            "source_dataset": str(self.dataset_path),
            "approved_files": [str(p) for p in self.approved],
            "rejected_files": [str(p) for p in self.rejected]
        }
        
        metadata_path = output_dir / "curation_metadata.json"
        with open(metadata_path, 'w', encoding='utf-8') as f:
            json.dump(metadata, f, indent=2, ensure_ascii=False)
        
        return exported_count
    
    def get_stats(self) -> Dict:
        """Get curation statistics"""
        total = len(self.images)
        approved = len(self.approved)
        rejected = len(self.rejected)
        pending = total - approved - rejected
        
        return {
            "total": total,
            "approved": approved,
            "rejected": rejected,
            "pending": pending,
            "progress_pct": (approved + rejected) / total * 100 if total > 0 else 0
        }
    
    def save_session(self, session_file: Path):
        """Save current curation session to JSON"""
        session_data = {
            "dataset_path": str(self.dataset_path),
            "timestamp": datetime.now().isoformat(),
            "approved": [str(p) for p in self.approved],
            "rejected": [str(p) for p in self.rejected],
            "current_index": self.current_index,
            "stats": self.get_stats()
        }
        
        with open(session_file, 'w', encoding='utf-8') as f:
            json.dump(session_data, f, indent=2, ensure_ascii=False)
    
    def load_session(self, session_file: Path) -> bool:
        """Load curation session from JSON. Returns True if successful."""
        try:
            with open(session_file, 'r', encoding='utf-8') as f:
                session_data = json.load(f)
            
            self.approved = [Path(p) for p in session_data.get("approved", [])]
            self.rejected = [Path(p) for p in session_data.get("rejected", [])]
            self.current_index = session_data.get("current_index", 0)
            
            return True
        except Exception as e:
            return False
