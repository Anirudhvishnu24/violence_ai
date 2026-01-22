# GitHub Push Guide - Violence Detection AI

## CASE 1: Include Trained Model (No Retraining Needed)

### Phase 1: Local Setup (PowerShell Commands)

Run these commands in PowerShell from `d:\violence_ai`:

```powershell
# 1. Initialize git repository
cd d:\violence_ai
git init

# 2. Configure git (use your GitHub email/name)
git config user.email "your.email@example.com"
git config user.name "Your Name"

# 3. Add all files (respects .gitignore - excludes data/, venv/, __pycache__/)
git add .

# 4. Check what will be committed
git status

# 5. Create first commit
git commit -m "Initial commit: Violence Detection AI with trained model"

# 6. Verify commit was created
git log --oneline
```

### Phase 2: Create GitHub Repository (Manual)

1. Go to https://github.com/new
2. Create repository named: `violence_ai`
3. Description: "Deep Learning Video Violence Detection with ResNet50+LSTM"
4. Choose **Public** or **Private** (recommended: Public for sharing)
5. **DO NOT** initialize with README, .gitignore, or license
6. Click **Create repository**

### Phase 3: Connect to GitHub & Push (PowerShell)

After creating the GitHub repo, GitHub will show you commands. Use these exact ones:

```powershell
# 7. Add remote origin (replace USERNAME with your GitHub username)
git remote add origin https://github.com/USERNAME/violence_ai.git

# 8. Rename branch to main (if on master)
git branch -M main

# 9. Push to GitHub
git push -u origin main

# 10. Verify push was successful
git remote -v
git log --oneline
```

### Phase 4: What Gets Pushed

✅ **INCLUDED:**
- Source code (src/*.py)
- Streamlit UI (app/ui.py)
- Trained model: `model/violence_model.h5` (the KEY file!)
- Requirements: `requirements.txt`
- Documentation: `README.md`, markdown files
- Configuration files

❌ **EXCLUDED** (per .gitignore):
- `data/` - Training datasets
- `venv/` - Virtual environment
- `__pycache__/` - Python cache
- `.vscode/` - IDE settings

### Phase 5: README Quick Start Section

Add this to your README.md for users who don't need to retrain:

```markdown
## Quick Start (No Training Needed)

The trained model is included in the repository, so you can run the application immediately without retraining.

### Installation

1. **Clone the repository:**
   ```bash
   git clone https://github.com/USERNAME/violence_ai.git
   cd violence_ai
   ```

2. **Create virtual environment:**
   ```bash
   python -m venv venv
   venv\Scripts\activate
   ```

3. **Install dependencies:**
   ```bash
   pip install -r requirements.txt
   ```

### Run the App

```bash
streamlit run app/ui.py
```

The app will open at `http://localhost:8501`

### Usage

1. Upload a video file (mp4, avi, mov, mkv, flv)
2. The model analyzes the video in real-time
3. Results show:
   - Prediction (VIOLENT/NONVIOLENT)
   - Violence Probability (%)
   - Risk Level (SAFE/MEDIUM/HIGH RISK)
   - Detailed analysis with insights

### Model Details

- **Architecture:** ResNet50 (CNN) + LSTM(128)
- **Input:** 30 frames × 224×224 pixels
- **Output:** Binary classification (0-1)
- **Threshold:** 0.50
- **Accuracy:** ~86% on validation set
- **Processing:** <5 seconds per video

### Training (Optional)

If you want to retrain the model with your own dataset:

```bash
# Place videos in:
# - data/violent/     (violent videos)
# - data/nonviolent/  (safe videos)

# Then run:
python -m src.train
```

The trained model will be saved to `model/violence_model.h5`
```

### Phase 6: Future Enhancements (After Pushing)

To add screenshots later:

```powershell
# Create screenshots directory
mkdir screenshots

# After adding screenshots:
git add screenshots/
git commit -m "Add UI screenshots to documentation"
git push origin main
```

Update README with screenshot section:

```markdown
## Screenshots

### Dashboard
![Dashboard](screenshots/dashboard.png)

### Prediction Results
![Results](screenshots/results.png)

### Detailed Analysis
![Analysis](screenshots/analysis.png)
```

### Phase 7: Verification Commands

After pushing, verify everything:

```powershell
# Check remote configuration
git remote -v

# View recent commits
git log --oneline -5

# Check branch status
git branch -v

# View what's tracked
git ls-files
```

### Common PowerShell Troubleshooting

```powershell
# If "fatal: not a git repository"
git init
git config user.email "your.email@example.com"
git config user.name "Your Name"

# If authentication fails, use GitHub Personal Access Token instead of password
# Go to: https://github.com/settings/tokens
# Generate new token with 'repo' scope
# Use token as password when prompted

# View current git config
git config --list

# Change remote if you made a mistake
git remote remove origin
git remote add origin https://github.com/USERNAME/violence_ai.git
```

### File Size Check

Before pushing, verify model file is reasonable size:

```powershell
ls -lh model/violence_model.h5
```

Expected: ~100-200 MB (should be fine for GitHub)

If model is >100 MB, GitHub may require Git LFS (Large File Storage):
- Instructions: https://git-lfs.github.com/

---

## Summary

**Total push should include:**
- ~10 source files
- 1 trained model (violence_model.h5)
- README + documentation
- Requirements file
- Total size: ~150-200 MB (mostly model)

**After push:**
- Others can clone and run WITHOUT training
- Only needs: Python 3.11 + pip install -r requirements.txt
- Trained model ready to use immediately

---

Replace `USERNAME` with your actual GitHub username before running commands!
