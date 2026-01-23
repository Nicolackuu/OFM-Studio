import random
from pathlib import Path
from typing import Dict, List

# ============================================================================
# DATA BANKS - Character Traits
# ============================================================================

BANK_NATIONALITY = [
    {"fr": "Française (Naturelle)", "en": "French Parisian student, naturally stunning, effortless beauty, minimal makeup aesthetic"},
    {"fr": "Brésilienne (Solaire)", "en": "Brazilian model, golden tan skin, warm undertones, radiant healthy glow, exotic beauty"},
    {"fr": "Russe (Froide)", "en": "Russian elegant beauty, pale porcelain skin, high cheekbones, striking and intense look"},
    {"fr": "Japonaise (Moderne)", "en": "Japanese Tokyo fashionista, flawless skin texture, almond eyes, trendy and cute"},
    {"fr": "Italienne (Intense)", "en": "Italian brunette, olive skin tone, passionate gaze, thick eyebrows, mediterranean charm"},
    {"fr": "Scandinave (Ange)", "en": "Swedish angelic beauty, sun-bleached hair, light skin with pink undertones, ethereal"},
    {"fr": "Américaine (Girl Next Door)", "en": "American girl next door, athletic, healthy flush, bright smile, accessible beauty"},
    {"fr": "Espagnole (Voluptueuse)", "en": "Spanish beauty, sun-kissed skin, expressive features, dark intense eyes"},
    {"fr": "Métisse (Caramel)", "en": "Mixed race goddess, glowing caramel skin, unique striking features, perfect symmetry"}
]

BANK_FACE_SHAPE = [
    {"fr": "Ovale (Mâchoire définie)", "en": "Symmetrical oval face with a sharp, defined jawline and elegant chin"},
    {"fr": "Cœur (Pommettes hautes)", "en": "Heart-shaped face, high prominent cheekbones, narrowing to a delicate chin"},
    {"fr": "Diamant (Sculpté)", "en": "Diamond face shape, sculpted hollow cheeks, angular features, very photogenic"},
    {"fr": "Rond (Douceur)", "en": "Soft round face shape, full cheeks, youthful and fresh appearance"},
    {"fr": "Carré (Caractère)", "en": "Square face shape with a strong jawline, intense and striking look"}
]

BANK_EYES = [
    {"fr": "Bleu Glace (Limbe Foncé)", "en": "Piercing ice-blue eyes with a dark limbal ring, sharp almond shape, heavy lashes"},
    {"fr": "Vert Émeraude (Chat)", "en": "Vivid emerald green eyes, upturned cat-eye shape, seductive and intense"},
    {"fr": "Noisette Miel (Soleil)", "en": "Warm hazel eyes with golden honey flecks, large round shape, expressive"},
    {"fr": "Brun Noir (Profond)", "en": "Deep dark chocolate eyes, mysterious, soulful, slightly hooded eyelids"},
    {"fr": "Gris Orage (Rare)", "en": "Rare storm-grey eyes, changing with light, melancholic and beautiful"},
    {"fr": "Hétérochromie (Vairons)", "en": "Heterochromia (left eye blue, right eye hazel), extremely unique and hypnotic"}
]

BANK_HAIR = [
    {"fr": "Blond Miel (Wavy)", "en": "Honey blonde hair, long layers, loose natural beach waves, slightly messy texture"},
    {"fr": "Brun Chocolat (Lisse)", "en": "Rich dark chocolate brown hair, waist length, silky straight with a middle part"},
    {"fr": "Roux Cuivré (Naturel)", "en": "Natural copper red hair, voluminous, soft curls catching the light"},
    {"fr": "Noir Jais (Carré)", "en": "Jet black hair, sharp bob cut (chin length), glossy and sleek texture"},
    {"fr": "Châtain Cendré (Balayage)", "en": "Ash brown hair with subtle blonde highlights (balayage), messy bun style with loose strands"},
    {"fr": "Blond Platine (Long)", "en": "Platinum blonde hair, extremely long, straight with curtain bangs framing the face"}
]

BANK_NOSE_LIPS = [
    {"fr": "Nez Fin / Lèvres Pulpeuses", "en": "Small straight button nose and naturally full, plush lips (cupid's bow defined)"},
    {"fr": "Nez Grec / Lèvres Douces", "en": "Elegant straight Grecian nose and soft, balanced rosebud lips"},
    {"fr": "Nez Mignon / Lèvres Larges", "en": "Slightly upturned cute nose and wide smile, prominent lower lip"},
    {"fr": "Nez Aquilin / Bouche Boudeuse", "en": "Slightly aquiline aristocratic nose and pouty, voluminous lips"},
    {"fr": "Nez Naturel / Lèvres Fines", "en": "Natural nose with a slight bump (character) and defined, elegant lips"}
]

BANK_DISTINCTIVE_FEATURES = [
    {"fr": "Grain de beauté sous l'œil gauche", "en": "Small beauty mark under the left eye, light freckles across the nose bridge"},
    {"fr": "Taches de rousseur dorées", "en": "Golden freckles scattered across cheeks and nose, sun-kissed look"},
    {"fr": "Cicatrice fine sourcil droit", "en": "Thin scar through right eyebrow, adds character and edge"},
    {"fr": "Fossette joue gauche", "en": "Deep dimple on left cheek when smiling, asymmetrical charm"},
    {"fr": "Peau parfaite (aucun défaut)", "en": "Flawless porcelain skin, no visible marks or imperfections"},
    {"fr": "Tache de naissance cou", "en": "Small birthmark on the side of neck, barely visible"},
    {"fr": "Grains de beauté multiples", "en": "Several small beauty marks scattered on face, like constellations"}
]

# ============================================================================
# Character Class
# ============================================================================

class Character:
    def __init__(self):
        self.dna = {
            'AGE': '22',
            'NATIONALITE': '',
            'FACE_SHAPE': '',
            'EYES': '',
            'HAIR': '',
            'NOSE_LIPS': '',
            'DISTINCTIVE_FEATURES': ''
        }
        self.prompts_dir = Path(__file__).parent / 'prompts_templates'
    
    def generate_random(self):
        """Generate random DNA from data bank"""
        nat = random.choice(BANK_NATIONALITY)
        face = random.choice(BANK_FACE_SHAPE)
        eyes = random.choice(BANK_EYES)
        hair = random.choice(BANK_HAIR)
        nose_lips = random.choice(BANK_NOSE_LIPS)
        features = random.choice(BANK_DISTINCTIVE_FEATURES)
        
        self.dna = {
            'AGE': str(random.randint(20, 28)),
            'NATIONALITE': nat['en'],
            'FACE_SHAPE': face['en'],
            'EYES': eyes['en'],
            'HAIR': hair['en'],
            'NOSE_LIPS': nose_lips['en'],
            'DISTINCTIVE_FEATURES': features['en']
        }
    
    def set_dna(self, field: str, value: str):
        """Manually set a DNA field"""
        if field in self.dna:
            self.dna[field] = value
    
    def get_dna_field(self, field: str) -> str:
        """Get a DNA field value"""
        return self.dna.get(field, '')
    
    def get_prompt_template(self, phase: str) -> str:
        """Load prompt template from file"""
        template_file = self.prompts_dir / f"PHASE {phase}.txt"
        
        if not template_file.exists():
            raise FileNotFoundError(f"Template not found: {template_file}")
        
        with open(template_file, 'r', encoding='utf-8') as f:
            return f.read()
    
    def build_prompt(self, phase: str) -> str:
        """Build prompt by replacing tags in template with DNA values"""
        template = self.get_prompt_template(phase)
        
        # For Phase 1, replace all tags
        if phase == "1":
            replacements = {
                '[AGE]': self.dna['AGE'],
                '[INSERER FORME DU VISAGE]': self.dna['FACE_SHAPE'],
                '[INSERER COULEUR ET FORME DES YEUX]': self.dna['EYES'],
                '[INSERER COULEUR, LONGUEUR, TEXTURE, STYLE DE COIFFURE]': self.dna['HAIR'],
                '[INSERER DETAILS NEZ ET LEVRES]': self.dna['NOSE_LIPS'],
                '[TRES IMPORTANT : INSERER GRAINS DE BEAUTE, TACHES DE ROUSSEUR, CICATRICES - SOIS PRECIS SUR LEUR POSITION]': self.dna['DISTINCTIVE_FEATURES']
            }
            
            prompt = template
            for tag, value in replacements.items():
                prompt = prompt.replace(tag, value)
            
            return prompt
        
        # For Phase 2 and 3, no replacements needed (they use reference image)
        return template
    
    def display(self):
        """Display DNA in console"""
        print(f"\n{'=' * 60}")
        print(f"  CHARACTER DNA")
        print(f"{'=' * 60}")
        print(f"Âge: {self.dna['AGE']} ans")
        print(f"Nationalité: {self.dna['NATIONALITE']}")
        print(f"Forme du visage: {self.dna['FACE_SHAPE']}")
        print(f"Yeux: {self.dna['EYES']}")
        print(f"Cheveux: {self.dna['HAIR']}")
        print(f"Nez/Lèvres: {self.dna['NOSE_LIPS']}")
        print(f"Signes distinctifs: {self.dna['DISTINCTIVE_FEATURES']}")
        print(f"{'=' * 60}\n")
    
    def is_complete(self) -> bool:
        """Check if all DNA fields are filled"""
        return all(value != '' for value in self.dna.values())

# ============================================================================
# Helper Functions
# ============================================================================

def get_all_nationalities() -> List[str]:
    """Get list of all nationalities (English descriptions)"""
    return [item['en'] for item in BANK_NATIONALITY]

def get_all_face_shapes() -> List[str]:
    """Get list of all face shapes (English descriptions)"""
    return [item['en'] for item in BANK_FACE_SHAPE]

def get_all_eyes() -> List[str]:
    """Get list of all eye types (English descriptions)"""
    return [item['en'] for item in BANK_EYES]

def get_all_hair() -> List[str]:
    """Get list of all hair types (English descriptions)"""
    return [item['en'] for item in BANK_HAIR]

def get_all_nose_lips() -> List[str]:
    """Get list of all nose/lips types (English descriptions)"""
    return [item['en'] for item in BANK_NOSE_LIPS]

def get_all_distinctive_features() -> List[str]:
    """Get list of all distinctive features (English descriptions)"""
    return [item['en'] for item in BANK_DISTINCTIVE_FEATURES]
