# 🎬 GEMINI STUDIO V16 - Architecture Modulaire

## 📋 RÉSUMÉ DES CHANGEMENTS

### ✅ RÉSOLUTION NATIVE 2K/4K CONFIRMÉE
**BONNE NOUVELLE** : Le modèle `gemini-3-pro-image-preview` supporte **NATIVEMENT** les résolutions 2K et 4K !

Selon la documentation officielle Google GenAI :
- `image_size` accepte : `"1K"`, `"2K"`, `"4K"` (majuscules obligatoires)
- Pas besoin d'upscaling externe
- Configuration par défaut : **2K** (meilleur compromis qualité/vitesse)

### 🏗️ ARCHITECTURE MODULAIRE

Le script monolithique a été découpé en 4 modules :

```
Scripts/
├── main.py          # Point d'entrée + Menu interactif
├── config.py        # Configuration API + Paramètres
├── data_bank.py     # Banques de données Casting
└── core_engine.py   # Moteur de génération Gemini
```

---

## 📁 DESCRIPTION DES MODULES

### 1️⃣ `config.py` - Configuration
**Contenu** :
- Clé API Google
- Nom du modèle (`gemini-3-pro-image-preview`)
- Paramètres de génération (température, top_p, ratio, résolution)
- Chemins de sortie
- Couleurs terminal

**Paramètres modifiables** :
```python
CONFIG_PARAMS = {
    "temperature": 0.85,
    "top_p": 0.9,
    "aspect_ratio": "3:2",  # 16:9, 3:2, 1:1, 3:4
    "image_size": "2K"      # 1K, 2K, 4K
}
```

---

### 2️⃣ `data_bank.py` - Banque de Données
**Contenu** :
- 9 Nationalités (Française, Brésilienne, Russe, etc.)
- 4 Types de corps
- 5 Formes de visage
- 6 Types d'yeux
- 6 Styles de cheveux
- 5 Combinaisons nez/lèvres
- 7 Imperfections charmantes

**Fonctions** :
- `random_casting()` : Génère un profil aléatoire complet
- `get_prompt_text(phase)` : Construit les prompts pour chaque phase

---

### 3️⃣ `core_engine.py` - Moteur de Génération
**Contenu** :
- Initialisation du client Google GenAI
- Fonction `generate_image()` : Appel API avec support 2K/4K
- Gestion des images de référence (Phases 2 & 3)
- Sauvegarde automatique avec timestamp
- Ouverture automatique de l'image

**Caractéristiques** :
- Nom de fichier : `Phase{X}_{Nationalité}_{Résolution}_{Timestamp}.png`
- Exemple : `Phase1_Française_2K_20260120_210530.png`

---

### 4️⃣ `main.py` - Point d'Entrée
**Contenu** :
- Menu interactif
- Gestion des 3 phases
- Options de configuration (ratio, résolution)
- Boucle Garder/Refaire

**Menu** :
```
[0] 🎰 SLOT MACHINE (Nouveau Modèle)
[R] 📐 CHANGER LE RATIO
[Q] 🎬 CHANGER LA RÉSOLUTION
1. PHASE 1 : Foundation
2. PHASE 2 : Structure
3. PHASE 3 : Dynamics
X. Quitter
```

---

## 🚀 UTILISATION

### Lancement
```bash
python main.py
```

### Workflow Typique
1. **[0]** Générer un nouveau modèle aléatoire
2. **[Q]** Choisir la résolution (2K recommandé, 4K pour max qualité)
3. **[R]** Ajuster le ratio si besoin (3:2 par défaut = meilleur pour visages)
4. **[1]** Lancer Phase 1 (3 angles de base)
5. **[2]** Lancer Phase 2 avec l'image Phase 1 en référence
6. **[3]** Lancer Phase 3 avec l'image Phase 2 en référence

---

## 🎯 RÉSOLUTIONS DISPONIBLES

| Résolution | Pixels (approx.) | Utilisation | Vitesse |
|------------|------------------|-------------|---------|
| **1K** | ~1024px | Tests rapides | ⚡⚡⚡ |
| **2K** | ~2048px | Production standard ⭐ | ⚡⚡ |
| **4K** | ~4096px | Maximum qualité | ⚡ |

**Recommandation** : Commencer en 2K, passer en 4K pour les images finales.

---

## 🎨 RATIOS DISPONIBLES

| Ratio | Description | Meilleur pour |
|-------|-------------|---------------|
| **3:2** | Photo Pro (Reflex) | Portraits, visages ⭐ |
| **16:9** | Cinéma | Scènes larges |
| **1:1** | Carré | Instagram |
| **3:4** | Portrait vertical | Pleine hauteur |

---

## 🔧 SYSTÈME DE PHASES

### Phase 1 : Foundation
- 3 angles (Profil gauche, Face, 3/4 droit)
- Établit l'identité faciale de base
- **Pas besoin d'image de référence**

### Phase 2 : Structure
- 5 angles (Haut, Bas, Face, Profil droit, Hairline)
- Maintient la consistance avec Phase 1
- **Nécessite l'image Phase 1 en référence**

### Phase 3 : Dynamics
- 5 émotions (Joie, Intensité, Sérénité, Sceptique, Surprise)
- Expressions faciales variées
- **Nécessite l'image Phase 2 en référence**

---

## 💡 AVANTAGES DE L'ARCHITECTURE MODULAIRE

✅ **Maintenabilité** : Chaque module a une responsabilité claire  
✅ **Réutilisabilité** : `core_engine.py` peut être importé dans d'autres scripts  
✅ **Évolutivité** : Facile d'ajouter de nouvelles nationalités dans `data_bank.py`  
✅ **Sécurité** : La clé API est isolée dans `config.py`  
✅ **Clarté** : Code plus lisible et organisé  

---

## 🔐 SÉCURITÉ

⚠️ **IMPORTANT** : Ne jamais commit `config.py` sur GitHub !

Créer un `.gitignore` :
```
config.py
*.png
*.jpg
__pycache__/
```

---

## 📊 COMPARAISON AVANT/APRÈS

| Aspect | Avant (V15) | Après (V16) |
|--------|-------------|-------------|
| **Fichiers** | 1 monolithe (346 lignes) | 4 modules (~250 lignes total) |
| **Résolution** | 1K fixe | 1K/2K/4K au choix |
| **Organisation** | Tout mélangé | Séparation claire |
| **Réutilisabilité** | Difficile | Facile (import modules) |
| **Évolutivité** | Complexe | Simple |

---

## 🎓 CONCLUSION

### ✅ MISSION ACCOMPLIE

1. **Architecture Pro** : Code modulaire et maintenable
2. **Résolution 2K/4K** : Support natif confirmé (pas d'upscaling nécessaire)
3. **Consistance** : Système de phases préservé
4. **Casting Automatique** : Fonctionnalité intacte

### 🚀 PROCHAINES ÉTAPES POSSIBLES

- Ajouter un système de sauvegarde de profils (JSON)
- Créer une interface web (Streamlit/Gradio)
- Implémenter un batch mode (générer plusieurs variantes)
- Ajouter un système de notation des résultats

---

**Créé le** : 20 Janvier 2026  
**Version** : 16.0 (Modular + 2K/4K)  
**Modèle** : gemini-3-pro-image-preview
