"""
Command-line interface for predicting violence in videos.

Usage:
    python -m src.predict --video "path/to/video.mp4"
"""

import os
import sys
import argparse
import numpy as np
from tensorflow import keras

try:
    # When running as module: python -m src.predict
    from src.frames import extract_frames
except ImportError:
    # When running directly
    from frames import extract_frames


def predict_video(video_path: str, model_path: str = "model/violence_model.h5"):
    """
    Load model and predict violence for a given video.
    
    Args:
        video_path: Path to the video file
        model_path: Path to the trained model
    
    Returns:
        Tuple of (label_string, confidence_score)
    """
    
    # Check if video file exists
    if not os.path.isfile(video_path):
        print(f"ERROR: Video file not found: {video_path}")
        return None, None
    
    # Check if model exists
    if not os.path.isfile(model_path):
        print(f"ERROR: Model not found: {model_path}")
        print("Please train the model first using: python -m src.train")
        return None, None
    
    # Load model
    print(f"Loading model from {model_path}...")
    model = keras.models.load_model(model_path)
    
    # Extract frames
    print(f"Extracting frames from {video_path}...")
    frames = extract_frames(video_path, num_frames=30, img_size=224)
    
    if frames is None:
        print(f"ERROR: Could not extract frames from video. Video may be corrupt or too short.")
        return None, None
    
    # Add batch dimension: (1, 30, 224, 224, 3)
    X = np.expand_dims(frames, axis=0)
    
    # Predict
    print("Running prediction...")
    prediction = model.predict(X, verbose=0)
    confidence = prediction[0][0]
    
    # Determine label
    label = "VIOLENT" if confidence > 0.5 else "NONVIOLENT"
    
    return label, confidence


def main():
    """CLI entry point."""
    parser = argparse.ArgumentParser(
        description="Predict violence content in video files"
    )
    parser.add_argument(
        "--video",
        type=str,
        required=True,
        help="Path to video file"
    )
    parser.add_argument(
        "--model",
        type=str,
        default="model/violence_model.h5",
        help="Path to trained model (default: model/violence_model.h5)"
    )
    
    args = parser.parse_args()
    
    label, confidence = predict_video(args.video, args.model)
    
    if label is not None:
        print("\n" + "=" * 60)
        print("PREDICTION RESULT")
        print("=" * 60)
        print(f"Label: {label}")
        print(f"Confidence: {confidence:.4f}")
        print("=" * 60)
    else:
        sys.exit(1)


if __name__ == "__main__":
    main()
