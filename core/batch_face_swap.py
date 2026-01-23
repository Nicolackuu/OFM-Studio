import os
import time
import logging
from pathlib import Path
from typing import List
import requests

# Imports pour le mode LOCAL
import cv2
import numpy as np
import insightface
from insightface.app import FaceAnalysis

# Imports pour le mode CLOUD
import replicate

from core.utils import print_success, print_error, Colors

# Configure logging
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

class BatchFaceSwap:
    def __init__(self, source_face_path: Path, output_dir: Path, engine: str = 'local'):
        """
        engine: 'local' (RTX 3070) ou 'replicate' (Cloud)
        """
        self.source_face_path = source_face_path
        self.output_dir = output_dir
        self.output_dir.mkdir(parents=True, exist_ok=True)
        self.stats = {'total': 0, 'success': 0, 'failed': 0}
        self.engine = engine.lower()

        print(f"\n{Colors.CYAN}🔧 Initialisation du moteur : {self.engine.upper()}{Colors.RESET}")

        if self.engine == 'local':
            self._init_local()
        elif self.engine == 'replicate':
            self._init_replicate()
        else:
            raise ValueError("Engine must be 'local' or 'replicate'")

    def _init_local(self):
        """Initialisation du moteur InsightFace sur GPU Local"""
        try:
            print("   Chargement des modèles GPU (cela peut prendre un moment)...")
            # Détection (Buffalo_L)
            self.app = FaceAnalysis(name='buffalo_l', providers=['CUDAExecutionProvider', 'CPUExecutionProvider'])
            self.app.prepare(ctx_id=0, det_size=(640, 640))
            
            # Swap (Inswapper)
            self.swapper = insightface.model_zoo.get_model('inswapper_128.onnx', download=True, download_zip=True)
            
            # Prépare le visage source
            self.source_face_embedding = self._get_local_source_face(self.source_face_path)
            print_success("✅ Moteur LOCAL (GPU) prêt.")
        except Exception as e:
            print_error(f"Erreur init Local : {e}")
            raise e

    def _init_replicate(self):
        """Initialisation du client Replicate"""
        if not os.environ.get("REPLICATE_API_TOKEN"):
            raise ValueError("Manque REPLICATE_API_TOKEN dans le .env")
        try:
            # Test simple
            self.client = replicate.Client(api_token=os.environ["REPLICATE_API_TOKEN"])
            print_success("✅ Moteur REPLICATE (Cloud) prêt.")
        except Exception as e:
            print_error(f"Erreur init Replicate : {e}")
            raise e

    def _get_local_source_face(self, path: Path):
        img = cv2.imread(str(path))
        faces = self.app.get(img)
        if not faces:
            raise ValueError(f"Aucun visage trouvé sur la source : {path.name}")
        return sorted(faces, key=lambda x: x.bbox[2] * x.bbox[3])[-1]

    def process_batch(self, target_directory: Path, output_directory: Path, naming_pattern: str = None) -> List[Path]:
        image_files = []
        for ext in ['.jpg', '.jpeg', '.png', '.webp']:
            image_files.extend(target_directory.glob(f"*{ext}"))
        
        self.stats['total'] = len(image_files)
        results = []
        
        print(f"{'='*60}")
        print(f"  BATCH PROCESSING - MODE: {self.engine.upper()}")
        print(f"{'='*60}")

        for idx, image_path in enumerate(image_files, 1):
            print(f"[{idx}/{len(image_files)}] {image_path.name}...", end="\r")
            
            try:
                success = False
                output_path = None
                
                # Routage vers le bon moteur
                if self.engine == 'local':
                    success, output_path = self._process_single_local(image_path, output_directory, naming_pattern, idx)
                else:
                    success, output_path = self._process_single_replicate(image_path, output_directory, naming_pattern, idx)

                if success and output_path:
                    results.append(output_path)
                    self.stats['success'] += 1
                    print(f"[{idx}/{len(image_files)}] {image_path.name} -> {Colors.GREEN}OK{Colors.RESET}   ")
                else:
                    self.stats['failed'] += 1
                    print(f"[{idx}/{len(image_files)}] {image_path.name} -> {Colors.RED}FAIL{Colors.RESET} ")

            except Exception as e:
                logger.error(f"Global Error {image_path.name}: {e}")
                self.stats['failed'] += 1
        
        self._print_stats()
        return results

    def _process_single_local(self, image_path, output_dir, naming_pattern, idx):
        try:
            target_img = cv2.imread(str(image_path))
            if target_img is None: return False, None
            
            faces = self.app.get(target_img)
            if not faces: return False, None

            res = target_img.copy()
            for face in faces:
                res = self.swapper.get(res, face, self.source_face_embedding, paste_back=True)

            out_name = naming_pattern.format(original=image_path.stem) if naming_pattern else f"swap_{idx:03d}_{image_path.stem}.png"
            out_path = output_dir / out_name
            cv2.imwrite(str(out_path), res)
            return True, out_path
        except Exception as e:
            logger.error(f"Local Error: {e}")
            return False, None

    def _process_single_replicate(self, image_path, output_dir, naming_pattern, idx):
        # Modèle Lucataco (InsightFace wrapper)
        MODEL = "lucataco/faceswap:9a4298548422074c3f57258c5d544497314ae4112df80d116f0d2109e843d20d"
        try:
            with open(self.source_face_path, "rb") as src, open(image_path, "rb") as tgt:
                output = replicate.run(MODEL, input={"swap_image": src, "target_image": tgt})
            
            url = output[0] if isinstance(output, list) else output
            if not url: return False, None

            out_name = naming_pattern.format(original=image_path.stem) if naming_pattern else f"swap_{idx:03d}_{image_path.stem}.png"
            out_path = output_dir / out_name
            
            # Téléchargement
            resp = requests.get(url)
            if resp.status_code == 200:
                with open(out_path, 'wb') as f:
                    f.write(resp.content)
                return True, out_path
            return False, None
        except Exception as e:
            logger.error(f"Replicate Error: {e}")
            return False, None

    def _print_stats(self):
        print(f"\nTerminé. Succès: {self.stats['success']} | Echecs: {self.stats['failed']}")