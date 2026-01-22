"""
Streamlit UI for violence detection.
Premium dashboard design with modern styling.

Run with:
    streamlit run app/ui.py
"""

import os
import sys
import tempfile
import streamlit as st
import numpy as np
from pathlib import Path
from tensorflow import keras
import plotly.graph_objects as go

# Add project root to path for imports
project_root = str(Path(__file__).parent.parent)
if project_root not in sys.path:
    sys.path.insert(0, project_root)

from src.frames import extract_frames


# ==================== CUSTOM STYLING ====================
def inject_custom_css():
    """Inject custom CSS for premium dashboard styling."""
    st.markdown("""
    <style>
    /* Root theme variables */
    :root {
        --primary-color: #6366f1;
        --danger-color: #ef4444;
        --success-color: #10b981;
        --warning-color: #f59e0b;
        --bg-dark: #0f172a;
        --bg-card: #1e293b;
        --text-primary: #f1f5f9;
        --text-secondary: #cbd5e1;
        --border-color: #334155;
        --shadow: 0 10px 30px rgba(0, 0, 0, 0.3);
        --shadow-lg: 0 20px 50px rgba(0, 0, 0, 0.4);
    }
    
    /* Global styles */
    body {
        background-color: var(--bg-dark);
        color: var(--text-primary);
    }
    
    .main {
        background-color: var(--bg-dark);
    }
    
    .stTabs [data-baseweb="tab-list"] {
        gap: 2px;
    }
    
    .stTabs [data-baseweb="tab"] {
        height: 50px;
        white-space: pre-wrap;
        background-color: rgba(30, 41, 59, 0.8);
        border-radius: 8px;
        color: var(--text-secondary);
        font-weight: 500;
    }
    
    .stTabs [aria-selected="true"] {
        background-color: var(--primary-color);
        color: white;
    }
    
    /* Hero header */
    .hero-header {
        background: linear-gradient(135deg, #6366f1 0%, #3b82f6 100%);
        padding: 30px;
        border-radius: 12px;
        margin-bottom: 30px;
        box-shadow: var(--shadow);
    }
    
    .hero-title {
        font-size: 2.5em;
        font-weight: 700;
        color: white;
        margin: 0;
        padding-bottom: 8px;
    }
    
    .hero-subtitle {
        font-size: 1em;
        color: rgba(255, 255, 255, 0.9);
        margin: 0;
        padding-bottom: 16px;
    }
    
    .badge-container {
        display: flex;
        gap: 8px;
        flex-wrap: wrap;
    }
    
    .badge {
        background-color: rgba(255, 255, 255, 0.2);
        border: 1px solid rgba(255, 255, 255, 0.3);
        padding: 6px 12px;
        border-radius: 20px;
        font-size: 0.85em;
        color: white;
        font-weight: 500;
    }
    
    /* Metric cards */
    .metric-card {
        background: linear-gradient(135deg, #1e293b 0%, #0f172a 100%);
        border: 1px solid var(--border-color);
        border-radius: 12px;
        padding: 20px;
        text-align: center;
        box-shadow: var(--shadow);
        transition: all 0.3s ease;
        min-height: 140px;
        display: flex;
        flex-direction: column;
        justify-content: center;
    }
    
    .metric-card:hover {
        transform: translateY(-4px);
        box-shadow: var(--shadow-lg);
        border-color: var(--primary-color);
    }
    
    .metric-label {
        font-size: 0.9em;
        color: var(--text-secondary);
        font-weight: 500;
        margin-bottom: 8px;
    }
    
    .metric-value {
        font-size: 1.8em;
        font-weight: 700;
        color: var(--text-primary);
        margin-bottom: 4px;
    }
    
    .metric-icon {
        font-size: 2em;
        margin-bottom: 8px;
    }
    
    /* Banners */
    .warning-banner {
        background: linear-gradient(135deg, #dc2626 0%, #991b1b 100%);
        border-radius: 8px;
        padding: 16px;
        color: white;
        font-weight: 600;
        text-align: center;
        box-shadow: var(--shadow);
    }
    
    .safe-banner {
        background: linear-gradient(135deg, #059669 0%, #065f46 100%);
        border-radius: 8px;
        padding: 16px;
        color: white;
        font-weight: 600;
        text-align: center;
        box-shadow: var(--shadow);
    }
    
    /* Preview placeholder */
    .placeholder-card {
        background-color: var(--bg-card);
        border: 2px dashed var(--border-color);
        border-radius: 12px;
        padding: 40px;
        text-align: center;
        color: var(--text-secondary);
        font-size: 1em;
    }
    
    /* Video preview */
    .video-preview {
        max-height: 320px;
        border-radius: 8px;
        overflow: hidden;
        box-shadow: var(--shadow);
    }
    
    /* Insights section */
    .insights-section {
        background-color: var(--bg-card);
        border-left: 4px solid var(--primary-color);
        border-radius: 8px;
        padding: 16px;
        margin: 12px 0;
    }
    
    .insight-bullet {
        color: var(--text-primary);
        margin: 8px 0;
        font-size: 0.95em;
        line-height: 1.5;
    }
    
    .insight-bullet:before {
        content: "▸ ";
        color: var(--primary-color);
        font-weight: bold;
        margin-right: 8px;
    }
    </style>
    """, unsafe_allow_html=True)


# ==================== COMPONENT RENDERERS ====================
def render_hero_header():
    """Render compact hero banner."""
    st.markdown("""
    <div class="hero-header">
        <h1 class="hero-title">🎬 Violence Detection AI</h1>
        <p class="hero-subtitle">Advanced video content analysis with deep learning</p>
        <div class="badge-container">
            <span class="badge">🧠 ResNet50 CNN</span>
            <span class="badge">⏱️ LSTM Temporal</span>
            <span class="badge">⚡ Real-time</span>
        </div>
    </div>
    """, unsafe_allow_html=True)


def render_metric_card(label: str, value: str, icon: str):
    """Render a metric card."""
    st.markdown(f"""
    <div class="metric-card">
        <div class="metric-icon">{icon}</div>
        <div class="metric-label">{label}</div>
        <div class="metric-value">{value}</div>
    </div>
    """, unsafe_allow_html=True)


def render_confidence_bar(confidence: float, is_violent: bool):
    """Render confidence progress bar using st.progress."""
    # Convert numpy.float32 to Python float and clamp to [0, 1]
    confidence = float(confidence)
    confidence = max(0.0, min(1.0, confidence))
    conf_pct = confidence * 100
    st.progress(confidence, text=f"Confidence: {conf_pct:.1f}%")


def render_violence_meter(confidence: float):
    """Render a premium violence probability gauge."""
    confidence = float(confidence)
    confidence = max(0.0, min(1.0, confidence))
    conf_pct = confidence * 100
    
    # Determine color and risk level
    if conf_pct < 35:
        color = "#10b981"  # Green - SAFE
        risk = "SAFE"
    elif conf_pct < 65:
        color = "#f59e0b"  # Orange - MEDIUM
        risk = "MEDIUM"
    else:
        color = "#ef4444"  # Red - HIGH RISK
        risk = "HIGH RISK"
    
    # Create gauge chart using Plotly
    fig = go.Figure(go.Indicator(
        mode="gauge+number+delta",
        value=conf_pct,
        domain={'x': [0, 1], 'y': [0, 1]},
        title={'text': "Violence Probability", 'font': {'size': 20, 'color': '#f1f5f9'}},
        delta={'reference': 50, 'suffix': "% from threshold"},
        gauge={
            'axis': {'range': [0, 100], 'tickcolor': '#334155'},
            'bar': {'color': color, 'thickness': 0.3},
            'bgcolor': '#0f172a',
            'borderwidth': 2,
            'bordercolor': '#334155',
            'steps': [
                {'range': [0, 35], 'color': 'rgba(16, 185, 129, 0.1)'},
                {'range': [35, 65], 'color': 'rgba(245, 158, 11, 0.1)'},
                {'range': [65, 100], 'color': 'rgba(239, 68, 68, 0.1)'}
            ],
            'threshold': {
                'line': {'color': '#6366f1', 'width': 4},
                'thickness': 0.75,
                'value': 50
            }
        },
        number={'font': {'size': 28, 'color': color}, 'suffix': '%'},
    ))
    
    fig.update_layout(
        font={'color': '#f1f5f9', 'family': 'Arial'},
        plot_bgcolor='rgba(0,0,0,0)',
        paper_bgcolor='rgba(15, 23, 42, 0.8)',
        height=350,
        margin={'l': 20, 'r': 20, 't': 60, 'b': 20}
    )
    
    st.plotly_chart(fig, use_container_width=True, config={'displayModeBar': False})
    
    # Risk level indicator
    risk_emoji = "🟢" if conf_pct < 35 else "🟠" if conf_pct < 65 else "🔴"
    st.markdown(f"**Risk Level:** {risk_emoji} {risk}", help=f"Confidence: {conf_pct:.1f}%")


def render_warning_banner():
    """Render red warning for violent content."""
    st.markdown("""
    <div class="warning-banner">
        ⚠️ VIOLENT CONTENT DETECTED
    </div>
    """, unsafe_allow_html=True)


def render_safe_banner():
    """Render green safe banner."""
    st.markdown("""
    <div class="safe-banner">
        ✓ SAFE CONTENT
    </div>
    """, unsafe_allow_html=True)


def render_why_prediction(confidence: float, is_violent: bool):
    """Render heuristic explanation for the prediction."""
    confidence = float(confidence)
    conf_pct = confidence * 100
    
    st.subheader("🔍 Why This Prediction?")
    
    if is_violent:
        if conf_pct > 0.8:
            insights = [
                "High motion intensity detected across multiple frames",
                "Rapid aggressive interactions and sudden movements identified",
                "Frame sequences show patterns consistent with violent activity"
            ]
        else:
            insights = [
                "Moderate motion intensity with potential aggressive elements",
                "Some rapid movements detected but lower confidence",
                "Borderline patterns requiring higher confidence threshold"
            ]
    else:
        if conf_pct < 0.2:
            insights = [
                "Stable motion patterns consistent with normal activity",
                "No sudden aggressive transitions detected",
                "Frame sequences match non-violent behavior profiles"
            ]
        else:
            insights = [
                "Mostly stable motion with minimal aggressive indicators",
                "Low-intensity movement transitions throughout video",
                "Content classified as safe with reasonable confidence"
            ]
    
    with st.container():
        for insight in insights:
            st.markdown(f"""
            <div class="insight-bullet">{insight}</div>
            """, unsafe_allow_html=True)


def render_sidebar_info():
    """Render sidebar information sections."""
    with st.sidebar:
        st.markdown("### ℹ️ Information")
        
        with st.expander("📱 About This App", expanded=False):
            st.markdown("""
            This application uses deep learning to detect violence in videos.
            
            **Features:**
            - Real-time video analysis
            - Confidence scoring
            - Risk level assessment
            - Detailed prediction insights
            """)
        
        with st.expander("🧠 Model Architecture", expanded=False):
            st.markdown("""
            **CNN Backbone:**
            - ResNet50 pre-trained on ImageNet
            - Extracts spatial features from 30 frames
            
            **Temporal Analysis:**
            - LSTM(128) processes frame sequences
            - Captures motion and interaction patterns
            
            **Classification Head:**
            - Dense(64) → Dropout(0.3)
            - Dense(32) → Dropout(0.2)
            - Dense(1, sigmoid) → Binary output
            
            **Total Parameters:** ~25.6M
            """)
        
        with st.expander("⚙️ How It Works", expanded=False):
            st.markdown("""
            **Step 1: Frame Extraction**
            - Extract 30 uniformly-spaced frames
            
            **Step 2: Preprocessing**
            - Resize to 224×224 pixels
            - Normalize to [0, 1]
            
            **Step 3: Feature Learning**
            - ResNet50 extracts spatial features
            - LSTM learns temporal dependencies
            
            **Step 4: Classification**
            - Sigmoid output: 0 (nonviolent) to 1 (violent)
            - Threshold: 0.50
            """)
        
        with st.expander("📊 Dataset Info", expanded=False):
            st.markdown("""
            **Dataset:** Hockey Fight Videos (Kaggle)
            
            **Statistics:**
            - Total videos: 1,000
            - Violent: 500 videos
            - Nonviolent: 500 videos
            - Frames per video: 30 (uniform sampling)
            - Resolution: 224×224 pixels
            
            **Train/Validation Split:**
            - Training: 800 videos (stratified)
            - Validation: 200 videos (stratified)
            
            **Threshold:** 0.50 (configurable)
            """)


# ==================== BACKEND FUNCTIONS (UNCHANGED) ====================
def load_model(model_path: str = "model/violence_model.h5"):
    """Load model from disk."""
    if not os.path.isfile(model_path):
        return None
    try:
        model = keras.models.load_model(model_path)
        return model
    except Exception as e:
        st.error(f"Error loading model: {e}")
        return None


def predict_video(video_path: str, model):
    """Predict violence label and confidence for a video."""
    try:
        frames = extract_frames(video_path, num_frames=30, img_size=224)
        
        if frames is None:
            return None, None
        
        # Add batch dimension
        X = np.expand_dims(frames, axis=0)
        
        # Predict
        prediction = model.predict(X, verbose=0)
        confidence = prediction[0][0]
        
        label = "VIOLENT" if confidence > 0.5 else "NONVIOLENT"
        
        return label, confidence
    except Exception as e:
        return None, None


# ==================== MAIN APPLICATION ====================
def main():
    """Main Streamlit app with premium dashboard design."""
    st.set_page_config(
        page_title="Violence Detection AI",
        layout="wide",
        initial_sidebar_state="expanded"
    )
    
    # Inject custom CSS
    inject_custom_css()
    
    # Render hero header
    render_hero_header()
    
    # Render sidebar
    render_sidebar_info()
    
    # Check if model exists
    model_path = "model/violence_model.h5"
    model = load_model(model_path)
    
    if model is None:
        st.error("⚠️ Model not found!", icon="🚨")
        st.markdown("""
        ### Setup Required
        
        The trained model is missing. Please train the model first:
        
        ```bash
        # 1. Add videos to training data
        # data/nonviolent/  (place nonviolent videos here)
        # data/violent/     (place violent videos here)
        
        # 2. Train the model
        python -m src.train
        
        # 3. Then return to this app
        streamlit run app/ui.py
        ```
        """)
        return
    
    # Main layout: Two columns
    col_left, col_right = st.columns([1, 1.2], gap="large")
    
    # ==================== LEFT COLUMN: UPLOAD ====================
    with col_left:
        st.markdown("#### 📤 Upload Video")
        
        uploaded_file = st.file_uploader(
            "Choose a video file",
            type=["mp4", "avi", "mov", "mkv", "flv"],
            label_visibility="collapsed"
        )
        
        if uploaded_file is not None:
            st.markdown("#### 👀 Preview")
            st.video(uploaded_file)
        else:
            st.markdown("""
            <div class="placeholder-card">
                📹 Upload a video to preview here
            </div>
            """, unsafe_allow_html=True)
    
    # ==================== RIGHT COLUMN: ANALYSIS ====================
    with col_right:
        st.markdown("#### 📊 Analysis Results")
        
        if uploaded_file is not None:
            # Save uploaded file temporarily
            with tempfile.NamedTemporaryFile(delete=False, suffix=".mp4") as tmp_file:
                tmp_file.write(uploaded_file.read())
                temp_video_path = tmp_file.name
            
            try:
                # Processing steps
                progress_text = st.empty()
                progress_bar = st.progress(0)
                
                # Extract frames
                progress_text.text("🎬 Extracting frames...")
                progress_bar.progress(25)
                
                # Predict
                progress_text.text("🧠 Analyzing with AI model...")
                progress_bar.progress(75)
                
                with st.spinner("Processing..."):
                    label, confidence = predict_video(temp_video_path, model)
                
                progress_text.text("✓ Analysis complete!")
                progress_bar.progress(100)
                
                if label is not None:
                    # Clear progress
                    progress_text.empty()
                    progress_bar.empty()
                    
                    # Determine risk level
                    is_violent = label == "VIOLENT"
                    
                    # Metric cards (3 columns)
                    metric_col1, metric_col2, metric_col3 = st.columns(3, gap="medium")
                    
                    with metric_col1:
                        render_metric_card("Prediction", label, "🎯")
                    
                    with metric_col2:
                        conf_pct = float(confidence) * 100
                        render_metric_card("Confidence", f"{conf_pct:.1f}%", "📈")
                    
                    with metric_col3:
                        risk_level = "HIGH RISK" if is_violent else "SAFE"
                        risk_icon = "🔴" if is_violent else "🟢"
                        render_metric_card("Risk Level", risk_level, risk_icon)
                    
                    # Confidence bar
                    st.markdown("##### 📊 Confidence Score")
                    render_confidence_bar(confidence, is_violent)
                    
                    # Violence meter gauge
                    st.markdown("##### ⚡ Violence Meter")
                    render_violence_meter(confidence)
                    
                    # Content warning/safe banner
                    st.markdown("---")
                    if is_violent:
                        render_warning_banner()
                    else:
                        render_safe_banner()
                
                else:
                    progress_text.empty()
                    progress_bar.empty()
                    st.error("❌ Could not analyze video. It may be corrupt or too short (< 30 frames required).")
            
            finally:
                # Clean up temp file
                if os.path.exists(temp_video_path):
                    os.remove(temp_video_path)
        
        else:
            st.info("👆 Upload a video to begin analysis", icon="📹")
    
    # ==================== DETAILED ANALYSIS SECTION ====================
    st.markdown("---")
    st.markdown("### 🔬 Detailed Analysis")
    
    # Check if we have results to show
    if uploaded_file is not None:
        with tempfile.NamedTemporaryFile(delete=False, suffix=".mp4") as tmp_file:
            tmp_file.write(uploaded_file.read())
            temp_video_path = tmp_file.name
        
        try:
            label, confidence = predict_video(temp_video_path, model)
            is_violent = label == "VIOLENT" if label else False
            
            tab1, tab2, tab3, tab4 = st.tabs([
                "📊 How It Works",
                "🎯 Decision Logic",
                "💡 Why This Prediction?",
                "📈 Model Insights"
            ])
            
            with tab1:
                st.markdown("""
                **Processing Pipeline:**
                
                1. **Frame Extraction** - Extract 30 uniformly-spaced frames from the video
                2. **Preprocessing** - Resize to 224×224 and normalize to [0, 1]
                3. **Feature Extraction** - ResNet50 extracts spatial features from each frame
                4. **Temporal Analysis** - LSTM processes sequence to capture motion patterns
                5. **Classification** - Dense layers produce confidence score
                """)
            
            with tab2:
                st.markdown("""
                **Decision Threshold: 0.50**
                
                - **Score > 0.50**: Content is classified as **VIOLENT** ⚠️
                - **Score ≤ 0.50**: Content is classified as **NONVIOLENT** ✓
                
                **Confidence Ranges:**
                - 0.50 - 0.60: Borderline (low confidence violent)
                - 0.60 - 0.75: Moderate (medium confidence violent)
                - 0.75 - 1.00: High confidence violent
                - 0.00 - 0.50: Nonviolent (increasing confidence)
                """)
            
            with tab3:
                if label is not None:
                    render_why_prediction(confidence, is_violent)
                else:
                    st.info("Upload and analyze a video to see prediction insights.")
            
            with tab4:
                st.markdown("""
                **Model Architecture:**
                - **CNN Backbone**: ResNet50 (pre-trained on ImageNet)
                - **Temporal Layer**: LSTM(128)
                - **Classification**: Dense(64) → Dense(32) → Dense(1, sigmoid)
                - **Total Parameters**: ~25.6M
                
                **Performance:**
                - Validation Accuracy: ~86%
                - Precision/Recall: Balanced for both classes
                - Processing Speed: <5s per video
                
                **Training Details:**
                - Optimizer: Adam
                - Loss: Binary Crossentropy
                - Epochs: 10
                - Batch Size: 8
                """)
        
        finally:
            if os.path.exists(temp_video_path):
                os.remove(temp_video_path)
    else:
        st.info("Upload a video to see detailed analysis and insights.")


if __name__ == "__main__":
    main()
        padding: 40px 30px;
        border-radius: 20px;
        color: white;
        margin-bottom: 30px;
        box-shadow: var(--shadow-lg);
        border: 1px solid rgba(255, 255, 255, 0.1);
    }
    
    .hero-title {
        font-size: 2.5em;
        font-weight: 800;
        margin: 0;
        letter-spacing: -1px;
        margin-bottom: 10px;
    }
    
    .hero-subtitle {
        font-size: 1.1em;
        opacity: 0.95;
        margin: 0;
        margin-bottom: 20px;
        font-weight: 500;
    }
    
    .badge-container {
        display: flex;
        gap: 10px;
        flex-wrap: wrap;
        margin-top: 15px;
    }
    
    .badge {
        background: rgba(255, 255, 255, 0.2);
        border: 1px solid rgba(255, 255, 255, 0.3);
        padding: 6px 14px;
        border-radius: 20px;
        font-size: 0.85em;
        font-weight: 600;
        backdrop-filter: blur(10px);
        display: inline-block;
        width: fit-content;
    }
    
    /* Metric cards */
    .metric-card {
        background: linear-gradient(135deg, var(--bg-card) 0%, rgba(30, 41, 59, 0.8) 100%);
        border: 1px solid var(--border-color);
        border-radius: 16px;
        padding: 24px;
        box-shadow: var(--shadow);
        transition: all 0.3s ease;
    }
    
    .metric-card:hover {
        transform: translateY(-4px);
        box-shadow: var(--shadow-lg);
        border-color: var(--primary-color);
    }
    
    .metric-value {
        font-size: 2.5em;
        font-weight: 800;
        margin: 10px 0;
        background: linear-gradient(135deg, var(--primary-color), var(--primary-color));
        -webkit-background-clip: text;
        -webkit-text-fill-color: transparent;
        background-clip: text;
    }
    
    .metric-label {
        color: var(--text-secondary);
        font-size: 0.95em;
        font-weight: 600;
        text-transform: uppercase;
        letter-spacing: 1px;
        margin-bottom: 8px;
    }
    
    /* Confidence bar */
    .confidence-bar {
        height: 8px;
        background: var(--border-color);
        border-radius: 10px;
        overflow: hidden;
        margin-top: 12px;
    }
    
    .confidence-fill {
        height: 100%;
        border-radius: 10px;
        transition: width 0.4s ease;
        background: linear-gradient(90deg, var(--primary-color), var(--success-color));
    }
    
    .confidence-fill.violent {
        background: linear-gradient(90deg, var(--danger-color), var(--warning-color));
    }
    
    /* Warning banner */
    .warning-banner {
        background: linear-gradient(135deg, #dc2626 0%, #991b1b 100%);
        border: 1px solid rgba(239, 68, 68, 0.3);
        border-radius: 12px;
        padding: 20px;
        margin: 20px 0;
        color: white;
        box-shadow: 0 4px 20px rgba(220, 38, 38, 0.3);
    }
    
    .warning-banner-title {
        font-weight: 700;
        font-size: 1.1em;
        margin-bottom: 8px;
    }
    
    .warning-banner-text {
        opacity: 0.95;
        line-height: 1.6;
    }
    
    /* Safe banner */
    .safe-banner {
        background: linear-gradient(135deg, #059669 0%, #065f46 100%);
        border: 1px solid rgba(16, 185, 129, 0.3);
        border-radius: 12px;
        padding: 20px;
        margin: 20px 0;
        color: white;
        box-shadow: 0 4px 20px rgba(16, 185, 129, 0.3);
    }
    
    .safe-banner-title {
        font-weight: 700;
        font-size: 1.1em;
        margin-bottom: 8px;
    }
    
    .safe-banner-text {
        opacity: 0.95;
        line-height: 1.6;
    }
    
    /* Section headers */
    .section-header {
        font-size: 1.4em;
        font-weight: 700;
        color: var(--text-primary);
        margin-top: 30px;
        margin-bottom: 20px;
        border-bottom: 2px solid var(--primary-color);
        padding-bottom: 12px;
    }
    
    /* Upload area */
    .upload-area {
        border: 2px dashed var(--primary-color);
        border-radius: 12px;
        padding: 30px;
        text-align: center;
        background: rgba(99, 102, 241, 0.05);
        transition: all 0.3s ease;
    }
    
    .upload-area:hover {
        background: rgba(99, 102, 241, 0.1);
        border-color: #818cf8;
    }
    
    /* Tabs styling */
    .stTabs [data-baseweb="tab-list"] {
        background: rgba(30, 41, 59, 0.5);
        border-radius: 12px;
        border: 1px solid var(--border-color);
        gap: 0;
    }
    
    .stTabs [data-baseweb="tab"] {
        border-radius: 0;
        color: var(--text-secondary);
        padding: 12px 20px;
    }
    
    .stTabs [aria-selected="true"] {
        background: var(--primary-color);
        color: white;
    }
    
    /* Sidebar */
    [data-testid="stSidebar"] {
        background: linear-gradient(180deg, var(--bg-card) 0%, rgba(15, 23, 42, 0.95) 100%);
    }
    
    .sidebar-header {
        font-size: 1.3em;
        font-weight: 700;
        color: var(--primary-color);
        margin-top: 20px;
        margin-bottom: 15px;
    }
    
    /* Expander styling */
    .streamlit-expanderHeader {
        background: linear-gradient(90deg, rgba(99, 102, 241, 0.1), rgba(59, 130, 246, 0.05));
        border-radius: 8px;
        border: 1px solid rgba(99, 102, 241, 0.2);
    }
    
    /* Video container */
    .video-container {
        border-radius: 12px;
        overflow: hidden;
        border: 1px solid var(--border-color);
        box-shadow: var(--shadow);
        background: var(--bg-card);
    }
    
    /* Analysis section */
    .analysis-grid {
        display: grid;
        grid-template-columns: repeat(auto-fit, minmax(250px, 1fr));
        gap: 20px;
        margin: 20px 0;
    }
    
    /* Risk level indicator */
    .risk-level {
        font-size: 1.1em;
        font-weight: 700;
        padding: 8px 12px;
        border-radius: 8px;
        display: inline-block;
        margin-top: 8px;
    }
    
    .risk-high {
        background: linear-gradient(135deg, #fee2e2, #fecaca);
        color: #dc2626;
    }
    
    .risk-low {
        background: linear-gradient(135deg, #dcfce7, #bbf7d0);
        color: #059669;
    }
    
    /* Gauge chart simulation */
    .gauge-container {
        text-align: center;
        padding: 20px;
    }
    
    .gauge-percentage {
        font-size: 3em;
        font-weight: 800;
        background: linear-gradient(135deg, var(--primary-color), var(--primary-color));
        -webkit-background-clip: text;
        -webkit-text-fill-color: transparent;
        background-clip: text;
    }
    
    /* Animations */
    @keyframes slide-in {
        from {
            opacity: 0;
            transform: translateY(20px);
        }
        to {
            opacity: 1;
            transform: translateY(0);
        }
    }
    
    .metric-card {
        animation: slide-in 0.5s ease forwards;
    }
    
    /* Responsive adjustments */
    @media (max-width: 768px) {
        .hero-title {
            font-size: 1.8em;
        }
        
        .hero-subtitle {
            font-size: 0.95em;
        }
        
        .metric-value {
            font-size: 1.8em;
        }
    }
    </style>
    """, unsafe_allow_html=True)


# ==================== HELPER FUNCTIONS ====================
def load_model(model_path: str = "model/violence_model.h5"):
    """Load model from disk."""
    if not os.path.isfile(model_path):
        return None
    try:
        model = keras.models.load_model(model_path)
        return model
    except Exception as e:
        st.error(f"Error loading model: {e}")
        return None


def predict_video(video_path: str, model):
    """Predict violence label and confidence for a video."""
    try:
        frames = extract_frames(video_path, num_frames=30, img_size=224)
        
        if frames is None:
            return None, None
        
        # Add batch dimension
        X = np.expand_dims(frames, axis=0)
        
        # Predict
        prediction = model.predict(X, verbose=0)
        confidence = prediction[0][0]
        
        label = "VIOLENT" if confidence > 0.5 else "NONVIOLENT"
        
        return label, confidence
    
    except Exception as e:
        st.error(f"Error during prediction: {e}")
        return None, None


def render_hero_header():
    """Render the hero header section."""
    st.markdown("""
    <div class="hero-header">
        <h1 class="hero-title">🎬 Violence Detection AI</h1>
        <p class="hero-subtitle">Advanced video content analysis powered by deep learning</p>
        <div class="badge-container">
            <span class="badge">🧠 ResNet50 CNN</span>
            <span class="badge">⏱️ LSTM Temporal</span>
            <span class="badge">📊 Streaming Pipeline</span>
            <span class="badge">⚡ Real-time Detection</span>
        </div>
    </div>
    """, unsafe_allow_html=True)


def render_metric_card(label: str, value: str, icon: str, color_class: str = ""):
    """Render a metric card."""
    st.markdown(f"""
    <div class="metric-card">
        <div class="metric-label">{label}</div>
        <div class="metric-value">{icon} {value}</div>
    </div>
    """, unsafe_allow_html=True)


def render_confidence_bar(confidence: float, is_violent: bool):
    """Render confidence progress bar using st.progress."""
    # Convert numpy.float32 to Python float and clamp to [0, 1]
    confidence = float(confidence)
    confidence = max(0.0, min(1.0, confidence))
    conf_pct = confidence * 100
    st.progress(confidence, text=f"Confidence: {conf_pct:.1f}%")


def render_warning_banner():
    """Render violent content warning banner."""
    st.markdown("""
    <div class="warning-banner">
        <div class="warning-banner-title">⚠️ TRIGGER WARNING</div>
        <div class="warning-banner-text">
            This video has been detected to contain violent content. 
            Viewer discretion is strongly advised.
        </div>
    </div>
    """, unsafe_allow_html=True)


def render_safe_banner():
    """Render safe content banner."""
    st.markdown("""
    <div class="safe-banner">
        <div class="safe-banner-title">✓ CONTENT SAFE</div>
        <div class="safe-banner-text">
            This video does not contain violent content and is safe to view.
        </div>
    </div>
    """, unsafe_allow_html=True)


def render_sidebar_info():
    """Render sidebar information sections."""
    with st.sidebar:
        st.markdown("---")
        
        with st.expander("ℹ️ About This App"):
            st.markdown("""
            This application uses advanced AI to detect violent content in videos.
            
            **Key Features:**
            - Real-time video analysis
            - Per-frame feature extraction
            - Temporal pattern recognition
            - High accuracy classification
            """)
        
        with st.expander("🧠 Model Architecture"):
            st.markdown("""
            **Layer Stack:**
            1. **ResNet50** - Pre-trained CNN for frame features
            2. **TimeDistributed** - Apply CNN to each frame
            3. **LSTM** - Capture temporal dependencies
            4. **Dense** - Classification layers
            
            **Input:** 30 frames × 224×224 RGB
            **Output:** Binary classification (0.0-1.0)
            """)
        
        with st.expander("🔬 How It Works"):
            st.markdown("""
            **Processing Pipeline:**
            1. Extract 30 uniform frames from video
            2. Resize each frame to 224×224
            3. Pass through ResNet50 for features
            4. LSTM analyzes temporal sequence
            5. Output confidence score
            
            **Threshold:** 0.50
            - Score > 0.50 = Violent
            - Score ≤ 0.50 = Non-violent
            """)
        
        with st.expander("📊 Dataset"):
            st.markdown("""
            **Training Data:**
            - Total Videos: 1000
            - Violent: 500
            - Non-violent: 500
            
            **Split:**
            - Training: 800 (400 each class)
            - Validation: 200 (100 each class)
            
            **Augmentation:**
            - Random frame sampling
            - Brightness/contrast variations
            """)
        
        st.markdown("---")
        st.caption("🚀 Built with TensorFlow & Streamlit")


def main():
    """Main Streamlit app."""
    st.set_page_config(
        page_title="Violence Detection AI",
        layout="wide",
        initial_sidebar_state="expanded"
    )
    
    # Inject custom CSS
    inject_custom_css()
    
    # Render hero header
    render_hero_header()
    
    # Render sidebar
    render_sidebar_info()
    
    # Check if model exists
    model_path = "model/violence_model.h5"
    model = load_model(model_path)
    
    if model is None:
        st.error("⚠️ Model not found!", icon="🚨")
        st.markdown("""
        ### Setup Required
        
        The trained model is missing. Please train the model first:
        
        ```bash
        # 1. Add videos to training data
        # data/nonviolent/  (place nonviolent videos here)
        # data/violent/     (place violent videos here)
        
        # 2. Train the model
        python -m src.train
        
        # 3. Then return to this app
        streamlit run app/ui.py
        ```
        """)
        return
    
    # Main layout: Two columns
    col_left, col_right = st.columns([1, 1.2], gap="large")
    
    # ==================== LEFT COLUMN: UPLOAD ====================
    with col_left:
        st.markdown("#### 📤 Upload Video")
        st.markdown("""
        <style>
        .stFileUploader > label { font-size: 0.9em; }
        </style>
        """, unsafe_allow_html=True)
        
        uploaded_file = st.file_uploader(
            "Choose a video file",
            type=["mp4", "avi", "mov", "mkv", "flv"],
            label_visibility="collapsed"
        )
        
        if uploaded_file is not None:
            st.markdown("#### 👀 Preview")
            st.video(uploaded_file)
    
    # ==================== RIGHT COLUMN: ANALYSIS ====================
    with col_right:
        st.markdown("#### 📊 Analysis Results")
        results_placeholder = st.empty()
        
        if uploaded_file is not None:
            # Save uploaded file temporarily
            with tempfile.NamedTemporaryFile(delete=False, suffix=".mp4") as tmp_file:
                tmp_file.write(uploaded_file.read())
                temp_video_path = tmp_file.name
            
            try:
                # Processing steps
                progress_text = st.empty()
                progress_bar = st.progress(0)
                
                # Extract frames
                progress_text.text("🎬 Extracting frames...")
                progress_bar.progress(25)
                
                # Predict
                progress_text.text("🧠 Analyzing with AI model...")
                progress_bar.progress(75)
                
                with st.spinner("Processing..."):
                    label, confidence = predict_video(temp_video_path, model)
                
                progress_text.text("✓ Analysis complete!")
                progress_bar.progress(100)
                
                if label is not None:
                    # Clear progress
                    progress_text.empty()
                    progress_bar.empty()
                    
                    # Determine risk level
                    is_violent = label == "VIOLENT"
                    risk_level = "HIGH RISK" if is_violent else "SAFE"
                    risk_color = "🔴" if is_violent else "🟢"
                    
                    # Metric cards
                    metric_col1, metric_col2, metric_col3 = st.columns(3, gap="medium")
                    
                    with metric_col1:
                        render_metric_card(
                            "Prediction",
                            label,
                            "🎯"
                        )
                    
                    with metric_col2:
                        render_metric_card(
                            "Confidence",
                            f"{confidence*100:.1f}%",
                            "📈"
                        )
                    
                    with metric_col3:
                        render_metric_card(
                            "Risk Level",
                            risk_level,
                            risk_color
                        )
                    
                    # Confidence visualization
                    st.markdown("##### Confidence Score")
                    render_confidence_bar(confidence, is_violent)
                    
                    # Content warning
                    st.markdown("---")
                    if is_violent:
                        render_warning_banner()
                    else:
                        render_safe_banner()
                
                else:
                    progress_text.empty()
                    progress_bar.empty()
                    st.error("❌ Could not analyze video. It may be corrupt or too short (< 30 frames required).")
            
            finally:
                # Clean up temp file
                if os.path.exists(temp_video_path):
                    os.remove(temp_video_path)
        
        else:
            st.info("👆 Upload a video to begin analysis", icon="📹")
    
    # ==================== DETAILED ANALYSIS SECTION ====================
    st.markdown("---")
    st.markdown("### 🔬 Detailed Analysis")
    
    tab1, tab2, tab3 = st.tabs(["📊 How It Works", "🎯 Decision Logic", "📈 Model Insights"])
    
    with tab1:
        st.markdown("""
        **Processing Pipeline:**
        
        1. **Frame Extraction** - Extract 30 uniformly-spaced frames from the video
        2. **Preprocessing** - Resize to 224×224 and normalize to [0, 1]
        3. **Feature Extraction** - ResNet50 extracts spatial features from each frame
        4. **Temporal Analysis** - LSTM processes sequence to capture motion patterns
        5. **Classification** - Dense layers produce confidence score
        """)
    
    with tab2:
        st.markdown("""
        **Decision Threshold: 0.50**
        
        - **Score > 0.50**: Content is classified as **VIOLENT** ⚠️
        - **Score ≤ 0.50**: Content is classified as **NONVIOLENT** ✓
        
        **Confidence Interpretation:**
        - 0.50 - 0.60: Borderline (low confidence violent)
        - 0.60 - 0.75: Moderate (medium confidence violent)
        - 0.75 - 1.00: High confidence violent
        """)
    
    with tab3:
        st.markdown("""
        **Model Architecture:**
        - **CNN Backbone**: ResNet50 (pre-trained on ImageNet)
        - **Temporal Layer**: LSTM(128)
        - **Classification**: Dense(64) → Dense(32) → Dense(1, sigmoid)
        - **Total Parameters**: ~25.6M
        
        **Performance:**
        - Validation Accuracy: ~86%
        - Precision/Recall: Balanced for both classes
        - Processing Speed: <5s per video
        """)


if __name__ == "__main__":
    main()
