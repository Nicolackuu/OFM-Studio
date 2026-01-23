# 🎭 InsightFace Setup Guide - Face Swapping pour LoRa

**Technologie de Face Swap Professionnelle**

---

## 🎯 Pourquoi InsightFace ?

### ❌ Ancien Système (Gemini Text-to-Image)
- Génération depuis zéro avec prompt texte
- Pas de contrôle précis sur le visage
- Qualité variable
- Lent et coûteux (API calls)

### ✅ Nouveau Système (InsightFace Image-to-Image)
- **Vrai face swap** : Transfert précis du visage source
- **Préservation du corps** : Garde 100% de la pose/vêtements
- **Qualité maximale** : Pas de compression pour LoRa
- **Local & Rapide** : Traitement sur ton PC
- **Gratuit** : Pas d'API externe

---

## 📦 Installation

### Méthode Automatique
```bash
pip install -r requirements.txt
```

### Méthode Manuelle
```bash
pip install insightface onnxruntime opencv-python numpy
```

---

## 🔧 Fonctionnement Technique

### Architecture InsightFace

**1. Face Analysis (buffalo_l)**
- Détecte les visages dans les images
- Extrait les landmarks (points clés du visage)
- Analyse les caractéristiques faciales

**2. Face Swapper (inswapper_128.onnx)**
- Modèle ONNX pré-entraîné
- Swap précis des traits faciaux
- Blend naturel avec l'image cible

### Workflow

```
SOURCE IMAGE (ton visage généré)
    ↓
[Face Detection] → Extrait le visage source
    ↓
TARGET IMAGE (photo Instagram)
    ↓
[Face Detection] → Détecte le(s) visage(s) cible(s)
    ↓
[Face Swap] → Remplace chaque visage cible par le visage source
    ↓
[Paste Back] → Intègre le résultat dans l'image originale
    ↓
OUTPUT IMAGE (haute qualité, pas de compression)
```

---

## 🎨 Qualité pour LoRa

### Préservation Maximale

**Ce qui est TRANSFÉRÉ (depuis source):**
- ✅ Structure faciale complète
- ✅ Couleur des yeux
- ✅ Forme du nez et des lèvres
- ✅ Teint de peau
- ✅ Traits distinctifs

**Ce qui est PRÉSERVÉ (depuis target):**
- ✅ Corps et proportions
- ✅ Vêtements et accessoires
- ✅ Pose et positionnement
- ✅ Arrière-plan
- ✅ Éclairage et ombres
- ✅ Grain et texture de l'image

### Paramètres de Qualité

```python
# Détection haute résolution
det_size=(640, 640)

# Sauvegarde sans compression
cv2.IMWRITE_PNG_COMPRESSION = 0

# Résolution native préservée
# Pas de redimensionnement forcé
```

---

## 🚀 Utilisation

### Via Dashboard (Recommandé)
```bash
streamlit run studio_dashboard.py
```
1. Page "Usine Dataset"
2. Onglet "Source Face" → Sélectionne ton visage
3. Onglet "Curation" → Choisis les photos Instagram
4. Onglet "Production" → Lance le face swap

### Via Terminal
```bash
python dataset_factory.py
```
1. Module 1: Sélectionne source face
2. Module 2: Scrape Instagram
3. Module 3: Curation
4. Module 4: Batch face swap

---

## 📊 Performance

### Vitesse
- **CPU:** ~2-5 secondes par image
- **GPU (si disponible):** ~0.5-1 seconde par image

### Mémoire
- **RAM:** ~2-4 GB
- **Modèles:** ~500 MB (téléchargés au premier lancement)

### Premier Lancement
```
⚠️ Le premier lancement télécharge les modèles:
- buffalo_l (détection de visage)
- inswapper_128.onnx (face swap)

Temps: ~2-5 minutes selon connexion
Taille: ~500 MB
```

---

## 🔍 Détection de Visages

### Cas Multiples Visages
Si une photo contient plusieurs visages:
- **Tous les visages sont swappés** avec le visage source
- Utile pour photos de groupe
- Chaque visage est traité individuellement

### Cas Aucun Visage
Si aucun visage n'est détecté:
- L'image est **skippée** (pas d'erreur)
- Comptée comme "failed" dans les stats
- Message d'avertissement affiché

---

## 🛠️ Dépannage

### "No module named 'insightface'"
```bash
pip install insightface onnxruntime opencv-python
```

### "Failed to download model"
- Vérifie ta connexion internet
- Les modèles sont téléchargés depuis GitHub
- Réessaye, le téléchargement reprendra

### "No face detected in source image"
- Vérifie que l'image source contient un visage visible
- Le visage doit être de face ou 3/4
- Évite les profils extrêmes

### "CUDA not available"
- Normal si pas de GPU NVIDIA
- Le CPU fonctionne très bien
- Pour activer GPU: `pip install onnxruntime-gpu`

### Lenteur sur CPU
- Normal pour traitement local
- ~2-5 secondes par image acceptable
- Pour 30 images: ~2-3 minutes total

---

## 📈 Comparaison Avant/Après

### Ancien (Gemini Text-to-Image)
```
Input: Prompt texte + 2 images
Process: Génération complète depuis zéro
Output: Nouvelle image générée
Temps: ~30 secondes par image
Coût: API calls (payant)
Qualité: Variable, pas de contrôle précis
```

### Nouveau (InsightFace Image-to-Image)
```
Input: 2 images (source face + target body)
Process: Swap précis du visage uniquement
Output: Image target avec visage source
Temps: ~2-5 secondes par image
Coût: Gratuit (local)
Qualité: Maximale, contrôle total
```

---

## 🎓 Conseils pour LoRa

### Source Face Idéale
- ✅ Visage de face ou 3/4
- ✅ Bonne résolution (2K minimum)
- ✅ Éclairage uniforme
- ✅ Expression neutre ou légère

### Photos Instagram Idéales
- ✅ Corps bien visible
- ✅ Poses variées
- ✅ Vêtements différents
- ✅ Angles divers
- ✅ Résolution native (pas de crop)

### Dataset Final
- **Quantité:** 20-40 images
- **Qualité:** Haute résolution, pas de compression
- **Variété:** Différentes poses, angles, vêtements
- **Cohérence:** Même visage sur tous

---

## 🔐 Sécurité & Confidentialité

### Traitement Local
- ✅ Tout se passe sur ton PC
- ✅ Pas d'envoi de données externes
- ✅ Pas de tracking
- ✅ Gratuit et privé

### Modèles Open Source
- InsightFace: MIT License
- Modèles pré-entraînés publics
- Code source disponible

---

## 📝 Fichiers Modifiés

### Code Réécrit
- `core/batch_face_swap.py` - **Complètement réécrit**
  - Ancien: Gemini text-to-image
  - Nouveau: InsightFace image-to-image

### Dépendances Ajoutées
- `requirements.txt`
  - insightface>=0.7.3
  - onnxruntime>=1.16.0
  - opencv-python>=4.8.0
  - numpy>=1.24.0

---

## 🚀 Prochaines Étapes

1. **Installe les dépendances**
   ```bash
   pip install -r requirements.txt
   ```

2. **Lance le dashboard**
   ```bash
   streamlit run studio_dashboard.py
   ```

3. **Teste le face swap**
   - Génère un visage (Casting)
   - Scrape des photos (Scraper)
   - Lance le face swap (Usine Dataset)

4. **Vérifie les résultats**
   - Ouvre `DATASET/FINAL_LORA/`
   - Vérifie la qualité des swaps
   - Prêt pour training LoRa!

---

**Créé le:** 20 Janvier 2026  
**Version:** 2.0 (InsightFace)  
**Statut:** Production Ready  
**Technologie:** Image-to-Image Face Swapping
