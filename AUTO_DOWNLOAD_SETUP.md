# AUTO-DOWNLOAD SETUP GUIDE

## Overview
Your violence_ai project now uses **auto-download from Google Drive** for the trained model. This solves the GitHub 100MB file size limit while maintaining "Case 1" deployment (users run without retraining).

## How It Works
```
User runs: streamlit run app/ui.py
    ↓
App loads and calls: ensure_model_exists()
    ↓
Check: Does model/violence_model.h5 exist locally?
    ↓
NO? → Download from Google Drive using gdown (~2-3 min)
YES? → Continue immediately (no download needed)
    ↓
App runs with model
```

## Setup Steps

### Step 1: Upload Model to Google Drive

1. Go to: https://drive.google.com
2. Create a new folder (optional): `violence_ai_models`
3. Upload your `model/violence_model.h5` file to Google Drive
4. Right-click file → "Share"
5. Set to: "Anyone with the link can view"
6. Copy the sharing link

### Step 2: Extract Google Drive File ID

From the sharing link:
```
https://drive.google.com/file/d/[FILE_ID_HERE]/view?usp=sharing
                                  ↑↑↑↑↑↑↑↑↑↑↑↑↑↑↑↑↑↑↑↑
```

Copy this ID (looks like: `1a2b3c4d5e6f7g8h9i0j1k2l3m4n5o6p`)

### Step 3: Update Configuration

Edit: `src/model_download.py`

Find this line:
```python
GDRIVE_FILE_ID = "REPLACE_WITH_FILE_ID"
```

Replace with:
```python
GDRIVE_FILE_ID = "1a2b3c4d5e6f7g8h9i0j1k2l3m4n5o6p"  # Your actual ID
```

### Step 4: Test the Download

```powershell
cd D:\violence_ai
python -m src.model_download
```

Expected output:
```
======================================================================
DOWNLOADING TRAINED MODEL FROM GOOGLE DRIVE
======================================================================

📥 Downloading model from Google Drive...
   Destination: model/violence_model.h5
   File ID: 1a2b3c4d5e6f7g8h9i0j1k2l3m4n5o6p

[....................] 100%

✓ Model downloaded successfully!
  Size: 103.25 MB
======================================================================
```

### Step 5: Commit and Push to GitHub

```powershell
cd D:\violence_ai

git add .

git commit -m "Add auto-download model from Google Drive (CASE 1 deployment)"

git push -u origin main
```

Files changed:
- `src/model_download.py` (new file with auto-download logic)
- `app/ui.py` (calls ensure_model_exists)
- `src/predict.py` (calls ensure_model_exists)
- `requirements.txt` (adds gdown dependency)
- `.gitignore` (excludes model/violence_model.h5)
- `README.md` (auto-download instructions)

## Usage

### Streamlit Web App
```bash
streamlit run app/ui.py
```
- First run: Downloads model (~2-3 minutes)
- Subsequent runs: Uses downloaded model (fast)

### Command-Line Prediction
```bash
python -m src.predict --video "path/to/video.mp4"
```
- Auto-downloads model if missing
- Returns: Label and confidence score

### Manual Check
```bash
python -m src.model_download
```
- Tests the download function
- Downloads if missing, verifies if exists

## File Structure

```
violence_ai/
├── src/
│   ├── model_download.py      ← NEW: Auto-download logic
│   ├── predict.py              ← UPDATED: Calls ensure_model_exists()
│   ├── frames.py
│   ├── load_data.py
│   ├── net.py
│   └── train.py
├── app/
│   └── ui.py                   ← UPDATED: Calls ensure_model_exists()
├── model/                      ← Created at runtime
│   └── violence_model.h5       ← Auto-downloaded on first run
├── data/                       ← For training only (excluded)
├── outputs/
├── .gitignore                  ← UPDATED: Excludes model/violence_model.h5
├── requirements.txt            ← UPDATED: Added gdown
├── README.md                   ← UPDATED: Auto-download instructions
└── ...
```

## Troubleshooting

### "gdown not found"
```bash
pip install gdown
```

### "File ID not configured"
Error message will show exactly what to do:
1. Upload model to Google Drive
2. Get the File ID
3. Update `src/model_download.py`

### "Download failed - connection error"
- Check internet connection
- Check Google Drive link is still shareable
- Try again (temporary network issue)

### "Download is slow"
- Normal for 103 MB file (2-3 minutes on typical connection)
- Model caches locally after first download
- Only happens once

### Model file exists but app won't start
- Delete `model/violence_model.h5`
- Run again to re-download fresh copy
- Or manually verify file integrity

## Security & Privacy

✓ Safe: Google Drive link is public read-only
✓ Automatic: No manual downloads needed
✓ Cached: Downloads only once, reuses locally
✓ Verified: File integrity checked on download
✓ Open Source: All code is transparent in `src/model_download.py`

## What Users See

**First run (with download):**
```
Uploading LFS objects: 100% (1/1), 108 MB | 1.6 MB/s, done.
Enumerating objects: 49, done.
...
======================================================================
DOWNLOADING TRAINED MODEL FROM GOOGLE DRIVE
======================================================================

📥 Downloading model from Google Drive...
   Destination: model/violence_model.h5
   File ID: 1a2b3c4d5e6f...

Downloading, please wait...

✓ Model downloaded successfully!
  Size: 103.25 MB
======================================================================

Streamlit app runs...
```

**Second run (no download):**
```
✓ Model found at: model/violence_model.h5

Streamlit app runs immediately...
```

## GitHub Repository Status

- ✅ All code on GitHub
- ✅ Model NOT on GitHub (too large)
- ✅ Auto-download from Google Drive on demand
- ✅ Users get "Case 1" experience (run without training)
- ✅ No retraining needed
- ✅ Works offline after first download

## Next Steps

1. Update Google Drive File ID in `src/model_download.py`
2. Test with: `python -m src.model_download`
3. Commit: `git add .` → `git commit -m "..."` → `git push`
4. Users can now clone and run immediately!

---

**Your project is now deployment-ready!** 🚀
