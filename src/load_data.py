"""
Load and prepare dataset for violence detection using generators.
Memory-efficient streaming of video samples without loading entire dataset into RAM.
"""

import os
import math
import numpy as np
from pathlib import Path
from typing import Generator, Tuple, List

try:
    # When running as module
    from src.frames import extract_frames
except ImportError:
    # When running directly
    from frames import extract_frames


def count_videos(data_dir: str = "data") -> Tuple[int, int]:
    """
    Count total videos in dataset without loading them.
    
    Args:
        data_dir: Root directory containing 'violent' and 'nonviolent' subdirectories
    
    Returns:
        (total_nonviolent, total_violent) counts
    """
    nonviolent_count = 0
    violent_count = 0
    
    nonviolent_dir = os.path.join(data_dir, "nonviolent")
    if os.path.isdir(nonviolent_dir):
        nonviolent_count = len([f for f in os.listdir(nonviolent_dir) if os.path.isfile(os.path.join(nonviolent_dir, f))])
    
    violent_dir = os.path.join(data_dir, "violent")
    if os.path.isdir(violent_dir):
        violent_count = len([f for f in os.listdir(violent_dir) if os.path.isfile(os.path.join(violent_dir, f))])
    
    return nonviolent_count, violent_count


def video_generator(data_dir: str = "data", num_frames: int = 30) -> Generator[Tuple[np.ndarray, int], None, None]:
    """
    Generator that yields (frames, label) for each video one at a time.
    Memory-efficient: does not load all videos into RAM.
    
    Args:
        data_dir: Root directory containing 'violent' and 'nonviolent' subdirectories
        num_frames: Number of frames to extract per video
    
    Yields:
        (frames, label) tuples where:
            - frames: np.ndarray of shape (num_frames, 224, 224, 3), dtype float32
            - label: int (0 for nonviolent, 1 for violent)
    """
    
    # Ensure data directory exists
    if not os.path.isdir(data_dir):
        print(f"Error: Data directory '{data_dir}' not found.")
        return
    
    # Process nonviolent videos (label 0)
    nonviolent_dir = os.path.join(data_dir, "nonviolent")
    if os.path.isdir(nonviolent_dir):
        for video_file in os.listdir(nonviolent_dir):
            video_path = os.path.join(nonviolent_dir, video_file)
            if os.path.isfile(video_path):
                frames = extract_frames(video_path, num_frames=num_frames)
                if frames is not None:
                    yield frames, np.int32(0)
    
    # Process violent videos (label 1)
    violent_dir = os.path.join(data_dir, "violent")
    if os.path.isdir(violent_dir):
        for video_file in os.listdir(violent_dir):
            video_path = os.path.join(violent_dir, video_file)
            if os.path.isfile(video_path):
                frames = extract_frames(video_path, num_frames=num_frames)
                if frames is not None:
                    yield frames, np.int32(1)


def get_dataset_split(data_dir: str = "data", num_frames: int = 30, 
                     batch_size: int = 8, validation_split: float = 0.2, 
                     epochs: int = 10) -> Tuple:
    """
    Create tf.data.Dataset objects for training and validation without loading full dataset.
    Uses stratified split to ensure both classes are in both train and validation sets.
    Training dataset is repeated for multiple epochs; validation dataset is not repeated.
    
    Args:
        data_dir: Root directory containing 'violent' and 'nonviolent' subdirectories
        num_frames: Number of frames to extract per video
        batch_size: Batch size for training
        validation_split: Fraction of data to use for validation (default 0.2)
        epochs: Number of training epochs (used for repeating train dataset)
    
    Returns:
        (train_dataset, val_dataset, train_steps, val_steps, class_counts)
        where:
            - train_dataset: tf.data.Dataset for training (repeated for epochs)
            - val_dataset: tf.data.Dataset for validation (not repeated)
            - train_steps: Number of steps per epoch for training
            - val_steps: Number of steps per validation epoch
            - class_counts: Dict with class distribution info
    """
    
    import tensorflow as tf
    
    print("Creating dataset generators...")
    
    # Count videos first
    nonviolent_count, violent_count = count_videos(data_dir)
    total_count = nonviolent_count + violent_count
    
    if total_count == 0:
        print("Error: No videos found in dataset.")
        return None, None, 0, 0, {}
    
    print(f"Found dataset:")
    print(f"  Nonviolent videos: {nonviolent_count}")
    print(f"  Violent videos: {violent_count}")
    print(f"  Total videos: {total_count}")
    
    # Calculate stratified split (80/20 for each class)
    nonviolent_train = int(nonviolent_count * (1 - validation_split))
    nonviolent_val = nonviolent_count - nonviolent_train
    violent_train = int(violent_count * (1 - validation_split))
    violent_val = violent_count - violent_train
    
    train_count = nonviolent_train + violent_train
    val_count = nonviolent_val + violent_val
    
    print(f"\nDataset split (stratified):")
    print(f"  Training videos: {train_count}")
    print(f"    - Nonviolent: {nonviolent_train}")
    print(f"    - Violent: {violent_train}")
    print(f"  Validation videos: {val_count}")
    print(f"    - Nonviolent: {nonviolent_val}")
    print(f"    - Violent: {violent_val}")
    
    # Define output signature for tf.data.Dataset
    output_signature = (
        tf.TensorSpec(shape=(num_frames, 224, 224, 3), dtype=tf.float32),
        tf.TensorSpec(shape=(), dtype=tf.int32)
    )
    
    # Create train generator (80% of each class)
    def train_gen():
        nonviolent_count = 0
        violent_count = 0
        
        # Generate nonviolent training samples
        nonviolent_dir = os.path.join(data_dir, "nonviolent")
        if os.path.isdir(nonviolent_dir):
            for video_file in os.listdir(nonviolent_dir):
                if nonviolent_count >= nonviolent_train:
                    break
                video_path = os.path.join(nonviolent_dir, video_file)
                if os.path.isfile(video_path):
                    frames = extract_frames(video_path, num_frames=num_frames)
                    if frames is not None:
                        yield frames, np.int32(0)
                        nonviolent_count += 1
        
        # Generate violent training samples
        violent_dir = os.path.join(data_dir, "violent")
        if os.path.isdir(violent_dir):
            for video_file in os.listdir(violent_dir):
                if violent_count >= violent_train:
                    break
                video_path = os.path.join(violent_dir, video_file)
                if os.path.isfile(video_path):
                    frames = extract_frames(video_path, num_frames=num_frames)
                    if frames is not None:
                        yield frames, np.int32(1)
                        violent_count += 1
    
    # Create validation generator (20% of each class)
    def val_gen():
        nonviolent_count = 0
        violent_count = 0
        nonviolent_skip = 0
        violent_skip = 0
        
        # Skip nonviolent training samples, collect validation samples
        nonviolent_dir = os.path.join(data_dir, "nonviolent")
        if os.path.isdir(nonviolent_dir):
            for video_file in os.listdir(nonviolent_dir):
                if nonviolent_count >= nonviolent_val:
                    break
                video_path = os.path.join(nonviolent_dir, video_file)
                if os.path.isfile(video_path):
                    frames = extract_frames(video_path, num_frames=num_frames)
                    if frames is not None:
                        if nonviolent_skip < nonviolent_train:
                            nonviolent_skip += 1
                        else:
                            yield frames, np.int32(0)
                            nonviolent_count += 1
        
        # Skip violent training samples, collect validation samples
        violent_dir = os.path.join(data_dir, "violent")
        if os.path.isdir(violent_dir):
            for video_file in os.listdir(violent_dir):
                if violent_count >= violent_val:
                    break
                video_path = os.path.join(violent_dir, video_file)
                if os.path.isfile(video_path):
                    frames = extract_frames(video_path, num_frames=num_frames)
                    if frames is not None:
                        if violent_skip < violent_train:
                            violent_skip += 1
                        else:
                            yield frames, np.int32(1)
                            violent_count += 1
    
    # Create tf.data.Dataset from generators
    train_dataset = tf.data.Dataset.from_generator(
        train_gen,
        output_signature=output_signature
    )
    
    val_dataset = tf.data.Dataset.from_generator(
        val_gen,
        output_signature=output_signature
    )
    
    # Shuffle training data (before repeat for better randomization)
    train_dataset = train_dataset.shuffle(buffer_size=min(1000, train_count))
    
    # Add batching and prefetching for performance
    train_dataset = train_dataset.batch(batch_size).prefetch(tf.data.AUTOTUNE)
    
    # IMPORTANT: Repeat train dataset AFTER batching to ensure proper epoch handling
    # This allows training to continue for multiple epochs without stopping
    train_dataset = train_dataset.repeat()
    
    # Validation dataset is NOT repeated (it should run once per epoch)
    val_dataset = val_dataset.batch(batch_size).prefetch(tf.data.AUTOTUNE)
    
    # Calculate steps per epoch using ceiling division
    # This ensures all samples are processed even if not evenly divisible
    train_steps = math.ceil(train_count / batch_size)
    val_steps = math.ceil(val_count / batch_size)
    
    class_counts = {
        'nonviolent': nonviolent_count,
        'violent': violent_count,
        'total': total_count,
        'train': train_count,
        'val': val_count,
        'train_nonviolent': nonviolent_train,
        'train_violent': violent_train,
        'val_nonviolent': nonviolent_val,
        'val_violent': violent_val
    }
    
    print(f"\nDataset ready:")
    print(f"  Train steps per epoch: {train_steps} (batch_size={batch_size})")
    print(f"  Val steps per epoch: {val_steps} (batch_size={batch_size})")
    print(f"  Training will repeat dataset for {epochs} epochs")
    
    return train_dataset, val_dataset, train_steps, val_steps, class_counts
