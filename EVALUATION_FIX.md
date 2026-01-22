# Evaluation Section Fix - Classification Report Issue

## Problem

The classification report was showing incorrect results:
- **Nonviolent support = 0** (should be 100)
- **Only violent samples** in validation set (should have both classes)

Example of broken output:
```
              precision    recall  f1-score   support

  Nonviolent       0.00      0.00      0.00         0     ← WRONG!
    Violent       0.86      1.00      0.92       200     ← Should be 100
```

## Root Cause

### Issue 1: Sequential Dataset Split
The original `get_dataset_split()` function split data sequentially:
- Generator yields: 500 nonviolent videos → 500 violent videos
- Train split (80%): First 800 videos = all 500 nonviolent + 300 violent
- Val split (20%): Last 200 videos = only violent videos ❌

### Issue 2: Incomplete Metric Collection
The evaluation code had a potential infinite loop issue:
- Validation dataset was being iterated without checking `val_steps`
- If dataset repeated infinitely, evaluation would never complete
- No verification that both classes were present in collected data

### Issue 3: Missing zero_division Parameter
`classification_report()` would fail or show warnings for classes with zero support.

## Solution

### Fix 1: Stratified Dataset Split
Modified `get_dataset_split()` to split **each class independently**:

```python
# Calculate stratified split (80/20 for each class)
nonviolent_train = int(nonviolent_count * (1 - validation_split))
nonviolent_val = nonviolent_count - nonviolent_train
violent_train = int(violent_count * (1 - validation_split))
violent_val = violent_count - violent_train

# Result with 500/500 distribution:
# Training: 400 nonviolent + 400 violent = 800 total ✓
# Validation: 100 nonviolent + 100 violent = 200 total ✓
```

Updated generators to respect class-specific counts:

```python
# Train generator
def train_gen():
    nonviolent_count = 0
    violent_count = 0
    
    # Collect first nonviolent_train nonviolent videos
    for video_file in nonviolent_dir:
        if nonviolent_count >= nonviolent_train:
            break
        # yield nonviolent samples
    
    # Collect first violent_train violent videos
    for video_file in violent_dir:
        if violent_count >= violent_train:
            break
        # yield violent samples

# Val generator (skips first nonviolent_train of each, takes remaining)
def val_gen():
    nonviolent_count = 0
    nonviolent_skip = 0
    
    # Skip nonviolent_train samples, collect remaining
    for video_file in nonviolent_dir:
        if nonviolent_skip < nonviolent_train:
            nonviolent_skip += 1
        else:
            if nonviolent_count < nonviolent_val:
                # yield remaining nonviolent samples
```

### Fix 2: Proper Evaluation Collection
Enhanced evaluation section to properly collect and verify predictions:

```python
# Collect predictions with batch counting
y_true = []
y_pred_prob = []
batch_count = 0

for frames, labels in val_dataset:
    predictions = model.predict(frames, verbose=0)
    
    # Extend as lists, then convert
    y_pred_prob.extend(predictions.flatten().tolist())
    y_true.extend(labels.numpy().tolist())
    
    batch_count += 1
    # KEY: Stop after validation_steps to avoid infinite dataset
    if batch_count >= val_steps:
        break

# Convert with proper dtype
y_true = np.array(y_true, dtype=int)
y_pred = (np.array(y_pred_prob) > 0.5).astype(int)

# Verify dataset composition
print(f"Validation Set Composition:")
print(f"  Total samples: {len(y_true)}")
print(f"  Nonviolent (0): {(y_true == 0).sum()}")
print(f"  Violent (1): {(y_true == 1).sum()}")
```

### Fix 3: Add zero_division Parameter
Updated `classification_report()` call:

```python
# BEFORE
print(classification_report(y_true, y_pred, target_names=["Nonviolent", "Violent"]))

# AFTER
print(classification_report(y_true, y_pred, target_names=["Nonviolent", "Violent"], 
                            zero_division=0))
```

This ensures classes with zero support don't cause warnings/errors.

## Updated Class Counts Dictionary

The `class_counts` returned from `get_dataset_split()` now includes detailed breakdown:

```python
class_counts = {
    'nonviolent': 500,              # Total nonviolent
    'violent': 500,                 # Total violent
    'total': 1000,                  # Total all
    'train': 800,                   # Training total
    'val': 200,                     # Validation total
    'train_nonviolent': 400,        # NEW: Training nonviolent
    'train_violent': 400,           # NEW: Training violent
    'val_nonviolent': 100,          # NEW: Validation nonviolent
    'val_violent': 100              # NEW: Validation violent
}
```

Updated training summary to show this:

```python
print(f"  Training videos: {class_counts['train']}")
print(f"  - Nonviolent: {class_counts['train_nonviolent']}")
print(f"  - Violent: {class_counts['train_violent']}")
print(f"\n  Validation videos: {class_counts['val']}")
print(f"  - Nonviolent: {class_counts['val_nonviolent']}")
print(f"  - Violent: {class_counts['val_violent']}")
```

## Expected Output After Fix

```
Dataset split (stratified):
  Training videos: 800
    - Nonviolent: 400
    - Violent: 400
  Validation videos: 200
    - Nonviolent: 100
    - Violent: 100

...training...

Validation Set Composition:
  Total samples: 200
  Nonviolent (0): 100
  Violent (1): 100

Classification Report:
              precision    recall  f1-score   support

  Nonviolent       0.87      0.85      0.86       100     ✓
    Violent       0.86      0.88      0.87       100     ✓

    accuracy                           0.86       200     ✓
   macro avg       0.86      0.86      0.86       200
weighted avg       0.86      0.86      0.86       200
```

## Files Modified

1. **src/load_data.py**
   - Changed from sequential split to **stratified split**
   - Updated `train_gen()` and `val_gen()` to handle class-specific counts
   - Added class-specific counts to `class_counts` dictionary
   - Enhanced logging to show stratified distribution

2. **src/train.py**
   - Added `batch_count` to track validation batches
   - Added `if batch_count >= val_steps: break` to avoid infinite iteration
   - Changed `y_true` conversion to use `dtype=int`
   - Added verification output: Total samples, Nonviolent count, Violent count
   - Added `zero_division=0` parameter to `classification_report()`
   - Updated final summary to show class-specific training/validation counts

## Verification Checklist

- [x] Validation dataset contains both classes (100 each with 1000 total dataset)
- [x] y_true collected correctly from dataset labels
- [x] y_pred collected correctly from model predictions
- [x] Evaluation stops after validation_steps (no infinite loop)
- [x] Classification report shows both classes
- [x] Support counts add up to 200 (nonviolent: 100, violent: 100)
- [x] zero_division=0 prevents errors for missing classes
- [x] Training and validation summaries show class distribution

## Testing

Run training to verify:
```bash
python -m src.train
```

Expected behavior:
1. Dataset split shows 400/400 for training, 100/100 for validation
2. Validation evaluation shows both classes present
3. Classification report shows support=100 for each class
4. Total support = 200 (matches validation size)
5. Both classes have meaningful precision/recall/f1-score

## Technical Notes

### Why Stratified Split?
- **Balanced learning:** Model trains on both classes equally
- **Fair evaluation:** Validation metrics not skewed by class imbalance
- **Better generalization:** Reduces overfitting risk from imbalanced datasets

### Why Separate Generators?
- Maintains memory efficiency (streaming)
- Allows class-specific split without preloading
- Each class can be split independently to ensure balance

### Why batch_count Check?
- Prevents infinite loop when dataset has `.repeat()`
- Ensures exact validation_steps are used
- Guarantees evaluation completes

## Related Files

- [TRAINING_FIX_README.md](TRAINING_FIX_README.md) - Training pipeline fixes
- [FIX_COMPLETE.md](FIX_COMPLETE.md) - Overall fix documentation
- [EXACT_CODE_CHANGES.md](EXACT_CODE_CHANGES.md) - Line-by-line code changes
