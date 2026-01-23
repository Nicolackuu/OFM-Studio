"""
Casting Page - 3-Phase Character Generation System
"""
import streamlit as st
from pathlib import Path
from core.gemini_engine import GeminiEngine
from ui.components import info_box, image_preview, copy_button, phase_button
import time

def render():
    """Render casting page with 3-phase system"""
    st.title("🧬 Casting - Système 3 Phases")
    
    info_box("Workflow: Phase 1 → Phase 2 (avec ref Phase 1) → Phase 3 (avec ref Phase 1 ou 2)", "info")
    
    # DNA Editor at top of page
    with st.expander("🧬 CONFIGURATION DE L'ADN DU PERSONNAGE", expanded=True):
        col_btn, col_status = st.columns([2, 1])
        
        with col_btn:
            if st.button("🎲 GÉNÉRER PROFIL RANDOM", use_container_width=True, key="random_dna_casting"):
                st.session_state.character.generate_random()
                st.success("✓ Profil généré!")
                st.rerun()
        
        with col_status:
            if st.session_state.character.is_complete():
                st.success("✅ ADN Complet")
            else:
                st.warning("⚠️ Incomplet")
        
        st.markdown("---")
        
        # Import DNA helper functions
        from core.character_bank import (
            get_all_nationalities,
            get_all_face_shapes,
            get_all_eyes,
            get_all_hair,
            get_all_nose_lips,
            get_all_distinctive_features
        )
        
        col1, col2 = st.columns(2)
        
        with col1:
            st.markdown("#### 👤 Identité")
            
            age = st.number_input(
                "Âge",
                min_value=18,
                max_value=35,
                value=int(st.session_state.character.get_dna_field('AGE')),
                key="dna_age_casting"
            )
            st.session_state.character.set_dna('AGE', str(age))
            
            nat_options = get_all_nationalities()
            current_nat = st.session_state.character.get_dna_field('NATIONALITE')
            nat_index = nat_options.index(current_nat) if current_nat in nat_options else 0
            
            nationality = st.selectbox(
                "Nationalité",
                nat_options,
                index=nat_index,
                key="dna_nat_casting"
            )
            st.session_state.character.set_dna('NATIONALITE', nationality)
            
            st.markdown("#### 👱 Visage")
            
            face_options = get_all_face_shapes()
            current_face = st.session_state.character.get_dna_field('FACE_SHAPE')
            face_index = face_options.index(current_face) if current_face in face_options else 0
            
            face_shape = st.selectbox(
                "Forme du Visage",
                face_options,
                index=face_index,
                key="dna_face_casting"
            )
            st.session_state.character.set_dna('FACE_SHAPE', face_shape)
            
            eyes_options = get_all_eyes()
            current_eyes = st.session_state.character.get_dna_field('EYES')
            eyes_index = eyes_options.index(current_eyes) if current_eyes in eyes_options else 0
            
            eyes = st.selectbox(
                "Yeux",
                eyes_options,
                index=eyes_index,
                key="dna_eyes_casting"
            )
            st.session_state.character.set_dna('EYES', eyes)
        
        with col2:
            st.markdown("#### 💇 Style")
            
            hair_options = get_all_hair()
            current_hair = st.session_state.character.get_dna_field('HAIR')
            hair_index = hair_options.index(current_hair) if current_hair in hair_options else 0
            
            hair = st.selectbox(
                "Cheveux",
                hair_options,
                index=hair_index,
                key="dna_hair_casting"
            )
            st.session_state.character.set_dna('HAIR', hair)
            
            nose_options = get_all_nose_lips()
            current_nose = st.session_state.character.get_dna_field('NOSE_LIPS')
            nose_index = nose_options.index(current_nose) if current_nose in nose_options else 0
            
            nose_lips = st.selectbox(
                "Nez/Lèvres",
                nose_options,
                index=nose_index,
                key="dna_nose_casting"
            )
            st.session_state.character.set_dna('NOSE_LIPS', nose_lips)
            
            features_options = get_all_distinctive_features()
            current_features = st.session_state.character.get_dna_field('DISTINCTIVE_FEATURES')
            features_index = features_options.index(current_features) if current_features in features_options else 0
            
            features = st.selectbox(
                "Signes Distinctifs",
                features_options,
                index=features_index,
                key="dna_features_casting"
            )
            st.session_state.character.set_dna('DISTINCTIVE_FEATURES', features)
    
    st.markdown("---")
    
    # Tabs for 3 phases
    tab1, tab2, tab3 = st.tabs(["🎬 PHASE 1: Foundation", "🎬 PHASE 2: Structure", "🎬 PHASE 3: Dynamics"])
    
    # === PHASE 1 ===
    with tab1:
        st.markdown("### Triptych (3 Vues)")
        st.markdown("Crée la base: Profil gauche, Face frontale, Vue 3/4 droite")
        
        col1, col2 = st.columns([1, 1])
        
        with col1:
            st.markdown("#### ⚙️ Configuration")
            
            col_res, col_ratio = st.columns(2)
            with col_res:
                resolution = st.selectbox("Résolution", ["1K", "2K", "4K"], index=1, key="phase1_res")
            with col_ratio:
                aspect_ratio = st.selectbox("Aspect Ratio", ["3:2", "16:9", "1:1"], index=0, key="phase1_ratio")
            
            st.markdown("---")
            
            if phase_button(1, enabled=st.session_state.character.is_complete(), 
                          completed=st.session_state.phase1_image is not None):
                with st.spinner("🎨 Génération Phase 1 en cours... (~30 secondes)"):
                    try:
                        engine = GeminiEngine()
                        engine.update_config(image_size=resolution, aspect_ratio=aspect_ratio)
                        
                        prompt = st.session_state.character.build_prompt("1")
                        
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
                            character_name=f"char_{st.session_state.character.get_dna_field('AGE')}",
                            usage_tracker=st.session_state.usage_tracker
                        )
                        
                        if result_path and result_path.exists():
                            st.session_state.phase1_image = str(result_path)
                            st.session_state.source_face = str(result_path)
                            
                            # Set active model name
                            nat_field = st.session_state.character.get_dna_field('NATIONALITE')
                            age_field = st.session_state.character.get_dna_field('AGE')
                            nat_short = nat_field.split()[0] if nat_field else "Model"
                            st.session_state.active_model_name = f"{nat_short} ({age_field}ans)"
                            
                            info_box(f"✓ Phase 1 générée: {result_path.name}", "success")
                            st.balloons()
                            st.rerun()
                        else:
                            info_box("Échec de la génération", "error")
                    
                    except Exception as e:
                        info_box(f"Erreur: {str(e)}", "error")
        
        with col2:
            st.markdown("#### 🖼️ Résultat")
            
            if st.session_state.phase1_image:
                image_preview(Path(st.session_state.phase1_image), "Phase 1: Foundation", zoom=True)
                
                st.markdown("---")
                
                # Copy prompt button
                prompt = st.session_state.character.build_prompt("1")
                with st.expander("📋 Voir le Prompt"):
                    st.code(prompt, language="text")
            else:
                st.info("Aucune image générée")
    
    # === PHASE 2 ===
    with tab2:
        st.markdown("### 5 Angles Techniques")
        st.markdown("Nécessite Phase 1 comme référence")
        
        if not st.session_state.phase1_image:
            info_box("⚠️ Générez Phase 1 d'abord", "warning")
        else:
            col1, col2 = st.columns([1, 1])
            
            with col1:
                st.markdown("#### ⚙️ Configuration")
                
                st.info(f"📎 Référence: {Path(st.session_state.phase1_image).name}")
                
                st.markdown("---")
                
                if phase_button(2, enabled=True, completed=st.session_state.phase2_image is not None):
                    with st.spinner("🎨 Génération Phase 2 en cours... (~30 secondes)"):
                        try:
                            engine = GeminiEngine()
                            prompt = st.session_state.character.build_prompt("2")
                            
                            progress_bar = st.progress(0)
                            for i in range(100):
                                time.sleep(0.3)
                                progress_bar.progress(i + 1)
                            
                            result_path = engine.generate_image(
                                prompt=prompt,
                                reference_image_path=st.session_state.phase1_image,
                                phase="2",
                                character_name=f"char_{st.session_state.character.get_dna_field('AGE')}",
                                usage_tracker=st.session_state.usage_tracker
                            )
                            
                            if result_path and result_path.exists():
                                st.session_state.phase2_image = str(result_path)
                                info_box(f"✓ Phase 2 générée: {result_path.name}", "success")
                                st.balloons()
                                st.rerun()
                            else:
                                info_box("Échec de la génération", "error")
                        
                        except Exception as e:
                            info_box(f"Erreur: {str(e)}", "error")
            
            with col2:
                st.markdown("#### 🖼️ Résultat")
                
                if st.session_state.phase2_image:
                    image_preview(Path(st.session_state.phase2_image), "Phase 2: Structure", zoom=True)
                else:
                    st.info("Aucune image générée")
    
    # === PHASE 3 ===
    with tab3:
        st.markdown("### 5 Émotions")
        st.markdown("Nécessite Phase 1 ou 2 comme référence")
        
        if not st.session_state.phase1_image:
            info_box("⚠️ Générez Phase 1 d'abord", "warning")
        else:
            col1, col2 = st.columns([1, 1])
            
            with col1:
                st.markdown("#### ⚙️ Configuration")
                
                ref_choice = st.radio("Image de référence:", ["Phase 1", "Phase 2"], horizontal=True)
                ref_image = st.session_state.phase1_image if ref_choice == "Phase 1" else st.session_state.phase2_image
                
                if ref_choice == "Phase 2" and not st.session_state.phase2_image:
                    info_box("⚠️ Phase 2 pas encore générée, utilise Phase 1", "warning")
                    ref_image = st.session_state.phase1_image
                
                st.info(f"📎 Référence: {Path(ref_image).name}")
                
                st.markdown("---")
                
                if phase_button(3, enabled=True, completed=st.session_state.phase3_image is not None):
                    with st.spinner("🎨 Génération Phase 3 en cours... (~30 secondes)"):
                        try:
                            engine = GeminiEngine()
                            prompt = st.session_state.character.build_prompt("3")
                            
                            progress_bar = st.progress(0)
                            for i in range(100):
                                time.sleep(0.3)
                                progress_bar.progress(i + 1)
                            
                            result_path = engine.generate_image(
                                prompt=prompt,
                                reference_image_path=ref_image,
                                phase="3",
                                character_name=f"char_{st.session_state.character.get_dna_field('AGE')}",
                                usage_tracker=st.session_state.usage_tracker
                            )
                            
                            if result_path and result_path.exists():
                                st.session_state.phase3_image = str(result_path)
                                info_box(f"✓ Phase 3 générée: {result_path.name}", "success")
                                st.balloons()
                                st.rerun()
                            else:
                                info_box("Échec de la génération", "error")
                        
                        except Exception as e:
                            info_box(f"Erreur: {str(e)}", "error")
            
            with col2:
                st.markdown("#### 🖼️ Résultat")
                
                if st.session_state.phase3_image:
                    image_preview(Path(st.session_state.phase3_image), "Phase 3: Dynamics", zoom=True)
                else:
                    st.info("Aucune image générée")
    
    # Summary section at bottom
    if st.session_state.phase1_image or st.session_state.phase2_image or st.session_state.phase3_image:
        st.markdown("---")
        st.markdown("### 📊 Résumé de la Session")
        
        cols = st.columns(3)
        
        with cols[0]:
            if st.session_state.phase1_image:
                st.success("✅ Phase 1 Complete")
                st.caption(Path(st.session_state.phase1_image).name)
            else:
                st.info("⏸️ Phase 1 Pending")
        
        with cols[1]:
            if st.session_state.phase2_image:
                st.success("✅ Phase 2 Complete")
                st.caption(Path(st.session_state.phase2_image).name)
            else:
                st.info("⏸️ Phase 2 Pending")
        
        with cols[2]:
            if st.session_state.phase3_image:
                st.success("✅ Phase 3 Complete")
                st.caption(Path(st.session_state.phase3_image).name)
            else:
                st.info("⏸️ Phase 3 Pending")
