"""
Build ResNet50 + LSTM model for violence detection.
"""

from tensorflow import keras
from tensorflow.keras import layers
from tensorflow.keras.applications import ResNet50


def build_model(num_frames: int = 30) -> keras.Model:
    """
    Build ResNet50 + LSTM model for binary video classification.
    
    Args:
        num_frames: Number of frames per video (default 30)
    
    Returns:
        Compiled keras model ready for training
    """
    
    # Input: (batch_size, num_frames, 224, 224, 3)
    inputs = layers.Input(shape=(num_frames, 224, 224, 3), dtype='float32')
    
    # Load pretrained ResNet50 without top classification layer
    resnet = ResNet50(weights='imagenet', include_top=False, input_shape=(224, 224, 3))
    
    # Freeze ResNet50 weights initially (can be unfrozen for fine-tuning)
    resnet.trainable = False
    
    # TimeDistributed wrapper to apply ResNet50 to each frame independently
    # Output shape: (batch_size, num_frames, 7, 7, 2048)
    x = layers.TimeDistributed(resnet)(inputs)
    
    # Global Average Pooling on spatial dimensions for each frame
    # Output shape: (batch_size, num_frames, 2048)
    x = layers.TimeDistributed(layers.GlobalAveragePooling2D())(x)
    
    # LSTM layer to capture temporal dependencies
    # Output shape: (batch_size, 128)
    x = layers.LSTM(128, return_sequences=False)(x)
    
    # Dense layers
    x = layers.Dense(64, activation='relu')(x)
    x = layers.Dropout(0.5)(x)
    x = layers.Dense(32, activation='relu')(x)
    x = layers.Dropout(0.3)(x)
    
    # Output layer with sigmoid for binary classification
    outputs = layers.Dense(1, activation='sigmoid')(x)
    
    # Create model
    model = keras.Model(inputs=inputs, outputs=outputs)
    
    # Compile model
    model.compile(
        optimizer=keras.optimizers.Adam(learning_rate=0.001),
        loss='binary_crossentropy',
        metrics=['accuracy', keras.metrics.Precision(), keras.metrics.Recall()]
    )
    
    return model
