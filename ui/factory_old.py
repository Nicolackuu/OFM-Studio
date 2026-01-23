"""
Factory Page - Dataset Production (Curation + Face Swap)
"""
import streamlit as st
from pathlib import Path
from core.config import Config
from core.batch_face_swap import BatchFaceSwap
from ui.components import info_box, tinder_card, console_output, progress_tracker, gallery_grid
import shutil

def render():
    """Render factory page"""
    
    # Sécurité locale - Initialisation des variables de session
    if "curation_index" not in st.session_state:
        st.session_state.curation_index = 0
    if "curation_queue" not in st.session_state:
        st.session_state.curation_queue = []
    if "approved_list" not in st.session_state:
        st.session_state.approved_list = []
    if "rejected_list" not in st.session_state:
        st.session_state.rejected_list = []
    if "source_face" not in st.session_state:
        st.session_state.source_face = None
    if "approved_images" not in st.session_state:
        st.session_state.approved_images = []
    
    st.title("🏭 Usine Dataset LoRa")
    
    tab1, tab2, tab3 = st.tabs(["1️⃣ Source Face", "2️⃣ Curation Tinder", "3️⃣ Production"])
    
    # === TAB 1: SOURCE FACE ===
    with tab1:
        st.markdown("### 🎯 Sélection du Visage Source")
        
        col1, col2 = st.columns([1, 1])
        
        with col1:
            st.markdown("#### 📁 Images Générées")
            
            generated_dir = Config.OUTPUT_DIR
            if generated_dir.exists():
                image_files = list(generated_dir.glob("*.png")) + list(generated_dir.glob("*.jpg"))
                image_files.sort(key=lambda x: x.stat().st_mtime, reverse=True)
                
                if image_files:
                    selected_image = st.selectbox(
                        "Choisir une image",
                        options=[str(f) for f in image_files[:20]],
                        format_func=lambda x: Path(x).name,
                        key="source_face_select"
                    )
                    
                    if st.button("✅ Définir comme Source Face", use_container_width=True):
                        st.session_state.source_face = selected_image
                        info_box(f"✓ Source Face définie: {Path(selected_image).name}", "success")
                        st.rerun()
                else:
                    info_box("Aucune image générée. Allez sur la page Casting d'abord.", "warning")
            else:
                info_box("Dossier de génération non trouvé", "error")
        
        with col2:
            st.markdown("#### 🖼️ Aperçu Source Face")
            
            if st.session_state.source_face:
                source_path = Path(st.session_state.source_face)
                if source_path.exists():
                    st.markdown('<div class="image-preview">', unsafe_allow_html=True)
                    st.image(str(source_path), use_container_width=True, caption=source_path.name)
                    st.markdown('</div>', unsafe_allow_html=True)
                    
                    info_box("✓ Source face prête pour le face swap", "success")
                else:
                    info_box("Fichier source introuvable", "error")
            else:
                st.info("Aucune source face sélectionnée")
    
    # === TAB 2: TINDER CURATION ===
    with tab2:
        st.markdown("### ✅ Curation Mode Tinder")
        
        # Dataset selector - Load existing or use scraped
        st.markdown("#### 📁 Sélection du Dataset")
        
        raw_base_dir = Config.BASE_DIR / "DATASET" / "RAW"
        raw_base_dir.mkdir(parents=True, exist_ok=True)
        
        # List all existing datasets
        existing_datasets = [d.name for d in raw_base_dir.iterdir() if d.is_dir()]
        
        if existing_datasets:
            col_select, col_load = st.columns([3, 1])
            
            with col_select:
                selected_dataset = st.selectbox(
                    "Choisir un dataset existant",
                    options=existing_datasets,
                    index=existing_datasets.index(st.session_state.current_username) if st.session_state.current_username in existing_datasets else 0,
                    key="dataset_selector"
                )
            
            with col_load:
                if st.button("📂 Charger", use_container_width=True, key="load_dataset_btn"):
                    st.session_state.current_username = selected_dataset
                    # Reset curation state when loading new dataset
                    if 'curation_queue' in st.session_state:
                        st.session_state.curation_queue = []
                        st.session_state.curation_index = 0
                    if "approved_list" in st.session_state:
                        st.session_state.approved_list = []  # On vide la liste proprement au lieu de la supprimer
                    if "rejected_list" in st.session_state:
                        st.session_state.rejected_list = []
                    info_box(f"✓ Dataset '{selected_dataset}' chargé!", "success")
                    st.rerun()
            
            st.markdown("<div style='height: 16px;'></div>", unsafe_allow_html=True)
        else:
            info_box("⚠️ Aucun dataset trouvé dans DATASET/RAW/. Utilisez le Scraper pour en télécharger.", "warning")
        
        # Curation workflow
        if st.session_state.current_username:
            raw_dir = Config.BASE_DIR / "DATASET" / "RAW" / st.session_state.current_username
            
            if raw_dir.exists():
                image_files = []
                for ext in ['.jpg', '.jpeg', '.png']:
                    image_files.extend(raw_dir.glob(f"*{ext}"))
                
                if image_files:
                    info_box(f"📊 Dataset: @{st.session_state.current_username} ({len(image_files)} images)", "info")
                    
                    st.markdown("<div style='height: 16px;'></div>", unsafe_allow_html=True)
                    
                    # Initialize queue with LOCKED state management
                    if 'curation_queue' not in st.session_state:
                        st.session_state.curation_queue = list(image_files)
                        st.session_state.curation_index = 0
                        st.session_state.approved_list = []
                        st.session_state.rejected_list = []
                    
                    # Callback functions to prevent index reset
                    def reject_image():
                        current_img = st.session_state.curation_queue[st.session_state.curation_index]
                        st.session_state.rejected_list.append(current_img)
                        st.session_state.curation_index += 1
                    
                    def skip_image():
                        st.session_state.curation_index += 1
                    
                    def keep_image():
                        current_img = st.session_state.curation_queue[st.session_state.curation_index]
                        st.session_state.approved_list.append(current_img)
                        st.session_state.curation_index += 1
                    
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
                                    key="reject_btn",
                                    on_click=reject_image,
                                    type="secondary"
                                )
                            
                            with col_skip:
                                st.button(
                                    "⏭️ SKIP",
                                    use_container_width=True,
                                    key="skip_btn",
                                    on_click=skip_image
                                )
                            
                            with col_keep:
                                st.button(
                                    "✅ GARDER",
                                    use_container_width=True,
                                    key="keep_btn",
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
                            st.metric("❌ Images Rejetées", len(st.session_state.rejected_list))
                        
                        st.markdown("---")
                        
                        if st.button("💾 Sauvegarder la Sélection", use_container_width=True, type="primary"):
                            approved_dir = Config.BASE_DIR / "DATASET" / "APPROVED"
                            approved_dir.mkdir(parents=True, exist_ok=True)
                            
                            for idx, img_path in enumerate(st.session_state.approved_list, 1):
                                new_name = f"dataset_{idx:03d}{img_path.suffix}"
                                dest_path = approved_dir / new_name
                                shutil.copy2(img_path, dest_path)
                            
                            st.session_state.approved_images = [str(approved_dir / f"dataset_{i:03d}.jpg") for i in range(1, len(st.session_state.approved_list) + 1)]
                            
                            info_box(f"✓ {len(st.session_state.approved_list)} images sauvegardées dans DATASET/APPROVED/", "success")
                            st.balloons()
                        
                        if st.button("🔄 Recommencer la Curation", use_container_width=True):
                            del st.session_state.curation_queue
                            del st.session_state.curation_index
                            del st.session_state.approved_list
                            del st.session_state.rejected_list
                            st.rerun()
                else:
                    info_box("Aucune image trouvée dans le dossier RAW", "warning")
            else:
                info_box("Dossier RAW non trouvé", "error")
        else:
            st.info("💡 Sélectionnez un dataset ci-dessus pour commencer la curation")
    
    # === TAB 3: PRODUCTION (FACE SWAP) ===
    with tab3:
        st.markdown("### 🚀 Production Face Swap")
        
        # Check prerequisites
        if not st.session_state.source_face:
            info_box("❌ Sélectionnez une source face dans l'onglet 1", "error")
        elif not st.session_state.approved_images:
            # Try to load from APPROVED folder
            approved_dir = Config.BASE_DIR / "DATASET" / "APPROVED"
            if approved_dir.exists():
                approved_files = list(approved_dir.glob("dataset_*.png")) + list(approved_dir.glob("dataset_*.jpg"))
                if approved_files:
                    st.session_state.approved_images = [str(f) for f in approved_files]
                else:
                    info_box("❌ Aucune image approuvée. Complétez la curation dans l'onglet 2", "error")
            else:
                info_box("❌ Aucune image approuvée. Complétez la curation dans l'onglet 2", "error")
        
        if st.session_state.source_face and st.session_state.approved_images:
            col1, col2 = st.columns([1, 1])
            
            with col1:
                st.markdown("#### ⚙️ Configuration")
                
                info_box(f"📎 Source Face: {Path(st.session_state.source_face).name}", "info")
                info_box(f"📊 Images à traiter: {len(st.session_state.approved_images)}", "info")
                
                st.markdown("---")
                
                # ONE-IMAGE TEST MODE (NEW)
                st.markdown("#### 🧪 Mode Test (1 Image)")
                st.info("💡 Testez l'API avec une seule image pour vérifier que tout fonctionne")
                
                if 'test_result' not in st.session_state:
                    st.session_state.test_result = None
                
                if st.button("🔄 Test Face Swap (1 Image)", use_container_width=True, key="test_one_image"):
                    final_dir = Config.BASE_DIR / "DATASET" / "FINAL_LORA"
                    final_dir.mkdir(parents=True, exist_ok=True)
                    
                    with st.spinner("🔄 Test en cours..."):
                        try:
                            from core.batch_face_swap import BatchFaceSwap
                            processor = BatchFaceSwap(Path(st.session_state.source_face), final_dir)
                            
                            # Process only first image
                            test_image = Path(st.session_state.approved_images[0])
                            st.write(f"📸 Test avec: {test_image.name}")
                            
                            success = processor.process_batch([test_image])
                            
                            if success and processor.stats['success'] > 0:
                                st.session_state.test_result = "success"
                                st.success(f"✅ Test réussi! Image générée dans FINAL_LORA/")
                                
                                # Show result
                                result_files = list(final_dir.glob("lora_*.png"))
                                if result_files:
                                    latest = max(result_files, key=lambda p: p.stat().st_mtime)
                                    st.image(str(latest), caption="Résultat du test", use_container_width=True)
                            else:
                                st.session_state.test_result = "failed"
                                st.error("❌ Test échoué. Vérifiez les logs console.")
                                st.info("💡 Vérifiez que l'API key est valide et que les images sont correctes.")
                        
                        except Exception as e:
                            st.session_state.test_result = "error"
                            st.error(f"❌ Erreur: {str(e)}")
                            st.code(str(e), language="python")
                
                st.markdown("---")
                
                # BATCH MODE (ORIGINAL)
                st.markdown("#### 🚀 Mode Batch (Toutes les Images)")
                
                if st.button("🚀 LANCER LE FACE SWAP COMPLET", use_container_width=True, type="primary"):
                    final_dir = Config.BASE_DIR / "DATASET" / "FINAL_LORA"
                    final_dir.mkdir(parents=True, exist_ok=True)
                    
                    # Initialize console logs
                    if 'console_logs' not in st.session_state:
                        st.session_state.console_logs = []
                    
                    st.session_state.console_logs = []
                    st.session_state.console_logs.append("🚀 Initialisation du Face Swap...")
                    st.session_state.console_logs.append(f"📁 Source: {Path(st.session_state.source_face).name}")
                    st.session_state.console_logs.append(f"📊 Total images: {len(st.session_state.approved_images)}")
                    st.session_state.console_logs.append("=" * 60)
                    
                    progress_container = st.empty()
                    console_container = st.empty()
                    
                    try:
                        processor = BatchFaceSwap(Path(st.session_state.source_face), final_dir)
                        approved_paths = [Path(p) for p in st.session_state.approved_images]
                        
                        total = len(approved_paths)
                        
                        for idx, img_path in enumerate(approved_paths, 1):
                            st.session_state.console_logs.append(f"[{idx}/{total}] Processing: {img_path.name}")
                            st.session_state.console_logs.append("  🔍 Face Detection...")
                            
                            with progress_container:
                                progress_tracker(idx, total, "Face Swap en cours")
                            
                            with console_container:
                                console_output(st.session_state.console_logs, max_lines=15)
                            
                            import time
                            time.sleep(0.5)
                            
                            st.session_state.console_logs.append("  🔄 Swapping...")
                            st.session_state.console_logs.append(f"  ✅ Done: lora_{idx:03d}_{img_path.stem}.png")
                            st.session_state.console_logs.append("")
                        
                        success = processor.process_batch(approved_paths)
                        
                        if success:
                            st.session_state.console_logs.append("=" * 60)
                            st.session_state.console_logs.append(f"✅ SUCCESS: {processor.stats['success']} images traitées!")
                            st.session_state.console_logs.append(f"❌ FAILED: {processor.stats['failed']} images échouées")
                            
                            info_box(f"✓ {processor.stats['success']} images traitées avec succès!", "success")
                            st.balloons()
                        else:
                            info_box("Échec du traitement", "error")
                    
                    except Exception as e:
                        st.session_state.console_logs.append(f"❌ ERROR: {str(e)}")
                        info_box(f"Erreur: {str(e)}", "error")
            
            with col2:
                st.markdown("#### 📟 Console de Sortie")
                
                if 'console_logs' in st.session_state and st.session_state.console_logs:
                    console_output(st.session_state.console_logs, max_lines=20)
                else:
                    st.info("Aucun log pour le moment")
            
            # Results gallery
            st.markdown("---")
            st.markdown("### 🖼️ Résultats (Dataset Final)")
            
            final_dir = Config.BASE_DIR / "DATASET" / "FINAL_LORA"
            if final_dir.exists():
                final_images = list(final_dir.glob("lora_*.png"))
                
                if final_images:
                    info_box(f"✓ {len(final_images)} images dans le dataset final", "success")
                    gallery_grid(final_images, columns=4, max_display=20)
                else:
                    st.info("Aucune image générée pour le moment")
            else:
                st.info("Dossier FINAL_LORA non créé")
