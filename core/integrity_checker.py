"""
OFM IA Studio - Integrity Checker
Vérifie l'intégrité de tous les fichiers et dossiers au démarrage
"""
import os
from pathlib import Path
from typing import Dict, List, Tuple
import json

class IntegrityChecker:
    """Vérifie l'intégrité du système OFM IA Studio"""
    
    def __init__(self, base_dir: Path = None):
        self.base_dir = base_dir or Path(__file__).parent.parent
        self.errors = []
        self.warnings = []
        self.info = []
        
    def check_all(self) -> Tuple[bool, Dict]:
        """Vérifie tous les composants du système"""
        print("🔍 OFM IA Studio - Integrity Check")
        print("=" * 60)
        
        # 1. Vérifier la structure des dossiers
        self._check_directory_structure()
        
        # 2. Vérifier les fichiers critiques
        self._check_critical_files()
        
        # 3. Vérifier les modules UI
        self._check_ui_modules()
        
        # 4. Vérifier les dépendances
        self._check_dependencies()
        
        # 5. Vérifier la configuration
        self._check_configuration()
        
        # Résumé
        return self._print_summary()
    
    def _check_directory_structure(self):
        """Vérifie que tous les dossiers requis existent"""
        print("\n📁 Vérification de la structure des dossiers...")
        
        required_dirs = [
            "core",
            "ui",
            "style",
            "data",
            "DATASET/RAW",
            "DATASET/APPROVED",
            "DATASET/FINAL_LORA",
            "OUTPUT"
        ]
        
        for dir_path in required_dirs:
            full_path = self.base_dir / dir_path
            if not full_path.exists():
                full_path.mkdir(parents=True, exist_ok=True)
                self.warnings.append(f"Créé: {dir_path}")
                print(f"  ⚠️  Créé: {dir_path}")
            else:
                self.info.append(f"OK: {dir_path}")
                print(f"  ✅ OK: {dir_path}")
    
    def _check_critical_files(self):
        """Vérifie que tous les fichiers critiques existent"""
        print("\n📄 Vérification des fichiers critiques...")
        
        critical_files = [
            "studio_premium.py",
            "core/config.py",
            "core/gemini_engine.py",
            "core/dna_mixer.py",
            "core/persistent_monitor.py",
            "core/batch_face_swap.py",
            "ui/components.py",
            "ui/home_premium.py",
            "ui/casting_premium.py",
            "ui/scraper.py",
            "ui/factory.py",
            "style/premium_linear.css",
            "requirements.txt"
        ]
        
        for file_path in critical_files:
            full_path = self.base_dir / file_path
            if not full_path.exists():
                self.errors.append(f"MANQUANT: {file_path}")
                print(f"  ❌ MANQUANT: {file_path}")
            else:
                # Vérifier que le fichier n'est pas vide
                if full_path.stat().st_size == 0:
                    self.errors.append(f"VIDE: {file_path}")
                    print(f"  ❌ VIDE: {file_path}")
                else:
                    self.info.append(f"OK: {file_path}")
                    print(f"  ✅ OK: {file_path}")
    
    def _check_ui_modules(self):
        """Vérifie que tous les modules UI sont importables"""
        print("\n🎨 Vérification des modules UI...")
        
        ui_modules = [
            "home_premium",
            "casting_premium",
            "scraper",
            "factory",
            "components"
        ]
        
        for module in ui_modules:
            try:
                # Vérifier que le fichier existe
                module_path = self.base_dir / "ui" / f"{module}.py"
                if module_path.exists():
                    # Vérifier qu'il contient une fonction render()
                    with open(module_path, 'r', encoding='utf-8') as f:
                        content = f.read()
                        if 'def render(' in content:
                            self.info.append(f"OK: ui/{module}.py (render found)")
                            print(f"  ✅ OK: ui/{module}.py")
                        else:
                            self.warnings.append(f"ui/{module}.py: pas de fonction render()")
                            print(f"  ⚠️  ui/{module}.py: pas de fonction render()")
                else:
                    self.errors.append(f"MANQUANT: ui/{module}.py")
                    print(f"  ❌ MANQUANT: ui/{module}.py")
            except Exception as e:
                self.errors.append(f"Erreur lors de la vérification de ui/{module}.py: {e}")
                print(f"  ❌ Erreur: ui/{module}.py - {e}")
    
    def _check_dependencies(self):
        """Vérifie que requirements.txt existe et contient les dépendances critiques"""
        print("\n📦 Vérification des dépendances...")
        
        req_file = self.base_dir / "requirements.txt"
        if not req_file.exists():
            self.errors.append("requirements.txt manquant")
            print(f"  ❌ requirements.txt manquant")
            return
        
        with open(req_file, 'r', encoding='utf-8') as f:
            content = f.read()
        
        critical_deps = [
            "streamlit",
            "google-genai",
            "pillow",
            "psutil",
            "instagrapi"
        ]
        
        for dep in critical_deps:
            if dep.lower() in content.lower():
                self.info.append(f"OK: {dep}")
                print(f"  ✅ OK: {dep}")
            else:
                self.warnings.append(f"Dépendance manquante: {dep}")
                print(f"  ⚠️  Dépendance manquante: {dep}")
    
    def _check_configuration(self):
        """Vérifie la configuration (.env et data/api_usage.json)"""
        print("\n⚙️  Vérification de la configuration...")
        
        # Vérifier .env
        env_file = self.base_dir / ".env"
        if env_file.exists():
            with open(env_file, 'r', encoding='utf-8') as f:
                content = f.read()
            
            if 'GOOGLE_API_KEY' in content:
                self.info.append("OK: GOOGLE_API_KEY dans .env")
                print(f"  ✅ OK: GOOGLE_API_KEY configuré")
            else:
                self.warnings.append("GOOGLE_API_KEY non configuré dans .env")
                print(f"  ⚠️  GOOGLE_API_KEY non configuré")
        else:
            self.warnings.append(".env manquant")
            print(f"  ⚠️  .env manquant")
        
        # Vérifier data/api_usage.json
        api_usage_file = self.base_dir / "data" / "api_usage.json"
        if api_usage_file.exists():
            try:
                with open(api_usage_file, 'r', encoding='utf-8') as f:
                    data = json.load(f)
                
                if 'quota_total' in data and data['quota_total'] == 100000:
                    self.info.append("OK: Quota 100k configuré")
                    print(f"  ✅ OK: Quota 100k configuré")
                else:
                    self.warnings.append("Quota non configuré correctement")
                    print(f"  ⚠️  Quota non configuré correctement")
            except Exception as e:
                self.errors.append(f"Erreur lors de la lecture de api_usage.json: {e}")
                print(f"  ❌ Erreur: api_usage.json - {e}")
        else:
            self.warnings.append("data/api_usage.json manquant (sera créé au démarrage)")
            print(f"  ⚠️  data/api_usage.json manquant (sera créé)")
    
    def _print_summary(self) -> Tuple[bool, Dict]:
        """Affiche le résumé et retourne le statut"""
        print("\n" + "=" * 60)
        print("📊 RÉSUMÉ DE LA VÉRIFICATION")
        print("=" * 60)
        
        print(f"\n✅ Info: {len(self.info)}")
        print(f"⚠️  Warnings: {len(self.warnings)}")
        print(f"❌ Erreurs: {len(self.errors)}")
        
        if self.errors:
            print("\n❌ ERREURS CRITIQUES:")
            for error in self.errors:
                print(f"  - {error}")
        
        if self.warnings:
            print("\n⚠️  AVERTISSEMENTS:")
            for warning in self.warnings[:5]:  # Limiter à 5
                print(f"  - {warning}")
            if len(self.warnings) > 5:
                print(f"  ... et {len(self.warnings) - 5} autres")
        
        print("\n" + "=" * 60)
        
        is_healthy = len(self.errors) == 0
        
        if is_healthy:
            print("✅ SYSTÈME OPÉRATIONNEL")
        else:
            print("❌ SYSTÈME NON OPÉRATIONNEL - Corrigez les erreurs ci-dessus")
        
        print("=" * 60 + "\n")
        
        return is_healthy, {
            'errors': self.errors,
            'warnings': self.warnings,
            'info': self.info
        }

def run_integrity_check():
    """Point d'entrée pour la vérification d'intégrité"""
    checker = IntegrityChecker()
    is_healthy, report = checker.check_all()
    return is_healthy, report

if __name__ == "__main__":
    run_integrity_check()
