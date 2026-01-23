# 🏗️ PHOTO CURING MODULE - ARCHITECTURE PROPOSAL

**Date:** 22 January 2026  
**Purpose:** Complete rebuild of Photo Curing feature from scratch  
**Status:** 📐 **DESIGN PHASE**

---

## 📋 PHASE 3: FEATURE OVERHAUL - ANALYSIS

### Current State (BROKEN)

**Existing Implementation:**
1. **Location:** `ui/factory.py` - Tab 2 "Curation Tinder" (lines 65-274)
2. **Also:** `ui/curation.py` - Standalone module (lines 1-235)

**Problems Identified:**
- ❌ Duplicate logic in 2 files (factory.py + curation.py)
- ❌ Tinder mode was broken (fixed in V21.4 but still fragmented)
- ❌ No AI-assisted curation (only manual swipe)
- ❌ No batch operations (approve/reject multiple)
- ❌ No quality filters (blur detection, face detection)
- ❌ No undo/redo functionality
- ❌ No export options (different formats)
- ❌ Session state management is fragile

**What Works:**
- ✅ Basic Tinder swipe UI (left/right)
- ✅ Progress bar and stats
- ✅ Dataset loading from DATASET/RAW/
- ✅ Save to DATASET/APPROVED/

---

## 🎯 NEW ARCHITECTURE - PRODUCTION-READY

### Design Principles

1. **Single Source of Truth:** One module, one responsibility
2. **Robust State Management:** Persistent across sessions
3. **AI-Assisted:** Optional auto-curation with confidence scores
4. **Batch Operations:** Select multiple, apply filters
5. **Quality Checks:** Blur detection, face detection, resolution checks
6. **Undo/Redo:** Full history with rollback
7. **Export Flexibility:** Multiple formats, custom naming

---

## 📦 MODULE STRUCTURE

```
core/
├── photo_curator.py          # NEW - Backend logic
│   ├── class PhotoCurator
│   │   ├── load_dataset()
│   │   ├── apply_quality_filters()
│   │   ├── auto_curate_with_ai()
│   │   ├── manual_approve()
│   │   ├── manual_reject()
│   │   ├── batch_approve()
│   │   ├── batch_reject()
│   │   ├── undo()
│   │   ├── redo()
│   │   ├── export_approved()
│   │   └── get_stats()
│   └── class QualityAnalyzer
│       ├── detect_blur()
│       ├── detect_faces()
│       ├── check_resolution()
│       └── calculate_quality_score()

ui/
├── curation_premium.py       # NEW - Modern UI (replaces curation.py)
│   ├── render()
│   ├── render_dataset_selector()
│   ├── render_quality_filters()
│   ├── render_tinder_mode()
│   ├── render_grid_mode()
│   ├── render_batch_mode()
│   ├── render_stats_panel()
│   └── render_export_panel()

data/
└── curation_history.json     # NEW - Persistent history
    ├── sessions[]
    │   ├── session_id
    │   ├── dataset_name
    │   ├── timestamp
    │   ├── approved[]
    │   ├── rejected[]
    │   └── actions[]
    └── current_session
```

---

## 🔧 BACKEND: core/photo_curator.py

### Class: PhotoCurator

**Responsibilities:**
- Load images from DATASET/RAW/
- Apply quality filters (blur, face detection, resolution)
- Manage approved/rejected lists
- Track history for undo/redo
- Export to DATASET/APPROVED/

**Key Methods:**

```python
class PhotoCurator:
    def __init__(self, dataset_path: Path):
        self.dataset_path = dataset_path
        self.images = []
        self.approved = []
        self.rejected = []
        self.history = []
        self.current_index = 0
        self.quality_analyzer = QualityAnalyzer()
    
    def load_dataset(self) -> List[Path]:
        """Load all images from dataset directory"""
        # Scan for .jpg, .jpeg, .png
        # Return sorted list of paths
    
    def apply_quality_filters(self, 
                             min_resolution: Tuple[int, int] = (512, 512),
                             max_blur_score: float = 100.0,
                             require_face: bool = True) -> List[Path]:
        """Filter images by quality criteria"""
        # Use QualityAnalyzer to score each image
        # Return filtered list
    
    def auto_curate_with_ai(self, 
                           model: str = "gemini-3-pro-image-preview",
                           criteria: str = "high quality portrait") -> Dict:
        """Use AI to auto-approve/reject images"""
        # Send batch to Gemini API
        # Get confidence scores
        # Auto-approve high confidence (>0.8)
        # Flag low confidence for manual review
    
    def manual_approve(self, image_path: Path):
        """Manually approve an image"""
        self.approved.append(image_path)
        self.history.append(("approve", image_path))
    
    def manual_reject(self, image_path: Path):
        """Manually reject an image"""
        self.rejected.append(image_path)
        self.history.append(("reject", image_path))
    
    def batch_approve(self, image_paths: List[Path]):
        """Approve multiple images at once"""
        for path in image_paths:
            self.manual_approve(path)
    
    def undo(self):
        """Undo last action"""
        if self.history:
            action, image_path = self.history.pop()
            if action == "approve":
                self.approved.remove(image_path)
            elif action == "reject":
                self.rejected.remove(image_path)
    
    def export_approved(self, 
                       output_dir: Path,
                       format: str = "dataset_{idx:03d}",
                       copy_mode: bool = True):
        """Export approved images to output directory"""
        # Copy or move files
        # Rename according to format
        # Create metadata JSON
```

### Class: QualityAnalyzer

**Responsibilities:**
- Detect blur using Laplacian variance
- Detect faces using OpenCV or InsightFace
- Check resolution
- Calculate overall quality score

**Key Methods:**

```python
class QualityAnalyzer:
    def detect_blur(self, image_path: Path) -> float:
        """Calculate blur score (0-100, lower = more blur)"""
        # Use cv2.Laplacian variance
        # Return normalized score
    
    def detect_faces(self, image_path: Path) -> int:
        """Count number of faces detected"""
        # Use cv2.CascadeClassifier or InsightFace
        # Return face count
    
    def check_resolution(self, image_path: Path) -> Tuple[int, int]:
        """Get image resolution"""
        # Use PIL.Image.open
        # Return (width, height)
    
    def calculate_quality_score(self, image_path: Path) -> Dict:
        """Calculate overall quality score"""
        return {
            "blur_score": self.detect_blur(image_path),
            "face_count": self.detect_faces(image_path),
            "resolution": self.check_resolution(image_path),
            "overall_score": weighted_average
        }
```

---

## 🎨 FRONTEND: ui/curation_premium.py

### Main Function: render()

**Layout:**
```
┌─────────────────────────────────────────────────────────┐
│ 🎯 Photo Curation - AI-Assisted Selection              │
├─────────────────────────────────────────────────────────┤
│ 📁 Dataset Selector                                     │
│   [Dropdown: @username] [Load Button]                   │
├─────────────────────────────────────────────────────────┤
│ 🔍 Quality Filters                                      │
│   Min Resolution: [1024x1024]                           │
│   Max Blur: [100] Require Face: [✓]                    │
│   [Apply Filters] [Auto-Curate with AI]                │
├─────────────────────────────────────────────────────────┤
│ 📊 Stats Panel                                          │
│   Total: 32 | Approved: 12 | Rejected: 8 | Pending: 12 │
│   [Progress Bar: ████████░░░░ 62%]                     │
├─────────────────────────────────────────────────────────┤
│ 🎴 Curation Mode: [Tinder] [Grid] [Batch]              │
│                                                         │
│   ┌─────────────────────────────────────┐             │
│   │                                     │             │
│   │         [Current Image]             │             │
│   │                                     │             │
│   └─────────────────────────────────────┘             │
│                                                         │
│   [❌ Reject] [⏭️ Skip] [✅ Approve]                   │
│   [↶ Undo] [↷ Redo]                                    │
├─────────────────────────────────────────────────────────┤
│ 💾 Export                                               │
│   Format: [dataset_{idx:03d}] Output: [APPROVED/]      │
│   [Export Approved Images]                              │
└─────────────────────────────────────────────────────────┘
```

### Key Features:

1. **Dataset Selector**
   - Dropdown of all datasets in DATASET/RAW/
   - Load button with progress indicator
   - Auto-load last used dataset

2. **Quality Filters**
   - Min resolution slider (512-2048px)
   - Max blur threshold (0-200)
   - Require face checkbox
   - Apply filters button (instant feedback)
   - Auto-curate with AI button (batch processing)

3. **Stats Panel**
   - Real-time counters (Total, Approved, Rejected, Pending)
   - Progress bar (Linear style)
   - Quality score distribution chart

4. **Curation Modes**
   - **Tinder Mode:** Swipe left/right (current implementation)
   - **Grid Mode:** See 9 images at once, click to approve/reject
   - **Batch Mode:** Select multiple with checkboxes, bulk actions

5. **Undo/Redo**
   - Full history tracking
   - Undo last action (↶)
   - Redo undone action (↷)

6. **Export Panel**
   - Custom naming format
   - Output directory selector
   - Copy vs Move option
   - Generate metadata JSON

---

## 🚀 IMPLEMENTATION PLAN

### Step 1: Backend (core/photo_curator.py)
1. Create PhotoCurator class
2. Implement load_dataset()
3. Implement QualityAnalyzer class
4. Implement manual approve/reject with history
5. Implement undo/redo
6. Implement export_approved()

### Step 2: Frontend (ui/curation_premium.py)
1. Create basic layout with tabs
2. Implement dataset selector
3. Implement quality filters UI
4. Implement Tinder mode (reuse existing)
5. Implement Grid mode (new)
6. Implement Batch mode (new)
7. Implement stats panel
8. Implement export panel

### Step 3: Integration
1. Replace `ui/curation.py` with `ui/curation_premium.py`
2. Remove Tab 2 from `ui/factory.py`
3. Update `studio_premium.py` navigation
4. Add persistent history (curation_history.json)

### Step 4: Testing
1. Test with 32-image dataset
2. Test quality filters
3. Test undo/redo
4. Test export
5. Test AI auto-curation (optional)

---

## 📊 COMPARISON: OLD vs NEW

| Feature | OLD (curation.py) | NEW (curation_premium.py) |
|---------|-------------------|---------------------------|
| **Tinder Mode** | ✅ Basic | ✅ Enhanced with undo |
| **Grid Mode** | ❌ None | ✅ 9-image grid |
| **Batch Mode** | ❌ None | ✅ Multi-select |
| **Quality Filters** | ❌ None | ✅ Blur, Face, Resolution |
| **AI Auto-Curation** | ❌ None | ✅ Gemini API |
| **Undo/Redo** | ❌ None | ✅ Full history |
| **Export Options** | ✅ Basic | ✅ Custom format |
| **Stats** | ✅ Basic | ✅ Detailed with charts |
| **Persistent History** | ❌ None | ✅ JSON file |

---

## ✅ APPROVAL REQUIRED

**This is the proposed architecture for the new Photo Curing module.**

**Questions:**
1. Do you approve this architecture?
2. Should I proceed with implementation?
3. Any specific features to add/remove?

**Next Steps (if approved):**
1. Implement `core/photo_curator.py` (backend)
2. Implement `ui/curation_premium.py` (frontend)
3. Integrate with main application
4. Test and deploy

