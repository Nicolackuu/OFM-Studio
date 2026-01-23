# 🎨 Studio Dashboard - Guide d'Utilisation

**Interface Web Moderne pour OFM IA Studio**

---

## 🚀 Lancement

```bash
streamlit run studio_dashboard.py
```

Le dashboard s'ouvrira automatiquement dans votre navigateur à l'adresse: `http://localhost:8501`

---

## 📱 Interface Principale

### Barre Latérale (Sidebar)

**API Status:**
- ✅ Google Gemini: Vérifie si la clé API est configurée
- ✅ Instagram: Vérifie si la session est active

**Session Info:**
- Affiche l'état du character actuel
- Affiche la source face sélectionnée
- Affiche le dataset en cours

**Navigation:**
- 🏠 Accueil
- 🧬 Casting (Gemini)
- 📸 Scraper Insta
- 🏭 Usine Dataset

---

## 📄 Pages du Dashboard

### 🏠 Page Accueil

**Statistiques en Temps Réel:**
- Images Générées (total)
- Dataset LoRa (images finales)
- Images Approuvées (en attente de face swap)
- Statut Système

**Workflow Rapide:**
- Guide visuel pour génération simple
- Guide visuel pour production dataset LoRa
- Aperçu des dernières générations

---

### 🧬 Page Casting (Gemini)

#### Section Génération

**Bouton "Générer Profil Random":**
- Crée un personnage aléatoire complet
- Affiche tous les traits DNA (nationalité, yeux, cheveux, etc.)
- Carte visuelle avec gradient coloré

**Configuration Phase 1:**
- Sélecteur de résolution: 1K, 2K, 4K
- Sélecteur d'aspect ratio: 3:2, 16:9, 1:1, 3:4

**Bouton "Lancer Phase 1":**
- Génère l'image avec Gemini API
- Barre de progression visuelle
- Affiche l'image immédiatement après génération
- Définit automatiquement comme source face

#### Section Résultat

**Affichage Image:**
- Aperçu grand format de l'image générée
- Informations: nom fichier, taille, résolution
- Bouton pour définir comme source face

---

### 📸 Page Scraper Insta

#### Section Configuration

**Champs de Saisie:**
- Nom d'utilisateur Instagram (sans @)
- Checkbox "Inclure Carousels" (par défaut: OUI)
- Checkbox "Ignorer Vidéos" (par défaut: OUI)
- Slider pour limite de posts (10-100)

**Info Box:**
- Résumé du mode actif
- Paramètres sélectionnés

**Bouton "Lancer le Téléchargement":**
- Télécharge les photos du compte
- Barre de progression
- Statistiques détaillées après téléchargement

#### Section Images Téléchargées

**Galerie:**
- Affichage en grille (3 colonnes)
- Slider pour nombre d'images à afficher
- Aperçu des images téléchargées

**Statistiques:**
- Posts traités
- Photos téléchargées
- Carousels trouvés
- Vidéos ignorées

---

### 🏭 Page Usine Dataset

#### Onglet 1: Source Face

**Option A: Images Générées**
- Liste déroulante des 20 images les plus récentes
- Sélection facile
- Bouton "Définir comme Source Face"

**Aperçu:**
- Affichage de la source face sélectionnée
- Informations du fichier

#### Onglet 2: Curation

**Système de Curation Visuel:**
- Grille d'images (4 colonnes)
- Checkbox sous chaque image: "Garder pour LoRa"
- Sélection multiple intuitive

**Compteur:**
- Nombre d'images sélectionnées en temps réel

**Bouton "Valider la Sélection":**
- Copie les images sélectionnées vers APPROVED
- Animation de succès
- Préparation pour face swap

#### Onglet 3: Production

**Info Box:**
- Source face utilisée
- Nombre d'images à traiter
- Temps estimé

**Bouton "LANCER LE FACE SWAP DE MASSE":**
- Traitement batch automatique
- Barre de progression en temps réel
- Affichage du fichier en cours
- Statistiques finales (succès/échecs/taux)

**Galerie Finale:**
- Affichage des 12 premières images du dataset final
- Grille 4 colonnes
- Aperçu rapide des résultats

---

## 🎨 Design & UX

### Thème Sombre
- Fond: `#0e1117`
- Cartes: `#1a1d29`
- Accents: Bleu `#1f77b4`

### Composants Visuels

**Boutons:**
- Largeur 100%
- Hover effect avec scale
- Couleurs primaires pour actions importantes

**Cartes:**
- Character Card: Gradient violet
- Success Box: Vert avec bordure gauche
- Error Box: Rouge avec bordure gauche
- Info Box: Bleu avec bordure gauche
- Stat Card: Fond sombre avec bordure

**Animations:**
- Balloons lors des succès
- Progress bars animées
- Transitions fluides

---

## 💡 Workflow Recommandé

### Génération Simple (5-10 min)

1. **Accueil** → Vérifier les stats
2. **Casting** → Générer profil random
3. **Casting** → Lancer Phase 1
4. **Résultat** → Image affichée immédiatement

### Production Dataset LoRa (1-2h)

1. **Casting** → Générer ou choisir source face
2. **Scraper** → Télécharger photos Instagram
   - Entrer username
   - Configurer options
   - Lancer téléchargement
3. **Usine → Source Face** → Sélectionner visage
4. **Usine → Curation** → Cocher images à garder
   - Sélectionner 20-40 meilleures images
   - Valider sélection
5. **Usine → Production** → Lancer face swap
   - Attendre traitement
   - Voir galerie finale

---

## 🔧 Fonctionnalités Techniques

### Session State
- Persistance des données entre les pages
- Character DNA sauvegardé
- Source face mémorisée
- Images scrappées en cache

### Gestion d'Erreurs
- Vérification API keys
- Messages d'erreur clairs
- Fallbacks visuels

### Performance
- Lazy loading des images
- Limitation d'affichage (évite surcharge)
- Progress bars pour feedback utilisateur

---

## 🎯 Raccourcis Clavier

**Navigation:**
- Utilise les onglets du navigateur normalement
- Sidebar toujours accessible

**Streamlit:**
- `R` → Rerun l'application
- `C` → Clear cache

---

## 📊 Indicateurs Visuels

### Statut API
- ✅ OK → Vert
- ❌ Missing → Rouge

### Session Info
- ✓ → Élément chargé (vert)
- ○ → Élément manquant (bleu)

### Progress Bars
- Bleu: En cours
- Vert: Succès

---

## 🐛 Dépannage

### Dashboard ne se lance pas
```bash
# Installer Streamlit
pip install streamlit pillow

# Relancer
streamlit run studio_dashboard.py
```

### Images ne s'affichent pas
- Vérifier que les chemins existent
- Vérifier les permissions de lecture
- Recharger la page (R)

### API errors
- Vérifier `.env` configuré
- Vérifier clés API valides
- Voir logs dans terminal

### Lenteur
- Limiter nombre d'images affichées
- Clear cache Streamlit
- Redémarrer le dashboard

---

## 🚀 Avantages vs Terminal

### Interface Graphique
✅ Visualisation immédiate des images
✅ Curation visuelle (vs texte)
✅ Progress bars visuelles
✅ Statistiques en temps réel
✅ Navigation intuitive
✅ Pas de commandes à taper

### Terminal
✅ Plus rapide pour experts
✅ Scriptable/automatisable
✅ Moins de ressources

**Recommandation:** Dashboard pour workflow interactif, terminal pour batch/automation.

---

## 📝 Prochaines Améliorations Possibles

- [ ] Upload d'images custom pour source face
- [ ] Édition manuelle du DNA character
- [ ] Historique des générations
- [ ] Export dataset en ZIP
- [ ] Comparaison avant/après face swap
- [ ] Mode batch pour plusieurs comptes Instagram
- [ ] Intégration training LoRa direct
- [ ] Système de tags pour images

---

## 🎓 Tips & Tricks

1. **Utilise les onglets** pour workflow séquentiel
2. **Vérifie la sidebar** pour état session
3. **Limite l'affichage** si beaucoup d'images
4. **Sauvegarde régulièrement** la source face
5. **Clear cache** si comportement étrange

---

**Créé le:** 20 Janvier 2026  
**Version:** 1.0  
**Framework:** Streamlit 1.30+  
**Statut:** Production Ready

---

## 🎬 Démo Rapide

```bash
# 1. Installer dépendances
pip install -r requirements.txt

# 2. Configurer .env
# Ajouter GOOGLE_API_KEY et INSTAGRAM_SESSION_ID

# 3. Lancer dashboard
streamlit run studio_dashboard.py

# 4. Ouvrir navigateur
# http://localhost:8501

# 5. Enjoy! 🎉
```
