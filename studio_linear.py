"""
OFM IA STUDIO - LINEAR.APP INSPIRED REBUILD
World-Class Minimal UI with Persistent Monitoring
Main Entry Point & Router
"""
import streamlit as st
from pathlib import Path
import os
import sys

# Ajout du chemin racine au path pour garantir les imports
root_path = Path(__file__).parent
sys.path.append(str(root_path))

# ============================================================================
# PAGE CONFIG
# ============================================================================

st.set_page_config(
    page_title="OFM IA Studio",
    page_icon="🧬",
    layout="wide",
    initial_sidebar_state="expanded"
)

# ============================================================================
# IMPORTS SÉCURISÉS
# ============================================================================

try:
    from ui import home_linear, casting_linear, scraper, factory, curation
    from core.persistent_monitor import PersistentMonitor
    from core.usage_tracker import UsageTracker
    from core.request_tracker import RequestTracker
    from core.config import Config
except ImportError as e:
    st.error(f"❌ Erreur critique d'importation : {e}")
    st.stop()

# ============================================================================
# LOAD CUSTOM CSS
# ============================================================================

def load_css():
    """Load Linear-inspired CSS theme"""
    css_file = Path(__file__).parent / "style" / "linear_theme.css"
    if css_file.exists():
        with open(css_file, 'r', encoding='utf-8') as f:
            st.markdown(f"<style>{f.read()}</style>", unsafe_allow_html=True)

load_css()

# ============================================================================
# SESSION STATE INITIALIZATION
# ============================================================================

def init_session_state():
    """Initialize all session state variables"""
    
    # --- Navigation ---
    if 'active_page' not in st.session_state:
        st.session_state.active_page = "home"
    
    # --- Core Logic ---
    if 'persistent_monitor' not in st.session_state:
        st.session_state.persistent_monitor = PersistentMonitor()
    
    if 'usage_tracker' not in st.session_state:
        st.session_state.usage_tracker = UsageTracker()
    
    if 'request_tracker' not in st.session_state:
        st.session_state.request_tracker = RequestTracker()
    
    # Force Sync des Quotas (Action unique au démarrage)
    if st.session_state.persistent_monitor.data['tokens_used'] < 47310:
        st.session_state.persistent_monitor.recalibrate_tokens(47310)
    if st.session_state.request_tracker.data['daily_requests'] < 123:
        st.session_state.request_tracker.sync_usage(123)
    
    # --- Casting / Gemini ---
    if 'phase1_image' not in st.session_state:
        st.session_state.phase1_image = None
    if 'phase2_image' not in st.session_state:
        st.session_state.phase2_image = None
    if 'phase3_image' not in st.session_state:
        st.session_state.phase3_image = None
    if 'total_images' not in st.session_state:
        st.session_state.total_images = 0
    if 'total_sessions' not in st.session_state:
        st.session_state.total_sessions = 0

    # --- Scraper (CORRECTIF ICI) ---
    if 'scraped_images' not in st.session_state:
        st.session_state.scraped_images = []  # Liste vide par défaut
    if 'current_username' not in st.session_state:
        st.session_state.current_username = None
    if 'scraper_progress' not in st.session_state:
        st.session_state.scraper_progress = 0

    # --- Factory / Face Swap (PRÉVENTION) ---
    if "source_face" not in st.session_state:
        st.session_state.source_face = None
    if "approved_images" not in st.session_state:
        st.session_state.approved_images = []
    
    # --- VARIABLES DE CURATION ---
    if 'curation_index' not in st.session_state:
        st.session_state['curation_index'] = 0
    if 'curation_queue' not in st.session_state:
        st.session_state['curation_queue'] = []
    if 'approved_list' not in st.session_state:
        st.session_state['approved_list'] = []
    if 'rejected_list' not in st.session_state:
        st.session_state['rejected_list'] = []
    if 'curation_mode' not in st.session_state:
        st.session_state['curation_mode'] = "Swipe" # Par défaut
    
    # --- API QUOTAS ---
    if 'api_requests_today' not in st.session_state:
        st.session_state['api_requests_today'] = 123
    if 'api_tokens_today' not in st.session_state:
        st.session_state['api_tokens_today'] = 47310
    if 'api_limit_requests' not in st.session_state:
        st.session_state['api_limit_requests'] = 250
    if 'api_limit_tokens' not in st.session_state:
        st.session_state['api_limit_tokens'] = 100000

init_session_state()

# ============================================================================
# SIDEBAR - PERSISTENT MONITORING
# ============================================================================

def render_sidebar():
    """Render minimal sidebar with persistent monitoring"""
    with st.sidebar:
        # Logo
        st.markdown("""
        <div style="text-align: center; margin-bottom: 32px;">
            <h2 style="font-size: 1.5rem; font-weight: 600; margin: 0;">OFM IA Studio</h2>
            <p style="font-size: 0.85rem; color: #8b949e; margin: 4px 0 0 0;">Production Pipeline</p>
        </div>
        """, unsafe_allow_html=True)
        
        st.markdown("---")
        
        # --- ÉTAT DES CONNEXIONS ---
        st.markdown("### 🔌 CONNECTIVITÉ")
        
        # Statut Gemini
        has_gemini = bool(os.getenv("GOOGLE_API_KEY"))
        gemini_label = "Google Gemini : CONNECTÉ" if has_gemini else "Google Gemini : DÉCONNECTÉ"
        gemini_color = "#3fb950" if has_gemini else "#f85149"
        st.markdown(f'<p style="color:{gemini_color}; font-size:0.85rem; margin-bottom:4px;">● {gemini_label}</p>', unsafe_allow_html=True)
        
        # Statut Instagram
        from core.config import Config
        # Vérification réelle de la présence du cookie
        has_insta = Config.SESSION_ID is not None and len(str(Config.SESSION_ID)) > 10
        insta_label = "Instagram : SESSION OK" if has_insta else "Instagram : SESSION ERROR"
        insta_color = "#3fb950" if has_insta else "#f85149"
        st.markdown(f'<p style="color:{insta_color}; font-size:0.85rem;">● {insta_label}</p>', unsafe_allow_html=True)
        
        st.markdown("---")
        
        # 📊 QUOTAS - Unification
        st.markdown("### 📊 QUOTAS")
        
        # Requêtes (X / 250)
        try:
            req_stats = st.session_state.request_tracker.get_stats()
            requests_today = req_stats['daily_requests']
            requests_limit = req_stats['daily_limit']
            requests_pct = requests_today / requests_limit
            
            st.sidebar.progress(requests_pct)
            st.caption(f"Requêtes : {requests_today} / {requests_limit}")
        except:
            st.caption("Requêtes indisponibles")
        
        # Tokens (X / 100K)
        try:
            persistent_stats = st.session_state.persistent_monitor.get_stats()
            tokens_used = persistent_stats['tokens_used']
            tokens_total = persistent_stats['quota_total']
            tokens_pct = tokens_used / tokens_total
            
            # Color based on usage
            if tokens_pct < 50:
                token_color = "#3fb950"
            elif tokens_pct < 80:
                token_color = "#d29922"
            else:
                token_color = "#f85149"
            
            st.sidebar.progress(tokens_pct)
            st.markdown(f"""
            <div style="display: flex; align-items: center; margin: 8px 0;">
                <span class="led-indicator led-{'green' if tokens_pct < 0.5 else 'orange' if tokens_pct < 0.8 else 'red'}"></span>
                <span style="color: {token_color}; font-weight: bold;">Tokens : {tokens_used/1000:.1f}K / {tokens_total/1000:.0f}K</span>
            </div>
            """, unsafe_allow_html=True)
        except:
            st.caption("Tokens indisponibles")
        
        st.markdown("---")
        
        # Hardware Monitor (RTX 3070)
        st.markdown("### 🎮 Hardware")
        
        try:
            # FIX: Import pynvml instead of nvidia_ml_py
            import pynvml as nvml
            nvml.nvmlInit()
            handle = nvml.nvmlDeviceGetHandleByIndex(0)
            info = nvml.nvmlDeviceGetMemoryInfo(handle)
            gpu_name = nvml.nvmlDeviceGetName(handle)
            
            # Gestion encodage nom GPU (bytes vs str)
            if isinstance(gpu_name, bytes):
                gpu_name = gpu_name.decode('utf-8')
                
            vram_used = info.used / (1024**3)
            vram_total = info.total / (1024**3)
            vram_pct = (info.used / info.total) * 100
            
            vram_color = "#3fb950" if vram_pct < 70 else "#d29922" if vram_pct < 85 else "#f85149"
            
            st.markdown(f"""
            <div class="metric-container">
                <div class="metric-label">VRAM ({gpu_name})</div>
                <div class="metric-value" style="color: {vram_color}; font-size: 1rem;">
                    {vram_used:.1f} GB / {vram_total:.1f} GB
                </div>
            </div>
            """, unsafe_allow_html=True)
            
            st.markdown(f"""
            <div class="quota-gauge">
                <div class="quota-fill" style="width: {vram_pct}%; background: {vram_color};"></div>
            </div>
            """, unsafe_allow_html=True)
            
            nvml.nvmlShutdown()
        except Exception as e:
            # Fallback silencieux si pas de GPU NVIDIA ou librairie manquante
            st.caption(f"GPU Monitor: Off")
        
        st.markdown("---")
        
        # Système de recalibrage manuelle pour les requêtes
        with st.sidebar.expander("⚙️ Recalibrer"):
            # Get current request stats for default value
            try:
                req_stats = st.session_state.request_tracker.get_stats()
                current_requests = req_stats['daily_requests']
                requests_limit = req_stats['daily_limit']
            except:
                current_requests = 123
                requests_limit = 250
            
            new_requests = st.number_input(
                "Requêtes journalières:",
                min_value=0,
                max_value=requests_limit,
                value=current_requests,
                key="recalibrate_requests"
            )
            
            if st.button("🔄 Recalibrer", key="recalibrate_btn"):
                st.session_state.api_requests_today = new_requests
                st.success("✅ Requêtes recalibrées")
                st.rerun()
        
        st.markdown("---")

render_sidebar()

# ============================================================================
# NAVIGATION
# ============================================================================

def render_navigation():
    """Render horizontal navigation tabs"""
    tabs = st.tabs(["🏠 Home", "🧬 Casting", "📸 Scraper", "📂 Curation", "🏭 Factory"])
    return tabs

# ============================================================================
# MAIN ROUTER
# ============================================================================

def main():
    """Main application router"""
    
    # --- CRITICAL: Crée les dossiers dès le lancement ---
    from core.config import Config
    Config.check_directories()
    
    # --- PITCH BLACK CSS ---
    st.markdown("""
    <style>
    /* Fond Pitch Black */
    .stApp {
        background-color: #000000 !important;
    }
    
    /* Sidebar pure black */
    [data-testid="stSidebar"] {
        background-color: #000000 !important;
        border-right: 1px solid #1A1A1A !important;
    }
    
    /* Sidebar control button - CRITICAL FIX */
    [data-testid="stSidebarCollapsedControl"] button {
        color: #FFFFFF !important;
        background-color: rgba(255,255,255,0.1) !important;
        border: 1px solid rgba(255,255,255,0.2) !important;
        backdrop-filter: blur(10px) !important;
    }
    
    [data-testid="stSidebarCollapsedControl"] button:hover {
        background-color: rgba(255,255,255,0.2) !important;
        border: 1px solid rgba(255,255,255,0.3) !important;
    }
    
    /* Ensure button is always visible */
    [data-testid="stSidebarCollapsedControl"] {
        position: relative !important;
        z-index: 999 !important;
    }
    
    /* Onglets et cartes très sombres */
    .stTabs [data-baseweb="tab-list"] {
        background-color: #0A0A0A;
        border-radius: 12px;
        border: 1px solid #1A1A1A;
    }
    
    .stTabs [data-baseweb="tab-list"] button {
        border-radius: 8px;
        color: #E1E5EA;
        background-color: #111111;
    }
    
    .stTabs [data-baseweb="tab-list"] button:hover {
        background-color: #1A1A1A;
    }
    
    /* Boutons avec relief subtil */
    .stButton > button {
        border: none;
        border-radius: 8px;
        background: linear-gradient(135deg, #1A1A1A, #111111);
        color: #E1E5EA;
        transition: all 0.3s ease;
        box-shadow: 0 2px 8px rgba(0,0,0,0.5);
    }
    
    .stButton > button:hover {
        background: linear-gradient(135deg, #2A2A2A, #1A1A1A);
        transform: translateY(-1px);
        box-shadow: 0 4px 12px rgba(0,0,0,0.7);
    }
    
    /* Scrollbar */
    ::-webkit-scrollbar {
        width: 8px;
    }
    
    ::-webkit-scrollbar-track {
        background: #0A0A0A;
    }
    
    ::-webkit-scrollbar-thumb {
        background: #1A1A1A;
        border-radius: 4px;
    }
    
    ::-webkit-scrollbar-thumb:hover {
        background: #2A2A2A;
    }
    
    /* Images avec relief accentué */
    img {
        border-radius: 12px;
        box-shadow: 0 8px 32px rgba(0,0,0,0.8);
        transition: all 0.3s ease;
    }
    
    img:hover {
        transform: scale(1.02);
        box-shadow: 0 12px 40px rgba(0,0,0,0.9);
    }
    
    /* Cartes et conteneurs */
    .stDataFrame {
        background-color: #0A0A0A;
        border-radius: 12px;
        border: 1px solid #1A1A1A;
    }
    
    .stMetric {
        background-color: #0A0A0A;
        border-radius: 8px;
        border: 1px solid #1A1A1A;
        padding: 12px;
    }
    
    /* Progress bar */
    .stProgress > div > div > div {
        background: linear-gradient(90deg, #1A1A1A, #2A2A2A);
        border-radius: 4px;
    }
    
    /* Expander */
    .streamlit-expanderHeader {
        background-color: #0A0A0A;
        border: 1px solid #1A1A1A;
    }
    
    /* Input fields */
    .stTextInput > div > div > input,
    .stNumberInput > div > div > input {
        background-color: #111111;
        border: 1px solid #1A1A1A;
        color: #E1E5EA;
    }
    
    /* Selectbox */
    .stSelectbox > div > div > select {
        background-color: #111111;
        border: 1px solid #1A1A1A;
        color: #E1E5EA;
    }
    
    /* Sidebar Permanente - Supprime tous les boutons de contrôle */
    header[data-testid='stHeader'] { background: transparent !important; }
    header[data-testid='stHeader'] > div:first-child { visibility: hidden; }
    
    /* Supprime tous les boutons de contrôle de la sidebar */
    [data-testid="stSidebarCollapsedControl"], 
    button[kind="headerNoSpacing"],
    [data-testid="stSidebar"] button {
        display: none !important;
    }
    
    /* Force la sidebar à rester ouverte et fixe */
    [data-testid="stSidebar"] {
        min-width: 300px !important;
        max-width: 300px !important;
        visibility: visible !important;
    }
    </style>
    """, unsafe_allow_html=True)
    
    init_session_state()  # <--- CRITIQUE : Appeler l'initialisation ici
    
    tabs = render_navigation()
    
    with tabs[0]:  # Home
        st.session_state.active_page = "home"
        home_linear.render()
    
    with tabs[1]:  # Casting
        st.session_state.active_page = "casting"
        casting_linear.render()
    
    with tabs[2]:  # Scraper
        st.session_state.active_page = "scraper"
        scraper.render()
    
    with tabs[3]:  # Curation
        st.session_state.active_page = "curation"
        curation.render()
    
    with tabs[4]:  # Factory
        st.session_state.active_page = "factory"
        factory.render()

if __name__ == "__main__":
    main()