"""
Home Page - Premium Linear Design
Breathing space, minimal hero, 4 massive cards (2x2 Grid)
"""
import streamlit as st

def navigate_to(page_name):
    """Helper to handle navigation state and rerun"""
    st.session_state.current_page = page_name
    st.rerun()

def render():
    """Render premium Linear-inspired home page"""
    
    # Hero section with breathing space
    st.markdown("""
    <div style="margin-bottom: 48px; padding-top: 32px;">
        <h1 class="hero-title">
            OFM IA Studio
        </h1>
        <p class="hero-subtitle">
            Pipeline de production professionnelle.
            DNA Mixer avancé, Curation intelligente, Factory batch.
        </p>
    </div>
    """, unsafe_allow_html=True)
    
    # --- ROW 1: CASTING & SCRAPER ---
    col1, col2 = st.columns(2, gap="large")
    
    with col1:
        st.markdown("""
        <div class="card-massive fade-in">
            <div>
                <div class="card-icon">🧬</div>
                <div class="card-title">Casting</div>
                <div class="card-description">
                    Génération de visages, définition de l'ADN, prompts et styles.
                </div>
            </div>
        </div>
        """, unsafe_allow_html=True)
        
        if st.button("Ouvrir Casting", key="nav_casting", use_container_width=True):
            navigate_to("casting")
    
    with col2:
        st.markdown("""
        <div class="card-massive fade-in" style="animation-delay: 0.1s;">
            <div>
                <div class="card-icon">📸</div>
                <div class="card-title">Scraper</div>
                <div class="card-description">
                    Téléchargement Instagram automatisé et création de datasets.
                </div>
            </div>
        </div>
        """, unsafe_allow_html=True)
        
        if st.button("Ouvrir Scraper", key="nav_scraper", use_container_width=True):
            navigate_to("scraper")
            
    # Spacer
    st.markdown("<div style='height: 24px;'></div>", unsafe_allow_html=True)

    # --- ROW 2: CURATION & FACTORY ---
    col3, col4 = st.columns(2, gap="large")
    
    with col3:
        # NEW CURATION CARD
        st.markdown("""
        <div class="card-massive fade-in" style="animation-delay: 0.2s; border: 1px solid rgba(255, 75, 75, 0.3);">
            <div>
                <div class="card-icon">🎯</div>
                <div class="card-title" style="color: #FF4B4B;">Curation</div>
                <div class="card-description">
                    Tri intelligent (Tinder-mode), filtres qualité et validation.
                </div>
            </div>
        </div>
        """, unsafe_allow_html=True)
        
        if st.button("Ouvrir Curation", key="nav_curation", use_container_width=True):
            navigate_to("curation")

    with col4:
        st.markdown("""
        <div class="card-massive fade-in" style="animation-delay: 0.3s;">
            <div>
                <div class="card-icon">🏭</div>
                <div class="card-title">Factory</div>
                <div class="card-description">
                    Pipeline Face Swap batch. Traitement automatisé haute vitesse.
                </div>
            </div>
        </div>
        """, unsafe_allow_html=True)
        
        if st.button("Ouvrir Factory", key="nav_factory", use_container_width=True):
            navigate_to("factory")
    
    # Divider with breathing space
    st.markdown("<hr style='margin: 64px 0;'>", unsafe_allow_html=True)
    
    # Stats section - minimal and clean
    st.markdown("### 📊 Statistiques Globales")
    
    # Note: We use try/except to avoid crashes if monitor is not initialized
    try:
        col1, col2, col3, col4 = st.columns(4)
        
        with col1:
            images_count = st.session_state.persistent_monitor.data.get("images_generated", 0)
            st.metric("Images Générées", images_count)
        
        with col2:
            # Check if APPROVED folder exists for stats
            import os
            approved_count = len(os.listdir("outputs/DATASET/APPROVED")) if os.path.exists("outputs/DATASET/APPROVED") else 0
            st.metric("Images Approuvées", approved_count)
        
        with col3:
            tokens_used = st.session_state.persistent_monitor.data.get("tokens_used", 0)
            st.metric("Tokens Utilisés", tokens_used)
        
        with col4:
            st.metric("Status", "En Ligne")
            
    except Exception:
        st.warning("Moniteur de stats en cours d'initialisation...")

    # Quick actions with breathing space
    st.markdown("<div style='height: 48px;'></div>", unsafe_allow_html=True)
    st.markdown("### ⚡ Actions Rapides")
    
    q1, q2 = st.columns(2)
    
    with q1:
        if st.button("🎲 Générer DNA Random", use_container_width=True):
            try:
                # Safe import inside button action
                if 'dna_mixer' not in st.session_state:
                    from core.dna_mixer import DNAMixer
                    st.session_state.dna_mixer = DNAMixer()
                
                st.session_state.dna_mixer.generate_random()
                st.success("✓ DNA généré! Allez dans l'onglet Casting.")
            except Exception as e:
                st.error(f"Erreur DNA: {e}")

    with q2:
        if st.button("🧹 Nettoyer le cache", use_container_width=True):
            st.cache_data.clear()
            st.success("Cache vidé.")