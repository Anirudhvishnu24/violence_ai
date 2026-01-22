# QUICK REFERENCE - AUTO-DOWNLOAD SETUP

## TL;DR

```powershell
# 1. Upload model to Google Drive
#    (Store model/violence_model.h5)

# 2. Get File ID from sharing link
#    https://drive.google.com/file/d/[FILE_ID_HERE]/view

# 3. Update src/model_download.py
#    GDRIVE_FILE_ID = "paste_your_file_id_here"

# 4. Test
python -m src.model_download

# 5. Commit and push
git add .
git commit -m "Add auto-download from Google Drive"
git push origin main
```

---

## Files Changed

| File | Change | Why |
|------|--------|-----|
| `src/model_download.py` | **NEW** | Core auto-download logic |
| `app/ui.py` | Updated | Calls `ensure_model_exists()` |
| `src/predict.py` | Updated | Calls `ensure_model_exists()` |
| `requirements.txt` | Updated | Added `gdown>=4.7.0` |
| `.gitignore` | Updated | Excludes `model/violence_model.h5` |
| `README.md` | Updated | Auto-download instructions |

---

## How Users Run It

```bash
# First time: Downloads model from Google Drive
streamlit run app/ui.py
# ⏳ "Downloading model..." (takes 2-3 min)
# ✓ Done! App runs

# Second time: Uses cached model
streamlit run app/ui.py
# ✓ Instant! (no download)
```

---

## Testing

```bash
# Test the download function
python -m src.model_download

# Expected output on first run:
# ======================================================================
# DOWNLOADING TRAINED MODEL FROM GOOGLE DRIVE
# ======================================================================
# 📥 Downloading model from Google Drive...
# [████████████████████] 100%
# ✓ Model downloaded successfully!
#   Size: 103.25 MB

# Expected output on second run:
# ✓ Model found at: model/violence_model.h5
```

---

## Configuration

**File:** `src/model_download.py`

**Line to change:**
```python
GDRIVE_FILE_ID = "REPLACE_WITH_FILE_ID"
```

**To:**
```python
GDRIVE_FILE_ID = "1a2b3c4d5e6f7g8h9i0j1k2l3m4n5o6p"
```

Where `1a2b3c4d5e6f7g8h9i0j1k2l3m4n5o6p` is your Google Drive File ID

---

## Feature Breakdown

| Feature | What It Does |
|---------|-------------|
| **Auto-detect** | Checks if model exists locally |
| **Auto-download** | Downloads from Google Drive if missing |
| **Progress** | Shows download percentage |
| **Cache** | Stores locally after download |
| **Error handling** | Clear messages if download fails |
| **Manual option** | Users can place file manually if needed |

---

## GitHub Push Command

```powershell
cd D:\violence_ai
git add .
git commit -m "Implement auto-download from Google Drive for CASE 1 deployment"
git push origin main
```

---

## Status Check

```powershell
# Verify files are in place
git status

# Should show these as modified/new:
# modified:   .gitignore
# modified:   README.md
# modified:   app/ui.py
# modified:   requirements.txt
# modified:   src/predict.py
# new file:   src/model_download.py
```

---

## Result

✅ **GitHub:** All code pushed (without huge model file)
✅ **Users:** Clone repo and run immediately
✅ **Download:** Automatic on first run (~2-3 min)
✅ **Cache:** Instant on subsequent runs
✅ **CASE 1:** No retraining needed!

---

## See Also

- **Full guide:** `AUTO_DOWNLOAD_SETUP.md`
- **Code:** `src/model_download.py`
- **README:** Check updated Quick Start section
- **CLI:** `python -m src.predict --video "path.mp4"`
