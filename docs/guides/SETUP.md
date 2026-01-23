# 🚀 Quick Setup Guide

Get started with OFM IA Studio in 5 minutes!

---

## ⚡ Quick Start

### 1. Install Python Dependencies
```bash
pip install -r requirements.txt
```

### 2. Configure Environment
```bash
# Copy the example file
copy .env.example .env

# Edit with your credentials
notepad .env
```

### 3. Add Your API Keys
Edit `.env` and add:
```env
GOOGLE_API_KEY=your_google_api_key_here
INSTAGRAM_USERNAME=your_instagram_username
INSTAGRAM_SESSION_ID=your_session_id_here
```

### 4. Launch!
```bash
python launcher.py
```

---

## 🔑 Getting API Keys

### Google Gemini API Key

1. Go to [Google AI Studio](https://aistudio.google.com/apikey)
2. Sign in with your Google account
3. Click "Create API Key"
4. Copy the key and paste it in `.env`

**Example:**
```env
GOOGLE_API_KEY=AIzaSyBNvA1PZp-3ZYRo5Nyewo6gQWFAnMXfzi0
```

### Instagram Session ID

1. Open Instagram in your browser
2. Log in to your account
3. Press `F12` to open Developer Tools
4. Go to **Application** tab
5. Click **Cookies** → **https://www.instagram.com**
6. Find `sessionid` and copy its value
7. Paste it in `.env`

**Example:**
```env
INSTAGRAM_SESSION_ID=79877415963%3Ab1FRUFTtw3PkjK%3A13%3AAYh6hvublltpw6aa2JUpcqV8nSZCRbEmuOhQGcCLZw
```

---

## 📦 Dependencies Explained

### Required Packages

**google-genai** (≥0.2.0)
- Google's Gemini API client
- Used for AI image generation
- [Documentation](https://ai.google.dev/gemini-api/docs)

**instaloader** (≥4.10.0)
- Instagram scraping library
- Downloads photos and videos
- [Documentation](https://instaloader.github.io/)

**python-dotenv** (≥1.0.0)
- Environment variable management
- Loads `.env` file securely
- [Documentation](https://pypi.org/project/python-dotenv/)

---

## 🎯 First Run

### Option 1: Use Launcher (Recommended)
```bash
python launcher.py
```
- Interactive menu
- Auto-checks dependencies
- Easy navigation

### Option 2: Run Directly
```bash
# Gemini Studio
python gemini_studio.py

# Instagram Scraper
python instagram_scraper.py

# Face Swap
python face_swap.py
```

---

## 🧪 Test Your Setup

### Test Gemini API
```bash
python gemini_studio.py
```
1. Press `[0]` to generate a random character
2. Press `[1]` to run Phase 1
3. Wait for image generation
4. Image should open automatically

**Success:** Image appears in `IMAGES/GENERATED/`

### Test Instagram Scraper
```bash
python instagram_scraper.py
```
1. Enter a public Instagram username
2. Choose mode `[1]` (All)
3. Set limit to `5` for testing
4. Wait for download

**Success:** Files appear in `Scripts/Insta_Scrap/{username}/`

---

## 🔧 Troubleshooting

### "Module not found" Error
```bash
# Reinstall dependencies
pip install -r requirements.txt --force-reinstall
```

### "API key not valid" Error
- Check your `.env` file exists
- Verify API key is correct (no extra spaces)
- Test key at [Google AI Studio](https://aistudio.google.com/)

### "Instagram authentication failed"
- Check session ID is current (expires after ~90 days)
- Get fresh session ID from browser
- Make sure no extra quotes in `.env`

### Images Not Opening
- Check `IMAGES/GENERATED/` folder manually
- Verify default image viewer is set
- Images are saved as `.png` files

### Permission Errors
```bash
# Run as administrator (Windows)
# Right-click Command Prompt → Run as administrator
```

---

## 📁 Folder Structure After Setup

```
OFM IA/
├── .env                       # Your credentials (gitignored)
├── .env.example              # Template
├── .gitignore                # Git rules
├── requirements.txt          # Dependencies
├── launcher.py               # Main launcher
├── gemini_studio.py          # Studio app
├── instagram_scraper.py      # Scraper app
├── face_swap.py              # Face swap app
├── README.md                 # Full documentation
├── SETUP.md                  # This file
├── MIGRATION_GUIDE.md        # V16→V17 guide
│
├── core/                     # Core modules
│   ├── config.py
│   ├── utils.py
│   ├── character_bank.py
│   └── gemini_engine.py
│
├── IMAGES/
│   └── GENERATED/            # AI-generated images
│
└── Scripts/
    ├── Insta_Scrap/          # Instagram downloads
    └── Face_Swap/            # Face swap files
```

---

## ⚙️ Configuration Options

### Gemini Studio Settings

**Resolution** (in-app menu `[Q]`):
- `1K` - Fast, good for testing
- `2K` - Recommended for production ⭐
- `4K` - Maximum quality, slower

**Aspect Ratio** (in-app menu `[R]`):
- `3:2` - Best for portraits ⭐
- `16:9` - Wide cinematic
- `1:1` - Square (Instagram)
- `3:4` - Tall portrait

### Instagram Scraper Settings

**Download Mode**:
- `[1]` All - Photos + Videos
- `[2]` Photos only
- `[3]` Videos only

**Limit**: Number of items to download (default: 50)

---

## 🎨 Your First Generation

### Step-by-Step Tutorial

1. **Launch Gemini Studio**
   ```bash
   python gemini_studio.py
   ```

2. **Generate Character**
   - Press `[0]`
   - See random profile generated

3. **Set Quality**
   - Press `[Q]` → Choose `[2]` (2K)
   - Press `[R]` → Choose `[2]` (3:2 ratio)

4. **Phase 1: Foundation**
   - Press `[1]`
   - Wait ~30 seconds
   - Image opens automatically
   - Press `[K]` to keep

5. **Phase 2: Structure**
   - Press `[2]`
   - Drag Phase 1 image when prompted
   - Wait for generation
   - Press `[K]` to keep

6. **Phase 3: Dynamics**
   - Press `[3]`
   - Drag Phase 2 image when prompted
   - Wait for generation
   - Press `[K]` to keep

**Done!** You now have 3 images showing your character from different angles and emotions.

---

## 📚 Next Steps

- Read **README.md** for full documentation
- Check **MIGRATION_GUIDE.md** if upgrading from V16
- Explore character DNA customization
- Try different aspect ratios and resolutions
- Experiment with Instagram scraper

---

## 💡 Pro Tips

1. **Always use Phase 1 output** as reference for Phase 2
2. **Keep character DNA consistent** across all phases
3. **Use 2K resolution** for best quality/speed balance
4. **Organize images by character** for easy reference
5. **Backup your `.env` file** securely (not in git!)

---

## 🆘 Need Help?

- Check the full **README.md**
- Review **MIGRATION_GUIDE.md** for V16 users
- Verify all dependencies are installed
- Check `.env` file is configured correctly

---

**Setup Complete!** 🎉

You're ready to create amazing AI-generated content!
