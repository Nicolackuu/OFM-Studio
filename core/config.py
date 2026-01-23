import os
from pathlib import Path
from dotenv import load_dotenv

# Charge les variables du fichier .env
load_dotenv(encoding='utf-8')

class Config:
    # --- CHEMINS DE BASE ---
    BASE_DIR = Path(__file__).parent.parent.absolute()
    
    # --- SÉCURITÉ (GOOGLE GEMINI) ---
    # On récupère la clé du .env. La valeur en dur est supprimée pour éviter le ban.
    GOOGLE_API_KEY = os.getenv('GOOGLE_API_KEY')
    MODEL_IMAGE = "gemini-3-pro-image-preview"
    
    # --- SÉCURITÉ (INSTAGRAM) ---
    # Tes identifiants sont maintenant protégés dans le .env
    INSTAGRAM_USERNAME = os.getenv('INSTAGRAM_USERNAME')
    INSTAGRAM_SESSION_ID = os.getenv('INSTAGRAM_SESSION_ID')
    
    @classmethod
    @property
    def SESSION_ID(cls):
        """Récupère le SESSION_ID depuis les variables d'environnement"""
        return os.getenv('INSTAGRAM_SESSION_ID')
    
    # --- CONFIGURATION GEMINI (TES PARAMÈTRES EXACTS) ---
    GEMINI_CONFIG = {
        "temperature": 0.85,
        "top_p": 0.9,
        "aspect_ratio": "3:2",
        "image_size": "2K"
    }
    
    # --- RÉPERTOIRES DE DONNÉES (100% minuscules) ---
    DATA_DIR = BASE_DIR / "data" / "dataset"
    RAW_DIR = DATA_DIR / "raw"
    PROCESSED_DIR = DATA_DIR / "processed"
    MODELS_DIR = PROCESSED_DIR / "models"
    CURATED_DIR = PROCESSED_DIR / "curated"
    TEMP_DIR = DATA_DIR / "temp"
    SWAPPED_DIR = PROCESSED_DIR / "swapped"

    # --- RÉPERTOIRES DE SORTIE ---
    OUTPUT_DIR = SWAPPED_DIR  # Face swap output directory
    FACE_SWAP_OUTPUT = SWAPPED_DIR  # Face swap output directory
    
    @classmethod
    def check_directories(cls):
        """Crée physiquement tous les dossiers nécessaires"""
        cls.DATA_DIR.mkdir(parents=True, exist_ok=True)
        cls.RAW_DIR.mkdir(parents=True, exist_ok=True)
        cls.PROCESSED_DIR.mkdir(parents=True, exist_ok=True)
        cls.MODELS_DIR.mkdir(parents=True, exist_ok=True)
        cls.CURATED_DIR.mkdir(parents=True, exist_ok=True)
        cls.TEMP_DIR.mkdir(parents=True, exist_ok=True)
        cls.SWAPPED_DIR.mkdir(parents=True, exist_ok=True)
    
    @classmethod
    def ensure_directories(cls):
        """Crée l'arborescence si elle n'existe pas"""
        cls.check_directories()

# Auto-exécution pour garantir que les dossiers sont là au démarrage
Config.ensure_directories()