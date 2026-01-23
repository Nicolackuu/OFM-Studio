# 🏭 Dataset Factory - Guide Complet

**Chaîne de production automatisée pour créer des datasets LoRa de 20-40 photos**

---

## 🎯 Objectif

Créer un dataset de haute qualité pour entraîner un modèle LoRa avec un visage spécifique appliqué sur différentes poses/vêtements.

---

## 🔄 Workflow Complet

```
┌─────────────────────────────────────────────────────────────┐
│  MODULE 1: SOURCE FACE                                      │
│  ├─ Option A: Générer nouveau visage (Gemini Phase 1)      │
│  └─ Option B: Choisir image existante                      │
└─────────────────────────────────────────────────────────────┘
                            ↓
┌─────────────────────────────────────────────────────────────┐
│  MODULE 2: INSTAGRAM SCRAPER                                │
│  ├─ Télécharge PHOTOS uniquement                           │
│  ├─ Récupère TOUTES les images des carousels               │
│  └─ Ignore vidéos et Reels                                 │
└─────────────────────────────────────────────────────────────┘
                            ↓
┌─────────────────────────────────────────────────────────────┐
│  MODULE 3: CURATION                                         │
│  ├─ Review image par image                                 │
│  ├─ Approve (garde) / Reject (supprime) / Skip             │
│  └─ Ne garde que les photos nettes avec corps visible      │
└─────────────────────────────────────────────────────────────┘
                            ↓
┌─────────────────────────────────────────────────────────────┐
│  MODULE 4: BATCH FACE SWAP                                  │
│  ├─ Applique le visage source sur TOUTES les images        │
│  ├─ Traitement automatique avec barre de progression       │
│  └─ Sauvegarde haute qualité (2K)                          │
└─────────────────────────────────────────────────────────────┘
                            ↓
                    DATASET FINAL
              (DATASET/FINAL_LORA/)
```

---

## 🚀 Lancement

```bash
python dataset_factory.py
```

---

## 📖 Guide Module par Module

### MODULE 1: Source Face Selection

**Objectif:** Choisir le visage qui sera appliqué sur toutes les images du dataset.

#### Option A: Générer Nouveau Visage
1. Sélectionne `[A]` dans le menu
2. Un personnage aléatoire est généré (DNA complet)
3. Confirme la génération
4. Phase 1 est créée automatiquement (3 angles)
5. L'image générée devient la source face

**Avantages:**
- Visage unique et cohérent
- Contrôle total sur les caractéristiques
- Haute qualité garantie

#### Option B: Choisir Image Existante
1. Sélectionne `[B]` dans le menu
2. Liste des 20 images les plus récentes dans `IMAGES/GENERATED`
3. Entre le numéro de l'image désirée
4. L'image sélectionnée devient la source face

**Avantages:**
- Réutilise un visage déjà généré
- Plus rapide
- Peut utiliser des visages de sessions précédentes

---

### MODULE 2: Instagram Scraper

**Objectif:** Télécharger des photos de qualité depuis Instagram pour servir de base au dataset.

#### Configuration
- **Mode:** PHOTOS UNIQUEMENT
- **Carousels:** TOUTES les images sont téléchargées
- **Vidéos:** Ignorées automatiquement
- **Reels:** Ignorés automatiquement

#### Processus
1. Entre le nom d'utilisateur Instagram (sans @)
2. Définis la limite de posts (20-50 recommandé)
3. Le scraper télécharge automatiquement
4. Statistiques affichées en temps réel

#### Règle d'Or: CAROUSELS
**CRITIQUE:** Le script télécharge **TOUTES** les images d'un carousel/album, pas seulement la première.

**Exemple:**
- Post carousel avec 5 photos → 5 images téléchargées
- Post simple avec 1 photo → 1 image téléchargée
- Post vidéo → ignoré

#### Stockage
```
DATASET/
└── RAW/
    └── {username}/
        ├── image_001.jpg
        ├── image_002.jpg
        └── ...
```

#### Statistiques Affichées
- Posts traités
- Photos téléchargées
- Carousels trouvés
- Vidéos ignorées
- Erreurs

---

### MODULE 3: Dataset Curation

**Objectif:** Trier rapidement les images pour ne garder que les meilleures.

#### Critères de Sélection
✅ **APPROVE (Garder):**
- Photo nette et claire
- Corps bien visible
- Bonne pose
- Éclairage correct
- Vêtements variés

❌ **REJECT (Supprimer):**
- Photo floue
- Corps coupé ou caché
- Mauvaise qualité
- Visage trop petit
- Pose inadaptée

⊘ **SKIP (Garder en RAW):**
- Incertain
- Peut-être utile plus tard
- Reste dans RAW mais pas approuvé

#### Contrôles
```
[Enter] ou [O] = APPROVE (Copie vers APPROVED)
[X] ou [N]     = REJECT (Supprime définitivement)
[S]            = SKIP (Garde en RAW)
[Q]            = QUIT (Quitte la curation)
```

#### Processus
1. Chaque image s'ouvre automatiquement
2. Tu décides: Approve / Reject / Skip
3. Statistiques en temps réel
4. Progression affichée

#### Stockage
```
DATASET/
├── RAW/
│   └── {username}/          (Images originales)
└── APPROVED/
    ├── dataset_001.jpg      (Images approuvées)
    ├── dataset_002.jpg
    └── ...
```

#### Recommandations
- **Objectif:** 20-40 images approuvées
- **Qualité > Quantité:** Mieux vaut 20 excellentes que 50 moyennes
- **Variété:** Différentes poses, angles, vêtements
- **Corps visible:** Important pour le face swap

---

### MODULE 4: Batch Face Swap

**Objectif:** Appliquer automatiquement le visage source sur toutes les images approuvées.

#### Configuration
- **Résolution:** 2K (haute qualité)
- **Aspect Ratio:** 3:2 (optimal pour portraits)
- **Température:** 0.7 (équilibre créativité/cohérence)

#### Processus
1. Charge le visage source
2. Pour chaque image approuvée:
   - Charge l'image cible
   - Envoie à Gemini API
   - Applique le face swap
   - Sauvegarde en haute qualité
3. Barre de progression en temps réel
4. Statistiques finales

#### Prompt Utilisé
Le système utilise un prompt optimisé pour:
- Transférer 100% du visage source
- Garder 100% du corps/pose cible
- Blend naturel et seamless
- Préserver l'éclairage
- Haute qualité photorealistic

#### Stockage Final
```
DATASET/
└── FINAL_LORA/
    ├── lora_001_image_001.png
    ├── lora_002_image_002.png
    ├── lora_003_image_003.png
    └── ...
```

#### Temps Estimé
- ~30 secondes par image
- 20 images = ~10 minutes
- 40 images = ~20 minutes

#### Barre de Progression
```
Processing: image_005.jpg
Progress: [████████████░░░░░░░░] 60.0% (12/20)
Success: 11 | Failed: 1
```

---

## 📊 Structure des Dossiers

```
DATASET/
├── RAW/                      # Images brutes téléchargées
│   └── {username}/
│       ├── image_001.jpg
│       └── ...
│
├── APPROVED/                 # Images approuvées après curation
│   ├── dataset_001.jpg
│   ├── dataset_002.jpg
│   └── ...
│
└── FINAL_LORA/              # Dataset final avec face swap
    ├── lora_001_*.png
    ├── lora_002_*.png
    └── ...
```

---

## 💡 Conseils & Best Practices

### Choix du Compte Instagram
✅ **Bon choix:**
- Comptes de mode/fitness
- Photos variées et de qualité
- Beaucoup de carousels
- Corps bien visible
- Différentes poses

❌ **Mauvais choix:**
- Comptes avec beaucoup de vidéos
- Photos de groupe
- Selfies rapprochés
- Qualité médiocre

### Curation
- **Sois sélectif:** Qualité > Quantité
- **Variété:** Différents angles, poses, vêtements
- **Corps visible:** Essentiel pour le face swap
- **Netteté:** Photos floues = résultats médiocres

### Optimisation
- **20-30 images:** Optimal pour LoRa
- **40 images max:** Plus = pas forcément mieux
- **Diversité:** Évite les poses trop similaires

---

## 🔧 Dépannage

### "No images found to curate"
**Solution:** Vérifie que Module 2 a bien téléchargé des images dans `DATASET/RAW/{username}/`

### "Failed to generate source face"
**Solution:** 
- Vérifie ta clé API Google dans `.env`
- Réessaye la génération
- Ou utilise Option B (image existante)

### "Instagram authentication failed"
**Solution:**
- Vérifie `INSTAGRAM_SESSION_ID` dans `.env`
- Session ID expire après ~90 jours
- Récupère un nouveau session ID depuis ton navigateur

### Face swap échoue
**Solution:**
- Vérifie la qualité de l'image source
- Vérifie la qualité des images cibles
- Certaines poses peuvent être difficiles
- Réessaye avec d'autres images

### Carousels incomplets
**Solution:**
- Le script télécharge automatiquement toutes les slides
- Si problème, vérifie la connexion Instagram
- Réessaye le téléchargement

---

## 📈 Statistiques Typiques

### Exemple de Session Complète

**Module 2 (Scraper):**
- Posts traités: 30
- Photos téléchargées: 85 (grâce aux carousels)
- Carousels trouvés: 12
- Vidéos ignorées: 8

**Module 3 (Curation):**
- Images reviewées: 85
- Approuvées: 28
- Rejetées: 52
- Skippées: 5

**Module 4 (Face Swap):**
- Images traitées: 28
- Succès: 26
- Échecs: 2
- Taux de succès: 92.8%

**Résultat Final:** 26 images haute qualité pour LoRa

---

## 🎓 Workflow Recommandé

### Session Complète (1-2 heures)

1. **Préparation (5 min)**
   - Choisis le compte Instagram cible
   - Décide: nouveau visage ou existant

2. **Module 1 (5-10 min)**
   - Génère ou sélectionne le visage source
   - Vérifie la qualité

3. **Module 2 (10-15 min)**
   - Télécharge 30-50 posts
   - Attends la fin du scraping

4. **Module 3 (20-30 min)**
   - Review toutes les images
   - Sois sélectif: garde 20-40 meilleures

5. **Module 4 (15-30 min)**
   - Lance le batch face swap
   - Attends la fin du traitement

6. **Vérification (10 min)**
   - Review le dataset final
   - Supprime les éventuels ratés
   - Dataset prêt pour LoRa!

---

## 🚀 Prochaines Étapes

Une fois le dataset créé:

1. **Review Final**
   - Ouvre `DATASET/FINAL_LORA/`
   - Vérifie chaque image
   - Supprime les ratés éventuels

2. **Training LoRa**
   - Utilise les 20-40 images finales
   - Configure ton trainer LoRa
   - Lance l'entraînement

3. **Archivage**
   - Sauvegarde le dataset
   - Note les paramètres utilisés
   - Garde la source face

---

## 📝 Notes Techniques

### Modules Core Utilisés
- `core/config.py` - Configuration
- `core/utils.py` - Utilitaires
- `core/gemini_engine.py` - API Gemini
- `core/character_bank.py` - Génération personnages
- `core/dataset_scraper.py` - Scraping Instagram
- `core/dataset_curator.py` - Curation images
- `core/batch_face_swap.py` - Face swap batch

### API Utilisées
- **Google Gemini 3 Pro Image Preview** - Génération et face swap
- **Instaloader** - Scraping Instagram

### Formats Supportés
- **Input:** JPG, JPEG, PNG
- **Output:** PNG (haute qualité)

---

**Créé le:** 20 Janvier 2026  
**Version:** 1.0  
**Statut:** Production Ready
