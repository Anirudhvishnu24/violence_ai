# README Quick Start Section - Copy This

Copy this section into your README.md to help users get started quickly:

---

## Quick Start (No Training Needed)

The trained model is included in this repository, so you can start detecting violence in videos immediately without retraining.

### Installation (5 minutes)

1. **Clone the repository:**
   ```bash
   git clone https://github.com/YOUR_USERNAME/violence_ai.git
   cd violence_ai
   ```

2. **Create and activate virtual environment:**
   ```bash
   python -m venv venv
   venv\Scripts\activate  # On Windows
   # OR
   source venv/bin/activate  # On macOS/Linux
   ```

3. **Install dependencies:**
   ```bash
   pip install -r requirements.txt
   ```

### Run the Application

```bash
streamlit run app/ui.py
```

The app opens at **http://localhost:8501**

### How to Use

1. **Upload a video** (mp4, avi, mov, mkv, flv)
2. **Wait for analysis** (<5 seconds typical)
3. **View results:**
   - Prediction: VIOLENT or NONVIOLENT
   - Violence Probability: 0-100%
   - Risk Level: SAFE / MEDIUM / HIGH RISK
   - Detailed analysis with insights

### Example Output

**VIOLENT Content:**
```
Prediction: ⚠️ VIOLENT
Violence Probability: 87.3%
Risk Level: 🔴 HIGH RISK
⚠️ TRIGGER WARNING — Violent content detected. Viewer discretion advised.
```

**NONVIOLENT Content:**
```
Prediction: ✅ NONVIOLENT
Violence Probability: 12.5%
Risk Level: 🟢 SAFE
✅ CONTENT SAFE — No violent content detected. Safe to view.
```

### Requirements

- Python 3.11+
- ~2 GB RAM (minimum)
- GPU (optional, for faster processing)

### Model Information

- **Architecture:** ResNet50 (CNN) + LSTM(128)
- **Input:** 30 frames × 224×224 pixels
- **Output:** Binary classification (0-1)
- **Decision Threshold:** 0.50
- **Validation Accuracy:** ~86%
- **Processing Speed:** <5 seconds per video
- **Model Size:** 103 MB

---

## Advanced: Retraining (Optional)

If you want to train with your own dataset:

### Prepare Your Data

```
data/
├── violent/          # Videos with violence (mp4, avi, mov, etc.)
└── nonviolent/       # Videos without violence
```

Aim for ~500 videos per class for best results.

### Run Training

```bash
python -m src.train
```

The script will:
1. Extract frames from all videos
2. Train ResNet50+LSTM model
3. Save trained model to `model/violence_model.h5`
4. Show validation metrics

**Training time:** ~2-4 hours (depending on GPU)

### Training Script Features

- Stratified train/validation split (80/20)
- Data streaming (no RAM pre-loading)
- Batch size: 8
- Epochs: 10
- Optimizer: Adam
- Loss: Binary Crossentropy

---

## Troubleshooting

| Issue | Solution |
|-------|----------|
| "ModuleNotFoundError: No module named 'tensorflow'" | Run `pip install -r requirements.txt` |
| "CUDA out of memory" | Reduce batch size in training or use CPU |
| "Video not analyzing" | Ensure video has ≥30 frames |
| "Port 8501 already in use" | Run `streamlit run app/ui.py --server.port 8502` |

---

## Project Structure

```
violence_ai/
├── app/
│   └── ui.py                 # Streamlit dashboard
├── model/
│   └── violence_model.h5     # Trained model (103 MB)
├── src/
│   ├── frames.py             # Frame extraction
│   ├── load_data.py          # Data pipeline
│   ├── net.py                # Model architecture
│   ├── predict.py            # Inference
│   └── train.py              # Training script
├── data/                     # [Not included] Place training videos here
├── requirements.txt          # Dependencies
└── README.md                 # This file
```

---

## Key Files Explained

| File | Purpose |
|------|---------|
| `app/ui.py` | Premium Streamlit dashboard with real-time analysis |
| `model/violence_model.h5` | Trained ResNet50+LSTM model (ready to use) |
| `src/train.py` | Training pipeline with stratified split |
| `src/predict.py` | Inference pipeline for video prediction |
| `src/load_data.py` | Dataset generator with stratified sampling |
| `requirements.txt` | All Python dependencies |

---

## Citation / Attribution

If you use this project in research or production, please attribute to:

```bibtex
@software{violence_detection_ai_2026,
  title={Violence Detection AI: Deep Learning Video Analysis},
  author={Your Name},
  year={2026},
  url={https://github.com/YOUR_USERNAME/violence_ai}
}
```

---

## License

[Add your license here - MIT recommended]

---

## Support

For issues, questions, or contributions:
- Open an issue on GitHub
- Check existing issues first
- Provide video example if reporting bug

---

## Performance Notes

- **CPU:** ~30-60 seconds per video
- **GPU (CUDA):** <5 seconds per video
- **Memory:** 1-2 GB typical
- **Accuracy:** ~86% validation accuracy
- **False positives:** ~10% (non-violent → violent)
- **False negatives:** ~4% (violent → non-violent)

---

## Roadmap

- [ ] Web API deployment (Flask/FastAPI)
- [ ] Batch processing support
- [ ] Fine-tuning interface
- [ ] Multi-label classification (type of violence)
- [ ] Hardware acceleration (TensorRT, ONNX)

---

## Acknowledgments

- Dataset: Hockey Fight Videos (Kaggle)
- Framework: TensorFlow/Keras, Streamlit
- Pre-trained backbone: ImageNet ResNet50

---

**Ready to detect violence?** Start above with Quick Start! 🎬🚀

