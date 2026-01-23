"""
Curation Premium - Modern Photo Curation UI
Tinder-style swipe interface with quality filters and batch operations
"""
import streamlit as st
from pathlib import Path
from typing import List
import shutil
from core.config import Config
from core.photo_curator import PhotoCurator, QualityAnalyzer


def render():
    """Render the premium curation page"""
    st.markdown("# 🎯 Photo Curation Premium")
    st.markdown("### Sélection intelligente avec filtres qualité")
    
    st.markdown("<div style='height: 24px;'></div>", unsafe_allow_html=True)
    
    # Initialize session state
    if 'curator' not in st.session_state:
        st.session_state.curator = None
    if 'curation_mode' not in st.session_state:
        st.session_state.curation_mode = "tinder"
    if 'current_curation_index' not in st.session_state:
        st.session_state.current_curation_index = 0
    
    # === DATASET SELECTOR ===
    st.markdown("## 📁 Sélection du Dataset")
    
    raw_base_dir = Config.BASE_DIR / "DATASET" / "RAW"
    raw_base_dir.mkdir(parents=True, exist_ok=True)
    
    existing_datasets = [d.name for d in raw_base_dir.iterdir() if d.is_dir()]
    
    if not existing_datasets:
        st.warning("⚠️ Aucun dataset trouvé dans DATASET/RAW/")
        st.info("💡 Utilisez le **Scraper** pour télécharger des images Instagram")
        return
    
    col_select, col_load = st.columns([3, 1])
    
    with col_select:
        selected_dataset = st.selectbox(
            "Dataset",
            options=existing_datasets,
            key="curation_dataset_selector"
        )
    
    with col_load:
        if st.button("📂 Charger", use_container_width=True, key="load_dataset_curation"):
            dataset_path = raw_base_dir / selected_dataset
            st.session_state.curator = PhotoCurator(dataset_path)
            st.session_state.curator.load_dataset()
            st.session_state.current_curation_index = 0
            st.success(f"✓ {len(st.session_state.curator.images)} images chargées")
            st.rerun()
    
    if st.session_state.curator is None:
        st.info("💡 Chargez un dataset pour commencer")
        return
    
    curator = st.session_state.curator
    
    # === QUALITY FILTERS ===
    st.markdown("---")
    st.markdown("## 🔍 Filtres Qualité")
    
    with st.expander("⚙️ Configuration des filtres", expanded=False):
        col1, col2, col3 = st.columns(3)
        
        with col1:
            min_width = st.number_input("Largeur min (px)", min_value=256, max_value=2048, value=512, step=64)
            min_height = st.number_input("Hauteur min (px)", min_value=256, max_value=2048, value=512, step=64)
        
        with col2:
            blur_threshold = st.slider("Seuil de netteté", min_value=0.0, max_value=100.0, value=30.0, step=5.0)
            st.caption("Plus élevé = plus strict")
        
        with col3:
            require_face = st.checkbox("Exiger 1 visage", value=False)
            st.caption("Détection automatique")
        
        if st.button("🔍 Appliquer les filtres", use_container_width=True):
            with st.spinner("Analyse en cours..."):
                filtered = curator.apply_quality_filters(
                    min_resolution=(min_width, min_height),
                    max_blur_threshold=blur_threshold,
                    require_face=require_face
                )
                
                st.success(f"✓ {len(filtered)}/{len(curator.images)} images passent les filtres")
                
                # Update curator images to filtered list
                curator.images = filtered
                st.session_state.current_curation_index = 0
                st.rerun()
    
    # === STATS PANEL ===
    st.markdown("---")
    st.markdown("## 📊 Statistiques")
    
    stats = curator.get_stats()
    
    col1, col2, col3, col4 = st.columns(4)
    
    with col1:
        st.metric("Total", stats['total'])
    with col2:
        st.metric("✅ Gardées", stats['approved'], delta=None)
    with col3:
        st.metric("❌ Rejetées", stats['rejected'], delta=None)
    with col4:
        st.metric("⏳ En attente", stats['pending'], delta=None)
    
    # Progress bar
    if stats['total'] > 0:
        progress = stats['progress_pct'] / 100
        st.progress(progress, text=f"Progression: {stats['progress_pct']:.1f}%")
    
    # === CURATION MODE SELECTOR ===
    st.markdown("---")
    st.markdown("## 🎴 Mode de Curation")
    
    mode_col1, mode_col2, mode_col3 = st.columns(3)
    
    with mode_col1:
        if st.button("👆 Tinder Mode", use_container_width=True, type="primary" if st.session_state.curation_mode == "tinder" else "secondary"):
            st.session_state.curation_mode = "tinder"
            st.rerun()
    
    with mode_col2:
        if st.button("🔲 Grid Mode", use_container_width=True, type="primary" if st.session_state.curation_mode == "grid" else "secondary"):
            st.session_state.curation_mode = "grid"
            st.rerun()
    
    with mode_col3:
        if st.button("☑️ Batch Mode", use_container_width=True, type="primary" if st.session_state.curation_mode == "batch" else "secondary"):
            st.session_state.curation_mode = "batch"
            st.rerun()
    
    st.markdown("<div style='height: 24px;'></div>", unsafe_allow_html=True)
    
    # === RENDER SELECTED MODE ===
    if st.session_state.curation_mode == "tinder":
        render_tinder_mode(curator)
    elif st.session_state.curation_mode == "grid":
        render_grid_mode(curator)
    elif st.session_state.curation_mode == "batch":
        render_batch_mode(curator)
    
    # === EXPORT PANEL ===
    st.markdown("---")
    st.markdown("## 💾 Export")
    
    if stats['approved'] > 0:
        col1, col2 = st.columns([2, 1])
        
        with col1:
            format_template = st.text_input("Format de nommage", value="dataset_{idx:03d}", key="export_format")
            st.caption("Utilisez {idx} pour le numéro d'index")
        
        with col2:
            st.markdown("<div style='height: 24px;'></div>", unsafe_allow_html=True)
            if st.button("💾 Exporter les images gardées", use_container_width=True, type="primary"):
                approved_dir = Config.BASE_DIR / "DATASET" / "APPROVED"
                
                with st.spinner("Export en cours..."):
                    count = curator.export_approved(approved_dir, format_template=format_template)
                    st.success(f"✅ {count} images exportées vers DATASET/APPROVED/")
                    st.balloons()
    else:
        st.info("💡 Gardez des images pour activer l'export")


def render_tinder_mode(curator: PhotoCurator):
    """Render Tinder-style swipe interface"""
    st.markdown("### 👆 Tinder Mode")
    
    # Get pending images (not approved or rejected)
    pending = [img for img in curator.images if img not in curator.approved and img not in curator.rejected]
    
    if not pending:
        st.success("✅ Toutes les images ont été traitées!")
        
        if st.button("🔄 Recommencer"):
            curator.approved.clear()
            curator.rejected.clear()
            curator.history.clear()
            st.session_state.current_curation_index = 0
            st.rerun()
        return
    
    # Current image
    current_img = pending[0]
    current_num = len(curator.approved) + len(curator.rejected) + 1
    total_num = len(curator.images)
    
    # Display image
    col_spacer1, col_img, col_spacer2 = st.columns([1, 3, 1])
    
    with col_img:
        try:
            st.image(str(current_img), use_container_width=True, caption=current_img.name)
        except Exception as e:
            st.error(f"❌ Impossible de charger l'image: {current_img.name}")
    
    st.markdown("<div style='height: 24px;'></div>", unsafe_allow_html=True)
    
    # Action buttons
    col1, col2, col3, col4 = st.columns([1, 1, 1, 1])
    
    with col1:
        if st.button("❌ Rejeter", use_container_width=True, key="reject_tinder"):
            curator.manual_reject(current_img)
            st.rerun()
    
    with col2:
        if st.button("⏭️ Passer", use_container_width=True, key="skip_tinder"):
            # Move to end of list
            curator.images.remove(current_img)
            curator.images.append(current_img)
            st.rerun()
    
    with col3:
        if st.button("✅ Garder", use_container_width=True, type="primary", key="approve_tinder"):
            curator.manual_approve(current_img)
            st.rerun()
    
    with col4:
        if st.button("↶ Annuler", use_container_width=True, key="undo_tinder"):
            if curator.undo():
                st.success("✓ Action annulée")
                st.rerun()
            else:
                st.warning("Rien à annuler")


def render_grid_mode(curator: PhotoCurator):
    """Render grid view with 9 images"""
    st.markdown("### 🔲 Grid Mode")
    
    pending = [img for img in curator.images if img not in curator.approved and img not in curator.rejected]
    
    if not pending:
        st.success("✅ Toutes les images ont été traitées!")
        return
    
    # Show 9 images at a time
    images_per_page = 9
    start_idx = st.session_state.current_curation_index
    end_idx = min(start_idx + images_per_page, len(pending))
    current_batch = pending[start_idx:end_idx]
    
    # Display in 3x3 grid
    for row in range(3):
        cols = st.columns(3)
        for col_idx, col in enumerate(cols):
            img_idx = row * 3 + col_idx
            if img_idx < len(current_batch):
                img_path = current_batch[img_idx]
                
                with col:
                    try:
                        st.image(str(img_path), use_container_width=True, caption=img_path.name[:20])
                    except:
                        st.error("❌ Erreur")
                    
                    col_btn1, col_btn2 = st.columns(2)
                    with col_btn1:
                        if st.button("❌", key=f"reject_grid_{img_idx}", use_container_width=True):
                            curator.manual_reject(img_path)
                            st.rerun()
                    with col_btn2:
                        if st.button("✅", key=f"approve_grid_{img_idx}", use_container_width=True):
                            curator.manual_approve(img_path)
                            st.rerun()
    
    # Navigation
    st.markdown("<div style='height: 24px;'></div>", unsafe_allow_html=True)
    col_prev, col_info, col_next = st.columns([1, 2, 1])
    
    with col_prev:
        if start_idx > 0:
            if st.button("⬅️ Précédent", use_container_width=True):
                st.session_state.current_curation_index = max(0, start_idx - images_per_page)
                st.rerun()
    
    with col_info:
        st.markdown(f"<div style='text-align: center;'>Page {start_idx // images_per_page + 1} / {(len(pending) - 1) // images_per_page + 1}</div>", unsafe_allow_html=True)
    
    with col_next:
        if end_idx < len(pending):
            if st.button("➡️ Suivant", use_container_width=True):
                st.session_state.current_curation_index = end_idx
                st.rerun()


def render_batch_mode(curator: PhotoCurator):
    """Render batch selection mode"""
    st.markdown("### ☑️ Batch Mode")
    
    pending = [img for img in curator.images if img not in curator.approved and img not in curator.rejected]
    
    if not pending:
        st.success("✅ Toutes les images ont été traitées!")
        return
    
    st.info("💡 Cochez les images à garder, puis cliquez sur 'Approuver la sélection'")
    
    # Selection state
    if 'batch_selection' not in st.session_state:
        st.session_state.batch_selection = []
    
    # Display images with checkboxes
    images_per_row = 4
    for i in range(0, len(pending), images_per_row):
        cols = st.columns(images_per_row)
        for col_idx, col in enumerate(cols):
            img_idx = i + col_idx
            if img_idx < len(pending):
                img_path = pending[img_idx]
                
                with col:
                    try:
                        st.image(str(img_path), use_container_width=True)
                    except:
                        st.error("❌")
                    
                    is_selected = st.checkbox(
                        img_path.name[:15],
                        key=f"batch_check_{img_idx}",
                        value=img_path in st.session_state.batch_selection
                    )
                    
                    if is_selected and img_path not in st.session_state.batch_selection:
                        st.session_state.batch_selection.append(img_path)
                    elif not is_selected and img_path in st.session_state.batch_selection:
                        st.session_state.batch_selection.remove(img_path)
    
    # Batch actions
    st.markdown("<div style='height: 24px;'></div>", unsafe_allow_html=True)
    
    col1, col2, col3 = st.columns([1, 1, 1])
    
    with col1:
        if st.button(f"✅ Approuver la sélection ({len(st.session_state.batch_selection)})", use_container_width=True, type="primary"):
            if st.session_state.batch_selection:
                curator.batch_approve(st.session_state.batch_selection)
                st.session_state.batch_selection.clear()
                st.success(f"✓ {len(st.session_state.batch_selection)} images approuvées")
                st.rerun()
    
    with col2:
        if st.button("❌ Rejeter la sélection", use_container_width=True):
            if st.session_state.batch_selection:
                curator.batch_reject(st.session_state.batch_selection)
                st.session_state.batch_selection.clear()
                st.rerun()
    
    with col3:
        if st.button("🔄 Tout désélectionner", use_container_width=True):
            st.session_state.batch_selection.clear()
            st.rerun()
