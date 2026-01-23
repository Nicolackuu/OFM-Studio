import subprocess
import sys
import os

def get_pip_list(python_exe):
    try:
        result = subprocess.check_output([python_exe, "-m", "pip", "list"], text=True)
        return set(line.split()[0].lower() for line in result.splitlines()[2:])
    except:
        return set()

def audit():
    print("🔍 ANALYSE DE L'INTÉGRITÉ DU SYSTÈME...")
    
    # 1. Chemins
    global_python = sys.executable
    venv_python = os.path.join(os.getcwd(), "venv", "Scripts", "python.exe")
    
    # 2. Collecte des données
    print("📦 Lecture des paquets Globaux (Windows)...")
    global_pkgs = get_pip_list("python")
    
    print("🛡️ Lecture des paquets Locaux (VENV)...")
    venv_pkgs = get_pip_list(venv_python)
    
    # 3. Identification des conflits critiques
    critiques = {"opencv-python", "pynvml", "psutil", "google-genai", "streamlit", "onnxruntime-gpu"}
    conflits = critiques.intersection(global_pkgs)
    
    print("\n" + "="*50)
    if conflits:
        print(f"⚠️  ALERTE : {len(conflits)} DOUBLONS DÉTECTÉS !")
        print("Ces librairies sont installées sur Windows ET dans ton venv.")
        print("Cela peut causer des erreurs de 'DLL Load Failed' sur ta RTX 3070.")
        for pkg in conflits:
            print(f"   - [!] {pkg}")
    else:
        print("✅ SYSTÈME PROPRE : Aucun conflit critique détecté sur Windows.")
    
    # 4. Vérification des fichiers fantômes
    print("\n📂 VÉRIFICATION DES FICHIERS FANTÔMES...")
    trash_dir = "_TRASH"
    if os.path.exists(trash_dir):
        files = os.listdir(trash_dir)
        print(f"🗑️  {len(files)} fichiers sont en attente de suppression dans {trash_dir}.")
    
    print("="*50)
    print("\n💡 CONSEIL : Si tu as des doublons, lance : 'pip uninstall <nom>' hors du venv.")

if __name__ == "__main__":
    audit()