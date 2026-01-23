"""
Casting Page - DNA Mixer Pro with Linear Design
French tags with multiselect, centralized interface
"""
import streamlit as st
from pathlib import Path
import shutil
import random
from core.dna_mixer import (
    DNAMixer,
    DNA_IDENTITE,
    DNA_VISAGE,
    DNA_YEUX,
    DNA_CHEVEUX,
    DNA_NEZ_LEVRES,
    DNA_SIGNES,
    DNA_STYLE
)
from core.gemini_engine import GeminiEngine
from core.config import Config
import time

# Banque de prénoms féminins (mélange Français/Anglais)
NAME_BANK = [
    'Léa', 'Chloé', 'Emma', 'Sarah', 'Jade', 'Luna', 'Olivia', 'Sophia', 'Mia', 'Amelia',
    'Isabella', 'Charlotte', 'Ava', 'Sophie', 'Manon', 'Camille', 'Alice', 'Rose', 'Grace', 'Lily',
    'Zoé', 'Inès', 'Louise', 'Juliette', 'Victoria', 'Eva', 'Gabrielle', 'Mathilde', 'Constance', 'Hélène',
    'Margaux', 'Clémence', 'Audrey', 'Jennifer', 'Laurence', 'Stéphanie', 'Nathalie', 'Catherine', 'Anne', 'Marie',
    'Laura', 'Marion', 'Céline', 'Vanessa', 'Aurélie', 'Caroline', 'Sabrina', 'Sandra', 'Brigitte', 'Monique'
]

def randomize_model():
    """Randomisation totale du modèle"""
    mixer = st.session_state.dna_mixer
    
    # Choisir un prénom au hasard
    random_name = random.choice(NAME_BANK)
    st.session_state.model_name = random_name
    
    # Sélectionner au hasard 1 à 3 origines dans DNA_IDENTITE
    identite_count = random.randint(1, 3)
    selected_identite = random.sample(DNA_IDENTITE, identite_count)
    mixer.selected_tags["identite"] = selected_identite
    
    # Sélectionner 1 à 2 formes dans DNA_VISAGE
    visage_count = random.randint(1, 2)
    selected_visage = random.sample(DNA_VISAGE, visage_count)
    mixer.selected_tags["visage"] = selected_visage
    
    # Sélectionner 1 à 2 types dans DNA_YEUX
    yeux_count = random.randint(1, 2)
    selected_yeux = random.sample(DNA_YEUX, yeux_count)
    mixer.selected_tags["yeux"] = selected_yeux
    
    # Sélectionner 1 à 2 styles dans DNA_CHEVEUX
    cheveux_count = random.randint(1, 2)
    selected_cheveux = random.sample(DNA_CHEVEUX, cheveux_count)
    mixer.selected_tags["cheveux"] = selected_cheveux
    
    # Sélectionner 1 combinaison dans DNA_NEZ_LEVRES
    selected_nez_levres = random.choice(DNA_NEZ_LEVRES)
    mixer.selected_tags["nez_levres"] = [selected_nez_levres]
    
    # Sélectionner 0 à 3 signes dans DNA_SIGNES
    signes_count = random.randint(0, 3)
    if signes_count > 0:
        selected_signes = random.sample(DNA_SIGNES, signes_count)
        mixer.selected_tags["signes"] = selected_signes
    else:
        mixer.selected_tags["signes"] = []
    
    # Sélectionner 1 style dans DNA_STYLE
    selected_style = random.choice(DNA_STYLE)
    mixer.selected_tags["style"] = [selected_style]
    
    # Âge aléatoire entre 18 et 35
    random_age = random.randint(18, 35)
    mixer.set_age(random_age)
    
    # Synchronisation DNA: met à jour directement le st.session_state des widgets
    st.session_state['dna_identite'] = mixer.selected_tags["identite"]
    st.session_state['dna_visage'] = mixer.selected_tags["visage"]
    st.session_state['dna_yeux'] = mixer.selected_tags["yeux"]
    st.session_state['dna_cheveux'] = mixer.selected_tags["cheveux"]
    st.session_state['dna_nez_levres'] = mixer.selected_tags["nez_levres"]
    st.session_state['dna_signes'] = mixer.selected_tags["signes"]
    st.session_state['dna_age_linear'] = mixer.age
    
    return random_name

def render():
    """Render casting page with DNA Mixer Pro"""
    
    st.title("🧬 DNA Mixer Pro")
    st.markdown("Créez des modèles uniques en mixant les tags DNA")
    
    # Interface de randomisation
    col_name, col_random = st.columns([2, 1])
    with col_name:
        model_name = st.text_input(
            "Nom du modèle:",
            placeholder="ex: Jade, Léa, Emma...",
            value=st.session_state.get('model_name', ''),
            key="model_name_input"
        )
    with col_random:
        if st.button("🎲 Randomizer Complet", use_container_width=True, key="randomize_btn"):
            random_name = randomize_model()
            st.success(f"🎲 Modèle randomisé: {random_name}")
            st.rerun()
    
    # Initialize DNA mixer in session state
    if 'dna_mixer' not in st.session_state:
        st.session_state.dna_mixer = DNAMixer()
    
    mixer = st.session_state.dna_mixer
    
    # DNA Configuration Section
    with st.expander("🧬 CONFIGURATION DNA", expanded=True):
        
        # Age
        col_age, col_status = st.columns([3, 1])
        with col_age:
            age = st.number_input(
                "Âge",
                min_value=18,
                max_value=35,
                value=mixer.age,
                key="dna_age_linear"
            )
            mixer.set_age(age)
        
        with col_status:
            if mixer.is_complete():
                st.success("✅ Complet")
            else:
                st.warning("⚠️ Incomplet")
        
        st.markdown("---")
        
        # 2-column layout for categories
        col_left, col_right = st.columns(2)
        
        with col_left:
            st.markdown("#### 👤 Identité")
            identite = st.multiselect(
                "Sélectionnez 1-3 origines",
                DNA_IDENTITE,
                default=mixer.selected_tags["identite"],
                max_selections=3,
                key="dna_identite",
                help="Choisissez les origines ethniques du personnage"
            )
            mixer.set_tags("identite", identite)
            
            st.markdown("#### 👱 Visage")
            visage = st.multiselect(
                "Sélectionnez 1-2 formes",
                DNA_VISAGE,
                default=mixer.selected_tags["visage"],
                max_selections=2,
                key="dna_visage",
                help="Forme générale du visage"
            )
            mixer.set_tags("visage", visage)
            
            st.markdown("#### 👀 Yeux")
            yeux = st.multiselect(
                "Sélectionnez 1-2 types",
                DNA_YEUX,
                default=mixer.selected_tags["yeux"],
                max_selections=2,
                key="dna_yeux",
                help="Couleur et forme des yeux"
            )
            mixer.set_tags("yeux", yeux)
        
        with col_right:
            st.markdown("#### 💇 Cheveux")
            cheveux = st.multiselect(
                "Sélectionnez 1-2 styles",
                DNA_CHEVEUX,
                default=mixer.selected_tags["cheveux"],
                max_selections=2,
                key="dna_cheveux",
                help="Couleur et style de cheveux"
            )
            mixer.set_tags("cheveux", cheveux)
            
            st.markdown("#### 👃 Nez & Lèvres")
            nez_levres = st.multiselect(
                "Sélectionnez 1 combinaison",
                DNA_NEZ_LEVRES,
                default=mixer.selected_tags["nez_levres"],
                max_selections=1,
                key="dna_nez_levres",
                help="Forme du nez et des lèvres"
            )
            mixer.set_tags("nez_levres", nez_levres)
            
            st.markdown("#### ✨ Signes Distinctifs")
            signes = st.multiselect(
                "Sélectionnez 0-3 signes",
                DNA_SIGNES,
                default=mixer.selected_tags["signes"],
                max_selections=3,
                key="dna_signes",
                help="Caractéristiques uniques"
            )
            mixer.set_tags("signes", signes)
        
        st.markdown("---")
        
        # Custom instructions
        st.markdown("#### 📝 Instructions Finales (Optionnel)")
        custom = st.text_area(
            "Ajoutez des instructions personnalisées en anglais",
            value=mixer.custom_instructions,
            height=100,
            key="dna_custom",
            placeholder="Ex: Wearing a red dress, studio lighting, professional makeup..."
        )
        mixer.set_custom_instructions(custom)
        
        # DNA Summary with Model Name - Affiche le nom du modèle tout en haut du résumé DNA
        current_model_name = st.session_state.get('model_name', 'Model')
        st.markdown(f"## 🎭 {current_model_name.upper()}")
        
        # Preview prompt
        if st.button("👁️ Prévisualiser le Prompt", use_container_width=True):
            with st.expander("📋 Master Prompt (Anglais)", expanded=True):
                prompt = mixer.build_master_prompt()
                st.code(prompt, language="text")
    
    st.markdown("---")
    
    # Phase 1 Generation
    st.markdown("## 🎬 Phase 1: Foundation")
    st.markdown("Génération du triptych de base (3 vues)")
    
    col_config, col_result = st.columns([1, 1])
    
    with col_config:
        st.markdown("### ⚙️ Configuration")
        
        resolution = st.selectbox(
            "Résolution",
            ["1K", "2K", "4K"],
            index=1,
            key="phase1_res"
        )
        
        aspect_ratio = st.selectbox(
            "Aspect Ratio",
            ["3:2", "16:9", "1:1"],
            index=0,
            key="phase1_ratio"
        )
        
        st.markdown("---")
        
        # Check quota before generation
        quota_remaining = st.session_state.persistent_monitor.get_quota_remaining()
        quota_exceeded = st.session_state.persistent_monitor.is_quota_exceeded()
        
        if quota_exceeded:
            st.error("❌ Quota dépassé ! Impossible de générer.")
            generate_enabled = False
        elif not mixer.is_complete():
            st.warning("⚠️ Complétez la configuration DNA")
            generate_enabled = False
        else:
            st.info(f"✅ Prêt | Quota restant: {st.session_state.persistent_monitor.format_tokens(quota_remaining)}")
            generate_enabled = True
        
        if st.button(
            "🎨 GÉNÉRER PHASE 1",
            disabled=not generate_enabled,
            use_container_width=True,
            key="generate_phase1"
        ):
            with st.spinner("🎨 Génération en cours... (~30 secondes)"):
                try:
                    engine = GeminiEngine()
                    engine.update_config(image_size=resolution, aspect_ratio=aspect_ratio)
                    
                    prompt = mixer.build_master_prompt()
                    
                    # Progress bar
                    progress_bar = st.progress(0)
                    status_text = st.empty()
                    
                    for i in range(100):
                        time.sleep(0.3)
                        progress_bar.progress(i + 1)
                        if i < 30:
                            status_text.text("🔄 Initialisation...")
                        elif i < 70:
                            status_text.text("🎨 Génération en cours...")
                        else:
                            status_text.text("✨ Finalisation...")
                    
                    result_path = engine.generate_image(
                        prompt=prompt,
                        reference_image_path=None,
                        phase="1",
                        character_name=f"char_{age}",
                        usage_tracker=st.session_state.usage_tracker
                    )
                    
                    if result_path and result_path.exists():
                        st.session_state.phase1_image = str(result_path)
                        st.session_state.last_gen_path = str(result_path)  # Store for persistent validation
                        
                        # Update persistent monitor
                        estimated_tokens = len(prompt) // 4
                        st.session_state.persistent_monitor.add_tokens(estimated_tokens)
                        st.session_state.persistent_monitor.add_image()
                        
                        st.success(f"✅ Phase 1 générée: {result_path.name}")
                    else:
                        st.error("❌ Échec de la génération")
                
                except Exception as e:
                    st.error(f"❌ Erreur: {str(e)}")
    
    with col_result:
        st.markdown("### 🖼️ Résultat")
        
        if 'phase1_image' in st.session_state and st.session_state.phase1_image:
            img_path = Path(st.session_state.phase1_image)
            if img_path.exists():
                st.image(str(img_path), use_container_width=True)
                st.caption(f"📁 {img_path.name}")
            else:
                st.info("Image non trouvée")
        else:
            st.info("Aucune image générée")
    
    # --- VALIDATION INTERFACE ---
    if st.session_state.get('last_generated_path'):
        st.markdown("---")
        st.markdown("### 💾 Sauvegarder le modèle")
        col_v, col_a = st.columns(2)
        
        if col_v.button("✅ OUI - Enregistrer", key="confirm_save", use_container_width=True):
            import shutil
            from core.config import Config
            
            model_name = st.session_state.get('model_name', 'Model').strip()
            clean_name = "".join([c for c in model_name if c.isalnum() or c in (' ', '_')]).rstrip()
            target = Config.MODELS_DIR / f"{clean_name}.png"
            
            # Gestion doublons
            counter = 2
            while target.exists():
                target = Config.MODELS_DIR / f"{clean_name}_{counter}.png"
                counter += 1
            
            shutil.copy2(st.session_state.last_generated_path, target)
            st.success(f"🎉 Sauvegardé : {target.name}")
            st.info(f"📍 Emplacement : {target}")
            st.balloons()
            
            st.session_state.last_generated_path = None
            st.rerun()
        
        if col_a.button("❌ NON", key="cancel_save", use_container_width=True):
            st.session_state.last_generated_path = None
            st.rerun()

    # DNA Summary
    st.markdown("---")
    st.markdown("### 📊 Résumé DNA")
    
    # Nom dans le Résumé: MODÈLE IA
    st.markdown(f"### 🎭 MODÈLE IA : {st.session_state.get('model_name', 'SANS NOM').upper()}")
    
    summary = mixer.get_summary()
    if summary != "Aucune configuration":
        st.code(summary, language="text")
    else:
        st.info("Aucune configuration DNA")
