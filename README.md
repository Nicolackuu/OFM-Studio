# 🎬 OFM IA - AI Content Creation Studio

**Professional AI-powered content creation suite** featuring image generation, Instagram scraping, and face consistency tools.

---

## 📋 Features

### 🎨 Gemini Studio
- **AI Portrait Generation** using Google's Gemini 3 Pro Image Preview
- **Random Character Generator** with detailed DNA profiles
- **3-Phase Workflow**: Foundation → Structure → Dynamics
- **Multiple Resolutions**: 1K, 2K, 4K support
- **Flexible Aspect Ratios**: 16:9, 3:2, 1:1, 3:4
- **Photorealistic Output** with natural imperfections

### 📸 Instagram Scraper
- **High-speed media downloads** from Instagram profiles
- **Selective downloading**: All, Photos only, or Videos only
- **Auto-organization** by date and media type
- **Session-based authentication** for reliable access
- **Batch processing** with customizable limits

### 🔄 Face Swap Studio
- **Consistent character generation** across multiple phases
- **Fixed DNA profiles** for reproducible results
- **Reference-based generation** for identity consistency

---

## 🚀 Installation

### 1. Clone or Download
```bash
cd "C:\Users\nicol\Desktop\OFM IA"
```

### 2. Install Dependencies
```bash
pip install -r requirements.txt
```

### 3. Configure Environment
Copy `.env.example` to `.env` and add your credentials:
```bash
copy .env.example .env
```

Edit `.env`:
```env
GOOGLE_API_KEY=your_google_api_key_here
INSTAGRAM_USERNAME=your_instagram_username
INSTAGRAM_SESSION_ID=your_session_id_here
```

---

## 📖 Usage

### Gemini Studio
```bash
python gemini_studio.py
```

**Workflow:**
1. **[0]** Generate a random character profile
2. **[Q]** Set resolution (2K recommended)
3. **[R]** Set aspect ratio (3:2 best for portraits)
4. **[1]** Run Phase 1 (Foundation - 3 angles)
5. **[2]** Run Phase 2 with Phase 1 image as reference
6. **[3]** Run Phase 3 with Phase 2 image as reference

### Instagram Scraper
```bash
python instagram_scraper.py
```

**Features:**
- Enter target username
- Choose download mode (All/Photos/Videos)
- Set download limit
- Auto-organized output in `Scripts/Insta_Scrap/{username}/`

### Face Swap Studio
```bash
python face_swap.py
```

**Fixed Character Workflow:**
- Uses predefined character DNA
- Same 3-phase process as Gemini Studio
- Ensures consistent character across generations

---

## 📁 Project Structure

```
OFM IA/
├── core/                          # Core modules
│   ├── __init__.py
│   ├── config.py                  # Centralized configuration
│   ├── utils.py                   # Utility functions
│   ├── character_bank.py          # Character generation
│   └── gemini_engine.py           # Gemini API wrapper
│
├── Scripts/                       # Legacy scripts
│   ├── Insta_Scrap/              # Instagram downloads
│   ├── Face_Swap/                # Face swap files
│   ├── main.py                   # Legacy modular studio
│   ├── config.py                 # Legacy config
│   ├── data_bank.py              # Legacy data
│   └── core_engine.py            # Legacy engine
│
├── IMAGES/
│   ├── GENERATED/                # AI-generated images
│   └── Reference image for FaceSwapping/
│
├── gemini_studio.py              # Main studio application
├── instagram_scraper.py          # Instagram scraper
├── face_swap.py                  # Face swap application
├── requirements.txt              # Python dependencies
├── .env.example                  # Environment template
├── .gitignore                    # Git ignore rules
└── README.md                     # This file
```

---

## ⚙️ Configuration

### Resolution Options
| Resolution | Pixels | Use Case | Speed |
|------------|--------|----------|-------|
| **1K** | ~1024px | Quick tests | ⚡⚡⚡ |
| **2K** | ~2048px | Production ⭐ | ⚡⚡ |
| **4K** | ~4096px | Maximum quality | ⚡ |

### Aspect Ratio Options
| Ratio | Description | Best For |
|-------|-------------|----------|
| **3:2** | Pro Photo | Portraits ⭐ |
| **16:9** | Cinema | Wide scenes |
| **1:1** | Square | Instagram |
| **3:4** | Portrait | Tall format |

---

## 🎯 Character DNA System

The character generator creates unique profiles with:
- **9 Nationalities**: French, Brazilian, Russian, Japanese, Italian, Scandinavian, American, Spanish, Mixed
- **4 Body Types**: Hourglass, Athletic, Model, Curvy
- **5 Face Shapes**: Oval, Heart, Diamond, Round, Square
- **6 Eye Types**: Ice Blue, Emerald Green, Hazel, Dark Brown, Storm Grey, Heterochromia
- **6 Hair Styles**: Honey Blonde, Chocolate Brown, Copper Red, Jet Black, Ash Brown, Platinum Blonde
- **5 Nose/Lip Combinations**
- **7 Distinctive Features**: Freckles, Beauty marks, Scars, Dimples, etc.

---

## 🔒 Security

**IMPORTANT:** Never commit sensitive credentials to version control!

- API keys are stored in `.env` (gitignored)
- Session IDs are environment variables
- Generated images are excluded from git

---

## 🛠️ Troubleshooting

### API Key Issues
```bash
# Check your .env file
cat .env

# Verify API key is valid at:
# https://aistudio.google.com/apikey
```

### Instagram Authentication
```bash
# Get session ID from browser:
# 1. Login to Instagram
# 2. Open DevTools (F12)
# 3. Application > Cookies > sessionid
```

### Module Import Errors
```bash
# Reinstall dependencies
pip install -r requirements.txt --force-reinstall
```

---

## 📊 Version History

### V17 (Current - Reorganized)
- ✅ Modular architecture with `core/` package
- ✅ Environment-based configuration
- ✅ Unified utilities and error handling
- ✅ Improved code quality and documentation
- ✅ Proper .gitignore and requirements.txt

### V16 (Modular + 2K/4K)
- ✅ Split into 4 modules (main, config, data_bank, core_engine)
- ✅ Native 2K/4K resolution support
- ✅ Improved file organization

### V15 (Monolithic)
- ✅ Single-file implementation
- ✅ Basic 3-phase workflow
- ✅ 1K resolution only

---

## 🎓 Tips & Best Practices

1. **Start with 2K resolution** for balance of quality and speed
2. **Use 3:2 aspect ratio** for best portrait results
3. **Always use Phase 1 output** as reference for Phase 2
4. **Keep character DNA consistent** across all phases
5. **Organize generated images** by character/session
6. **Backup your .env file** securely (not in git!)

---

## 📝 License

Personal project - All rights reserved.

---

## 👤 Author

**OFM IA Studio**  
Created: January 2026  
Version: 17.0 (Reorganized & Improved)

---

## 🔗 Resources

- [Google Gemini API Docs](https://ai.google.dev/gemini-api/docs)
- [Instaloader Documentation](https://instaloader.github.io/)
- [Python dotenv Guide](https://pypi.org/project/python-dotenv/)
