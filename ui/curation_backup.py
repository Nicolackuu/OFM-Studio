"""
OFM IA Studio - Curation Module (Independent)
Mode Tinder pour la curation d'images
"""
import streamlit as st
from pathlib import Path
import shutil
from core.config import Config
from ui.components import info_box, tinder_card

def render():
    st.markdown("# 🧬 Curation")
    
    # --- LE SÉLECTEUR DE MODE (RESTAURATION VISUELLE) ---
    mode = st.radio(
        "Mode de sélection :",
        ["🔥 Tinder Swap", "📸 Grid View", "📦 Batch Process"],
        horizontal=True,
        key="curation_mode_selector"
    )

    # Dispatcher vers la bonne fonction selon le choix
    if "Tinder" in mode:
        render_tinder_mode()
    elif "Grid" in mode:
        render_grid_mode()
    else:
        render_batch_mode()

def render_tinder_mode():
    """Render Tinder-style curation mode"""
    st.markdown("### 🔥 Tinder Mode - Swipe Interface")
    
    # Sécurité pour éviter les crashs
    if not st.session_state.curation_queue:
        st.info("ℹ️ La file d'attente est vide. Scrappez des images d'abord.")
        return
        
    # Dataset selector
    st.markdown("## 📁 Sélection du Dataset")
    
    raw_base_dir = Config.BASE_DIR / "DATASET" / "RAW"
    raw_base_dir.mkdir(parents=True, exist_ok=True)
    
    existing_datasets = [d.name for d in raw_base_dir.iterdir() if d.is_dir()]
    
    if not existing_datasets:
        info_box("⚠️ Aucun dataset trouvé dans DATASET/RAW/. Utilisez le Scraper pour en télécharger.", "warning")
        st.info("💡 Allez dans **Scraper** pour télécharger des images Instagram")
        return
    
    col_select, col_load = st.columns([3, 1])
    
    with col_select:
        selected_dataset = st.selectbox(
            "Choisir un dataset existant",
            options=existing_datasets,
            index=existing_datasets.index(st.session_state.current_username) if st.session_state.current_username in existing_datasets else 0,
            key="curation_dataset_selector"
        )
    
    with col_load:
        if st.button("� Charger", use_container_width=True, key="curation_load_btn"):
            st.session_state.current_username = selected_dataset
            # Reset curation state when loading new dataset
            if 'curation_queue' in st.session_state:
                st.session_state.curation_queue = []
                st.session_state.curation_index = 0
            if "approved_list" in st.session_state:
                st.session_state.approved_list = []
            if "rejected_list" in st.session_state:
                st.session_state.rejected_list = []
            info_box(f"✓ Dataset '{selected_dataset}' chargé!", "success")
            st.rerun()
    
    # Curation workflow
    if st.session_state.current_username:
        raw_dir = Config.BASE_DIR / "DATASET" / "RAW" / st.session_state.current_username
        
        if not raw_dir.exists():
            info_box("Dossier dataset non trouvé", "error")
            return
        
        # Load images into queue
        if not st.session_state.curation_queue:
            image_extensions = ['.jpg', '.jpeg', '.png', '.webp']
            images = []
            for ext in image_extensions:
                images.extend(raw_dir.glob(f"*{ext}"))
                images.extend(raw_dir.glob(f"*{ext.upper()}"))
            
            if images:
                st.session_state.curation_queue = sorted([str(img) for img in images])
                st.session_state.curation_index = 0
                info_box(f"✓ {len(images)} images chargées dans la file d'attente", "success")
                st.rerun()
            else:
                info_box("Aucune image trouvée dans le dataset", "warning")
                return
        
        # Display current image
        index = st.session_state.curation_index
        if index < len(st.session_state.curation_queue):
            current_image = st.session_state.curation_queue[index]
            
            col1, col2, col3 = st.columns([1, 3, 1])
            
            with col2:
                st.image(current_image, use_container_width=True, caption=f"Image {index + 1}/{len(st.session_state.curation_queue)}")
            
            # Action buttons
            col_reject, col_skip, col_approve = st.columns(3)
            
            with col_reject:
                if st.button("❌ Rejeter", use_container_width=True, key="reject_tinder"):
                    if "rejected_list" not in st.session_state:
                        st.session_state.rejected_list = []
                    st.session_state.rejected_list.append(current_image)
                    st.session_state.curation_index += 1
                    st.rerun()
            
            with col_skip:
                if st.button("⏭️ Passer", use_container_width=True, key="skip_tinder"):
                    st.session_state.curation_index += 1
                    st.rerun()
            
            with col_approve:
                if st.button("✅ Approuver", use_container_width=True, type="primary", key="approve_tinder"):
                    st.session_state.approved_list.append(current_image)
                    st.session_state.curation_index += 1
                    st.rerun()
            
            # Stats
            approved = len(st.session_state.approved_list)
            rejected = len(st.session_state.rejected_list)
            remaining = len(st.session_state.curation_queue) - index
            
            st.markdown("---")
            col1, col2, col3 = st.columns(3)
            with col1:
                st.metric("✅ Approuvées", approved)
            with col2:
                st.metric("❌ Rejetées", rejected)
            with col3:
                st.metric("⏳ Restantes", remaining)
        else:
            st.success("🎉 Curation terminée!")
            if st.session_state.approved_list:
                st.info(f"✅ {len(st.session_state.approved_list)} images approuvées")

def render_grid_mode():
    """Render grid view mode"""
    st.markdown("### 📸 Grid Mode - Vue d'ensemble")
    st.info("💡 Mode Grid en cours de développement...")

def render_batch_mode():
    """Render batch process mode"""
    st.markdown("### 📦 Batch Mode - Traitement par lots")
    st.info("💡 Mode Batch en cours de développement...")
    
    # Dataset selector
    st.markdown("## 📁 Sélection du Dataset")
    
    raw_base_dir = Config.BASE_DIR / "DATASET" / "RAW"
    raw_base_dir.mkdir(parents=True, exist_ok=True)
    
    # List all existing datasets
    existing_datasets = [d.name for d in raw_base_dir.iterdir() if d.is_dir()]
    
    if not existing_datasets:
        info_box("⚠️ Aucun dataset trouvé dans DATASET/RAW/. Utilisez le Scraper pour en télécharger.", "warning")
        st.info("💡 Allez dans **Scraper** pour télécharger des images Instagram")
        return
    
    col_select, col_load = st.columns([3, 1])
    
    with col_select:
        selected_dataset = st.selectbox(
            "Choisir un dataset existant",
            options=existing_datasets,
            index=existing_datasets.index(st.session_state.current_username) if st.session_state.current_username in existing_datasets else 0,
            key="curation_dataset_selector"
        )
    
    with col_load:
        if st.button("📂 Charger", use_container_width=True, key="curation_load_btn"):
            st.session_state.current_username = selected_dataset
            # Reset curation state when loading new dataset
            if 'curation_queue' in st.session_state:
                st.session_state.curation_queue = []
                st.session_state.curation_index = 0
            if "approved_list" in st.session_state:
                st.session_state.approved_list = []
            if "rejected_list" in st.session_state:
                st.session_state.rejected_list = []
            info_box(f"✓ Dataset '{selected_dataset}' chargé!", "success")
            st.rerun()
    
    st.markdown("<div style='height: 32px;'></div>", unsafe_allow_html=True)
    
    # Curation workflow
    if st.session_state.current_username:
        raw_dir = Config.BASE_DIR / "DATASET" / "RAW" / st.session_state.current_username
        
        if not raw_dir.exists():
            info_box("❌ Dossier RAW non trouvé", "error")
            return
        
        # Load images
        image_files = []
        for ext in ['.jpg', '.jpeg', '.png']:
            image_files.extend(raw_dir.glob(f"*{ext}"))
        
        if not image_files:
            info_box("⚠️ Aucune image trouvée dans le dossier RAW", "warning")
            return
        
        # Display dataset info
        info_box(f"📊 Dataset: @{st.session_state.current_username} ({len(image_files)} images)", "info")
        
        st.markdown("<div style='height: 24px;'></div>", unsafe_allow_html=True)
        
        # Initialize queue with LOCKED state management
        if 'curation_queue' not in st.session_state:
            st.session_state.curation_queue = list(image_files)
            st.session_state.curation_index = 0
            st.session_state.approved_list = []
            st.session_state.rejected_list = []
        
        # Callback functions to prevent index reset
        def reject_image():
            if st.session_state.curation_index < len(st.session_state.curation_queue):
                current_img = st.session_state.curation_queue[st.session_state.curation_index]
                st.session_state.rejected_list.append(current_img)
                st.session_state.curation_index += 1
        
        def skip_image():
            if st.session_state.curation_index < len(st.session_state.curation_queue):
                st.session_state.curation_index += 1
        
        def keep_image():
            if st.session_state.curation_index < len(st.session_state.curation_queue):
                current_img = st.session_state.curation_queue[st.session_state.curation_index]
                st.session_state.approved_list.append(current_img)
                st.session_state.curation_index += 1
        
        # Check if curation is complete
        if st.session_state.curation_index < len(st.session_state.curation_queue):
            current_img = st.session_state.curation_queue[st.session_state.curation_index]
            
            # Linear-style progress bar
            current_num = st.session_state.curation_index + 1
            total_num = len(st.session_state.curation_queue)
            progress_pct = (current_num / total_num) * 100
            
            st.markdown(f"""
            <div style="
                background: linear-gradient(90deg, #10b981 0%, #10b981 {progress_pct}%, #1f2937 {progress_pct}%, #1f2937 100%);
                height: 8px;
                border-radius: 4px;
                margin-bottom: 8px;
            "></div>
            <div style="
                font-family: 'Inter', -apple-system, sans-serif;
                font-size: 13px;
                color: #9ca3af;
                text-align: center;
                margin-bottom: 24px;
                font-weight: 500;
            ">Image {current_num} sur {total_num}</div>
            """, unsafe_allow_html=True)
            
            # Tinder card
            col1, col2, col3 = st.columns([1, 2, 1])
            
            with col2:
                tinder_card(current_img, st.session_state.curation_index, len(st.session_state.curation_queue))
                
                st.markdown("<div style='height: 24px;'></div>", unsafe_allow_html=True)
                
                # Action buttons with callbacks
                col_reject, col_skip, col_keep = st.columns(3)
                
                with col_reject:
                    st.button(
                        "❌ REJETER",
                        use_container_width=True,
                        key="curation_reject_btn",
                        on_click=reject_image,
                        type="secondary"
                    )
                
                with col_skip:
                    st.button(
                        "⏭️ SKIP",
                        use_container_width=True,
                        key="curation_skip_btn",
                        on_click=skip_image
                    )
                
                with col_keep:
                    st.button(
                        "✅ GARDER",
                        use_container_width=True,
                        key="curation_keep_btn",
                        on_click=keep_image,
                        type="primary"
                    )
                
                # Real-time stats
                st.markdown("<div style='height: 24px;'></div>", unsafe_allow_html=True)
                
                col_stats1, col_stats2 = st.columns(2)
                with col_stats1:
                    st.markdown(f"""
                    <div style="
                        background: #1f2937;
                        border: 1px solid #374151;
                        border-radius: 8px;
                        padding: 12px;
                        text-align: center;
                    ">
                        <div style="color: #10b981; font-size: 24px; font-weight: 600;">{len(st.session_state.approved_list)}</div>
                        <div style="color: #9ca3af; font-size: 12px; margin-top: 4px;">✅ Gardées</div>
                    </div>
                    """, unsafe_allow_html=True)
                
                with col_stats2:
                    st.markdown(f"""
                    <div style="
                        background: #1f2937;
                        border: 1px solid #374151;
                        border-radius: 8px;
                        padding: 12px;
                        text-align: center;
                    ">
                        <div style="color: #ef4444; font-size: 24px; font-weight: 600;">{len(st.session_state.rejected_list)}</div>
                        <div style="color: #9ca3af; font-size: 12px; margin-top: 4px;">❌ Rejetées</div>
                    </div>
                    """, unsafe_allow_html=True)
        
        else:
            # Curation complete
            info_box(f"✓ Curation terminée! {len(st.session_state.approved_list)} images gardées", "success")
            
            st.markdown("---")
            
            col1, col2 = st.columns(2)
            
            with col1:
                st.metric("✅ Images Gardées", len(st.session_state.approved_list))
            
            with col2:
                # On récupère la longueur avec une valeur par défaut de 0 si la liste n'existe pas
                rejected_count = len(st.session_state.get('rejected_list', []))
                st.metric("❌ Images Rejetées", rejected_count)
            
            st.markdown("---")
            
            if st.button("💾 Sauvegarder la Sélection", use_container_width=True, type="primary", key="curation_save_btn"):
                approved_dir = Config.BASE_DIR / "DATASET" / "APPROVED"
                approved_dir.mkdir(parents=True, exist_ok=True)
                
                for idx, img_path in enumerate(st.session_state.approved_list, 1):
                    new_name = f"dataset_{idx:03d}{img_path.suffix}"
                    dest_path = approved_dir / new_name
                    shutil.copy2(img_path, dest_path)
                
                st.session_state.approved_images = [str(approved_dir / f"dataset_{i:03d}.jpg") for i in range(1, len(st.session_state.approved_list) + 1)]
                
                info_box(f"✓ {len(st.session_state.approved_list)} images sauvegardées dans DATASET/APPROVED/", "success")
                st.balloons()
            
            if st.button("🔄 Recommencer la Curation", use_container_width=True, key="curation_restart_btn"):
                del st.session_state.curation_queue
                del st.session_state.curation_index
                del st.session_state.approved_list
                del st.session_state.rejected_list
                st.rerun()
    else:
        st.info("💡 Sélectionnez un dataset ci-dessus pour commencer la curation")
