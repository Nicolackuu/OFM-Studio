"""
Home Page - Dashboard Overview
"""
import streamlit as st
from pathlib import Path
from core.config import Config
from ui.components import stat_card, info_box

def render():
    """Render home page"""
    st.title("🎬 OFM IA Studio Cockpit")
    st.markdown("### Production-Ready AI Content Pipeline")
    
    info_box("Welcome to your professional AI studio. Monitor your production pipeline in real-time.", "info")
    
    st.markdown("---")
    
    # Stats Grid
    col1, col2, col3, col4 = st.columns(4)
    
    with col1:
        generated_count = len(list(Config.OUTPUT_DIR.glob("*.png"))) if Config.OUTPUT_DIR.exists() else 0
        stat_card("Images Générées", str(generated_count), "🎨")
    
    with col2:
        dataset_dir = Config.BASE_DIR / "DATASET" / "FINAL_LORA"
        dataset_count = len(list(dataset_dir.glob("*.png"))) if dataset_dir.exists() else 0
        target = 100
        stat_card("Dataset LoRa", str(dataset_count), "🏭", progress=dataset_count, target=target)
    
    with col3:
        approved_dir = Config.BASE_DIR / "DATASET" / "APPROVED"
        approved_count = len(list(approved_dir.glob("*.*"))) if approved_dir.exists() else 0
        stat_card("Images Approuvées", str(approved_count), "✅")
    
    with col4:
        stat_card("Statut Système", "🟢 Opérationnel", "⚡")
    
    st.markdown("---")
    
    # Workflow Overview
    st.markdown("### 🔄 Production Workflow")
    
    col1, col2 = st.columns(2)
    
    with col1:
        st.markdown("""
        <div class="info-box">
        <h4>📋 Système 3 Phases</h4>
        <p><strong>PHASE 1 (Foundation):</strong> Triptych - 3 vues (Profil, Face, 3/4)</p>
        <p><strong>PHASE 2 (Structure):</strong> 5 angles techniques (Plongée, Contre-plongée, etc.)</p>
        <p><strong>PHASE 3 (Dynamics):</strong> 5 émotions (Sourire, Colère, Serein, etc.)</p>
        </div>
        """, unsafe_allow_html=True)
    
    with col2:
        st.markdown("""
        <div class="info-box">
        <h4>🏭 Pipeline Dataset</h4>
        <p><strong>1. Scraping:</strong> Télécharge photos Instagram</p>
        <p><strong>2. Curation:</strong> Tri style Tinder (Garder/Rejeter)</p>
        <p><strong>3. Face Swap:</strong> Batch processing avec Gemini API</p>
        <p><strong>4. Export:</strong> Dataset final pour training LoRa</p>
        </div>
        """, unsafe_allow_html=True)
    
    st.markdown("---")
    
    # Recent Activity
    st.markdown("### 📸 Dernières Générations")
    
    if Config.OUTPUT_DIR.exists():
        recent_images = sorted(Config.OUTPUT_DIR.glob("*.png"), key=lambda x: x.stat().st_mtime, reverse=True)[:6]
        
        if recent_images:
            cols = st.columns(3)
            for idx, img_path in enumerate(recent_images):
                with cols[idx % 3]:
                    st.markdown('<div class="image-preview">', unsafe_allow_html=True)
                    st.image(str(img_path), use_container_width=True, caption=img_path.name[:20])
                    st.markdown('</div>', unsafe_allow_html=True)
        else:
            st.info("Aucune image générée pour le moment")
    else:
        st.warning("Dossier de génération non trouvé")
    
    st.markdown("---")
    
    # Quick Actions
    st.markdown("### ⚡ Actions Rapides")
    
    col1, col2, col3 = st.columns(3)
    
    with col1:
        if st.button("🧬 Nouveau Casting", use_container_width=True):
            st.session_state.page = "🧬 Casting (3 Phases)"
            st.rerun()
    
    with col2:
        if st.button("📸 Scraper Instagram", use_container_width=True):
            st.session_state.page = "📸 Scraper Insta"
            st.rerun()
    
    with col3:
        if st.button("🏭 Usine Dataset", use_container_width=True):
            st.session_state.page = "🏭 Usine Dataset"
            st.rerun()
