#!/usr/bin/env python3
"""
OFM IA STUDIO DASHBOARD v19.0
Professional SaaS-Style AI Content Production Cockpit
Horizontal Navigation & Pipeline Workflow
Main Entry Point & Router
"""
import streamlit as st
from pathlib import Path

# Import UI modules
from ui import home, casting, scraper, factory
from ui.components import led_indicator, system_monitor, token_wallet

# Import core
from core.config import Config
from core.usage_tracker import UsageTracker
from core.character_bank import (
    Character,
    get_all_nationalities,
    get_all_face_shapes,
    get_all_eyes,
    get_all_hair,
    get_all_nose_lips,
    get_all_distinctive_features
)

# ============================================================================
# PAGE CONFIG
# ============================================================================

st.set_page_config(
    page_title="OFM IA Studio Cockpit",
    page_icon="🎬",
    layout="wide",
    initial_sidebar_state="expanded"
)

# ============================================================================
# LOAD CUSTOM CSS
# ============================================================================

def load_css():
    """Load custom CSS from style/custom.css"""
    css_file = Path(__file__).parent / "style" / "custom.css"
    if css_file.exists():
        with open(css_file, 'r', encoding='utf-8') as f:
            st.markdown(f"<style>{f.read()}</style>", unsafe_allow_html=True)
    else:
        st.warning("Custom CSS file not found")

load_css()

# ============================================================================
# SESSION STATE INITIALIZATION
# ============================================================================

def init_session_state():
    """Initialize all session state variables"""
    if 'character' not in st.session_state:
        st.session_state.character = Character()
    if 'phase1_image' not in st.session_state:
        st.session_state.phase1_image = None
    if 'phase2_image' not in st.session_state:
        st.session_state.phase2_image = None
    if 'phase3_image' not in st.session_state:
        st.session_state.phase3_image = None
    if 'source_face' not in st.session_state:
        st.session_state.source_face = None
    if 'scraped_images' not in st.session_state:
        st.session_state.scraped_images = []
    if 'approved_images' not in st.session_state:
        st.session_state.approved_images = []
    if 'current_username' not in st.session_state:
        st.session_state.current_username = None
    if 'active_tab' not in st.session_state:
        st.session_state.active_tab = 0
    if 'active_model_name' not in st.session_state:
        st.session_state.active_model_name = None
    if 'usage_tracker' not in st.session_state:
        st.session_state.usage_tracker = UsageTracker()

# ============================================================================
# SIDEBAR
# ============================================================================

def render_sidebar():
    """Render sidebar with system monitoring only"""
    with st.sidebar:
        # Logo/Header
        st.markdown("""
        <div style="text-align: center; padding: 20px 0;">
            <h1 style="color: #4facfe; font-size: 2rem; margin: 0;">🎬 OFM IA</h1>
            <p style="color: #8b92a7; font-size: 0.9rem; margin: 5px 0;">Studio Cockpit v19.0</p>
        </div>
        """, unsafe_allow_html=True)
        
        st.markdown("---")
        
        # API Status
        st.markdown("### 🔌 API Status")
        
        google_status = bool(Config.GOOGLE_API_KEY)
        insta_status = bool(Config.INSTAGRAM_USERNAME and Config.INSTAGRAM_SESSION_ID)
        
        led_indicator(google_status, "Google Gemini", "green", "red")
        led_indicator(insta_status, "Instagram", "green", "red")
        
        st.markdown("---")
        
        # Active Model
        st.markdown("### 🎭 Modèle Actif")
        
        if st.session_state.active_model_name:
            st.markdown(f"""
            <div class="info-box" style="padding: 10px; margin: 5px 0;">
                <strong>👤 {st.session_state.active_model_name}</strong><br>
                <span style="font-size: 0.85rem; color: #8b92a7;">Âge: {st.session_state.character.get_dna_field('AGE')} ans</span>
            </div>
            """, unsafe_allow_html=True)
        else:
            st.info("Aucun modèle actif")
        
        st.markdown("---")
        
        # Token Wallet
        st.markdown("---")
        token_wallet(st.session_state.usage_tracker)
        
        # System Monitor
        st.markdown("---")
        system_monitor()
        
        st.markdown("---")
        st.markdown("""
        <div style="text-align: center; color: #8b92a7; font-size: 0.8rem;">
            <p>OFM IA Studio v19.0</p>
            <p>Professional AI Pipeline</p>
        </div>
        """, unsafe_allow_html=True)

# ============================================================================
# MAIN ROUTER
# ============================================================================

def render_top_navigation():
    """Render horizontal top navigation bar"""
    st.markdown("""
    <div style="text-align: center; margin-bottom: 30px;">
        <h1 style="color: #ffffff; font-size: 2.5rem; margin: 0;">🎬 OFM IA Studio Cockpit</h1>
        <p style="color: #8b92a7; font-size: 1rem; margin: 5px 0;">Professional AI Content Production Pipeline</p>
    </div>
    """, unsafe_allow_html=True)
    
    # Horizontal navigation tabs
    tab_names = [
        "🏠 Dashboard",
        "🧬 1. Casting",
        "📸 2. Scraper",
        "🏭 3. Factory",
        "🚀 4. Training (Soon)"
    ]
    
    tabs = st.tabs(tab_names)
    
    return tabs

def main():
    """Main application router"""
    init_session_state()
    render_sidebar()
    
    # Render top navigation and get tabs
    tabs = render_top_navigation()
    
    # Tab 0: Dashboard
    with tabs[0]:
        st.session_state.active_tab = 0
        home.render()
    
    # Tab 1: Casting
    with tabs[1]:
        st.session_state.active_tab = 1
        casting.render()
    
    # Tab 2: Scraper
    with tabs[2]:
        st.session_state.active_tab = 2
        scraper.render()
    
    # Tab 3: Factory
    with tabs[3]:
        st.session_state.active_tab = 3
        factory.render()
    
    # Tab 4: Training (Coming Soon)
    with tabs[4]:
        st.session_state.active_tab = 4
        st.markdown("""
        <div style="text-align: center; padding: 100px 20px;">
            <h2 style="color: #4facfe; font-size: 3rem;">🚀</h2>
            <h3 style="color: #ffffff;">LoRa Training Module</h3>
            <p style="color: #8b92a7; font-size: 1.2rem;">Coming Soon...</p>
            <p style="color: #8b92a7;">Automatic LoRa model training from your curated dataset</p>
        </div>
        """, unsafe_allow_html=True)

# ============================================================================
# ENTRY POINT
# ============================================================================

if __name__ == "__main__":
    try:
        main()
    except Exception as e:
        st.error("🚨 Erreur Critique")
        st.error(f"Une erreur s'est produite: {str(e)}")
        
        with st.expander("🔧 Détails Techniques"):
            import traceback
            st.code(traceback.format_exc())
        
        st.info("💡 Essayez de rafraîchir la page (F5)")
