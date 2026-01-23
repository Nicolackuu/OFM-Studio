from datetime import datetime
from pathlib import Path
from typing import Optional, Dict, Any
import time
import logging
from PIL import Image
import io
from google import genai
from google.genai import types
import streamlit as st

from core.config import Config
from core.utils import print_info, print_success, print_error, save_binary_file, open_file, get_image_bytes
from core.request_tracker import RequestTracker

# Configure logging for API debugging
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

class GeminiEngine:
    def __init__(self):
        self.client = None
        self.config = Config.GEMINI_CONFIG.copy()
        self.last_request_time = 0
        self.tracker = RequestTracker()
        self._initialize_client()
    
    def _initialize_client(self):
        try:
            self.client = genai.Client(api_key=Config.GOOGLE_API_KEY)
            logger.info("✅ Gemini API client initialized successfully")
            print_success("Gemini API initialized")
        except Exception as e:
            logger.error(f"❌ Failed to initialize Gemini API: {e}")
            print_error(f"Failed to initialize Gemini API: {e}")
            raise
    
    def _resize_image_to_768px(self, image_path: str) -> bytes:
        """Resize image to max 768px on longest side to prevent API timeouts"""
        try:
            logger.info(f"📐 Resizing image: {image_path}")
            with Image.open(image_path) as img:
                # Get original dimensions
                width, height = img.size
                logger.info(f"   Original size: {width}x{height}")
                
                # Calculate new dimensions (max 768px on longest side)
                max_size = 768
                if width > height:
                    if width > max_size:
                        new_width = max_size
                        new_height = int((max_size / width) * height)
                    else:
                        new_width, new_height = width, height
                else:
                    if height > max_size:
                        new_height = max_size
                        new_width = int((max_size / height) * width)
                    else:
                        new_width, new_height = width, height
                
                # Resize if needed
                if (new_width, new_height) != (width, height):
                    img = img.resize((new_width, new_height), Image.Resampling.LANCZOS)
                    logger.info(f"   Resized to: {new_width}x{new_height}")
                else:
                    logger.info(f"   No resize needed (already <= 768px)")
                
                # Convert to bytes
                buffer = io.BytesIO()
                img.save(buffer, format='PNG')
                return buffer.getvalue()
        except Exception as e:
            logger.error(f"❌ Image resize failed: {e}")
            raise
    
    def _enforce_rate_limit(self):
        """Enforce 2-second delay between API requests"""
        current_time = time.time()
        time_since_last_request = current_time - self.last_request_time
        
        if time_since_last_request < 2.0:
            sleep_time = 2.0 - time_since_last_request
            logger.info(f"⏳ Rate limiting: sleeping {sleep_time:.2f}s")
            time.sleep(sleep_time)
        
        self.last_request_time = time.time()
    
    def update_config(self, **kwargs):
        self.config.update(kwargs)
    
    def generate_image(
        self,
        prompt: str,
        reference_image_path: Optional[str] = None,
        phase: str = "1",
        character_name: str = "Model",
        usage_tracker = None
    ) -> Optional[Path]:
        
        if not self.client:
            print_error("Client not initialized")
            return None
        
        # Check session state availability
        if not hasattr(st, 'session_state'):
            logger.error("❌ Streamlit session_state not available")
            print_error("Streamlit session not available")
            return None
        
        # Check persistent_monitor availability
        if 'persistent_monitor' not in st.session_state:
            logger.error("❌ Persistent monitor not found in session state")
            print_error("Persistent monitor not initialized")
            return None
        
        logger.info("✅ Session state and persistent monitor available")
        
        contents = [prompt]
        
        # Track input tokens (estimate: ~4 chars per token)
        if usage_tracker:
            estimated_input_tokens = len(prompt) // 4
            usage_tracker.add_tokens(input_tokens=estimated_input_tokens)
        
        if reference_image_path:
            try:
                logger.info(f"📸 Loading reference image: {reference_image_path}")
                # Resize image to 768px max before sending to API
                img_bytes = self._resize_image_to_768px(reference_image_path)
                contents.append(types.Part.from_bytes(data=img_bytes, mime_type="image/png"))
                logger.info("✅ Reference image loaded and resized")
                print_success("Reference image loaded")
            except Exception as e:
                logger.error(f"❌ Could not load reference image: {e}")
                print_error("Could not load reference image")
                return None
        
        logger.info(f"🎨 Generating image (Resolution: {self.config['image_size']}, Ratio: {self.config['aspect_ratio']})")
        print_info(f"Generating image (Resolution: {self.config['image_size']}, Ratio: {self.config['aspect_ratio']})...")
        
        # Enforce rate limiting (2s between requests)
        self._enforce_rate_limit()
        
        try:
            logger.info("📡 Sending request to Gemini API...")
            
            # Safety settings: BLOCK_NONE for all categories (required for face processing)
            safety_settings = [
                types.SafetySetting(
                    category="HARM_CATEGORY_HATE_SPEECH",
                    threshold="BLOCK_NONE"
                ),
                types.SafetySetting(
                    category="HARM_CATEGORY_HARASSMENT",
                    threshold="BLOCK_NONE"
                ),
                types.SafetySetting(
                    category="HARM_CATEGORY_SEXUALLY_EXPLICIT",
                    threshold="BLOCK_NONE"
                ),
                types.SafetySetting(
                    category="HARM_CATEGORY_DANGEROUS_CONTENT",
                    threshold="BLOCK_NONE"
                )
            ]
            
            # Check API limits before making request
            if not self.tracker.check_limits():
                logger.error("❌ Daily API limit reached")
                st.error("🚫 Limite API journalière atteinte (250/250)")
                return None
            
            # Track this request
            if not self.tracker.track_request():
                logger.error("❌ Request blocked by rate limiter")
                st.error("⏱️ Trop de requêtes, veuillez attendre")
                return None
            
            response = self.client.models.generate_content(
                model=Config.MODEL_IMAGE,
                contents=contents,
                config=types.GenerateContentConfig(
                    temperature=self.config['temperature'],
                    top_p=self.config['top_p'],
                    response_modalities=["IMAGE"],
                    safety_settings=safety_settings,
                    image_config=types.ImageConfig(
                        image_size=self.config['image_size'],
                        aspect_ratio=self.config['aspect_ratio']
                    )
                )
            )
            
            logger.info("✅ API response received")

            # Tracking Automatique: Récupère le chiffre exact
            if hasattr(response, 'usage_metadata') and response.usage_metadata:
                # Après l'appel API, récupère le chiffre exact : tokens = response.usage_metadata.total_token_count
                tokens = response.usage_metadata.total_token_count
                logger.info(f"📊 Exact tokens used: {tokens}")
                
                # Ajoute-le immédiatement au persistent_monitor pour qu'il soit sauvegardé
                if 'persistent_monitor' in st.session_state:
                    st.session_state.persistent_monitor.add_tokens(tokens)
                    logger.info(f"✅ Persistent monitor updated with exact {tokens} tokens")
                    logger.info("🎯 Quota 100K updated instantly in sidebar")
                else:
                    logger.error("❌ Persistent monitor not found in session state")
                    
            else:
                logger.warning("⚠️ No usage metadata in response")
            
            # Track requests for daily limit
            if 'request_tracker' in st.session_state:
                st.session_state.request_tracker.track_request()
                logger.info("✅ Request tracker updated")

            if response.candidates and response.candidates[0].content.parts[0].inline_data:
                logger.info("💾 Saving generated image...")
                part = response.candidates[0].content.parts[0]
                timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
                filename = f"Phase{phase}_{character_name}_{self.config['image_size']}_{timestamp}.png"
                file_path = Config.OUTPUT_DIR / filename
                
                # Track image generation
                if usage_tracker:
                    usage_tracker.add_image()
                
                if save_binary_file(file_path, part.inline_data.data):
                    logger.info(f"✅ Image saved: {filename}")
                    open_file(file_path)
                    return file_path
                else:
                    logger.error("❌ Failed to save image file")
                    return None
            else:
                logger.error("❌ No image data received from API")
                print_error("No image data received from API")
                return None

        except Exception as e:
            logger.error(f"❌ Generation failed: {e}")
            logger.error(f"   Exception type: {type(e).__name__}")
            logger.error(f"   Exception details: {str(e)}")
            print_error(f"Generation failed: {e}")
            return None

class PromptBuilder:
    @staticmethod
    def build_phase_1(character_dna: Dict[str, Any]) -> str:
        dna = character_dna['EN_FULL']
        age = character_dna['AGE']
        
        return f"""
### PROFESSIONAL PORTRAIT STUDY: PHASE 1 (FOUNDATION) ###
OBJECTIVE: Create a high-resolution photographic triptych to establish the primary facial structure.
Focus on maximum detail clarity but maintaining extreme attractiveness.
Layout: 3 large frames side-by-side.
Subject: Fictional female model, {age} years old. {dna['NATIONALITY']}.

FRAME 1 (LEFT): Strict 90-degree left profile.
FRAME 2 (CENTER): Dead-center frontal headshot. Neutral expression, symmetrical.
FRAME 3 (RIGHT): Three-quarter view (45 degrees right).

PHOTOREALISM & TEXTURE PROTOCOL:
- Aesthetic: High-end editorial photography, raw but flattering lighting.
- DETAILS: Ultra-sharp focus on iris patterns, natural skin texture with visible pores.
- RESTRICTIONS: NO plastic smoothing, NO AI-blur. Skin must look human.

MODEL SPECIFICS:
- FACE SHAPE: {dna['FACE']}
- EYES: {dna['EYES']}
- HAIR: {dna['HAIR']}
- NOSE & LIPS: {dna['NOSE_LIPS']}
- DISTINCTIVE FEATURES: {dna['IMP']}
- BODY TYPE: {dna['BODY']}
"""
    
    @staticmethod
    def build_phase_2(character_dna: Dict[str, Any]) -> str:
        dna = character_dna['EN_FULL']
        
        return f"""
### PROFESSIONAL PORTRAIT STUDY: PHASE 2 (STRUCTURE) ###
REFERENCE MANDATE: Maintain absolute 100% facial identity consistency with the attached image.
Feature to track strictly: {dna['IMP']}.
Layout: Horizontal strip of 5 frames.
FRAME 1: High Angle (Looking down).
FRAME 2: Low Angle (Looking up).
FRAME 3: Frontal recall.
FRAME 4: Right Profile.
FRAME 5: Hairline Focus.
PHOTOREALISM PROTOCOL: Raw but beautiful aesthetic.
"""
    
    @staticmethod
    def build_phase_3(character_dna: Dict[str, Any]) -> str:
        dna = character_dna['EN_FULL']
        
        return f"""
### PROFESSIONAL PORTRAIT STUDY: PHASE 3 (DYNAMICS) ###
REFERENCE MANDATE: Maintain absolute 100% facial identity consistency.
Feature to track strictly: {dna['IMP']}.
Layout: Horizontal strip of 5 frames (Emotions).
FRAME 1 (JOY): Wide, genuine smile.
FRAME 2 (INTENSITY): Fierce, focused "baddie" stare.
FRAME 3 (SERENE): Eyes closed gently.
FRAME 4 (SKEPTICAL): One eyebrow raised.
FRAME 5 (SURPRISE): Mouth slightly open, gasp.
"""
