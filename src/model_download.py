"""
Auto-download trained model from Google Drive if not present locally.

The model file is hosted on Google Drive because it exceeds GitHub's 100MB per-file limit.
This module handles automatic download with user-friendly error messages.

Usage:
    from src.model_download import ensure_model_exists
    ensure_model_exists()  # Download if missing, do nothing if present
"""

import os
import sys
from pathlib import Path

# Model configuration
MODEL_PATH = os.path.join("model", "violence_model.h5")
GDRIVE_FILE_ID = "10rBn5SKjwuzrc3lxUeq4M1G-6-h1LL6S"  # Violence model trained ResNet50+LSTM

# Google Drive download URL template
GDRIVE_DOWNLOAD_URL = f"https://drive.google.com/uc?id={GDRIVE_FILE_ID}&export=download"


def ensure_model_exists(model_path: str = MODEL_PATH, file_id: str = GDRIVE_FILE_ID) -> None:
    """
    Ensure the trained model exists. Download from Google Drive if missing.
    
    Args:
        model_path: Path where the model should be located (default: model/violence_model.h5)
        file_id: Google Drive file ID for the model (user must set this)
    
    Raises:
        RuntimeError: If model is missing and download fails
    
    Returns:
        None (silent success if model exists or download succeeds)
    """
    
    # Check if model already exists
    if os.path.isfile(model_path):
        print(f"✓ Model found at: {model_path}")
        return
    
    print("\n" + "="*70)
    print("DOWNLOADING TRAINED MODEL FROM GOOGLE DRIVE")
    print("="*70)
    
    # Create model directory if it doesn't exist
    model_dir = os.path.dirname(model_path)
    if not os.path.isdir(model_dir):
        print(f"Creating directory: {model_dir}")
        os.makedirs(model_dir, exist_ok=True)
    
    # Check if gdown is available
    try:
        import gdown
    except ImportError:
        raise RuntimeError(
            "\n❌ ERROR: gdown is not installed.\n"
            "Install it with:\n"
            "    pip install gdown\n"
            "Then try again."
        )
    
    # Check if file_id is set
    if file_id == "REPLACE_WITH_FILE_ID":
        raise RuntimeError(
            "\n❌ ERROR: Google Drive file ID not configured.\n"
            "\nTo set up the model:\n"
            "1. Upload model/violence_model.h5 to your Google Drive\n"
            "2. Get the file ID from the sharing link\n"
            "3. Update GDRIVE_FILE_ID in src/model_download.py\n"
            "4. Update the file ID in app/ui.py and src/predict.py (if used)\n\n"
            "Example:\n"
            "    GDRIVE_FILE_ID = '1abc123def456ghi789jkl'\n"
        )
    
    # Build download URL
    download_url = f"https://drive.google.com/uc?id={file_id}&export=download"
    
    print(f"\n📥 Downloading model from Google Drive...")
    print(f"   Destination: {model_path}")
    print(f"   File ID: {file_id}")
    
    try:
        gdown.download(download_url, model_path, quiet=False)
        
        # Verify download
        if os.path.isfile(model_path):
            file_size_mb = os.path.getsize(model_path) / (1024 * 1024)
            print(f"\n✓ Model downloaded successfully!")
            print(f"  Size: {file_size_mb:.2f} MB")
            print("="*70 + "\n")
            return
        else:
            raise RuntimeError("Download completed but file not found.")
    
    except Exception as e:
        raise RuntimeError(
            f"\n❌ ERROR: Failed to download model from Google Drive.\n"
            f"Error: {str(e)}\n\n"
            f"MANUAL OPTION:\n"
            f"1. Download model from: https://drive.google.com/file/d/{file_id}\n"
            f"2. Place file at: {os.path.abspath(model_path)}\n"
            f"3. Run the app again\n\n"
            f"For help, see README.md\n"
        )


def get_model_path() -> str:
    """Get the absolute path to the model file."""
    return os.path.abspath(MODEL_PATH)


if __name__ == "__main__":
    # Test the download function
    print("Testing model auto-download...")
    ensure_model_exists()
    print("Test complete!")
