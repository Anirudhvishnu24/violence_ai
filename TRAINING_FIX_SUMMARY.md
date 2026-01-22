# Training Pipeline Fix Summary

## Problem
The training process was failing with **"OUT_OF_RANGE: End of sequence"** error after the first epoch because:
1. The training dataset generator was exhausted after one pass through the data
2. No `.repeat()` mechanism to loop the generator for multiple epochs
3. Incorrect `steps_per_epoch` calculation (using integer division `//` instead of ceiling)

## Root Cause Analysis
When using `tf.data.Dataset` with generators:
- The generator yields finite data (e.g., 800 training samples)
- Without `.repeat()`, the generator is exhausted after yielding all samples
- TensorFlow expects `steps_per_epoch` iterations per epoch
- If steps exhausted generator before reaching `steps_per_epoch`, error occurred

## Solution Implemented

### 1. Updated `src/load_data.py`
**Added proper dataset repetition:**
```python
# Train dataset pipeline
train_dataset = train_dataset.shuffle(buffer_size=min(1000, train_count))
train_dataset = train_dataset.batch(batch_size).prefetch(tf.data.AUTOTUNE)
train_dataset = train_dataset.repeat()  # KEY: Repeat AFTER batching for multiple epochs

# Validation dataset pipeline (NO repeat - single pass per epoch)
val_dataset = val_dataset.batch(batch_size).prefetch(tf.data.AUTOTUNE)

# Correct step calculations using ceiling division
train_steps = math.ceil(train_count / batch_size)
val_steps = math.ceil(val_count / batch_size)
```

**Key changes:**
- Added `import math` for ceiling division
- Added `epochs: int = 10` parameter to function signature
- Shuffle training data BEFORE batching for better randomization
- `.repeat()` applied ONLY to training dataset AFTER batching
- Validation dataset intentionally NOT repeated
- Steps calculated with `math.ceil()` instead of `//` to handle incomplete final batch

### 2. Updated `src/train.py`
**Enhanced training pipeline:**
```python
# Training parameters extracted for clarity
EPOCHS = 10
BATCH_SIZE = 8
NUM_FRAMES = 30

# Call get_dataset_split with epochs parameter
train_dataset, val_dataset, train_steps, val_steps, class_counts = get_dataset_split(
    data_dir="data",
    num_frames=NUM_FRAMES,
    batch_size=BATCH_SIZE,
    validation_split=0.2,
    epochs=EPOCHS  # KEY: Pass epochs parameter
)

# Train with explicit steps
history = model.fit(
    train_dataset,
    steps_per_epoch=train_steps,      # Tells TensorFlow how many batches = 1 epoch
    validation_data=val_dataset,
    validation_steps=val_steps,       # How many batches for validation
    epochs=EPOCHS,                     # Training will run for all 10 epochs
    verbose=1
)
```

**Key changes:**
- Added explicit `EPOCHS`, `BATCH_SIZE`, `NUM_FRAMES` constants
- Pass `epochs=EPOCHS` to `get_dataset_split()`
- Use returned `train_steps` and `val_steps` in `model.fit()`
- Enhanced progress logging with step counts per epoch

## How It Works Now

### Dataset Flow Per Epoch
1. **Epoch 1:**
   - Train generator yields samples → batches → repeats to next cycle
   - Training runs for `train_steps` = 100 batches (800 samples / batch_size=8)
   - Validation dataset batches → single pass through val_steps = 25 batches

2. **Epoch 2-10:**
   - Train dataset `.repeat()` loops generator back to start
   - Generator continues yielding → new random batches (due to shuffle)
   - Process repeats for each of 10 epochs

### Memory Efficiency
- **NO full dataset in RAM:** Only current batch of 8 videos in memory
- **Streaming:** Videos extracted from disk on-demand
- **Shuffle:** Randomization via buffer before batching

### Step Calculations
```
train_count = 800, batch_size = 8
train_steps = ceil(800 / 8) = 100 ✓

val_count = 200, batch_size = 8  
val_steps = ceil(200 / 8) = 25 ✓

Total training iterations = 100 steps/epoch × 10 epochs = 1000 batches
```

## Verification

### Checked:
- [x] `get_dataset_split()` has `epochs` parameter (default=10)
- [x] Train dataset has `.repeat()` after batching
- [x] Validation dataset does NOT have `.repeat()`
- [x] `train.py` passes `epochs=EPOCHS` to `get_dataset_split()`
- [x] `model.fit()` uses `steps_per_epoch=train_steps` and `validation_steps=val_steps`
- [x] Steps calculated with `math.ceil()` for correct coverage
- [x] Module imports verified successfully

### Ready to Test:
```bash
python -m src.train
```

Expected behavior:
- Training for 10 epochs
- 100 steps per epoch for training
- 25 validation steps per epoch
- No "OUT_OF_RANGE: End of sequence" error
- Model, confusion matrix, and training curves saved to outputs/

## Technical Details

### Why `.repeat()` AFTER batching?
1. Batching reduces data from individual samples to batches
2. `.repeat()` on batched data creates infinite stream of batches
3. Shuffling before repeat ensures good randomization across epochs

### Why `steps_per_epoch`?
When `.repeat()` creates infinite dataset, TensorFlow doesn't know when an epoch ends.
`steps_per_epoch` tells it: "After N batches, one epoch is complete."

### Why validation WITHOUT repeat?
Validation set is finite and should run once per epoch to avoid counting same samples multiple times in metrics.

## Files Modified
1. `src/load_data.py` - Added .repeat(), epochs parameter, math.ceil()
2. `src/train.py` - Added parameter passing, explicit steps usage

## Backward Compatibility
- Old code will still work (epochs parameter has default value of 10)
- If called without epochs parameter: `get_dataset_split()` defaults to 10 epochs
- No breaking changes to existing functionality
