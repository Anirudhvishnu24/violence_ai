# REPO CLEANUP - MOVE DOCS TO docs/ FOLDER

## Overview

Organize guide files into `docs/` folder for a clean, professional repository layout.

**Before:**
```
root/
├── README.md
├── AUTO_DOWNLOAD_SETUP.md
├── COPY_PASTE_COMMANDS.txt
├── DEPLOYMENT_CHECKLIST.md
├── EVALUATION_FIX.md
├── ... (many more guide files)
├── src/
└── app/
```

**After:**
```
root/
├── README.md
├── docs/
│   ├── AUTO_DOWNLOAD_SETUP.md
│   ├── COPY_PASTE_COMMANDS.txt
│   ├── DEPLOYMENT_CHECKLIST.md
│   ├── EVALUATION_FIX.md
│   ├── ... (all guides here)
├── src/
└── app/
```

---

## Step-by-Step Commands

### Step 1: Navigate to Project Root

```powershell
cd D:\violence_ai
```

### Step 2: Move Guide Files to docs/ Folder

Use `git mv` to move files (tracks the move in git history):

```powershell
# Auto-download guides
git mv AUTO_DOWNLOAD_SETUP.md docs/
git mv QUICK_REFERENCE_AUTO_DOWNLOAD.md docs/
git mv COPY_PASTE_COMMANDS.txt docs/
git mv GITHUB_PUSH_COMMANDS.ps1 docs/
git mv GITHUB_EXACT_COMMANDS.md docs/
git mv GITHUB_FINAL_PUSH.md docs/
git mv GITHUB_FINAL_PUSH.txt docs/
git mv GITHUB_PUSH_GUIDE.md docs/
git mv GITHUB_PUSH_QUICK_REFERENCE.md docs/
git mv GITHUB_PUSH_STEPS.md docs/

# Deployment guides
git mv DEPLOYMENT_CHECKLIST.md docs/

# Training/Evaluation guides
git mv EVALUATION_FIX.md docs/
git mv EVALUATION_FIX_BEFORE_AFTER.md docs/
git mv EVALUATION_FIX_COMPLETE.md docs/
git mv EVALUATION_FIX_VERIFICATION.md docs/
git mv TRAINING_FIX_README.md docs/
git mv TRAINING_FIX_SUMMARY.md docs/

# UI guides
git mv UI_DESIGN_REFERENCE.md docs/
git mv UI_IMPLEMENTATION_REPORT.md docs/
git mv UI_REDESIGN.md docs/
git mv UI_REDESIGN_COMPLETE.md docs/
git mv UI_UPGRADE_COMPLETE.md docs/

# Other documentation
git mv FIX_COMPLETE.md docs/
git mv EXACT_CODE_CHANGES.md docs/
git mv START_HERE_DEPLOYMENT.ps1 docs/
git mv STREAMLIT_QUICK_START.md docs/
git mv README_QUICK_START_SECTION.md docs/
git mv QUICK_REFERENCE_AUTO_DOWNLOAD.md docs/

# Any other markdown files in root (except README.md)
```

---

## All Commands at Once (Copy-Paste)

Run this entire block in PowerShell:

```powershell
cd D:\violence_ai

# Auto-download related
git mv AUTO_DOWNLOAD_SETUP.md docs/ 2>$null
git mv QUICK_REFERENCE_AUTO_DOWNLOAD.md docs/ 2>$null
git mv COPY_PASTE_COMMANDS.txt docs/ 2>$null
git mv GITHUB_PUSH_COMMANDS.ps1 docs/ 2>$null
git mv GITHUB_EXACT_COMMANDS.md docs/ 2>$null
git mv GITHUB_FINAL_PUSH.md docs/ 2>$null
git mv GITHUB_FINAL_PUSH.txt docs/ 2>$null
git mv GITHUB_PUSH_GUIDE.md docs/ 2>$null
git mv GITHUB_PUSH_QUICK_REFERENCE.md docs/ 2>$null
git mv GITHUB_PUSH_STEPS.md docs/ 2>$null

# Deployment
git mv DEPLOYMENT_CHECKLIST.md docs/ 2>$null

# Evaluation/Training
git mv EVALUATION_FIX.md docs/ 2>$null
git mv EVALUATION_FIX_BEFORE_AFTER.md docs/ 2>$null
git mv EVALUATION_FIX_COMPLETE.md docs/ 2>$null
git mv EVALUATION_FIX_VERIFICATION.md docs/ 2>$null
git mv EXACT_CODE_CHANGES.md docs/ 2>$null
git mv FIX_COMPLETE.md docs/ 2>$null
git mv TRAINING_FIX_README.md docs/ 2>$null
git mv TRAINING_FIX_SUMMARY.md docs/ 2>$null

# UI
git mv UI_DESIGN_REFERENCE.md docs/ 2>$null
git mv UI_IMPLEMENTATION_REPORT.md docs/ 2>$null
git mv UI_REDESIGN.md docs/ 2>$null
git mv UI_REDESIGN_COMPLETE.md docs/ 2>$null
git mv UI_UPGRADE_COMPLETE.md docs/ 2>$null

# Other docs
git mv START_HERE_DEPLOYMENT.ps1 docs/ 2>$null
git mv STREAMLIT_QUICK_START.md docs/ 2>$null
git mv README_QUICK_START_SECTION.md docs/ 2>$null
```

---

## Step 3: Review Changes

```powershell
git status
```

**Expected output:**
```
On branch main
Your branch is up to date with 'origin/main'.

Changes to be committed:
  renamed:    AUTO_DOWNLOAD_SETUP.md -> docs/AUTO_DOWNLOAD_SETUP.md
  renamed:    QUICK_REFERENCE_AUTO_DOWNLOAD.md -> docs/QUICK_REFERENCE_AUTO_DOWNLOAD.md
  renamed:    ... (all guides moved)
  modified:   README.md
```

---

## Step 4: Commit Changes

```powershell
git commit -m "Organize documentation into docs/ folder for cleaner repository structure"
```

---

## Step 5: Push to GitHub

```powershell
git push origin main
```

---

## Verify on GitHub

Go to: https://github.com/Anirudhvishnu24/violence_ai

Check:
- ✅ Root folder shows only: `app/`, `src/`, `outputs/`, `model/`, `README.md`, `requirements.txt`, etc.
- ✅ New `docs/` folder visible with all guides
- ✅ README.md has "Documentation" section with links to `docs/` files
- ✅ No clutter in root folder

---

## Files That Remain in Root

✅ Keep these in root:
- `README.md` - Main project documentation
- `requirements.txt` - Python dependencies
- `.gitignore` - Git configuration
- `.gitattributes` - Git LFS configuration
- `app/` - Application code
- `src/` - Source code
- `outputs/` - Generated outputs
- `model/` - Model directory (empty at clone time)
- `data/` - Training data (if applicable)

---

## Final Result

**Root folder now contains only:**
```
violence_ai/
├── README.md              ← Main documentation
├── requirements.txt       ← Dependencies
├── .gitignore
├── .gitattributes
├── app/                   ← Streamlit UI
├── src/                   ← Source code
├── model/                 ← Model directory
├── outputs/               ← Generated files
├── docs/                  ← All guides organized here
│   ├── AUTO_DOWNLOAD_SETUP.md
│   ├── DEPLOYMENT_CHECKLIST.md
│   ├── GITHUB_FINAL_PUSH.md
│   ├── ... (all other guides)
└── ... (minimal clutter)
```

---

## Professional Appearance

✅ **For Recruiters:**
- Clean, organized repository structure
- Main documentation in README.md
- Detailed guides in docs/ folder (not cluttering root)
- Code easily visible (app/, src/)
- Professional first impression

---

## Rollback (If Needed)

If you want to undo this:

```powershell
git reset --hard HEAD~1
git push origin main -f
```

---

**All set! Run the commands above to clean up your repo! 🎉**
