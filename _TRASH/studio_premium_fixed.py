"""
OFM IA STUDIO - PREMIUM LINEAR DESIGN V21.4
Ultra-Fluid SaaS Interface with Perfect Harmony
Main Entry Point & Router with Integrity Check
"""
import streamlit as st
from pathlib import Path
import os

# Import core
from core.config import Config

# ============================================================================
# PAGE CONFIG
# ============================================================================

st.set_page_config(
    page_title="OFM IA Studio",
    page_icon="🧬",
    layout="wide",
    initial_sidebar_state="collapsed"
)

# ============================================================================
# INTEGRITY CHECK AT STARTUP
# ============================================================================

def run_startup_check():
    """Run integrity check only once at startup"""
    if 'integrity_checked' not in st.session_state:
        from core.integrity_checker import run_integrity_check
        
        with st.spinner("🔍 Vérification de l'intégrité du système..."):
            is_healthy, report = run_integrity_check()
        
        st.session_state.integrity_checked = True
        st.session_state.system_healthy = is_healthy
        
        if not is_healthy:
            st.error("❌ Système non opérationnel - Corrigez les erreurs ci-dessus")
            st.stop()

run_startup_check()

# ============================================================================
# LOAD PREMIUM CSS
# ============================================================================

def load_css():
    css_file = Path(__file__).parent / "style" / "premium_linear.css"
    if css_file.exists():
        with open(css_file, 'r', encoding='utf-8') as f:
            st.markdown(f"<style>{f.read()}</style>", unsafe_allow_html=True)

load_css()

# ============================================================================
# SESSION STATE INITIALIZATION
# ============================================================================

def init_session_state():
    # Navigation
    if 'current_page' not in st.session_state:
        st.session_state.current_page = "home"
    
    # Persistent Monitor
    if 'persistent_monitor' not in st.session_state:
        from core.persistent_monitor import PersistentMonitor
        st.session_state.persistent_monitor = PersistentMonitor()
    
    # Usage Tracker (session)
    if 'usage_tracker' not in st.session_state:
        from core.usage_tracker import UsageTracker
        st.session_state.usage_tracker = UsageTracker()
    
    # Scraper state
    if 'scraped_images' not in st.session_state:
        st.session_state.scraped_images = []
    if 'current_username' not in st.session_state:
        st.session_state.current_username = ""
    if 'scraper_progress' not in st.session_state:
        st.session_state.scraper_progress = 0
    
    # Factory state
    if 'source_face' not in st.session_state:
        st.session_state.source_face = None
    if 'approved_images' not in st.session_state:
        st.session_state.approved_images = []
    if 'approved_list' not in st.session_state:
        st.session_state.approved_list = []
    if 'rejected_list' not in st.session_state:
        st.session_state.rejected_list = []
    if 'curation_queue' not in st.session_state:
        st.session_state.curation_queue = []
    if 'curation_index' not in st.session_state:
        st.session_state.curation_index = 0
    if 'factory_logs' not in st.session_state:
        st.session_state.factory_logs = []
    if 'production_results' not in st.session_state:
        st.session_state.production_results = []
    
    # DNA Mixer state
    if 'dna_mixer' not in st.session_state:
        from core.dna_mixer import DNAMixer
        st.session_state.dna_mixer = DNAMixer()
    
    # Stats
    if 'total_images' not in st.session_state:
        st.session_state.total_images = 0
    if 'total_sessions' not in st.session_state:
        st.session_state.total_sessions = 0

init_session_state()

# ============================================================================
# SIDEBAR - MINIMAL MONITORING
# ============================================================================

def render_sidebar():
    """Render minimal sidebar with seamless monitoring"""
    with st.sidebar:
        # Logo
        st.markdown("""
        <div style="text-align: center; margin-bottom: 48px;">
            <h2 style="font-size: 1.25rem; font-weight: 600; margin: 0; color: var(--text-primary);">
                OFM IA Studio
            </h2>
            <p style="font-size: 0.75rem; color: var(--text-tertiary); margin: 8px 0 0 0; text-transform: uppercase; letter-spacing: 0.1em;">
                Production Pipeline
            </p>
        </div>
        """, unsafe_allow_html=True)
        
        # API Status
        st.markdown("### 🔌 API Status")
        st.markdown("<div style='height: 12px;'></div>", unsafe_allow_html=True)
        
        # Google Gemini
        try:
            google_status = "green" if Config.GOOGLE_API_KEY else "red"
        except:
            google_status = "red"
        
        st.markdown(f"""
        <div style="display: flex; align-items: center; margin: 12px 0; font-size: 0.875rem;">
            <span class="led-indicator led-{google_status}"></span>
            <span style="color: var(--text-secondary);">Google Gemini</span>
        </div>
        """, unsafe_allow_html=True)
        
        # Instagram
        try:
            insta_user = os.getenv('INSTA_USER')
            insta_session = os.getenv('INSTA_SESSION_ID')
            insta_status = "green" if (insta_user and insta_session) else "red"
        except:
            insta_status = "red"
        
        st.markdown(f"""
        <div style="display: flex; align-items: center; margin: 12px 0; font-size: 0.875rem;">
            <span class="led-indicator led-{insta_status}"></span>
            <span style="color: var(--text-secondary);">Instagram</span>
        </div>
        """, unsafe_allow_html=True)
        
        st.markdown("<hr style='margin: 32px 0;'>", unsafe_allow_html=True)
        
        # Quota Global
        st.markdown("### 💎 Quota Global")
        st.markdown("<div style='height: 12px;'></div>", unsafe_allow_html=True)
        
        stats = st.session_state.persistent_monitor.get_stats()
        quota_pct = stats['quota_percentage']
        tokens_used = stats['tokens_used']
        quota_total = stats['quota_total']
        quota_remaining = stats['quota_remaining']
        
        if quota_pct < 50:
            quota_color = "var(--status-success)"
        elif quota_pct < 80:
            quota_color = "var(--status-warning)"
        else:
            quota_color = "var(--status-error)"
        
        st.markdown(f"""
        <div class="metric-container">
            <div class="metric-label">Utilisé / Total</div>
            <div class="metric-value" style="color: {quota_color}; font-size: 1.125rem;">
                {st.session_state.persistent_monitor.format_tokens(tokens_used)} / {st.session_state.persistent_monitor.format_tokens(quota_total)}
            </div>
        </div>
        """, unsafe_allow_html=True)
        
        st.markdown(f"""
        <div class="quota-gauge">
            <div class="quota-fill" style="width: {min(quota_pct, 100)}%; background: {quota_color};"></div>
        </div>
        """, unsafe_allow_html=True)
        
        st.markdown(f"""
        <p style="font-size: 0.75rem; color: var(--text-tertiary); margin-top: 8px;">
            Restant: {st.session_state.persistent_monitor.format_tokens(quota_remaining)} tokens
        </p>
        """, unsafe_allow_html=True)

render_sidebar()

# ============================================================================
# MAIN ROUTER
# ============================================================================

def main():
    """Main application router"""
    
    # Horizontal Navigation Tabs
    st.markdown("<div style='height: 24px;'></div>", unsafe_allow_html=True)
    
    col1, col2, col3, col4, col5 = st.columns(5)
    
    with col1:
        if st.button("🏠 Home", use_container_width=True, type="primary" if st.session_state.current_page == "home" else "secondary"):
            st.session_state.current_page = "home"
            st.rerun()
    
    with col2:
        if st.button("🎬 Casting", use_container_width=True, type="primary" if st.session_state.current_page == "casting" else "secondary"):
            st.session_state.current_page = "casting"
            st.rerun()
    
    with col3:
        if st.button("📸 Scraper", use_container_width=True, type="primary" if st.session_state.current_page == "scraper" else "secondary"):
            st.session_state.current_page = "scraper"
            st.rerun()
    
    with col4:
        if st.button("🎯 Curation", use_container_width=True, type="primary" if st.session_state.current_page == "curation" else "secondary"):
            st.session_state.current_page = "curation"
            st.rerun()
    
    with col5:
        if st.button("🏭 Factory", use_container_width=True, type="primary" if st.session_state.current_page == "factory" else "secondary"):
            st.session_state.current_page = "factory"
            st.rerun()
    
    st.markdown("<div style='height: 48px;'></div>", unsafe_allow_html=True)
    
    # Router
    if st.session_state.current_page == "home":
        from ui import home_premium
        home_premium.render()
    
    elif st.session_state.current_page == "casting":
        from ui import casting_premium
        casting_premium.render()
    
    elif st.session_state.current_page == "scraper":
        from ui import scraper
        scraper.render()
    
    elif st.session_state.current_page == "curation":
        from ui import curation
        curation.render()
    
    elif st.session_state.current_page == "factory":
        from ui import factory
        factory.render()

if __name__ == "__main__":
    main()
