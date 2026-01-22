"""
Extract frames from video files for the violence detection model.
"""

import cv2
import numpy as np
from typing import Optional


def extract_frames(video_path: str, num_frames: int = 30, img_size: int = 224) -> Optional[np.ndarray]:
    """
    Extract uniformly sampled frames from a video file.
    
    Args:
        video_path: Path to the video file
        num_frames: Number of frames to extract (default 30)
        img_size: Target frame size (224x224 for ResNet50)
    
    Returns:
        np.ndarray of shape (num_frames, img_size, img_size, 3) normalized to [0, 1] as float32,
        or None if video is corrupt or has fewer frames than required
    """
    try:
        cap = cv2.VideoCapture(video_path)
        
        # Check if video is corrupted
        if not cap.isOpened():
            return None
        
        total_frames = int(cap.get(cv2.CAP_PROP_FRAME_COUNT))
        
        # Return None if video has fewer frames than required
        if total_frames < num_frames:
            cap.release()
            return None
        
        # Calculate frame indices to sample uniformly
        frame_indices = np.linspace(0, total_frames - 1, num_frames, dtype=int)
        
        frames_list = []
        frame_count = 0
        target_idx = 0
        
        while cap.isOpened() and target_idx < num_frames:
            ret, frame = cap.read()
            
            if not ret:
                cap.release()
                return None
            
            # Check if this frame should be included
            if frame_count == frame_indices[target_idx]:
                # Convert BGR to RGB
                frame = cv2.cvtColor(frame, cv2.COLOR_BGR2RGB)
                # Resize to img_size x img_size
                frame = cv2.resize(frame, (img_size, img_size))
                # Normalize to [0, 1] as float32
                frame = frame.astype(np.float32) / 255.0
                frames_list.append(frame)
                target_idx += 1
            
            frame_count += 1
        
        cap.release()
        
        # Return array of shape (num_frames, img_size, img_size, 3)
        if len(frames_list) == num_frames:
            return np.array(frames_list, dtype=np.float32)
        else:
            return None
    
    except Exception as e:
        print(f"Error extracting frames from {video_path}: {e}")
        return None
