# GITHUB PUSH - EXACT POWERSHELL COMMANDS

## STEP 1: Initialize Git and Create First Commit
Run these commands in PowerShell from your project folder (d:\violence_ai):

```powershell
# Navigate to project
cd d:\violence_ai

# Initialize git repo
git init

# Configure git (REPLACE with your GitHub email & name)
git config user.email "YOUR_GITHUB_EMAIL@gmail.com"
git config user.name "Your Name"

# Stage all files (respects .gitignore)
git add .

# Verify staged files (should show 23 files)
git status

# Create first commit
git commit -m "Initial commit: Violence Detection AI with trained ResNet50+LSTM model"

# Verify commit
git log --oneline -1
```

**Expected output after `git status`:**
```
On branch master

No commits yet

Changes to be committed:
  (use "git rm --cached <file>..." to unstable)
    new file: .gitignore
    new file: GITHUB_PUSH_GUIDE.md
    new file: GITHUB_PUSH_QUICK_REFERENCE.md
    new file: README.md
    new file: requirements.txt
    new file: app/ui.py
    new file: model/violence_model.h5
    ... (23 files total)

Untracked files: (none)
```

---

## STEP 2: Create GitHub Repository (MANUAL - Do This on GitHub Website)

1. Go to: **https://github.com/new**
2. Fill in:
   - **Repository name:** `violence_ai`
   - **Description:** `Deep Learning Video Violence Detection using ResNet50+LSTM. Pre-trained model included - ready to use immediately.`
   - **Visibility:** Select **PUBLIC** (to share with others)
   - ⚠️ **DO NOT** check "Initialize this repository with a README" (we have one)
   - ⚠️ **DO NOT** add .gitignore or license (we have our own)
3. Click **Create repository**
4. You'll see a page with commands - we'll use the second option

---

## STEP 3: Connect Local Repo to GitHub and Push

Back in PowerShell, run:

```powershell
# Replace YOUR_USERNAME with your GitHub username
git remote add origin https://github.com/YOUR_USERNAME/violence_ai.git

# Rename branch to 'main' (GitHub's default)
git branch -M main

# Push code to GitHub
git push -u origin main
```

**Replace `YOUR_USERNAME` with your actual GitHub username!**

Example if your username is "jane-doe":
```powershell
git remote add origin https://github.com/jane-doe/violence_ai.git
```

**This command will:**
- Upload all 23 files
- Include the trained model (103 MB)
- Exclude data/ folder and venv/ (as per .gitignore)
- Create 'main' branch on GitHub

---

## STEP 4: Verify Push Success

```powershell
# Check remote is connected
git remote -v

# Show commit history
git log --oneline -3

# Check current branch
git branch -v

# Verify push
git log origin/main --oneline -1
```

**Expected output:**
```
origin	https://github.com/YOUR_USERNAME/violence_ai.git (fetch)
origin	https://github.com/YOUR_USERNAME/violence_ai.git (push)

commit_hash Initial commit: Violence Detection AI...

* main    commit_hash [origin/main: ahead 0, behind 0] Initial commit...
```

---

## What Gets Pushed ✅ / Excluded ❌

### ✅ PUSHED (23 files, ~200 MB total):
```
.gitignore                          1 KB
README.md                         ~5 KB
GITHUB_PUSH_GUIDE.md              ~8 KB
GITHUB_PUSH_QUICK_REFERENCE.md    ~4 KB
requirements.txt                  ~1 KB
test_training_fix.py              ~2 KB
TRAINING_FIX_README.md            ~3 KB
TRAINING_FIX_SUMMARY.md           ~2 KB
[10+ more markdown docs]          ~20 KB
app/ui.py                        ~20 KB
src/train.py                     ~8 KB
src/net.py                       ~6 KB
src/predict.py                   ~4 KB
src/load_data.py                 ~8 KB
src/frames.py                    ~5 KB
src/__init__.py                  ~1 KB
model/violence_model.h5          103 MB  ← TRAINED MODEL (INCLUDED!)
```

### ❌ EXCLUDED (by .gitignore):
```
data/                            (raw video dataset)
venv/                            (Python virtual environment)
outputs/                         (temporary output files)
__pycache__/                     (Python cache)
*.log                            (log files)
.vscode/, .idea/                 (IDE settings)
```

---

## View Your Repository

After successful push, visit:
```
https://github.com/YOUR_USERNAME/violence_ai
```

You should see:
- All code files listed
- Model file (103 MB) included
- README displayed on front page
- Green "main" branch selector

---

## Next Steps on GitHub

1. **Share the link** with colleagues/team
2. **Add GitHub topics:** Edit repo settings → Add topics: `python` `machine-learning` `violence-detection` `deep-learning` `tensorflow` `streamlit`
3. **Add screenshots:**
   - Create `screenshots/` folder locally
   - Add UI screenshots
   - Commit and push: `git add screenshots/` → `git commit -m "Add UI screenshots"` → `git push`
4. **Add badges to README** (optional):
   - Python version badge
   - License badge
   - GitHub stars badge

---

## Troubleshooting

**Problem:** `fatal: not a git repository`
- **Solution:** Run `git init` first, then `git config user.email "..."` etc.

**Problem:** `error: The file will have its original line endings in your working directory`
- **Solution:** This is normal on Windows. Just proceed - git handles it.

**Problem:** `Permission denied (publickey)`
- **Solution:** 
  - Generate SSH key: `ssh-keygen -t rsa -b 4096`
  - Add to GitHub: Settings → SSH and GPG keys → New SSH key
  - Copy public key from `~/.ssh/id_rsa.pub`
  - Use SSH URL instead: `git@github.com:YOUR_USERNAME/violence_ai.git`

**Problem:** `error: failed to push some refs to 'origin'`
- **Solution:** 
  - Run: `git pull origin main --allow-unrelated-histories`
  - Then: `git push -u origin main`

**Problem:** Model file (103 MB) too slow to push?
- **Solution:** This is normal - GitHub limits file size to 100 MB per file after initial push
  - Our 103 MB is within limits for initial commit
  - If issues occur, use Git LFS: https://git-lfs.com/

---

## Verify Model File on GitHub

After push, verify model is on GitHub:

```powershell
# Check file size matches locally
(Get-Item model/violence_model.h5).Length / 1MB  # Shows: 103.25 MB

# Check remote has it
git ls-tree -r origin/main | grep "violence_model.h5"
```

---

## Users Can Now Clone & Run

Once pushed, users will:

```bash
# Clone repo with trained model included
git clone https://github.com/YOUR_USERNAME/violence_ai.git
cd violence_ai

# Install & run (no retraining needed!)
pip install -r requirements.txt
streamlit run app/ui.py
```

**They get your trained model immediately** - no 2-4 hour training wait! 🚀

---

## Complete Command Sequence (Copy-Paste)

```powershell
cd d:\violence_ai
git init
git config user.email "YOUR_EMAIL@gmail.com"
git config user.name "Your Name"
git add .
git commit -m "Initial commit: Violence Detection AI with trained ResNet50+LSTM model"
git remote add origin https://github.com/YOUR_USERNAME/violence_ai.git
git branch -M main
git push -u origin main
git remote -v
git log --oneline -3
```

Replace `YOUR_EMAIL@gmail.com`, `Your Name`, and `YOUR_USERNAME` before running!

---

**That's it!** Your violence_ai project is now on GitHub with the trained model included. 🎉
