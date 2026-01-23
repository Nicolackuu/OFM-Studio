"""
Casting Page - Premium Linear Design
DNA Mixer central, natural workflow, breathing space
"""
import streamlit as st
from pathlib import Path
from core.dna_mixer import (
    DNAMixer,
    DNA_IDENTITE,
    DNA_VISAGE,
    DNA_YEUX,
    DNA_CHEVEUX,
    DNA_NEZ_LEVRES,
    DNA_SIGNES
)
from core.gemini_engine import GeminiEngine
import time

def render():
    """Render premium casting page with DNA Mixer"""
    
    # Page header with breathing space
    st.markdown("# 🧬 Casting")
    st.markdown("""
    <p style="color: var(--text-secondary); font-size: 0.9375rem; margin-bottom: 48px;">
        Séquenceur génétique avancé avec tags français et traduction automatique vers l'API.
    </p>
    """, unsafe_allow_html=True)
    
    # Initialize DNA mixer
    if 'dna_mixer' not in st.session_state:
        st.session_state.dna_mixer = DNAMixer()
    
    mixer = st.session_state.dna_mixer
    
    # DNA Configuration - Central and prominent
    st.markdown("## 🧬 Configuration DNA")
    st.markdown("<div style='height: 16px;'></div>", unsafe_allow_html=True)
    
    # Status bar
    col_age, col_status, col_preview = st.columns([2, 1, 1])
    
    with col_age:
        age = st.number_input(
            "Âge du personnage",
            min_value=18,
            max_value=35,
            value=mixer.age,
            key="dna_age_premium",
            help="Âge du personnage (18-35 ans)"
        )
        mixer.set_age(age)
    
    with col_status:
        if mixer.is_complete():
            st.markdown("""
            <div class="status-badge success" style="margin-top: 28px;">
                ✓ Complet
            </div>
            """, unsafe_allow_html=True)
        else:
            st.markdown("""
            <div class="status-badge warning" style="margin-top: 28px;">
                ⚠ Incomplet
            </div>
            """, unsafe_allow_html=True)
    
    with col_preview:
        if st.button("👁️ Preview Prompt", key="preview_prompt", use_container_width=True):
            st.session_state.show_prompt_preview = not st.session_state.get('show_prompt_preview', False)
    
    # Prompt preview
    if st.session_state.get('show_prompt_preview', False):
        st.markdown("<div style='height: 16px;'></div>", unsafe_allow_html=True)
        with st.expander("📋 Master Prompt (Anglais)", expanded=True):
            prompt = mixer.build_master_prompt()
            st.code(prompt, language="text")
    
    st.markdown("<div style='height: 32px;'></div>", unsafe_allow_html=True)
    
    # DNA Categories - 2 column layout with breathing space
    col_left, col_right = st.columns(2, gap="large")
    
    with col_left:
        # Identité
        st.markdown("### 👤 Identité")
        st.markdown("<div style='height: 8px;'></div>", unsafe_allow_html=True)
        identite = st.multiselect(
            "Origines ethniques (1-3)",
            DNA_IDENTITE,
            default=mixer.selected_tags["identite"],
            max_selections=3,
            key="dna_identite_premium",
            help="Choisissez 1 à 3 origines pour créer un mélange unique"
        )
        mixer.set_tags("identite", identite)
        
        st.markdown("<div style='height: 24px;'></div>", unsafe_allow_html=True)
        
        # Visage
        st.markdown("### 👱 Visage")
        st.markdown("<div style='height: 8px;'></div>", unsafe_allow_html=True)
        visage = st.multiselect(
            "Forme du visage (1-2)",
            DNA_VISAGE,
            default=mixer.selected_tags["visage"],
            max_selections=2,
            key="dna_visage_premium",
            help="Forme générale et structure du visage"
        )
        mixer.set_tags("visage", visage)
        
        st.markdown("<div style='height: 24px;'></div>", unsafe_allow_html=True)
        
        # Yeux
        st.markdown("### 👀 Yeux")
        st.markdown("<div style='height: 8px;'></div>", unsafe_allow_html=True)
        yeux = st.multiselect(
            "Couleur et forme (1-2)",
            DNA_YEUX,
            default=mixer.selected_tags["yeux"],
            max_selections=2,
            key="dna_yeux_premium",
            help="Couleur et caractéristiques des yeux"
        )
        mixer.set_tags("yeux", yeux)
    
    with col_right:
        # Cheveux
        st.markdown("### 💇 Cheveux")
        st.markdown("<div style='height: 8px;'></div>", unsafe_allow_html=True)
        cheveux = st.multiselect(
            "Couleur et style (1-2)",
            DNA_CHEVEUX,
            default=mixer.selected_tags["cheveux"],
            max_selections=2,
            key="dna_cheveux_premium",
            help="Couleur et style de coiffure"
        )
        mixer.set_tags("cheveux", cheveux)
        
        st.markdown("<div style='height: 24px;'></div>", unsafe_allow_html=True)
        
        # Nez & Lèvres
        st.markdown("### 👃 Nez & Lèvres")
        st.markdown("<div style='height: 8px;'></div>", unsafe_allow_html=True)
        nez_levres = st.multiselect(
            "Combinaison (1)",
            DNA_NEZ_LEVRES,
            default=mixer.selected_tags["nez_levres"],
            max_selections=1,
            key="dna_nez_levres_premium",
            help="Forme du nez et des lèvres"
        )
        mixer.set_tags("nez_levres", nez_levres)
        
        st.markdown("<div style='height: 24px;'></div>", unsafe_allow_html=True)
        
        # Signes Distinctifs
        st.markdown("### ✨ Signes Distinctifs")
        st.markdown("<div style='height: 8px;'></div>", unsafe_allow_html=True)
        signes = st.multiselect(
            "Caractéristiques uniques (0-3)",
            DNA_SIGNES,
            default=mixer.selected_tags["signes"],
            max_selections=3,
            key="dna_signes_premium",
            help="Traits distinctifs optionnels"
        )
        mixer.set_tags("signes", signes)
    
    # Custom instructions with breathing space
    st.markdown("<hr style='margin: 48px 0;'>", unsafe_allow_html=True)
    
    st.markdown("### 📝 Instructions Personnalisées")
    st.markdown("<div style='height: 8px;'></div>", unsafe_allow_html=True)
    custom = st.text_area(
        "Ajoutez des instructions en anglais (optionnel)",
        value=mixer.custom_instructions,
        height=100,
        key="dna_custom_premium",
        placeholder="Ex: Wearing elegant black dress, studio lighting, professional makeup, confident expression...",
        help="Instructions additionnelles fusionnées avec les tags traduits"
    )
    mixer.set_custom_instructions(custom)
    
    # Generation section with breathing space
    st.markdown("<hr style='margin: 48px 0;'>", unsafe_allow_html=True)
    
    st.markdown("## 🎬 Phase 1: Foundation")
    st.markdown("""
    <p style="color: var(--text-secondary); font-size: 0.875rem; margin-bottom: 24px;">
        Génération du triptych de base (3 vues: profil gauche, face frontale, vue 3/4 droite)
    </p>
    """, unsafe_allow_html=True)
    
    col_config, col_result = st.columns([1, 1], gap="large")
    
    with col_config:
        st.markdown("### ⚙️ Configuration")
        st.markdown("<div style='height: 16px;'></div>", unsafe_allow_html=True)
        
        col_res, col_ratio = st.columns(2)
        
        with col_res:
            resolution = st.selectbox(
                "Résolution",
                ["1K", "2K", "4K"],
                index=1,
                key="phase1_res_premium"
            )
        
        with col_ratio:
            aspect_ratio = st.selectbox(
                "Aspect Ratio",
                ["3:2", "16:9", "1:1"],
                index=0,
                key="phase1_ratio_premium"
            )
        
        st.markdown("<div style='height: 24px;'></div>", unsafe_allow_html=True)
        
        # Quota check
        quota_remaining = st.session_state.persistent_monitor.get_quota_remaining()
        quota_exceeded = st.session_state.persistent_monitor.is_quota_exceeded()
        
        if quota_exceeded:
            st.markdown("""
            <div class="error-box">
                ❌ Quota dépassé ! Impossible de générer.
            </div>
            """, unsafe_allow_html=True)
            generate_enabled = False
        elif not mixer.is_complete():
            st.markdown("""
            <div class="warning-box">
                ⚠️ Complétez la configuration DNA pour continuer.
            </div>
            """, unsafe_allow_html=True)
            generate_enabled = False
        else:
            st.markdown(f"""
            <div class="info-box">
                ✓ Prêt à générer<br>
                <small>Quota restant: {st.session_state.persistent_monitor.format_tokens(quota_remaining)}</small>
            </div>
            """, unsafe_allow_html=True)
            generate_enabled = True
        
        st.markdown("<div style='height: 16px;'></div>", unsafe_allow_html=True)
        
        if st.button(
            "🎨 Générer Phase 1",
            disabled=not generate_enabled,
            use_container_width=True,
            key="generate_phase1_premium",
            type="primary"
        ):
            with st.spinner("Génération en cours..."):
                try:
                    engine = GeminiEngine()
                    engine.update_config(image_size=resolution, aspect_ratio=aspect_ratio)
                    
                    prompt = mixer.build_master_prompt()
                    
                    # Progress
                    progress_bar = st.progress(0)
                    status_text = st.empty()
                    
                    for i in range(100):
                        time.sleep(0.25)
                        progress_bar.progress(i + 1)
                        if i < 30:
                            status_text.text("🔄 Initialisation...")
                        elif i < 70:
                            status_text.text("🎨 Génération...")
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
                        
                        # Update persistent monitor
                        estimated_tokens = len(prompt) // 4
                        st.session_state.persistent_monitor.add_tokens(estimated_tokens)
                        st.session_state.persistent_monitor.add_image()
                        
                        st.success(f"✓ Phase 1 générée: {result_path.name}")
                        st.balloons()
                        st.rerun()
                    else:
                        st.error("❌ Échec de la génération")
                
                except Exception as e:
                    st.error(f"❌ Erreur: {str(e)}")
    
    with col_result:
        st.markdown("### 🖼️ Résultat")
        st.markdown("<div style='height: 16px;'></div>", unsafe_allow_html=True)
        
        if 'phase1_image' in st.session_state and st.session_state.phase1_image:
            img_path = Path(st.session_state.phase1_image)
            if img_path.exists():
                st.image(str(img_path), use_column_width=True)
                st.caption(f"📁 {img_path.name}")
            else:
                st.info("Image non trouvée")
        else:
            st.markdown("""
            <div style="
                background: var(--bg-surface);
                border: 1px dashed var(--border-default);
                border-radius: var(--radius-md);
                padding: 64px 24px;
                text-align: center;
                color: var(--text-tertiary);
            ">
                <div style="font-size: 3rem; margin-bottom: 16px;">🖼️</div>
                <div>Aucune image générée</div>
            </div>
            """, unsafe_allow_html=True)
