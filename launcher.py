import os
import sys
import subprocess
from pathlib import Path

def main():
    # Nettoyage console (Windows/Mac/Linux)
    os.system('cls' if os.name == 'nt' else 'clear')
    
    print("="*60)
    print("      🚀 OFM STUDIO - LAUNCHER V2 (AUTO-LOCATED)      ")
    print("="*60)

    # 1. LOCALISATION ABSOLUE (Le Secret)
    # On récupère le dossier exact où se trouve CE fichier launcher.py
    current_dir = Path(__file__).resolve().parent
    
    # 2. DÉFINITION DE LA CIBLE
    target_script = current_dir / "studio_linear.py"
    
    print(f"📂 Dossier racine : {current_dir}")
    print(f"🎯 Fichier cible  : {target_script.name}")
    print("-" * 60)

    # 3. VÉRIFICATION DE PRÉSENCE
    if not target_script.exists():
        print(f"\n❌ ERREUR CRITIQUE : '{target_script.name}' est introuvable !")
        print(f"   Chemin cherché : {target_script}")
        print("\n👉 Vérifie que 'launcher.py' et 'studio_linear.py' sont bien côte à côte.")
        input("\nAppuyez sur Entrée pour quitter...")
        sys.exit(1)

    # 4. DÉTECTION DU BON PYTHON (VENV)
    # On cherche le python dans le dossier venv local pour éviter les erreurs de modules
    possible_venvs = [
        current_dir / "venv" / "Scripts" / "python.exe",  # Windows standard
        current_dir / ".venv" / "Scripts" / "python.exe", # Alternative
        current_dir / "env" / "Scripts" / "python.exe",   # Ancienne convention
    ]
    
    python_exe = sys.executable # Par défaut : le python qui lance le script
    using_venv = False
    
    for venv_path in possible_venvs:
        if venv_path.exists():
            python_exe = str(venv_path)
            using_venv = True
            break
            
    if using_venv:
        print("✅ Environnement virtuel détecté (venv)")
    else:
        print("⚠️  Aucun venv trouvé, utilisation du Python système")
        print("   (Si ça plante, vérifiez que vos modules sont installés ici)")

    # 5. LANCEMENT
    print("\n🚀 Démarrage de l'interface...")
    print("   (Ne fermez pas cette fenêtre noire tant que le studio est ouvert)")
    
    # Commande : [python] -m streamlit run [script]
    cmd = [python_exe, "-m", "streamlit", "run", str(target_script)]
    
    try:
        # cwd=current_dir force l'exécution DANS le dossier du projet
        subprocess.run(cmd, cwd=current_dir, check=True)
    except KeyboardInterrupt:
        print("\n👋 Arrêt utilisateur.")
    except Exception as e:
        print(f"\n❌ CRASH DU PROCESSUS : {e}")
        input("\nAppuyez sur Entrée pour fermer...")

if __name__ == "__main__":
    main()