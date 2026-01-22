# Violence Detection System v2

## ⚡ Quick Start (5 minutes - No Training Needed!)

**The trained model is included!** You can run immediately without any training.

### Step 1: Clone Repository
```bash
git clone https://github.com/YOUR_USERNAME/violence_ai.git
cd violence_ai
```

### Step 2: Install Dependencies
```bash
pip install -r requirements.txt
```

### Step 3: Run the App
```bash
streamlit run app/ui.py
```

Open **http://localhost:8501** in your browser. Upload a video and get instant predictions! 

**What you get:**
- ✅ NONVIOLENT / ⚠️ VIOLENT classification
- Confidence score (0-100%)
- Risk level indicator (🟢 SAFE / 🟡 MEDIUM / 🔴 HIGH RISK)
- Real-time video preview
- Detailed analysis

---

## Problem Statement

This project detects violent content in video files using deep learning. Violence detection has critical applications in:
- Content moderation platforms
- News/broadcast filtering
- Security monitoring systems
- Streaming service content rating

## Dataset Structure

```
data/
├── nonviolent/    (Label 0 - safe content videos)
└── violent/       (Label 1 - violent content videos)
```

Place your training videos in the appropriate directories before training.

## Model Architecture

**ResNet50 + LSTM (Temporal CNN-RNN Hybrid)**

- **Spatial Feature Extraction:** TimeDistributed ResNet50 (pretrained on ImageNet)
  - Processes each frame independently
  - Extracts 2048-dim feature vectors per frame
  - Output: (batch, 30, 2048)

- **Temporal Modeling:** LSTM Layer
  - Captures temporal patterns across 30 frames
  - Learns dependencies between frames
  - Output: (batch, 128)

- **Classification:** Dense Layers
  - Dense(64, relu) + Dropout(0.5)
  - Dense(32, relu) + Dropout(0.3)
  - Dense(1, sigmoid) → Binary classification [0, 1]

**Total Parameters:** ~25M (mostly pretrained ResNet50)

## Setup

### 1. Install Dependencies

```bash
pip install -r requirements.txt
```

### 2. Verify Installation (Smoke Test)

Verify everything is installed correctly:

```bash
python -c "from src.net import build_model; m = build_model(); print('✓ Installation OK')"
```

Expected output: `✓ Installation OK`

### 3. Prepare Dataset

```bash
# Add videos to data directories
mkdir -p data/nonviolent
mkdir -p data/violent

# Copy your training videos
# - Safe content videos → data/nonviolent/
# - Violent content videos → data/violent/
```

### 4. Create Output Directories

```bash
mkdir -p model
mkdir -p outputs
```

## How to Train

Train the model on your dataset using memory-efficient streaming (no full dataset loaded into RAM):

```bash
python -m src.train
```

**What happens:**
1. Scans videos from `data/nonviolent/` and `data/violent/`
2. Streams data from disk using `tf.data.Dataset` generators
3. Extracts 30 frames per video on-the-fly
4. Automatically splits: 80% train, 20% validation
5. Trains ResNet50 + LSTM for 10 epochs with batch_size=8
6. Saves model to `model/violence_model.h5`
7. Generates metrics:
   - `outputs/confusion_matrix.png` - Validation confusion matrix
   - `outputs/training_curves.png` - Accuracy and loss curves
8. Prints classification report (precision, recall, F1-score)

**Memory Efficiency:**
- Uses `tf.data.Dataset.from_generator()` to stream videos one at a time
- Does NOT load entire dataset into RAM
- Each video extracted on-demand during training
- Suitable for large datasets (1000+ videos)
- Automatically prefetches next batches for performance

**Typical Training Time:** 
- 30-60 minutes on GPU (depending on dataset size)
- CPU fallback supported but slower

## How to Predict

### Command-Line Interface (CLI)

```bash
python -m src.predict --video "path/to/video.mp4"
```

**Output:**
```
============================================================
PREDICTION RESULT
============================================================
Label: VIOLENT (or NONVIOLENT)
Confidence: 0.9523
============================================================
```

### Python API

```python
from src.predict import predict_video

label, confidence = predict_video("video.mp4")
print(f"{label}: {confidence:.4f}")
```

## Run Streamlit Demo

Interactive web UI for batch predictions:

```bash
streamlit run app/ui.py
```

**Features:**
- Upload video files
- Real-time prediction with confidence score
- Trigger warning for violent content
- Detailed analysis metrics

## Project Structure

```
violence_ai/
├── app/
│   └── ui.py                    # Streamlit web interface
├── src/
│   ├── __init__.py
│   ├── frames.py                # Video frame extraction
│   ├── load_data.py             # Dataset loading
│   ├── net.py                   # Model architecture
│   ├── train.py                 # Training pipeline
│   └── predict.py               # Prediction CLI
├── data/
│   ├── nonviolent/              # Training: safe videos
│   └── violent/                 # Training: violent videos
├── model/
│   └── violence_model.h5        # Trained model (after training)
├── outputs/
│   ├── confusion_matrix.png     # Test metrics (after training)
│   └── training_curves.png      # Training history (after training)
├── requirements.txt             # Python dependencies
└── README.md                    # This file
```

## Key Features

✓ **Efficient Frame Sampling** - Uniformly samples 30 frames from any video length  
✓ **Error Handling** - Gracefully handles corrupt or short videos  
✓ **Pretrained Features** - Uses ImageNet-pretrained ResNet50 for fast convergence  
✓ **Temporal Modeling** - LSTM captures violence patterns across time  
✓ **Memory Efficient** - Streams data from disk via `tf.data.Dataset` generators  
✓ **Production Ready** - CLI, API, and web UI for different use cases  
✓ **Windows Compatible** - All file paths and imports work on Windows  

## Technical Implementation

### Memory-Efficient Streaming
The training pipeline uses TensorFlow's `tf.data.Dataset` with Python generators to stream video data from disk instead of loading the entire dataset into RAM:

```python
# Videos are loaded on-demand during training
train_dataset = tf.data.Dataset.from_generator(
    video_generator(...),
    output_signature=(frames_spec, label_spec)
)
train_dataset = train_dataset.batch(8).prefetch(tf.data.AUTOTUNE)
```

**Benefits:**
- Handles datasets of any size (RAM not a bottleneck)
- Each video extracted from disk just before training
- Automatic prefetching keeps GPU busy
- Validation split done efficiently without reloading

### Data Flow
1. `load_data.py` - Generator yields (frames, label) one video at a time
2. `tf.data.Dataset.from_generator()` - Creates lazy dataset
3. `.batch(8)` - Groups into batches
4. `.prefetch(AUTOTUNE)` - Pre-loads next batch while GPU trains
5. `model.fit(train_dataset, validation_data=val_dataset)`

## Configuration

Edit these parameters in source files:

- **frames.py:**
  - `num_frames=30` - Frames per video
  - `img_size=224` - Frame resolution

- **net.py:**
  - `LSTM(128)` - LSTM units
  - `learning_rate=0.001` - Training rate

- **train.py:**
  - `epochs=10` - Training epochs
  - `batch_size=8` - Batch size (adjust based on GPU memory)

## Metrics & Outputs

After training, check:

1. **Console Output**
   - Classification Report (Precision, Recall, F1)
   - Test Accuracy
   - Training time

2. **outputs/confusion_matrix.png**
   - True Positives / True Negatives
   - False Positives / False Negatives

3. **outputs/training_curves.png**
   - Training vs Validation Accuracy
   - Training vs Validation Loss

## Example Screenshots

_(Screenshots will appear after first training run)_

- `outputs/confusion_matrix.png` - Test set performance
- `outputs/training_curves.png` - Model convergence

## Performance Notes

- **Input:** Video files (any resolution)
- **Output:** Binary label (VIOLENT / NONVIOLENT) with confidence [0-1]
- **Latency:** ~2-5 seconds per video on CPU (frames extraction + inference)
- **Memory:** ~4GB for training with batch_size=8

## Troubleshooting

**Model not found:**
```bash
# Train model first
python -m src.train
```

**No videos loaded:**
- Check `data/nonviolent/` and `data/violent/` directories exist
- Ensure video files are readable (mp4, avi, mov formats supported)

**Frame extraction fails:**
- Video may be corrupt - try converting to mp4
- Video may have < 30 frames - resample
- Use OpenCV: `ffmpeg -i input.avi -vf scale=1280:720 output.mp4`

**Out of memory:**
- Reduce `batch_size` in train.py
- Use fewer videos for training

## Windows / PowerShell Notes

### Running from Project Root

All commands support Windows PowerShell and should be run from the project root:

```powershell
# Verify installation
python -c "from src.net import build_model; print('OK')"

# Train model
python -m src.train

# Predict on video
python -m src.predict --video "path\to\video.mp4"

# Run Streamlit UI
streamlit run app/ui.py
```

### Virtual Environment

Create and activate a virtual environment:

```powershell
# Create
python -m venv venv

# Activate (PowerShell)
.\venv\Scripts\Activate.ps1

# Or for cmd
venv\Scripts\activate.bat
```

### Path Handling

- All paths use forward slashes or `os.path.join()` for cross-platform compatibility
- Windows backslashes in CLI should use quotes: `"data\violent\video.mp4"`

## Citation & References

- ResNet: He et al., "Deep Residual Learning for Image Recognition" (2015)
- LSTM: Hochreiter & Schmidhuber, "Long Short-Term Memory" (1997)
- Dataset structure inspired by action recognition conventions

## License

MIT License

---

**Last Updated:** January 2026  
**Version:** 2.0 (ResNet50 + LSTM)
