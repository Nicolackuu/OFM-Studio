# 🗑️ MANIFEST TO DELETE - OFM IA PROJECT CLEANUP

**Generated:** 22 January 2026  
**Purpose:** Identify and remove versioned/duplicate files for project sanitization

---

## 📊 SCAN SUMMARY

**Total files scanned:** 8 root Python files + 21 documentation files + _TRASH folder  
**Versioned files found:** 13 (excluding venv)  
**Recommendation:** DELETE 10 files, KEEP 3 for reference

---

## 🔴 CATEGORY 1: VERSIONED DOCUMENTATION (TO DELETE)

These are historical documentation files that are **superseded** by current versions or no longer relevant:

### 1. `REFACTORING_V18.md`
- **Status:** OBSOLETE
- **Reason:** Superseded by V19, V21 documentation
- **Action:** ❌ DELETE

### 2. `NAVIGATION_V19.md`
- **Status:** OBSOLETE
- **Reason:** Superseded by V21 fixes
- **Action:** ❌ DELETE

### 3. `UI_UX_FIX_V19.md`
- **Status:** OBSOLETE
- **Reason:** Superseded by V21 fixes
- **Action:** ❌ DELETE

### 4. `FINAL_V19_DEPLOYMENT.md`
- **Status:** OBSOLETE
- **Reason:** Superseded by V21 deployment
- **Action:** ❌ DELETE

### 5. `FACTORY_V21_2_FIX.md`
- **Status:** OBSOLETE
- **Reason:** Superseded by V21.3, V21.4, V21.5
- **Action:** ❌ DELETE

### 6. `SYSTEM_REPAIR_V21_3.md`
- **Status:** OBSOLETE
- **Reason:** Superseded by MISSION_COMPLETE_V21_3.md
- **Action:** ❌ DELETE

---

## 🟡 CATEGORY 2: VERSIONED DOCUMENTATION (TO KEEP)

These contain **unique/valuable** information or represent the **latest** version:

### 1. `MISSION_COMPLETE_V21_3.md`
- **Status:** KEEP
- **Reason:** Comprehensive summary of V21.3 repairs
- **Action:** ✅ KEEP

### 2. `URGENT_FIX_V21_4.md`
- **Status:** KEEP
- **Reason:** Documents Curation module creation + infrastructure fixes
- **Action:** ✅ KEEP

### 3. `API_FIX_V21_5.md`
- **Status:** KEEP
- **Reason:** Critical API fix documentation (response_modalities issue)
- **Action:** ✅ KEEP

---

## 🔴 CATEGORY 3: _TRASH FOLDER (TO DELETE)

All files in `_TRASH/` are **obsolete** and can be safely deleted:

### 1. `_TRASH/studio_dashboard_old.py`
- **Status:** OBSOLETE
- **Reason:** Superseded by studio_premium.py
- **Action:** ❌ DELETE

### 2. `_TRASH/studio_dashboard_v17.py`
- **Status:** OBSOLETE
- **Reason:** Superseded by studio_premium.py
- **Action:** ❌ DELETE

### 3. `_TRASH/face_swap.py`
- **Status:** OBSOLETE
- **Reason:** Superseded by core/batch_face_swap.py
- **Action:** ❌ DELETE

### 4. `_TRASH/gemini_studio.py`
- **Status:** OBSOLETE
- **Reason:** Superseded by core/gemini_engine.py
- **Action:** ❌ DELETE

### 5. `_TRASH/instagram_scraper.py`
- **Status:** OBSOLETE
- **Reason:** Superseded by ui/scraper.py
- **Action:** ❌ DELETE

---

## 🟢 CATEGORY 4: ROOT PYTHON FILES (ANALYSIS)

### Files to KEEP (Active/Current):

1. **`studio_premium.py`** ✅
   - **Status:** PRIMARY ENTRY POINT
   - **Reason:** Main application file (fixed in V21.5)
   - **Action:** KEEP

2. **`studio_premium_fixed.py`** ✅
   - **Status:** ALTERNATIVE ENTRY POINT
   - **Reason:** Contains integrity checker + 5-tab navigation
   - **Action:** KEEP (or merge with studio_premium.py)

3. **`launcher.py`** ✅
   - **Status:** UTILITY
   - **Reason:** Launcher script
   - **Action:** KEEP

4. **`Show_Tree.py`** ✅
   - **Status:** UTILITY
   - **Reason:** Project structure visualization
   - **Action:** KEEP

5. **`integrity_cleaner.py`** ✅
   - **Status:** UTILITY
   - **Reason:** Cleanup utility
   - **Action:** KEEP

### Files to DELETE/MERGE:

1. **`studio_dashboard.py`** ⚠️
   - **Status:** DUPLICATE
   - **Reason:** Likely superseded by studio_premium.py
   - **Action:** ❌ DELETE (after verification)

2. **`studio_linear.py`** ⚠️
   - **Status:** DUPLICATE
   - **Reason:** Likely superseded by studio_premium.py
   - **Action:** ❌ DELETE (after verification)

3. **`dataset_factory.py`** ⚠️
   - **Status:** STANDALONE SCRIPT
   - **Reason:** May contain unique logic for dataset generation
   - **Action:** 🔍 REVIEW FIRST (check for unique functions)

---

## 🔴 CATEGORY 5: SCRIPTS FOLDER (TO REVIEW)

### `Scripts/Face_Swap/Gemini_Creator_V2.py`
- **Status:** VERSIONED
- **Reason:** May contain unique logic not in current batch_face_swap.py
- **Action:** 🔍 REVIEW FIRST

---

## 📋 DELETION CHECKLIST

### Phase 1: Safe Deletions (No Review Needed)
- [ ] Delete `REFACTORING_V18.md`
- [ ] Delete `NAVIGATION_V19.md`
- [ ] Delete `UI_UX_FIX_V19.md`
- [ ] Delete `FINAL_V19_DEPLOYMENT.md`
- [ ] Delete `FACTORY_V21_2_FIX.md`
- [ ] Delete `SYSTEM_REPAIR_V21_3.md`
- [ ] Delete entire `_TRASH/` folder (5 files)

**Total: 11 files**

### Phase 2: Review Before Deletion
- [ ] Review `studio_dashboard.py` (compare with studio_premium.py)
- [ ] Review `studio_linear.py` (compare with studio_premium.py)
- [ ] Review `dataset_factory.py` (check for unique functions)
- [ ] Review `Scripts/Face_Swap/Gemini_Creator_V2.py` (compare with batch_face_swap.py)

**Total: 4 files**

---

## 🎯 RECOMMENDED ACTIONS

### Immediate (No Risk):
```bash
# Delete obsolete documentation
rm REFACTORING_V18.md
rm NAVIGATION_V19.md
rm UI_UX_FIX_V19.md
rm FINAL_V19_DEPLOYMENT.md
rm FACTORY_V21_2_FIX.md
rm SYSTEM_REPAIR_V21_3.md

# Delete _TRASH folder
rm -rf _TRASH/
```

### After Review:
```bash
# If studio_dashboard.py is duplicate
rm studio_dashboard.py

# If studio_linear.py is duplicate
rm studio_linear.py

# If dataset_factory.py logic is integrated
rm dataset_factory.py

# If Gemini_Creator_V2.py is obsolete
rm Scripts/Face_Swap/Gemini_Creator_V2.py
```

---

## 📊 IMPACT ANALYSIS

### Before Cleanup:
- **Root Python files:** 8
- **Documentation files:** 21
- **_TRASH files:** 5
- **Total clutter:** 34 files

### After Cleanup (Conservative):
- **Root Python files:** 5 (delete 3)
- **Documentation files:** 15 (delete 6)
- **_TRASH files:** 0 (delete 5)
- **Total removed:** 14 files (41% reduction)

### After Cleanup (Aggressive):
- **Root Python files:** 5 (delete 3)
- **Documentation files:** 15 (delete 6)
- **_TRASH files:** 0 (delete 5)
- **Scripts cleaned:** 1 (delete Gemini_Creator_V2.py)
- **Total removed:** 15 files (44% reduction)

---

## ⚠️ WARNINGS

1. **DO NOT DELETE** without backup if unsure
2. **VERIFY** that studio_premium.py works before deleting alternatives
3. **CHECK** dataset_factory.py for unique batch processing logic
4. **REVIEW** Gemini_Creator_V2.py for any improvements over current code

---

## ✅ APPROVAL REQUIRED

**Please confirm deletion of Phase 1 files (11 files) before proceeding.**

Type "APPROVED" to proceed with safe deletions.
