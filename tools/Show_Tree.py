import os

# Le dossier à scanner
ROOT_DIR = r"C:\Users\nicol\Desktop\OFM IA"

def generate_tree(dir_path, prefix=""):
    # On récupère la liste des fichiers et dossiers
    try:
        contents = os.listdir(dir_path)
    except PermissionError:
        print(f"{prefix}[ACCESS DENIED]")
        return

    # On sépare les dossiers et les fichiers pour l'affichage
    dirs = [d for d in contents if os.path.isdir(os.path.join(dir_path, d))]
    files = [f for f in contents if os.path.isfile(os.path.join(dir_path, f))]
    
    # On trie pour que ce soit propre
    dirs.sort()
    files.sort()
    
    entries = dirs + files
    pointers = [("├── " if i < len(entries) - 1 else "└── ") for i in range(len(entries))]

    for pointer, entry in zip(pointers, entries):
        full_path = os.path.join(dir_path, entry)
        
        # On affiche
        print(f"{prefix}{pointer}{entry}")
        
        # Si c'est un dossier, on plonge dedans (récursivité)
        if os.path.isdir(full_path):
            # On ignore les dossiers système cachés (.git, etc)
            if entry.startswith("."): continue
            
            extension = "│   " if pointer == "├── " else "    "
            generate_tree(full_path, prefix + extension)

def main():
    os.system('cls' if os.name == 'nt' else 'clear')
    print(f"=== STRUCTURE DU DOSSIER : {ROOT_DIR} ===\n")
    
    if os.path.exists(ROOT_DIR):
        print(os.path.basename(ROOT_DIR))
        generate_tree(ROOT_DIR)
    else:
        print(f"ERREUR : Le dossier {ROOT_DIR} n'existe pas.")

    input("\nAppuie sur Entree pour copier/fermer...")

if __name__ == "__main__":
    main()