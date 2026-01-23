# 🎬 Système 3 Phases - Documentation Complète

**Version:** 18.0  
**Date:** 20 Janvier 2026  
**Statut:** ✅ Production Ready

---

## 🎯 Concept Core

Le système de Casting ne génère pas "juste une image". Il suit un **processus chronologique en 3 phases interconnectées** pour créer un personnage cohérent et détaillé.

---

## 📋 Les 3 Phases

### PHASE 1: Foundation (Triptych)
**Objectif:** Établir l'ADN facial de base

**Output:** 3 vues horizontales
- **Frame 1:** Profil gauche strict (90°)
- **Frame 2:** Face frontale neutre
- **Frame 3:** Vue 3/4 droite (45°)

**Caractéristiques:**
- Pas de référence nécessaire
- Utilise le DNA complet du personnage
- Prompt chargé depuis `core/prompts_templates/PHASE 1.txt`
- Tags remplacés: `[AGE]`, `[INSERER FORME DU VISAGE]`, etc.

### PHASE 2: Structure (5 Angles Techniques)
**Objectif:** Explorer les angles et la structure osseuse

**Input:** Image Phase 1 comme référence
**Output:** 5 vues horizontales
- **Frame 1:** Plongée (high angle)
- **Frame 2:** Contre-plongée (low angle)
- **Frame 3:** Frontal recall (identique à Phase 1 centre)
- **Frame 4:** Profil droit (90°)
- **Frame 5:** Vue couronne/hairline

**Caractéristiques:**
- **NÉCESSITE** Phase 1 comme référence
- Maintient 100% d'identité faciale
- Prompt depuis `core/prompts_templates/PHASE 2.txt`

### PHASE 3: Dynamics (5 Émotions)
**Objectif:** Capturer la gamme émotionnelle

**Input:** Image Phase 1 OU Phase 2 comme référence
**Output:** 5 vues horizontales
- **Frame 1:** Joie (sourire large)
- **Frame 2:** Intensité (regard fierce)
- **Frame 3:** Sérénité (yeux fermés)
- **Frame 4:** Scepticisme (sourcil levé, smirk)
- **Frame 5:** Surprise (bouche ouverte, yeux larges)

**Caractéristiques:**
- **NÉCESSITE** Phase 1 ou 2 comme référence
- Seules les expressions changent, pas la structure
- Prompt depuis `core/prompts_templates/PHASE 3.txt`

---

## 🧬 Éditeur d'ADN (Sidebar)

### Fonctionnalités

**Bouton "🎲 GÉNÉRER PROFIL RANDOM"**
- Tire aléatoirement tous les traits depuis les banques de données
- Remplit instantanément tous les champs
- Peut être cliqué plusieurs fois pour régénérer

**Champs Éditables:**
- **Âge** (18-35 ans, number input)
- **Nationalité** (selectbox avec 9 options)
- **Forme du Visage** (selectbox avec 5 options)
- **Yeux** (selectbox avec 6 options incluant hétérochromie)
- **Cheveux** (selectbox avec 6 options)
- **Nez/Lèvres** (selectbox avec 5 options)
- **Signes Distinctifs** (selectbox avec 7 options)

**Workflow:**
1. Clique "Générer Random" → Tous les champs se remplissent
2. Modifie manuellement n'importe quel champ (ex: change "Blonde" → "Rousse")
3. Les valeurs finales sont utilisées pour générer les prompts

---

## 📁 Gestion des Prompts (Fichiers Externes)

### Emplacement
```
core/prompts_templates/
├── PHASE 1.txt
├── PHASE 2.txt
└── PHASE 3.txt
```

### Système de Tags

**PHASE 1.txt contient:**
```
[AGE]
[INSERER FORME DU VISAGE]
[INSERER COULEUR ET FORME DES YEUX]
[INSERER COULEUR, LONGUEUR, TEXTURE, STYLE DE COIFFURE]
[INSERER DETAILS NEZ ET LEVRES]
[TRES IMPORTANT : INSERER GRAINS DE BEAUTE, TACHES DE ROUSSEUR, CICATRICES - SOIS PRECIS SUR LEUR POSITION]
```

**Remplacement Automatique:**
```python
character.build_prompt("1")
# Remplace tous les tags par les valeurs DNA
# Retourne le prompt complet prêt pour Gemini
```

**PHASE 2 et 3:**
- Pas de tags à remplacer
- Utilisent directement le template
- La référence image assure la cohérence

---

## 🎨 Interface Streamlit

### Page Casting

**Colonne Gauche:**
- 3 sections verticales (Phase 1, 2, 3)
- Chaque phase a son bouton "LANCER"
- Phase 2/3 désactivées si Phase 1 pas générée
- Phase 3 permet de choisir ref (Phase 1 ou 2)

**Colonne Droite:**
- Affichage des résultats
- Images empilées verticalement
- Phase 1 en haut, puis 2, puis 3
- Captions avec noms de fichiers

**Sidebar (Menu Latéral):**
- Section "🧬 ÉDITEUR D'ADN"
- Bouton "Générer Random"
- 7 champs éditables
- Mise à jour en temps réel

---

## 🔧 Architecture Technique

### Fichiers Modifiés/Créés

**Core:**
- ✅ `core/character_bank.py` - Réécrit complètement
  - Classe `Character` avec méthodes `build_prompt()`, `set_dna()`, `get_dna_field()`
  - Banques de données (BANK_NATIONALITY, BANK_EYES, etc.)
  - Fonctions helper pour Streamlit selectbox

- ✅ `core/prompts_templates/` - Nouveau dossier
  - PHASE 1.txt, PHASE 2.txt, PHASE 3.txt
  - Copiés depuis `IMAGES/Reference image for FaceSwapping/`

- ✅ `core/config.py` - UTF-8 encoding fixé
  - `load_dotenv(encoding='utf-8')`

**Dashboard:**
- ✅ `studio_dashboard.py` - Réécrit complètement
  - Sidebar avec éditeur DNA
  - Page Casting avec 3 phases
  - Session state pour phase1_image, phase2_image, phase3_image
  - Workflow référence image automatique

**Nettoyage:**
- ✅ `_TRASH/` - Dossier créé
  - Vieux scripts déplacés (gemini_studio.py, face_swap.py, etc.)
  - Garde la racine propre

---

## 🚀 Workflow Utilisateur

### Session Complète

**1. Ouvrir Dashboard**
```bash
streamlit run studio_dashboard.py
```

**2. Aller sur Page "Casting"**
- Sidebar s'affiche automatiquement

**3. Générer DNA**
- Clique "🎲 GÉNÉRER PROFIL RANDOM"
- Modifie manuellement si besoin (ex: change cheveux)

**4. Phase 1**
- Clique "🚀 LANCER PHASE 1"
- Attends ~30 secondes
- Image Triptych s'affiche à droite

**5. Phase 2**
- Clique "🚀 LANCER PHASE 2"
- Utilise automatiquement Phase 1 comme référence
- Image 5 angles s'affiche

**6. Phase 3**
- Choisis référence (Phase 1 ou 2)
- Clique "🚀 LANCER PHASE 3"
- Image 5 émotions s'affiche

**7. Résultat**
- 3 images générées
- Toutes sauvegardées dans `IMAGES/GENERATED/`
- Prêtes pour face swap ou dataset

---

## 📊 Avantages du Système

### Cohérence
- ✅ Même personnage sur les 3 phases
- ✅ DNA fixé dès le début
- ✅ Référence image assure l'identité

### Flexibilité
- ✅ Édition manuelle de chaque trait
- ✅ Génération random rapide
- ✅ Choix de référence pour Phase 3

### Qualité
- ✅ Prompts professionnels externes
- ✅ Pas de hard-coding
- ✅ Facile à modifier les templates

### UX
- ✅ Interface visuelle claire
- ✅ Workflow guidé
- ✅ Feedback immédiat

---

## 🔍 Différences vs Ancien Système

### Ancien (Simplifié)
```
- 1 bouton "Générer"
- Prompt dans le code Python
- Pas d'édition DNA
- Pas de phases
```

### Nouveau (3 Phases)
```
- 3 boutons distincts (Phase 1, 2, 3)
- Prompts dans fichiers externes .txt
- Éditeur DNA complet dans sidebar
- Workflow chronologique avec références
```

---

## 🎓 Cas d'Usage

### Génération Simple
1. Random DNA
2. Phase 1 uniquement
3. Utilise pour face swap

### Génération Complète
1. Random DNA + édition manuelle
2. Phase 1 → Phase 2 → Phase 3
3. 3 planches différentes du même personnage

### Dataset LoRa
1. Phase 1 pour visage source
2. Scraper Instagram
3. Face swap batch
4. Dataset final

---

## 📝 Notes Importantes

### Prompts Templates
- **Ne pas modifier** les tags dans les .txt
- **Garder** l'encodage UTF-8
- **Respecter** le format exact

### DNA Fields
- **Toujours** remplir tous les champs avant Phase 1
- **Utiliser** les descriptions anglaises (pour Gemini)
- **Modifier** librement après génération random

### Références Images
- **Phase 2** nécessite absolument Phase 1
- **Phase 3** peut utiliser Phase 1 OU 2
- **Pas de référence** pour Phase 1

---

## 🐛 Dépannage

### "Template not found"
- Vérifie que `core/prompts_templates/` existe
- Vérifie les 3 fichiers .txt sont présents

### "Complétez l'ADN d'abord"
- Remplis tous les champs dans la sidebar
- Ou clique "Générer Random"

### Phase 2/3 ne se lance pas
- Génère Phase 1 d'abord
- Vérifie que l'image Phase 1 existe

### Erreur UTF-8
- Vérifie `.env` avec encoding UTF-8
- Vérifie `core/config.py` a `load_dotenv(encoding='utf-8')`

---

**Créé le:** 20 Janvier 2026  
**Version:** 18.0  
**Système:** 3-Phase Casting avec Prompts Externes  
**Statut:** Production Ready
