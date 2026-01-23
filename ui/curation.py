import streamlit as st
import os
import base64
import shutil
from pathlib import Path
from core.config import Config

def get_image_base64(path):
    """Convert image to base64 for HTML display"""
    with open(path, 'rb') as f:
        return base64.b64encode(f.read()).decode()

def load_dataset(dataset_name):
    """Scan le dossier et remplit la file d'attente"""
    dataset_path = Path(Config.RAW_DIR) / dataset_name
    if not dataset_path.exists():
        st.error(f"Dossier non trouvé : {dataset_path}")
        return

    extensions = ('.jpg', '.jpeg', '.png', '.webp')
    images = [str(f) for f in dataset_path.iterdir() if f.suffix.lower() in extensions]
    
    if images:
        st.session_state.curation_queue = images
        st.session_state.curation_index = 0
        st.session_state.approved_list = []
        st.session_state.rejected_list = []
        st.success(f"🔥 {len(images)} images chargées !")
    else:
        st.warning("⚠️ Aucune image trouvée.")


def render_swipe_mode():
    st.subheader("🔥 Swipe Interface")
    queue = st.session_state.curation_queue
    idx = st.session_state.curation_index

    if idx >= len(queue):
        st.success("✅ Curation terminée !")
        if st.button("🔄 Recommencer la curation"):
            st.session_state.curation_index = 0
            st.rerun()
        return

    # Stats et Progression
    st.progress(idx / len(queue))
    st.write(f"Progression : {idx + 1} / {len(queue)}")

    # Layout principal : Image + Contrôles
    col_img, col_controls = st.columns([1.5, 1])
    
    with col_img:
        img_path = queue[idx]
        # Convert image to base64 for HTML display
        img_base64 = get_image_base64(img_path)
        
        # Cadre d'image pour affichage complet sans déformation
        st.markdown(f"""
        <div style='display: flex; justify-content: center; align-items: center; width: 100%; background-color: #0E1117; border-radius: 12px; padding: 10px;'>
            <img src='data:image/jpeg;base64,{img_base64}' style='
                max-width: 100%;
                max-height: 75vh;
                width: auto;
                height: auto;
                object-fit: contain;
                border-radius: 8px;
            '>
        </div>
        """, unsafe_allow_html=True)
    
    with col_controls:
        st.markdown("### Décision")
        
        # Stats compactes
        approved = len(st.session_state.approved_list)
        rejected = len(st.session_state.rejected_list)
        remaining = len(queue) - idx
        
        st.metric("✅ Approuvées", approved)
        st.metric("❌ Rejetées", rejected)
        st.metric("⏳ Restantes", remaining)
        
        st.markdown("---")
        
        # Boutons trois choix avec styles personnalisés
        col_trash, col_skip, col_keep = st.columns(3)
        
        with col_trash:
            st.markdown("""
            <style>
            .btn-trash {
                background-color: #1A1D29 !important;
                color: #ff4757 !important;
                border: 2px solid #ff4757 !important;
                border-radius: 8px !important;
                padding: 12px !important;
                font-weight: bold !important;
                transition: all 0.3s ease !important;
            }
            .btn-trash:hover {
                background-color: #ff4757 !important;
                color: white !important;
            }
            </style>
            """, unsafe_allow_html=True)
            if st.button("🗑️ POUBELLE", use_container_width=True, key="btn_trash", help="Supprimer du disque"):
                try:
                    os.remove(img_path)
                    st.session_state.curation_index += 1
                    st.success("🗑️ Effacé du disque")
                    st.rerun()
                except Exception as e:
                    st.error(f"❌ Impossible de supprimer: {e}")
        
        with col_skip:
            st.markdown("""
            <style>
            .btn-skip {
                background-color: #1A1D29 !important;
                color: #ffa500 !important;
                border: 2px solid #ffa500 !important;
                border-radius: 8px !important;
                padding: 12px !important;
                font-weight: bold !important;
                transition: all 0.3s ease !important;
            }
            .btn-skip:hover {
                background-color: #ffa500 !important;
                color: white !important;
            }
            </style>
            """, unsafe_allow_html=True)
            if st.button("⏭️ PASSER", use_container_width=True, key="btn_skip", help="Passer cette image"):
                st.session_state.curation_index += 1
                st.rerun()
        
        with col_keep:
            st.markdown("""
            <style>
            .btn-keep {
                background-color: #2e7d32 !important;
                color: white !important;
                border: none !important;
                border-radius: 8px !important;
                padding: 12px !important;
                font-weight: bold !important;
                transition: all 0.3s ease !important;
            }
            .btn-keep:hover {
                background-color: #388e3c !important;
                transform: translateY(-1px) !important;
            }
            </style>
            """, unsafe_allow_html=True)
            if st.button("✅ GARDER", use_container_width=True, key="btn_keep", help="Approuver cette image"):
                st.session_state.approved_list.append(img_path)
                st.session_state.curation_index += 1
                st.rerun()
        
        # Messages de feedback visuel
        if img_path in st.session_state.rejected_list:
            st.error("⛔ Image REJETÉE !")
        elif img_path in st.session_state.approved_list:
            st.success("🎉 Image APPROUVÉE !")

def render_grid_mode():
    st.subheader("🖼️ Sélection en Grille")
    queue = st.session_state.curation_queue
    
    st.info(f"Cochez les images à garder. ({len(st.session_state.approved_list)} déjà validées)")
    
    # Configuration de la grille (4 colonnes)
    cols = st.columns(4)
    for i, img_path in enumerate(queue):
        with cols[i % 4]:
            st.image(img_path, use_container_width=True)
            # On utilise le chemin comme clé unique
            is_checked = st.checkbox("Garder", key=f"grid_{img_path}", value=(img_path in st.session_state.approved_list))
            if is_checked and img_path not in st.session_state.approved_list:
                st.session_state.approved_list.append(img_path)
            elif not is_checked and img_path in st.session_state.approved_list:
                st.session_state.approved_list.remove(img_path)

    if st.button("💾 Finaliser la sélection", use_container_width=True):
        import shutil
        from core.config import Config
        
        # Create curated dataset folder
        dataset_name = st.session_state.get('current_dataset_name', 'dataset')
        curated_folder = Config.CURATED_DIR / dataset_name
        curated_folder.mkdir(parents=True, exist_ok=True)
        
        # Copy approved images to curated folder
        for img_path in st.session_state.approved_list:
            src = Path(img_path)
            dst = curated_folder / src.name
            shutil.copy2(src, dst)
        
        st.success(f"Fait ! {len(st.session_state.approved_list)} images sauvegardées dans {curated_folder} !")

def render():
    st.markdown("# 🧬 Curation & Sélection")

    # --- 1. SÉLECTION DU DATASET ---
    with st.expander("📁 Sélectionner mon Dataset", expanded=not st.session_state.curation_queue):
        if not Config.RAW_DIR.exists():
            st.error("Dossier RAW_DIR manquant.")
            return
            
        datasets = [d.name for d in Config.RAW_DIR.iterdir() if d.is_dir()]
        selected = st.selectbox("Choisir un dossier :", ["---"] + datasets)
        
        if st.button("🚀 Charger pour Curation") and selected != "---":
            load_dataset(selected)
            # Store current dataset name for saving
            st.session_state.current_dataset_name = selected

    if not st.session_state.curation_queue:
        st.info("💡 Chargez un dataset ci-dessus pour commencer le tri.")
        return

    # --- 2. NAVIGATION ---
    st.markdown("---")
    mode = st.radio("Mode de tri :", ["👉 Swipe Mode", "🖼️ Grid View"], horizontal=True)

    if "Swipe" in mode:
        render_swipe_mode()
    else:
        render_grid_mode()

    # --- 3. SAUVEGARDE FINALE ---
    if st.session_state.approved_list:
        st.markdown("---")
        st.markdown("### 💾 Sauvegarder le Dataset Trié")
        
        col1, col2 = st.columns([1, 1])
        with col1:
            st.metric("✅ Images approuvées", len(st.session_state.approved_list))
        with col2:
            st.metric("❌ Images rejetées", len(st.session_state.rejected_list))
        
        if st.button("💾 Enregistrer ce Dataset Trié", use_container_width=True, type="primary"):
            if 'current_dataset_name' in st.session_state:
                dataset_name = st.session_state.current_dataset_name
                curated_path = Config.CURATED_DIR / dataset_name
                curated_path.mkdir(parents=True, exist_ok=True)
                
                # Copier toutes les images approuvées (même si le tri n'est pas terminé)
                copied_count = 0
                for img_path in st.session_state.approved_list:
                    src_path = Path(img_path)
                    if src_path.exists():  # Vérifier que le fichier existe toujours
                        dst_path = curated_path / src_path.name
                        shutil.copy2(src_path, dst_path)
                        copied_count += 1
                
                # Afficher les statistiques
                total_processed = st.session_state.curation_index
                total_images = len(st.session_state.curation_queue)
                
                st.success(f"🎉 Dataset sauvegardé partiellement !")
                st.info(f"📍 {copied_count} images sauvegardées dans: {curated_path}")
                st.info(f"📊 Progression: {total_processed}/{total_images} images traitées")
                
                # Option de continuer ou terminer
                col_continue, col_finish = st.columns(2)
                with col_continue:
                    if st.button("🔄 Continuer le tri", key="continue_tri"):
                        st.rerun()
                with col_finish:
                    if st.button("✅ Terminer & Vider", key="finish_tri"):
                        # Vider la file d'attente
                        st.session_state.curation_queue = []
                        st.session_state.curation_index = 0
                        st.session_state.approved_list = []
                        st.session_state.rejected_list = []
                        st.success("🎉 Dataset prêt pour la Factory !")
                        st.balloons()
                        st.rerun()
            else:
                st.error("⚠️ Aucun dataset sélectionné.")
