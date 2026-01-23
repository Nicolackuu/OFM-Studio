# 🔄 Migration Guide - V16 to V17

This guide explains the changes from the old structure to the new reorganized structure.

---

## 📊 What Changed?

### Old Structure (V16)
```
OFM IA/
├── Scripts/
│   ├── main.py
│   ├── config.py
│   ├── data_bank.py
│   ├── core_engine.py
│   ├── Gemini_Studio_Production.py (monolithic)
│   ├── Insta_Scrap/
│   │   └── Insta_Ultimate.py
│   └── Face_Swap/
│       └── Gemini_Creator_V2.py
```

### New Structure (V17)
```
OFM IA/
├── core/                      # NEW: Centralized modules
│   ├── config.py             # Environment-based config
│   ├── utils.py              # Shared utilities
│   ├── character_bank.py     # Character generation
│   └── gemini_engine.py      # Gemini API wrapper
│
├── gemini_studio.py          # NEW: Main studio app
├── instagram_scraper.py      # NEW: Improved scraper
├── face_swap.py              # NEW: Unified face swap
├── launcher.py               # NEW: Application launcher
├── requirements.txt          # NEW: Dependencies
├── .env.example              # NEW: Config template
└── .gitignore                # NEW: Git rules
```

---

## 🔑 Key Improvements

### 1. **Environment Variables**
**Old:** API keys hardcoded in scripts
```python
GOOGLE_API_KEY = "AIzaSy..."  # Hardcoded!
```

**New:** Secure environment variables
```python
# .env file (gitignored)
GOOGLE_API_KEY=your_key_here
```

### 2. **Modular Architecture**
**Old:** Code duplicated across files
- `main.py`, `Gemini_Studio_Production.py`, `Gemini_Creator_V2.py` all had similar code

**New:** Shared core modules
- `core/gemini_engine.py` - Single API wrapper
- `core/utils.py` - Shared utilities
- `core/character_bank.py` - Character system

### 3. **Better Error Handling**
**Old:** Basic try/except
```python
try:
    # code
except:
    pass  # Silent failure
```

**New:** Descriptive error messages
```python
try:
    # code
except Exception as e:
    print_error(f"Failed: {e}")
    return None
```

### 4. **Consistent UI**
**Old:** Mixed color codes and formatting
**New:** Unified `Colors` class and helper functions

---

## 🚀 Migration Steps

### Step 1: Backup Your Data
```bash
# Backup generated images
copy "IMAGES\GENERATED\*" "BACKUP\IMAGES\"

# Backup Instagram downloads
copy "Scripts\Insta_Scrap\*" "BACKUP\Insta_Scrap\"
```

### Step 2: Set Up Environment
```bash
# Copy environment template
copy .env.example .env

# Edit .env with your credentials
notepad .env
```

### Step 3: Install Dependencies
```bash
pip install -r requirements.txt
```

### Step 4: Test New Applications
```bash
# Test launcher
python launcher.py

# Or run directly
python gemini_studio.py
python instagram_scraper.py
python face_swap.py
```

---

## 📝 Configuration Mapping

### Old `Scripts/config.py` → New `.env`
```python
# OLD
GOOGLE_API_KEY = "AIzaSy..."
MODEL_IMAGE = "gemini-3-pro-image-preview"
CONFIG_PARAMS = {
    "temperature": 0.85,
    "aspect_ratio": "3:2",
    "image_size": "2K"
}
```

```env
# NEW (.env file)
GOOGLE_API_KEY=AIzaSy...
```

```python
# NEW (core/config.py)
class Config:
    GOOGLE_API_KEY = os.getenv('GOOGLE_API_KEY')
    MODEL_IMAGE = "gemini-3-pro-image-preview"
    GEMINI_CONFIG = {
        "temperature": 0.85,
        "aspect_ratio": "3:2",
        "image_size": "2K"
    }
```

---

## 🔄 Code Migration Examples

### Example 1: Character Generation

**Old (`Scripts/data_bank.py`):**
```python
from config import CYAN, GREEN, YELLOW, RESET

def random_casting():
    global CHAR_DNA
    print(f"\n{CYAN}=== SLOT MACHINE ==={RESET}")
    # ... generation code
```

**New (`core/character_bank.py`):**
```python
from core.utils import Colors

class Character:
    def generate_random(self):
        print(f"\n{Colors.CYAN}=== SLOT MACHINE ==={Colors.RESET}")
        # ... generation code
        return self.dna
```

### Example 2: Image Generation

**Old (`Scripts/core_engine.py`):**
```python
def generate_image(prompt, reference_image_path=None):
    # Inline API call
    response = client.models.generate_content(...)
```

**New (`core/gemini_engine.py`):**
```python
class GeminiEngine:
    def generate_image(self, prompt, reference_image_path=None):
        # Wrapped with error handling
        try:
            response = self.client.models.generate_content(...)
            return self._process_response(response)
        except Exception as e:
            print_error(f"Generation failed: {e}")
            return None
```

---

## ⚠️ Breaking Changes

### 1. Import Paths Changed
**Old:**
```python
from config import CONFIG_PARAMS
from data_bank import random_casting
from core_engine import generate_image
```

**New:**
```python
from core.config import Config
from core.character_bank import Character
from core.gemini_engine import GeminiEngine
```

### 2. Function Signatures Changed
**Old:**
```python
generate_image(prompt, ref_path, "1")
```

**New:**
```python
engine = GeminiEngine()
engine.generate_image(
    prompt=prompt,
    reference_image_path=ref_path,
    phase="1",
    character_name="Model"
)
```

### 3. Global Variables Removed
**Old:**
```python
CHAR_DNA = {}  # Global variable
```

**New:**
```python
character = Character()
character.dna  # Instance variable
```

---

## 🎯 Feature Parity

All features from V16 are preserved in V17:

| Feature | V16 | V17 | Status |
|---------|-----|-----|--------|
| Random Character Generation | ✅ | ✅ | ✓ Improved |
| 3-Phase Workflow | ✅ | ✅ | ✓ Same |
| 2K/4K Support | ✅ | ✅ | ✓ Same |
| Multiple Aspect Ratios | ✅ | ✅ | ✓ Same |
| Instagram Scraper | ✅ | ✅ | ✓ Improved |
| Face Swap | ✅ | ✅ | ✓ Improved |
| Keep/Redo Loop | ✅ | ✅ | ✓ Same |

---

## 🐛 Troubleshooting

### Issue: "Module not found"
**Solution:**
```bash
pip install -r requirements.txt
```

### Issue: "API key not found"
**Solution:**
Check your `.env` file exists and contains:
```env
GOOGLE_API_KEY=your_actual_key
```

### Issue: "Old scripts not working"
**Solution:**
Old scripts in `Scripts/` are preserved and still work independently. Use new applications for better experience.

---

## 📚 Where to Find Things

| Old Location | New Location | Notes |
|--------------|--------------|-------|
| `Scripts/main.py` | `gemini_studio.py` | Improved UI |
| `Scripts/config.py` | `core/config.py` + `.env` | Split config |
| `Scripts/data_bank.py` | `core/character_bank.py` | Class-based |
| `Scripts/core_engine.py` | `core/gemini_engine.py` | Better errors |
| `Scripts/Insta_Scrap/Insta_Ultimate.py` | `instagram_scraper.py` | Cleaner code |
| `Scripts/Face_Swap/Gemini_Creator_V2.py` | `face_swap.py` | Unified |

---

## ✅ Checklist

- [ ] Backup your data
- [ ] Create `.env` file from `.env.example`
- [ ] Add your API keys to `.env`
- [ ] Install dependencies: `pip install -r requirements.txt`
- [ ] Test launcher: `python launcher.py`
- [ ] Test each application
- [ ] Verify generated images work
- [ ] Check Instagram scraper works
- [ ] Confirm face swap works

---

## 🎓 Next Steps

1. **Use the launcher** for easy access to all tools
2. **Read README.md** for detailed documentation
3. **Keep old scripts** as backup (they still work)
4. **Report issues** if you find any problems

---

**Migration completed!** 🎉

Your old scripts are preserved in `Scripts/` and will continue to work.
The new applications provide better organization and features.
