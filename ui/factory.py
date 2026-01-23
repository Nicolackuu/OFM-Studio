"""
Factory Page - Dataset Production (Models + Curated Datasets + Face Swap)
"""
import streamlit as st
from pathlib import Path
from core.config import Config
from core.batch_face_swap import BatchFaceSwap
import shutil

def render():
    """Render factory page with new production workflow"""
    
    # Initialize session state
    if "source_face" not in st.session_state:
        st.session_state.source_face = None
    if "selected_model" not in st.session_state:
        st.session_state.selected_model = None
    if "selected_dataset" not in st.session_state:
        st.session_state.selected_dataset = None
    
    st.title("🏭 Usine de Production")
    st.markdown("Modèles IA + Datasets Triés + Face Swap")
    
    # Layout compact avec les deux étapes côte à côte
    col_source, col_target = st.columns([1, 1])
    
    # === ÉTAPE 1: SOURCE (MODÈLE IA) ===
    with col_source:
        st.markdown("### 🎯 Étape 1: Source (Modèle IA)")
        
        # Le sélecteur 'Source Face' doit lister tous les fichiers dans DATASET/PROCESSED/MODELS
        from core.config import Config
        models_dir = Config.MODELS_DIR
        if not models_dir.exists():
            models_dir.mkdir(parents=True, exist_ok=True)
            st.warning(f"📁 Dossier créé : {models_dir}. Ajoute des images dedans !")

        model_files = list(Config.MODELS_DIR.glob("*.png")) + list(Config.MODELS_DIR.glob("*.jpg"))  # Only images
        if not model_files:
            st.error("❌ Aucun modèle trouvé dans data/dataset/processed/models. Va dans l'onglet 'Casting' pour en créer un !")
        else:
            model_files.sort(key=lambda x: x.stat().st_mtime, reverse=True)
            selected_model = st.selectbox(
                "Source Face:",
                options=[str(f) for f in model_files],
                format_func=lambda x: Path(x).name,
                key="model_selector"
            )
            
            # Aperçu: Dès qu'un modèle est sélectionné, afficher sa miniature
            model_path = Path(selected_model)
            if model_path.exists():
                st.image(str(model_path), use_container_width=True, caption=f"📸 {model_path.name}")
                st.info(f"✅ Modèle sélectionné: {model_path.name}")
                
                if st.button("✅ Utiliser ce modèle", use_container_width=True, key="use_model_btn"):
                    st.session_state.source_face = selected_model
                    # Stocker le nom du modèle (sans extension)
                    model_name = model_path.stem
                    st.session_state.selected_model_name = model_name
                    st.success(f"✅ Modèle sélectionné: {model_name}")
                    st.rerun()
    
    # === ÉTAPE 2: TARGET (DATASET TRIÉ) ===
    with col_target:
        st.markdown("### 🎯 Étape 2: Target (Dataset Trié)")
        
        # Lister les datasets dans CURATED_DIR
        curated_dir = Config.CURATED_DIR
        if curated_dir.exists():
            curated_datasets = [d.name for d in curated_dir.iterdir() if d.is_dir()]
            
            if curated_datasets:
                selected_dataset = st.selectbox(
                    "Choisir un dataset trié:",
                    options=curated_datasets,
                    key="dataset_selector"
                )
                
                # Afficher une petite galerie de preview
                dataset_path = curated_dir / selected_dataset
                if dataset_path.exists():
                    st.markdown(f"**📁 {selected_dataset}**")
                    
                    # Lister les images du dataset
                    image_files = list(dataset_path.glob("*.png")) + list(dataset_path.glob("*.jpg"))
                    image_files = image_files[:6]  # Limiter à 6 images pour le preview
                    
                    if image_files:
                        # Afficher en grille 2x3
                        cols = st.columns(3)
                        for i, img_path in enumerate(image_files):
                            with cols[i % 3]:
                                st.image(str(img_path), use_container_width=True, caption=img_path.name)
                        
                        st.info(f"📊 {len(list(dataset_path.glob('*.png')) + list(dataset_path.glob('*.jpg')))} images au total")
                        
                        if st.button("✅ Utiliser ce dataset", use_container_width=True, key="use_dataset_btn"):
                            st.session_state.selected_dataset = selected_dataset
                            # Stocker le nom du dataset
                            st.session_state.selected_dataset_name = selected_dataset
                            st.success(f"✅ Dataset sélectionné: {selected_dataset}")
                            st.rerun()
                    else:
                        st.warning("⚠️ Dataset vide.")
            else:
                st.warning("⚠️ Aucun dataset trié trouvé. Utilisez l'onglet Curation pour en créer un.")
        else:
            st.error("❌ Dossier CURATED_DIR non trouvé.")
    
    # === ÉTAPE 3: PRODUCTION ===
    st.markdown("---")
    st.markdown("### 🚀 Étape 3: Production")
    
    # Vérifier que les deux étapes sont complétées
    if st.session_state.source_face and st.session_state.selected_dataset:
        col_info, col_action = st.columns([2, 1])
        
        with col_info:
            st.markdown("#### 📋 Résumé de la production")
            
            # Utiliser les noms stockés
            model_name = st.session_state.get('selected_model_name', 'Modèle')
            dataset_name = st.session_state.get('selected_dataset_name', 'Dataset')
            
            st.markdown(f"""
            **🎭 Modèle Source:** {model_name}  
            **📁 Dataset Cible:** {dataset_name}  
            **🔧 Opération:** Face Swap Batch
            **📝 Format:** {model_name}_{dataset_name}_[original].jpg
            """)
            
            # Compter les images dans le dataset
            dataset_path = Config.CURATED_DIR / dataset_name
            image_count = len(list(dataset_path.glob("*.png")) + list(dataset_path.glob("*.jpg")))
            st.metric("📸 Images à traiter", image_count)
        
        with col_action:
            st.markdown("#### ⚡ Lancement")
            
            if st.button("🚀 START BATCH SWAP", use_container_width=True, type="primary"):
                with st.spinner("🔄 Production en cours..."):
                    try:
                        # Chemins
                        source_path = Path(st.session_state.source_face)
                        
                        # Sécurité: vérifier que le fichier existe
                        if not source_path.exists():
                            st.error(f"❌ Fichier source introuvable: {source_path}")
                            return
                        
                        target_dir = Config.CURATED_DIR / dataset_name
                        output_dir = Config.FACE_SWAP_OUTPUT / f"{model_name}_{dataset_name}_swapped"  # Uses SWAPPED_DIR
                        output_dir.mkdir(parents=True, exist_ok=True)
                        
                        # Initialiser le batch face swap avec le bon chemin
                        swap_engine = BatchFaceSwap(source_path, output_dir)
                        
                        # Lancer le traitement avec nommage automatisé
                        results = swap_engine.process_batch(
                            target_directory=target_dir,
                            output_directory=output_dir,
                            naming_pattern=f"{model_name}_{dataset_name}_{{original}}.jpg"
                        )
                        
                        if results:
                            st.success(f"🎉 Production terminée! {len(results)} images générées.")
                            st.info(f"📍 Résultats dans: {output_dir}")
                            st.info(f"📝 Format: {model_name}_{dataset_name}_[original].jpg")
                            st.balloons()
                        else:
                            st.error("❌ Aucune image générée.")
                            
                    except Exception as e:
                        st.error(f"❌ Erreur lors de la production: {str(e)}")
    else:
        st.warning("⚠️ Veuillez compléter les Étapes 1 et 2 avant de lancer la production.")
        
        # Afficher l'état actuel
        col1, col2 = st.columns(2)
        with col1:
            if st.session_state.source_face:
                st.success("✅ Étape 1: Modèle sélectionné")
            else:
                st.error("❌ Étape 1: Modèle manquant")
        
        with col2:
            if st.session_state.selected_dataset:
                st.success("✅ Étape 2: Dataset sélectionné")
            else:
                st.error("❌ Étape 2: Dataset manquant")
