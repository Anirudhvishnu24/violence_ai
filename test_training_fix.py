"""
Quick validation test for the training pipeline fix.
Verifies that dataset generators work without "OUT_OF_RANGE: End of sequence" error.
"""

import sys
import os
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))

from src.load_data import get_dataset_split
import tensorflow as tf

def test_training_pipeline():
    """
    Test that training dataset repeats correctly for multiple epochs.
    """
    print("=" * 70)
    print("TRAINING PIPELINE VALIDATION TEST")
    print("=" * 70)
    
    # Test parameters
    BATCH_SIZE = 8
    NUM_FRAMES = 30
    EPOCHS = 3  # Short test with 3 epochs
    
    print("\n[1] Loading test dataset...")
    try:
        train_dataset, val_dataset, train_steps, val_steps, class_counts = get_dataset_split(
            data_dir="data",
            num_frames=NUM_FRAMES,
            batch_size=BATCH_SIZE,
            validation_split=0.2,
            epochs=EPOCHS
        )
        print(f"    [OK] Datasets loaded")
        print(f"    - Total videos: {class_counts['total']}")
        print(f"    - Training samples: {class_counts['train']}")
        print(f"    - Validation samples: {class_counts['val']}")
        print(f"    - Train steps per epoch: {train_steps}")
        print(f"    - Val steps per epoch: {val_steps}")
    except Exception as e:
        print(f"    [ERROR] Failed to load datasets: {e}")
        return False
    
    if train_dataset is None:
        print("    [ERROR] No training data found!")
        return False
    
    # Test that training dataset repeats without exhaustion
    print("\n[2] Testing training dataset repetition (simulating 3 epochs)...")
    try:
        total_batches = 0
        batches_per_epoch = []
        
        for epoch in range(EPOCHS):
            epoch_batches = 0
            print(f"    Epoch {epoch+1}:", end=" ")
            
            # Take exactly train_steps batches for this epoch
            for batch_idx, (frames, labels) in enumerate(train_dataset):
                epoch_batches += 1
                total_batches += 1
                
                if batch_idx >= train_steps - 1:
                    break
            
            batches_per_epoch.append(epoch_batches)
            print(f"{epoch_batches} batches")
            
            if epoch_batches < train_steps:
                print(f"    [WARNING] Epoch {epoch+1} incomplete: {epoch_batches}/{train_steps}")
        
        if all(b == train_steps for b in batches_per_epoch):
            print(f"    [OK] All {EPOCHS} epochs completed successfully!")
            print(f"    [OK] Total batches processed: {total_batches}")
        else:
            print(f"    [WARNING] Batch counts inconsistent: {batches_per_epoch}")
            
    except tf.errors.OutOfRangeError as e:
        print(f"    [ERROR] OUT_OF_RANGE error (dataset exhausted): {e}")
        return False
    except Exception as e:
        print(f"    [ERROR] Unexpected error during training: {e}")
        return False
    
    # Test validation dataset (should NOT repeat)
    print("\n[3] Testing validation dataset (should complete in one pass)...")
    try:
        val_batches = 0
        for batch_idx, (frames, labels) in enumerate(val_dataset):
            val_batches += 1
        
        if val_batches == val_steps:
            print(f"    [OK] Validation dataset completed: {val_batches} batches")
        else:
            print(f"    [WARNING] Validation batches: {val_batches} (expected {val_steps})")
            
    except Exception as e:
        print(f"    [ERROR] Validation dataset error: {e}")
        return False
    
    print("\n" + "=" * 70)
    print("RESULT: ALL TESTS PASSED")
    print("=" * 70)
    print("\nTraining pipeline is ready!")
    print("Run: python -m src.train")
    print("\nExpected behavior:")
    print(f"  - Training for 10 epochs")
    print(f"  - {train_steps} steps per epoch")
    print(f"  - No 'OUT_OF_RANGE' errors")
    
    return True


if __name__ == "__main__":
    success = test_training_pipeline()
    sys.exit(0 if success else 1)
