# GitHub Push - Quick Command Reference

## Your Project is Ready! ✓

- ✓ Model file: `model/violence_model.h5` (103.25 MB)
- ✓ .gitignore created and configured
- ✓ Source code complete
- ✓ README and documentation ready

---

## 4 Simple Steps to Push

### Step 1: Initialize Git (Run ONCE)

```powershell
cd d:\violence_ai
git init
git config user.email "your.github.email@gmail.com"
git config user.name "Your GitHub Name"
```

### Step 2: Stage and Commit

```powershell
git add .
git status
git commit -m "Initial commit: Violence Detection AI with trained model"
```

### Step 3: Create GitHub Repo

1. Go to **https://github.com/new**
2. Repository name: `violence_ai`
3. Description: "Deep Learning Video Violence Detection with ResNet50+LSTM"
4. Choose **Public** (recommended)
5. **Skip** initialization options
6. Click **Create repository**

### Step 4: Push to GitHub

```powershell
# Replace YOUR_USERNAME with your actual GitHub username
git remote add origin https://github.com/YOUR_USERNAME/violence_ai.git
git branch -M main
git push -u origin main
```

**That's it!** Your project is now on GitHub.

---

## Verify Success

```powershell
# Check remote
git remote -v

# See your commits
git log --oneline -3

# Confirm branch
git branch -v
```

---

## What Gets Pushed

✅ **INCLUDED** (~200 MB total):
- `src/` - Training and prediction code
- `app/ui.py` - Streamlit dashboard
- `model/violence_model.h5` - **Trained model** (103 MB)
- `requirements.txt` - Dependencies
- `README.md` - Documentation
- All markdown guides

❌ **EXCLUDED**:
- `data/` - Training videos (too large)
- `venv/` - Virtual environment (unnecessary)
- `__pycache__/` - Python cache files
- `.vscode/` - IDE settings

---

## For Others to Use Your Project

After you push, anyone can:

```bash
# 1. Clone
git clone https://github.com/YOUR_USERNAME/violence_ai.git
cd violence_ai

# 2. Setup
python -m venv venv
venv\Scripts\activate
pip install -r requirements.txt

# 3. Run (model already included!)
streamlit run app/ui.py
```

**No training needed!** Model is ready to use.

---

## Adding Screenshots Later

```powershell
# 1. Create folder
mkdir screenshots

# 2. Add screenshots (png/jpg files)
# Place images in screenshots/ folder

# 3. Commit and push
git add screenshots/
git commit -m "Add UI screenshots"
git push origin main
```

Then update README with:

```markdown
## Screenshots

![Dashboard](screenshots/dashboard.png)
![Results](screenshots/results.png)
```

---

## Troubleshooting

**"fatal: not a git repository"**
```powershell
git init
```

**"fatal: could not read Username"**
```powershell
# Use Personal Access Token instead of password
# Generate at: https://github.com/settings/tokens (scope: repo)
```

**Authentication issues**
```powershell
# Configure git
git config --global user.email "your@email.com"
git config --global user.name "Your Name"
```

**Check what will be pushed**
```powershell
git status
```

---

## File Manifest (What's Being Pushed)

```
violence_ai/
├── .gitignore                          # Excludes data/ venv/ __pycache__/
├── app/
│   ├── ui.py                          # Streamlit dashboard (premium design)
│   └── ui_backup.py                   # Backup
├── model/
│   └── violence_model.h5              # ⭐ TRAINED MODEL (103 MB)
├── src/
│   ├── __init__.py
│   ├── frames.py                      # Frame extraction
│   ├── load_data.py                   # Dataset pipeline (stratified split)
│   ├── net.py                         # Model architecture
│   ├── predict.py                     # Prediction pipeline
│   └── train.py                       # Training script
├── requirements.txt                   # All dependencies
├── README.md                          # Main documentation
├── GITHUB_PUSH_GUIDE.md              # This guide
├── STREAMLIT_QUICK_START.md          # Quick start
├── UI_UPGRADE_COMPLETE.md            # UI improvements
└── [Other markdown docs...]
```

**Total Size:** ~200 MB (model: 103 MB, code: ~1 MB, docs: <1 MB)

---

## Quick Answers

**Q: Will others need to train?**
A: No! Model is included. They just download and run.

**Q: Why is model so large?**
A: ResNet50 backbone + LSTM + dense layers = ~25.6M parameters

**Q: Can I use Git via VS Code instead?**
A: Yes! VS Code has built-in Git support. Same end result.

**Q: Do I need GitHub Desktop?**
A: No, PowerShell git commands work fine.

**Q: What if model file is too large?**
A: At 103 MB, it's fine. GitHub allows up to 100 GB per repo. Consider Git LFS if >500 MB.

---

## Next Steps After Pushing

1. ✓ Push to GitHub (Steps 1-4 above)
2. □ Add screenshots to `screenshots/` folder
3. □ Update README with screenshot section
4. □ Share GitHub link with others
5. □ Accept issues/PRs (optional)

---

**Ready to push?** Start with Step 1! 🚀
