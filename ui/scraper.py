"""
Scraper Page - Instagram Photo Downloader
"""
import streamlit as st
from pathlib import Path
from core.config import Config
from core.dataset_scraper import DatasetScraper
from ui.components import info_box, progress_tracker, gallery_grid

def render():
    """Render scraper page"""
    st.title("📸 Instagram Scraper")
    
    col1, col2 = st.columns([1, 1])
    
    with col1:
        st.markdown("### ⚙️ Configuration")
        
        username = st.text_input("Nom d'utilisateur Instagram", 
                                placeholder="username", 
                                help="Sans le @",
                                key="scraper_username")
        
        col_opt1, col_opt2 = st.columns(2)
        with col_opt1:
            include_carousels = st.checkbox("Inclure Carousels", value=True)
        with col_opt2:
            ignore_videos = st.checkbox("Ignorer Vidéos", value=True)
        
        limit = st.slider("Nombre maximum de posts", min_value=10, max_value=100, value=30, step=5)
        
        st.markdown("---")
        
        if st.button("🚀 Lancer le Téléchargement", use_container_width=True, type="primary"):
            if not username:
                info_box("Veuillez entrer un nom d'utilisateur", "error")
            else:
                # Initialize progress tracking
                if 'scraper_progress' not in st.session_state:
                    st.session_state.scraper_progress = 0
                
                progress_container = st.empty()
                status_container = st.empty()
                
                try:
                    scraper = DatasetScraper(Config.RAW_DIR)
                    
                    status_container.info(f"🔄 Connexion à @{username}...")
                    
                    # Simulate progress (in real implementation, hook into scraper)
                    for i in range(0, 101, 10):
                        st.session_state.scraper_progress = i
                        with progress_container:
                            progress_tracker(i, 100, f"Téléchargement de @{username}")
                        
                        if i < 30:
                            status_container.info("🔍 Analyse du profil...")
                        elif i < 70:
                            status_container.info(f"📥 Téléchargement des posts ({i//10}/{limit})...")
                        else:
                            status_container.info("✨ Organisation des fichiers...")
                        
                        import time
                        time.sleep(0.3)
                    
                    success = scraper.download_photos_only(username, limit)
                    
                    if success:
                        image_files = scraper.organize_files(username)
                        st.session_state.scraped_images = [str(f) for f in image_files]
                        st.session_state.current_username = username
                        
                        info_box(f"✓ {len(image_files)} images téléchargées avec succès!", "success")
                        st.balloons()
                        st.rerun()
                    else:
                        info_box("Échec du téléchargement. Vérifiez le nom d'utilisateur et votre session Instagram.", "error")
                
                except Exception as e:
                    info_box(f"Erreur: {str(e)}", "error")
                    st.error("Détails techniques:", icon="🔧")
                    st.code(str(e))
    
    with col2:
        st.markdown("### 📊 Images Téléchargées")
        
        if st.session_state.scraped_images:
            info_box(f"✓ {len(st.session_state.scraped_images)} images disponibles", "success")
            
            # Lazy loading gallery
            st.markdown("#### 🖼️ Galerie (Dernières 20)")
            
            image_paths = [Path(p) for p in st.session_state.scraped_images if Path(p).exists()]
            
            if image_paths:
                gallery_grid(image_paths, columns=3, max_display=20)
            else:
                info_box("Aucune image trouvée dans le dossier", "warning")
        else:
            st.info("Aucune image téléchargée pour le moment")
            
            st.markdown("---")
            
            st.markdown("""
            <div class="info-box">
            <h4>📝 Instructions</h4>
            <p>1. Entrez le nom d'utilisateur Instagram (sans @)</p>
            <p>2. Configurez les options de téléchargement</p>
            <p>3. Cliquez sur "Lancer le Téléchargement"</p>
            <p>4. Les images seront sauvegardées dans <code>data/dataset/raw/</code></p>
            </div>
            """, unsafe_allow_html=True)
    
    # Stats section
    if st.session_state.current_username:
        st.markdown("---")
        st.markdown("### 📈 Statistiques")
        
        col1, col2, col3 = st.columns(3)
        
        with col1:
            st.metric("Utilisateur", f"@{st.session_state.current_username}")
        
        with col2:
            st.metric("Images Téléchargées", len(st.session_state.scraped_images))
        
        with col3:
            raw_dir = Config.RAW_DIR / st.session_state.current_username
            total_size = sum(f.stat().st_size for f in raw_dir.glob("*.*") if f.is_file()) / (1024**2) if raw_dir.exists() else 0
            st.metric("Taille Totale", f"{total_size:.1f} MB")
