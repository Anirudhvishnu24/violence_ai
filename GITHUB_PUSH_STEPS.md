# GITHUB PUSH - QUICK REFERENCE FOR WINDOWS POWERSHELL

## Your Command Sequence (Copy-Paste Ready)

Replace `YOUR_USERNAME` with your actual GitHub username. Replace `your.email@gmail.com` with your email.

```powershell
# COPY ALL THESE LINES AND PASTE INTO POWERSHELL

cd D:\violence_ai

git init

git config user.email "your.email@gmail.com"
git config user.name "Your Name"

git add .

git status

git commit -m "Initial commit: Violence Detection AI with trained ResNet50+LSTM model (CASE 1 - model included)"

git remote add origin https://github.com/YOUR_USERNAME/violence_ai.git

git branch -M main

git push -u origin main
```

---

## Step by Step

### 1️⃣ INITIALIZE (Run this first)
```powershell
cd D:\violence_ai
git init
git config user.email "your.email@gmail.com"
git config user.name "Your Name"
```

**What to expect:** No output (silent success)

---

### 2️⃣ STAGE & COMMIT (Run this second)
```powershell
git add .
git status
```

**What to expect:** Green text showing files to be committed (~25 files)

```powershell
git commit -m "Initial commit: Violence Detection AI with trained ResNet50+LSTM model (CASE 1 - model included)"
```

**What to expect:** Output showing files changed and insertions

---

### 3️⃣ CREATE EMPTY REPO ON GITHUB (Manual - Do this in browser)

Go to: **https://github.com/new**

Fill in:
- **Repository name:** `violence_ai`
- **Description:** `Deep Learning Violence Detection AI with pre-trained ResNet50+LSTM model`
- **Visibility:** Select "Public"

⚠️ **IMPORTANT:** Do NOT check any boxes like:
- "Initialize this repository with a README"
- "Add .gitignore"  
- "Add a license"

Click **Create repository** button

---

### 4️⃣ CONNECT & PUSH (Run this fourth)

Replace `YOUR_USERNAME` with your GitHub username:

```powershell
git remote add origin https://github.com/YOUR_USERNAME/violence_ai.git
git branch -M main
git push -u origin main
```

**What to expect:** GitHub will ask for authentication (login window pops up)
- Sign in with your GitHub account
- Authorize Git Credential Manager

**Success:** You'll see output like:
```
Enumerating objects: 26, done.
Counting objects: 100% (26/26), done.
Delta compression using up to 8 threads
Compressing objects: 100% (...)
Writing objects: 100% (...)
...
To https://github.com/YOUR_USERNAME/violence_ai.git
 * [new branch]      main -> main
Branch 'main' set up to track remote branch 'main' from 'origin'.
```

---

### 5️⃣ VERIFY SUCCESS (Run this to confirm)

```powershell
git remote -v
git log --oneline -3
git branch -v
```

**Expected output:**
```
origin  https://github.com/YOUR_USERNAME/violence_ai.git (fetch)
origin  https://github.com/YOUR_USERNAME/violence_ai.git (push)

hash1234567 Initial commit: Violence Detection AI...

* main    hash1234567 [origin/main] Initial commit...
```

---

## Troubleshooting

| Problem | Solution |
|---------|----------|
| "fatal: not a git repository" | Run `git init` first |
| "Permission denied (publickey)" | GitHub login window should pop up - sign in there |
| "error: The file will have its original line endings" | This is normal on Windows - just proceed |
| "Push rejected" | Run `git pull origin main --allow-unrelated-histories` then `git push -u origin main` |
| "Port 8501 already in use" when running app | Run `streamlit run app/ui.py --server.port 8502` |

---

## What Gets Pushed

✅ **Pushed to GitHub:**
- Source code: src/*.py
- App: app/ui.py
- Trained model: model/violence_model.h5 (103 MB)
- Documentation: README.md, requirements.txt, all markdown files
- Total: ~26 files (~200 MB)

❌ **NOT Pushed (excluded):**
- data/ folder (raw videos)
- venv/ folder (virtual environment)
- __pycache__/ (Python cache)
- *.log files (logs)

---

## After Push - Users Can Use Your Model

Users will do:

```bash
git clone https://github.com/YOUR_USERNAME/violence_ai.git
cd violence_ai
pip install -r requirements.txt
streamlit run app/ui.py
```

**✨ Your trained model is included - they don't need to train!**

---

## View Your Repository

After successful push, visit:
```
https://github.com/YOUR_USERNAME/violence_ai
```

You should see:
- All your code files listed
- README displayed on front page
- Model file (103 MB) included
- Green "main" branch selector

---

**That's it! You're deploying with CASE 1 (model included). 🚀**
