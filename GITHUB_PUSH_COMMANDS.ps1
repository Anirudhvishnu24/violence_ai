# ============================================================================
# VIOLENCE AI - GITHUB PUSH COMMANDS (WINDOWS POWERSHELL)
# ============================================================================
# CASE 1: Include trained model so users can run immediately without training
# 
# What gets pushed:
#   ✅ Source code (src/*.py)
#   ✅ Streamlit app (app/ui.py)
#   ✅ Trained model (model/violence_model.h5 - 103 MB)
#   ✅ Documentation (README.md, requirements.txt)
#
# What gets excluded:
#   ❌ data/ folder (raw video dataset - too large)
#   ❌ venv/ folder (virtual environment)
#   ❌ temp/ (temporary files)
#   ❌ __pycache__/ (Python cache)
# ============================================================================

# STEP 1: Initialize Git Repository
# ============================================================================
Write-Host "Step 1: Initialize Git Repository" -ForegroundColor Cyan
Write-Host "Run this command in PowerShell:" -ForegroundColor Yellow

Write-Host @"
cd D:\violence_ai
git init
"@ -ForegroundColor White

# Then configure your git identity (replace with your actual info)
Write-Host @"
git config user.email "your.email@gmail.com"
git config user.name "Your Name"
"@ -ForegroundColor White

Write-Host ""

# STEP 2: Stage and Commit All Files
# ============================================================================
Write-Host "Step 2: Stage Files and Create Commit" -ForegroundColor Cyan
Write-Host "Run these commands:" -ForegroundColor Yellow

Write-Host @"
git add .
git status
git commit -m "Initial commit: Violence Detection AI with trained ResNet50+LSTM model (CASE 1 - model included)"
"@ -ForegroundColor White

Write-Host "✓ Expected: You should see ~25 files staged (model, code, docs)" -ForegroundColor Green
Write-Host ""

# STEP 3: Create GitHub Repository (MANUAL - DO THIS ON GITHUB WEBSITE)
# ============================================================================
Write-Host "Step 3: Create Empty Repository on GitHub Website" -ForegroundColor Cyan
Write-Host "Go to: https://github.com/new" -ForegroundColor Yellow
Write-Host @"
Fill in these fields:
  • Repository name: violence_ai
  • Description: Deep Learning Violence Detection AI (ResNet50+LSTM) with pre-trained model
  • Visibility: Public
  
  ⚠️  DO NOT check:
    - "Initialize this repository with a README"
    - "Add .gitignore"
    - "Add a license"

Click "Create repository"
"@ -ForegroundColor White

Write-Host ""

# STEP 4: Connect to GitHub and Push
# ============================================================================
Write-Host "Step 4: Connect Local Repo to GitHub and Push" -ForegroundColor Cyan
Write-Host "Run these commands (replace YOUR_USERNAME):" -ForegroundColor Yellow

Write-Host @"
git remote add origin https://github.com/YOUR_USERNAME/violence_ai.git
git branch -M main
git push -u origin main
"@ -ForegroundColor White

Write-Host "Example if your username is 'jane-doe':" -ForegroundColor Gray
Write-Host @"
git remote add origin https://github.com/jane-doe/violence_ai.git
"@ -ForegroundColor Gray

Write-Host ""

# STEP 5: Verify Push Success
# ============================================================================
Write-Host "Step 5: Verify Push Success" -ForegroundColor Cyan
Write-Host "Run these commands to verify:" -ForegroundColor Yellow

Write-Host @"
git remote -v
git log --oneline -3
git branch -v
"@ -ForegroundColor White

Write-Host "Expected output:" -ForegroundColor Gray
Write-Host @"
origin  https://github.com/YOUR_USERNAME/violence_ai.git (fetch)
origin  https://github.com/YOUR_USERNAME/violence_ai.git (push)

hash1 Initial commit: Violence Detection AI...
hash2 [previous commits if any]

* main    hash [origin/main] Initial commit...
"@ -ForegroundColor Gray

Write-Host ""

# ============================================================================
# SUMMARY
# ============================================================================
Write-Host "=" * 75 -ForegroundColor Cyan
Write-Host "SUMMARY" -ForegroundColor Cyan
Write-Host "=" * 75 -ForegroundColor Cyan

Write-Host @"
What you're pushing:
  • Source Code: src/*.py (train, predict, network)
  • UI: app/ui.py (Streamlit dashboard)
  • Model: model/violence_model.h5 (103 MB - trained ResNet50+LSTM)
  • Docs: README.md, requirements.txt
  • Total: ~26 files, ~200 MB

What you're NOT pushing:
  • data/ folder (raw videos - excluded)
  • venv/ folder (virtual environment - excluded)
  • __pycache__/ (Python cache - excluded)

After push, users can:
  git clone https://github.com/YOUR_USERNAME/violence_ai.git
  cd violence_ai
  pip install -r requirements.txt
  streamlit run app/ui.py

  ✓ They get your trained model immediately - NO retraining needed!
"@ -ForegroundColor Green

Write-Host ""
Write-Host "Ready to deploy? Follow the steps above! 🚀" -ForegroundColor Yellow
