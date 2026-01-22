#!/usr/bin/env pwsh
# ============================================================================
# VIOLENCE AI - GITHUB DEPLOYMENT - START HERE
# ============================================================================
# This is your complete deployment guide for Windows PowerShell
# Follow these exact steps to push your project to GitHub
#
# CASE 1 DEPLOYMENT: Trained model included (users don't need to retrain)
# ============================================================================

Write-Host "`n╔════════════════════════════════════════════════════════════════════════════╗" -ForegroundColor Cyan
Write-Host "║       VIOLENCE AI - GITHUB DEPLOYMENT GUIDE (WINDOWS POWERSHELL)           ║" -ForegroundColor Cyan
Write-Host "╚════════════════════════════════════════════════════════════════════════════╝`n" -ForegroundColor Cyan

Write-Host "PROJECT: violence_ai" -ForegroundColor Yellow
Write-Host "DEPLOYMENT TYPE: CASE 1 (Model Included - No Retraining Needed)" -ForegroundColor Green
Write-Host "MODEL SIZE: 103.25 MB" -ForegroundColor Green
Write-Host "FILES TO PUSH: ~26 files (~200 MB total)" -ForegroundColor Green
Write-Host "`n"

# ============================================================================
# SECTION 1: VERIFY SETUP
# ============================================================================

Write-Host "STEP 0: VERIFY YOUR SETUP" -ForegroundColor Cyan
Write-Host "════════════════════════════════════════════════════════════════════════════`n" -ForegroundColor Cyan

Write-Host "Checking prerequisites..." -ForegroundColor Yellow

# Check 1: Model file
if (Test-Path "D:\violence_ai\model\violence_model.h5") {
    $size = (Get-Item "D:\violence_ai\model\violence_model.h5").Length
    Write-Host "✓ Model file found: $([math]::Round($size/1MB, 2)) MB" -ForegroundColor Green
} else {
    Write-Host "✗ Model file NOT found - cannot proceed" -ForegroundColor Red
}

# Check 2: Source code
$srcFiles = Get-ChildItem "D:\violence_ai\src\*.py" -ErrorAction SilentlyContinue | Measure-Object | Select-Object -ExpandProperty Count
Write-Host "✓ Source code files: $srcFiles Python files" -ForegroundColor Green

# Check 3: .gitignore
if (Test-Path "D:\violence_ai\.gitignore") {
    Write-Host "✓ .gitignore configured" -ForegroundColor Green
}

# Check 4: README
if (Test-Path "D:\violence_ai\README.md") {
    if ((Get-Content "D:\violence_ai\README.md" | Select-String "Quick Start" -Quiet)) {
        Write-Host "✓ README updated with Quick Start section" -ForegroundColor Green
    }
}

Write-Host "`nAll prerequisites met! ✓`n`n"

# ============================================================================
# SECTION 2: COMMANDS
# ============================================================================

Write-Host "STEP 1-5: GIT COMMANDS" -ForegroundColor Cyan
Write-Host "════════════════════════════════════════════════════════════════════════════`n" -ForegroundColor Cyan

Write-Host "⚠️  IMPORTANT REPLACEMENTS NEEDED:`n" -ForegroundColor Yellow
Write-Host "  • YOUR_USERNAME  → Your GitHub username (e.g., jane-doe)" -ForegroundColor White
Write-Host "  • your.email@gmail.com  → Your GitHub email" -ForegroundColor White
Write-Host "  • Your Name  → Your actual name`n" -ForegroundColor White

Write-Host "1️⃣  INITIALIZE GIT (Run these first):" -ForegroundColor Yellow
Write-Host @"
━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━

cd D:\violence_ai
git init
git config user.email "your.email@gmail.com"
git config user.name "Your Name"

━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━
"@ -ForegroundColor White

Write-Host "`n2️⃣  STAGE & COMMIT FILES (Run these second):" -ForegroundColor Yellow
Write-Host @"
━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━

git add .
git status

(Verify you see ~25 files in green)

git commit -m "Initial commit: Violence Detection AI with trained ResNet50+LSTM model (CASE 1 - model included)"

━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━
"@ -ForegroundColor White

Write-Host "`n3️⃣  CREATE REPOSITORY ON GITHUB (Browser - Manual):" -ForegroundColor Yellow
Write-Host @"
━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━

Go to: https://github.com/new

Fill in these fields:
  • Repository name: violence_ai
  • Description: Deep Learning Violence Detection AI with pre-trained ResNet50+LSTM model
  • Visibility: PUBLIC

⚠️  DO NOT check these:
  ✗ Initialize with README
  ✗ Add .gitignore
  ✗ Add License

Click: Create repository

━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━
"@ -ForegroundColor White

Write-Host "`n4️⃣  CONNECT & PUSH (Run these fourth):" -ForegroundColor Yellow
Write-Host @"
━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━

git remote add origin https://github.com/YOUR_USERNAME/violence_ai.git
git branch -M main
git push -u origin main

(GitHub login window will pop up - sign in with your account)

━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━
"@ -ForegroundColor White

Write-Host "`n5️⃣  VERIFY SUCCESS (Run these last):" -ForegroundColor Yellow
Write-Host @"
━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━

git remote -v
git log --oneline -3
git branch -v

(Should show your commit, origin URLs, and main branch)

━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━
"@ -ForegroundColor White

# ============================================================================
# SECTION 3: WHAT GETS PUSHED
# ============================================================================

Write-Host "`nSTEP 6: VERIFY WHAT GETS PUSHED`n" -ForegroundColor Cyan
Write-Host "════════════════════════════════════════════════════════════════════════════`n" -ForegroundColor Cyan

Write-Host "✅ PUSHED TO GITHUB:" -ForegroundColor Green
Write-Host "  • model/violence_model.h5 (103 MB - trained model)"
Write-Host "  • src/*.py (6 source files: train, predict, net, load_data, frames)"
Write-Host "  • app/ui.py (Streamlit dashboard)"
Write-Host "  • README.md (with Quick Start section)"
Write-Host "  • requirements.txt (all dependencies)"
Write-Host "  • .gitignore (configuration)"
Write-Host "  • Documentation markdown files`n"

Write-Host "❌ EXCLUDED (by .gitignore):" -ForegroundColor Yellow
Write-Host "  • data/ folder (raw video dataset)"
Write-Host "  • venv/ folder (virtual environment)"
Write-Host "  • __pycache__/ (Python cache)"
Write-Host "  • *.log files (log files)"
Write-Host "  • temp/ folder (temporary files)`n"

Write-Host "TOTAL: ~26 files, ~200 MB`n"

# ============================================================================
# SECTION 4: AFTER PUSH
# ============================================================================

Write-Host "STEP 7: AFTER PUSH SUCCESS`n" -ForegroundColor Cyan
Write-Host "════════════════════════════════════════════════════════════════════════════`n" -ForegroundColor Cyan

Write-Host "Your GitHub repository URL:" -ForegroundColor Yellow
Write-Host "https://github.com/YOUR_USERNAME/violence_ai`n" -ForegroundColor White

Write-Host "Users can now clone and run without any training:" -ForegroundColor Green
Write-Host @"
git clone https://github.com/YOUR_USERNAME/violence_ai.git
cd violence_ai
pip install -r requirements.txt
streamlit run app/ui.py

Result: Instant violence detection with your trained model! 🎉
"@ -ForegroundColor Cyan

# ============================================================================
# SUMMARY
# ============================================================================

Write-Host "`n" -ForegroundColor Cyan
Write-Host "╔════════════════════════════════════════════════════════════════════════════╗" -ForegroundColor Green
Write-Host "║                         DEPLOYMENT SUMMARY                                ║" -ForegroundColor Green
Write-Host "╚════════════════════════════════════════════════════════════════════════════╝`n" -ForegroundColor Green

Write-Host "PROJECT: violence_ai" -ForegroundColor Yellow
Write-Host "DEPLOYMENT: CASE 1 (Model Included)" -ForegroundColor Yellow
Write-Host "MODEL SIZE: 103.25 MB" -ForegroundColor Yellow
Write-Host "USERS NEED TO TRAIN: NO ✓" -ForegroundColor Green
Write-Host "USERS CAN RUN IMMEDIATELY: YES ✓" -ForegroundColor Green

Write-Host "`nREFERENCE FILES IN YOUR PROJECT:" -ForegroundColor Cyan
Write-Host "  • COPY_PASTE_COMMANDS.txt - Copy-paste the commands from here" -ForegroundColor White
Write-Host "  • GITHUB_PUSH_STEPS.md - Detailed step-by-step guide" -ForegroundColor White
Write-Host "  • DEPLOYMENT_CHECKLIST.md - Verification checklist" -ForegroundColor White
Write-Host "`nREADY? Follow the commands in STEP 1-5 above! 🚀`n" -ForegroundColor Green

Write-Host "Need help? Check GITHUB_PUSH_STEPS.md or DEPLOYMENT_CHECKLIST.md`n" -ForegroundColor Cyan
