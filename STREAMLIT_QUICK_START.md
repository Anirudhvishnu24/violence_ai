# Streamlit UI - Quick Start Guide

## Running the App

```bash
# From project root (d:\violence_ai)
streamlit run app/ui.py
```

Your browser will open to: **http://localhost:8501**

## UI Sections Overview

### 1. Hero Header
- Title: "🎬 Violence Detection AI"
- Subtitle: "Advanced video content analysis powered by deep learning"
- Technology badges showing key architecture components

### 2. Left Column - Upload & Preview
```
1. Click "Choose a video file"
2. Select a video (mp4, avi, mov, mkv, flv)
3. Video preview appears below
```

### 3. Right Column - Live Results
```
Shows after upload and analysis:
- 3 Metric Cards: Prediction | Confidence | Risk Level
- Confidence Progress Bar with percentage
- Content Warning or Safe Banner
```

### 4. Processing Flow
```
1. Extracting frames... (25%)
2. Analyzing with AI model... (75%)
3. Analysis complete! (100%)

Results auto-display with animations
```

### 5. Sidebar Information
Click to expand any section:
- **About This App** - General information
- **Model Architecture** - Technical details
- **How It Works** - Processing pipeline
- **Dataset** - Training data statistics

### 6. Detailed Analysis Tabs
After analysis, scroll down to see:
- **How It Works** - Step-by-step processing
- **Decision Logic** - Threshold and classification
- **Model Insights** - Architecture and performance

## Understanding Results

### Prediction
- **VIOLENT**: Content contains violent material (confidence > 0.50)
- **NONVIOLENT**: Content is safe (confidence ≤ 0.50)

### Confidence
- 50-60%: Borderline (low confidence)
- 60-75%: Moderate confidence
- 75-100%: High confidence

### Risk Level
- 🔴 HIGH RISK: Violent content detected
- 🟢 SAFE: No violent content

### Confidence Bar
- Red fill: Violent content
- Blue-green fill: Non-violent content
- Width represents confidence percentage

## Visual Design Features

✨ **Premium Dark Theme**
- Deep navy backgrounds
- Indigo accent colors
- Smooth gradients
- Subtle shadows

🎨 **Modern Components**
- Rounded cards
- Hover effects (lift animation)
- Animated progress bar
- Gradient text
- Responsive layout

🎯 **Professional Layout**
- Hero header section
- Two-column design
- Clean spacing
- Organized sections
- Collapsible menus

⚡ **Interactive Elements**
- Smooth animations
- Real-time progress
- Auto-clearing spinners
- Color-coded warnings
- Expandable sections

## Tips & Best Practices

1. **Video Format**
   - Supports: MP4, AVI, MOV, MKV, FLV
   - Minimum length: 30 frames
   - Works with any resolution

2. **Best Results**
   - Clear video quality
   - Stable frame rate
   - Representative content

3. **Sidebar Navigation**
   - Read "About This App" first time
   - Use "How It Works" to understand process
   - Check "Model Insights" for performance details

4. **Error Handling**
   - Corrupt videos show error message
   - Too-short videos rejected
   - Model missing shows setup instructions

## Display Sections

### Top Section (Hero)
```
┌─────────────────────────────────────┐
│  🎬 Violence Detection AI           │
│  Advanced video analysis...         │
│  [Badge] [Badge] [Badge] [Badge]   │
└─────────────────────────────────────┘
```

### Main Section (Two Columns)
```
┌──────────────────┬──────────────────┐
│  📤 Upload       │  📊 Results      │
│  Video Preview   │  Metric Cards    │
│                  │  Progress Bar    │
│                  │  Warning Banner  │
└──────────────────┴──────────────────┘
```

### Bottom Section (Tabs)
```
┌─────────────────────────────────────┐
│  🔬 Detailed Analysis               │
│  [How It Works] [Logic] [Insights] │
│                                     │
│  Content here changes per tab      │
└─────────────────────────────────────┘
```

### Sidebar (Always Available)
```
┌─────────────────┐
│ ℹ️ About       │ (expandable)
│ 🧠 Model       │ (expandable)
│ 🔬 How It Works│ (expandable)
│ 📊 Dataset     │ (expandable)
└─────────────────┘
```

## Keyboard Shortcuts

- **Ctrl+S** - Rerun app (Streamlit)
- **r** - Rerun (in app)
- **C** - Clear cache
- **P** - Print page

## Troubleshooting

| Issue | Solution |
|-------|----------|
| Model not found | Run `python -m src.train` first |
| Video won't upload | Check format (mp4, avi, mov, mkv, flv) |
| Analysis errors | Ensure video has ≥30 frames |
| Slow processing | Normal for CPU inference (~5s) |
| CSS looks wrong | Clear browser cache (Ctrl+Shift+R) |
| Sidebar collapsed | Click sidebar toggle button |

## Performance

- **Upload**: Instant
- **Frame extraction**: ~1-2 seconds
- **Model inference**: ~2-4 seconds
- **Total**: ~3-6 seconds per video

## Mobile Access

The app is responsive and works on mobile:
- Tablets: Full two-column layout
- Phones: Single column (stacked)
- Touch-friendly buttons and upload area

## System Requirements

- Python 3.9+
- TensorFlow 2.13+
- Streamlit 1.31+
- Modern web browser
- 2GB RAM minimum
- 500MB disk space

## Advanced Usage

### Change Colors
Edit `app/ui.py`, find `inject_custom_css()`:
```python
--primary-color: #6366f1;  # Change this hex
```

### Adjust Layout
Find column definitions:
```python
col_left, col_right = st.columns([1, 1.2])  # Change ratios
```

### Modify Content
Edit sidebar content in `render_sidebar_info()`
Edit tab content in bottom `with st.tabs()` section

## Support

For issues or questions:
1. Check the sidebar "About" section
2. Review "How It Works" tab
3. Check model is trained and saved
4. Verify video format is supported

## Credits

- **Model**: ResNet50 + LSTM
- **Framework**: TensorFlow/Keras
- **UI**: Streamlit
- **Design**: Modern Premium Dashboard Pattern
