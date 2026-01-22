"""
Train the violence detection model using tf.data generators for memory efficiency.
"""

import os
import numpy as np
import matplotlib.pyplot as plt
from sklearn.metrics import confusion_matrix, classification_report, accuracy_score
import seaborn as sns
from tensorflow import keras

try:
    # When running as module: python -m src.train
    from src.load_data import get_dataset_split
    from src.net import build_model
except ImportError:
    # When running directly
    from load_data import get_dataset_split
    from net import build_model


def train_model():
    """
    Train the ResNet50 + LSTM model end-to-end using tf.data generators.
    Memory-efficient: streams data from disk instead of loading into RAM.
    
    Saves:
        - model/violence_model.h5: Trained model
        - outputs/confusion_matrix.png: Confusion matrix visualization
        - outputs/training_curves.png: Training/validation accuracy and loss curves
    """
    
    # Create output directories if they don't exist
    os.makedirs("model", exist_ok=True)
    os.makedirs("outputs", exist_ok=True)
    
    print("=" * 60)
    print("Violence Detection Model Training")
    print("=" * 60)
    
    # Training parameters
    EPOCHS = 10
    BATCH_SIZE = 8
    NUM_FRAMES = 30
    
    # Get dataset generators with correct steps_per_epoch
    print("\n[1/5] Loading dataset (streaming from disk)...")
    train_dataset, val_dataset, train_steps, val_steps, class_counts = get_dataset_split(
        data_dir="data",
        num_frames=NUM_FRAMES,
        batch_size=BATCH_SIZE,
        validation_split=0.2,
        epochs=EPOCHS
    )
    
    if train_dataset is None:
        print("ERROR: No data loaded. Check data directory structure.")
        print("Expected structure:")
        print("  data/")
        print("    nonviolent/  (video files)")
        print("    violent/     (video files)")
        return
    
    # Build model
    print("\n[2/5] Building ResNet50 + LSTM model...")
    model = build_model(num_frames=NUM_FRAMES)
    print("Model architecture:")
    model.summary()
    
    # Train model using generators with explicit steps_per_epoch
    print(f"\n[3/5] Training model for {EPOCHS} epochs...")
    print(f"     (streaming {train_steps} steps per epoch)")
    
    history = model.fit(
        train_dataset,
        steps_per_epoch=train_steps,
        validation_data=val_dataset,
        validation_steps=val_steps,
        epochs=EPOCHS,
        verbose=1
    )
    
    # Save model
    model_path = "model/violence_model.h5"
    model.save(model_path)
    print(f"\n[4/5] Model saved to {model_path}")
    
    # Evaluate on validation set
    print("\n" + "=" * 60)
    print("Validation Set Evaluation")
    print("=" * 60)
    
    # Get all validation data for detailed metrics
    print("\nGenerating predictions on validation set...")
    y_true = []
    y_pred_prob = []
    batch_count = 0
    
    # Iterate through validation dataset and collect predictions
    for frames, labels in val_dataset:
        # Get model predictions
        predictions = model.predict(frames, verbose=0)
        
        # Collect predictions and true labels
        y_pred_prob.extend(predictions.flatten().tolist())
        y_true.extend(labels.numpy().tolist())
        
        batch_count += 1
        # Stop after validation_steps to avoid infinite dataset
        if batch_count >= val_steps:
            break
    
    # Convert to numpy arrays and apply threshold
    y_true = np.array(y_true, dtype=int)
    y_pred = (np.array(y_pred_prob) > 0.5).astype(int)
    
    # Verify dataset composition
    print(f"\nValidation Set Composition:")
    print(f"  Total samples: {len(y_true)}")
    print(f"  Nonviolent (0): {(y_true == 0).sum()}")
    print(f"  Violent (1): {(y_true == 1).sum()}")
    
    val_accuracy = accuracy_score(y_true, y_pred)
    print(f"\nValidation Accuracy: {val_accuracy:.4f}")
    
    print("\nClassification Report:")
    print(classification_report(y_true, y_pred, target_names=["Nonviolent", "Violent"], 
                                zero_division=0))
    
    # Generate and save confusion matrix
    print("\n[5/5] Generating metrics...")
    cm = confusion_matrix(y_true, y_pred)
    
    plt.figure(figsize=(8, 6))
    sns.heatmap(cm, annot=True, fmt='d', cmap='Blues', 
                xticklabels=["Nonviolent", "Violent"],
                yticklabels=["Nonviolent", "Violent"])
    plt.title("Confusion Matrix - Validation Set")
    plt.ylabel("True Label")
    plt.xlabel("Predicted Label")
    plt.tight_layout()
    
    cm_path = "outputs/confusion_matrix.png"
    plt.savefig(cm_path, dpi=150, bbox_inches='tight')
    print(f"Confusion matrix saved to {cm_path}")
    plt.close()
    
    # Generate and save training curves
    print("Generating training curves...")
    fig, axes = plt.subplots(1, 2, figsize=(14, 5))
    
    # Accuracy curve
    axes[0].plot(history.history['accuracy'], label='Train Accuracy', marker='o')
    axes[0].plot(history.history['val_accuracy'], label='Validation Accuracy', marker='o')
    axes[0].set_xlabel('Epoch')
    axes[0].set_ylabel('Accuracy')
    axes[0].set_title('Model Accuracy')
    axes[0].legend()
    axes[0].grid(True, alpha=0.3)
    
    # Loss curve
    axes[1].plot(history.history['loss'], label='Train Loss', marker='o')
    axes[1].plot(history.history['val_loss'], label='Validation Loss', marker='o')
    axes[1].set_xlabel('Epoch')
    axes[1].set_ylabel('Loss')
    axes[1].set_title('Model Loss')
    axes[1].legend()
    axes[1].grid(True, alpha=0.3)
    
    plt.tight_layout()
    
    curves_path = "outputs/training_curves.png"
    plt.savefig(curves_path, dpi=150, bbox_inches='tight')
    print(f"Training curves saved to {curves_path}")
    plt.close()
    
    print("\n" + "=" * 60)
    print("Training Complete!")
    print("=" * 60)
    print(f"\nDataset Summary:")
    print(f"  Total videos: {class_counts['total']}")
    print(f"  - Nonviolent: {class_counts['nonviolent']}")
    print(f"  - Violent: {class_counts['violent']}")
    print(f"\n  Training videos: {class_counts['train']}")
    print(f"  - Nonviolent: {class_counts['train_nonviolent']}")
    print(f"  - Violent: {class_counts['train_violent']}")
    print(f"\n  Validation videos: {class_counts['val']}")
    print(f"  - Nonviolent: {class_counts['val_nonviolent']}")
    print(f"  - Violent: {class_counts['val_violent']}")
    print(f"\nTraining Summary:")
    print(f"  Epochs: {EPOCHS}")
    print(f"  Steps per epoch: {train_steps}")
    print(f"  Batch size: {BATCH_SIZE}")
    print(f"  Final validation accuracy: {val_accuracy:.4f}")
    print(f"\nModel saved to: {model_path}")
    print(f"Metrics saved to: outputs/")


if __name__ == "__main__":
    train_model()
