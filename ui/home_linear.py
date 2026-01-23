"""
Home Page - Linear.app Inspired Landing
Minimal 3-card layout for main workflows
"""
import streamlit as st

def render():
    """Render Linear-inspired home page"""
    
    # Hero section
    st.markdown("""
    <div style="margin-bottom: 48px;">
        <h1 style="font-size: 3rem; font-weight: 600; margin-bottom: 16px; letter-spacing: -0.02em;">
            OFM IA Studio
        </h1>
        <p style="font-size: 1.25rem; color: #8b949e; max-width: 600px;">
            Production pipeline professionnelle pour la génération de personnages IA.
        </p>
    </div>
    """, unsafe_allow_html=True)
    
    # 3 massive cards
    col1, col2, col3 = st.columns(3, gap="large")
    
    with col1:
        if st.button("🧬", key="nav_casting", use_container_width=True):
            st.session_state.active_page = "casting"
            st.rerun()
        
        st.markdown("""
        <div class="card-massive">
            <div class="card-icon">🧬</div>
            <div class="card-title">Casting</div>
            <div class="card-description">
                Système de génération 3 phases avec DNA Mixer Pro.
                Créez des personnages uniques avec précision.
            </div>
        </div>
        """, unsafe_allow_html=True)
    
    with col2:
        if st.button("📸", key="nav_scraper", use_container_width=True):
            st.session_state.active_page = "scraper"
            st.rerun()
        
        st.markdown("""
        <div class="card-massive">
            <div class="card-icon">📸</div>
            <div class="card-title">Scraper</div>
            <div class="card-description">
                Téléchargement Instagram automatisé.
                Collecte de datasets pour entraînement LoRa.
            </div>
        </div>
        """, unsafe_allow_html=True)
    
    with col3:
        if st.button("🏭", key="nav_factory", use_container_width=True):
            st.session_state.active_page = "factory"
            st.rerun()
        
        st.markdown("""
        <div class="card-massive">
            <div class="card-icon">🏭</div>
            <div class="card-title">Factory</div>
            <div class="card-description">
                Pipeline de production face swap.
                Curation Tinder-style et traitement batch.
            </div>
        </div>
        """, unsafe_allow_html=True)
    
