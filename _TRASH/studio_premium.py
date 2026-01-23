"""
OFM IA STUDIO - PREMIUM LINEAR DESIGN
Ultra-Fluid SaaS Interface with Perfect Harmony
Main Entry Point & Router
"""
import streamlit as st
from pathlib import Path
import os

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
# IMPORTS (Avec sécurité)
# ============================================================================
try:
    from core.config import Config
    from core.persistent_monitor import PersistentMonitor
    from core.usage_tracker import UsageTracker
    
    # UI Modules
    from ui import home_premium
    
    # Imports conditionnels
    try: from ui import casting_premium
    except ImportError: casting_premium = None
    
    try: from ui import scraper
    except ImportError: scraper = None
    
    try: from ui import factory
    except ImportError: factory = None
    
    try: from ui import curation_premium
    except ImportError: curation_premium = None

except ImportError as e:
    st.error(f"Erreur critique d'importation : {e}")
    st.stop()

# ============================================================================
# LOAD PREMIUM CSS
# ============================================================================

def load_css():
    """Load premium Linear-inspired CSS"""
    try:
        css_file = Path(__file__).parent / "style" / "premium_linear.css"
        if css_file.exists():
            with open(css_file, 'r', encoding='utf-8') as f:
                st.markdown(f"<style>{f.read()}</style>", unsafe_allow_html=True)
    except Exception:
        pass

load_css()

# ============================================================================
# SESSION STATE INITIALIZATION (VERSION COMPLETE)
# ============================================================================

def init_session_state():
    """Initialize all session state variables"""
    
    # Navigation
    if 'current_page' not in st.session_state:
        st.session_state.current_page = "home"
    
    # Persistent monitor
    if 'persistent_monitor' not in st.session_state:
        st.session_state.persistent_monitor = PersistentMonitor()
    
    # Usage tracker (session-based)
    if 'usage_tracker' not in st.session_state:
        st.session_state.usage_tracker = UsageTracker()
    
    # Phase images
    if 'phase1_image' not in st.session_state: st.session_state.phase1_image = None
    if 'phase2_image' not in st.session_state: st.session_state.phase2_image = None
    if 'phase3_image' not in st.session_state: st.session_state.phase3_image = None
    
    # UI state
    if 'show_prompt_preview' not in st.session_state: st.session_state.show_prompt_preview = False
    
    # Scraper state
    if 'scraped_images' not in st.session_state: st.session_state.scraped_images = []
    if 'current_username' not in st.session_state: st.session_state.current_username = None
    if 'scraper_progress' not in st.session_state: st.session_state.scraper_progress = 0
    
    # Factory state
    if 'source_face' not in st.session_state: st.session_state.source_face = None
    if 'approved_images' not in st.session_state: st.session_state.approved_images = []
    if 'approved_list' not in st.session_state: st.session_state.approved_list = []
    if 'rejected_list' not in st.session_state: st.session_state.rejected_list = []
    if 'curation_queue' not in st.session_state: st.session_state.curation_queue = []
    if 'curation_index' not in st.session_state: st.session_state.curation_index = 0
    if 'factory_logs' not in st.session_state: st.session_state.factory_logs = []
    if 'production_results' not in st.session_state: st.session_state.production_results = []
    
    # DNA Mixer state
    if 'dna_mixer' not in st.session_state:
        try:
            from core.dna_mixer import DNAMixer
            st.session_state.dna_mixer = DNAMixer()
        except: pass
    
    # Stats
    if 'total_images' not in st.session_state: st.session_state.total_images = 0
    if 'total_sessions' not in st.session_state: st.session_state.total_sessions = 0

init_session_state()

# ============================================================================
# SIDEBAR - MINIMAL MONITORING (VERSION COMPLETE)
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
            <span class="led-indicator led-{google_status}" style="margin-right: 8px;">●</span>
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
            <span class="led-indicator led-{insta_status}" style="margin-right: 8px;">●</span>
            <span style="color: var(--text-secondary);">Instagram</span>
        </div>
        """, unsafe_allow_html=True)
        
        st.markdown("<hr style='margin: 32px 0;'>", unsafe_allow_html=True)
        
        # Quota Global
        st.markdown("### 💎 Quota Global")
        st.markdown("<div style='height: 12px;'></div>", unsafe_allow_html=True)
        
        stats = st.session_state.persistent_monitor.get_stats()
        quota_pct = stats.get('quota_percentage', 0)
        tokens_used = stats.get('tokens_used', 0)
        quota_total = stats.get('quota_total', 0)
        quota_remaining = stats.get('quota_remaining', 0)
        
        # Color based on usage
        if quota_pct < 50: quota_color = "var(--status-success)"
        elif quota_pct < 80: quota_color = "var(--status-warning)"
        else: quota_color = "var(--status-error)"
        
        st.markdown(f"""
        <div class="metric-container">
            <div class="metric-label">Utilisé / Total</div>
            <div class="metric-value" style="color: {quota_color}; font-size: 1.125rem;">
                {st.session_state.persistent_monitor.format_tokens(tokens_used)} / {st.session_state.persistent_monitor.format_tokens(quota_total)}
            </div>
        </div>
        """, unsafe_allow_html=True)
        
        # Gauge
        st.markdown(f"""
        <div class="quota-gauge" style="background: #333; height: 4px; border-radius: 2px; margin-top: 5px;">
            <div class="quota-fill" style="width: {min(quota_pct, 100)}%; background: {quota_color}; height: 100%; border-radius: 2px;"></div>
        </div>
        """, unsafe_allow_html=True)
        
        st.markdown(f"""
        <p style="font-size: 0.75rem; color: var(--text-tertiary); margin-top: 8px;">
            Restant: {st.session_state.persistent_monitor.format_tokens(quota_remaining)} tokens
        </p>
        """, unsafe_allow_html=True)
        
        st.markdown("<hr style='margin: 32px 0;'>", unsafe_allow_html=True)
        
        # Hardware Monitor
        st.markdown("### 🎮 Hardware")
        st.markdown("<div style='height: 12px;'></div>", unsafe_allow_html=True)
        
        try:
            import nvidia_ml_py as nvml
            nvml.nvmlInit()
            handle = nvml.nvmlDeviceGetHandleByIndex(0)
            info = nvml.nvmlDeviceGetMemoryInfo(handle)
            gpu_name = nvml.nvmlDeviceGetName(handle)
            vram_used = info.used / (1024**3)
            vram_total = info.total / (1024**3)
            vram_pct = (info.used / info.total) * 100
            
            vram_color = "var(--status-success)" if vram_pct < 70 else "var(--status-warning)" if vram_pct < 85 else "var(--status-error)"
            
            st.markdown(f"""
            <div class="metric-container">
                <div class="metric-label">VRAM ({gpu_name})</div>
                <div class="metric-value" style="color: {vram_color}; font-size: 0.9375rem;">
                    {vram_used:.1f} / {vram_total:.1f} GB
                </div>
            </div>
            """, unsafe_allow_html=True)
            
            st.markdown(f"""
            <div class="quota-gauge" style="background: #333; height: 4px; border-radius: 2px; margin-top: 5px;">
                <div class="quota-fill" style="width: {vram_pct}%; background: {vram_color}; height: 100%; border-radius: 2px;"></div>
            </div>
            """, unsafe_allow_html=True)
            
            nvml.nvmlShutdown()
        except Exception:
            st.markdown("""<p style="font-size: 0.75rem; color: var(--text-tertiary);">GPU non disponible</p>""", unsafe_allow_html=True)
        
        st.markdown("<hr style='margin: 32px 0;'>", unsafe_allow_html=True)
        
        # Session Stats
        st.markdown("### 📊 Session")
        st.markdown("<div style='height: 12px;'></div>", unsafe_allow_html=True)
        
        session_stats = st.session_state.usage_tracker.get_stats()
        
        col1, col2 = st.columns(2)
        with col1:
            st.markdown(f"""
            <div class="metric-container">
                <div class="metric-label">Images</div>
                <div class="metric-value" style="font-size: 1.125rem;">{session_stats['images_generated']}</div>
            </div>
            """, unsafe_allow_html=True)
        
        with col2:
            tokens_display = st.session_state.usage_tracker.format_tokens(session_stats['total_tokens'])
            st.markdown(f"""
            <div class="metric-container">
                <div class="metric-label">Tokens</div>
                <div class="metric-value" style="font-size: 1.125rem;">{tokens_display}</div>
            </div>
            """, unsafe_allow_html=True)

render_sidebar()

# ============================================================================
# NAVIGATION (MODIFIÉE POUR FONCTIONNER AVEC LES BOUTONS)
# ============================================================================

def navigate_to(page_name):
    """Force la navigation et le rechargement"""
    st.session_state.current_page = page_name
    st.rerun()

def render_navbar():
    """Barre de navigation horizontale avec BOUTONS (remplace les Tabs)"""
    st.markdown("---")
    c1, c2, c3, c4, c5 = st.columns(5)
    
    # Helper pour style actif/inactif
    def btn_type(p): return "primary" if st.session_state.current_page == p else "secondary"

    with c1:
        if st.button("🏠 Home", key="nav_home", use_container_width=True, type=btn_type("home")):
            navigate_to("home")
    with c2:
        if st.button("🧬 Casting", key="nav_casting", use_container_width=True, type=btn_type("casting")):
            navigate_to("casting")
    with c3:
        if st.button("📸 Scraper", key="nav_scraper", use_container_width=True, type=btn_type("scraper")):
            navigate_to("scraper")
    with c4:
        if st.button("🎯 Curation", key="nav_curation", use_container_width=True, type=btn_type("curation")):
            navigate_to("curation")
    with c5:
        if st.button("🏭 Factory", key="nav_factory", use_container_width=True, type=btn_type("factory")):
            navigate_to("factory")
            
    st.markdown("---")

# ============================================================================
# MAIN ROUTER
# ============================================================================

def main():
    """Main application router with seamless flow and safety net"""
    
    # 1. On affiche la barre de navigation
    render_navbar()
    
    # 2. Router Logic
    try:
        page = st.session_state.current_page
        
        if page == "home":
            home_premium.render()
        
        elif page == "casting":
            if casting_premium: casting_premium.render()
            else: st.error("❌ Module Casting non disponible (vérifiez casting_premium.py)")
        
        elif page == "scraper":
            if scraper: scraper.render()
            else: st.error("❌ Module Scraper non disponible")
        
        elif page == "curation":
            if curation_premium: curation_premium.render()
            else: st.error("❌ Module Curation non disponible")
        
        elif page == "factory":
            if factory: factory.render()
            else: st.error("❌ Module Factory non disponible")
    
    except Exception as e:
        st.error(f"❌ Erreur critique: {str(e)}")
        st.info("💡 Rechargez la page pour réinitialiser l'application.")
        if st.button("Retour Secours Accueil"):
            navigate_to("home")

if __name__ == "__main__":
    main()