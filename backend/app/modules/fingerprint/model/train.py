import os
import json
import numpy as np
import tensorflow as tf

from tensorflow.keras.preprocessing.image import ImageDataGenerator
from tensorflow.keras.callbacks import EarlyStopping, ReduceLROnPlateau
from sklearn.utils.class_weight import compute_class_weight

from cnn_model import build_fingerprint_model

# Dataset path
DATASET_PATH = "../dataset"

# Image parameters
IMG_SIZE = 128
BATCH_SIZE = 32
EPOCHS = 40

# Data augmentation (improved)
train_datagen = ImageDataGenerator(
    rescale=1./255,
    validation_split=0.2,
    rotation_range=20,
    zoom_range=0.2,
    width_shift_range=0.1,
    height_shift_range=0.1,
    shear_range=0.1,
    horizontal_flip=True
)

# Training data
train_generator = train_datagen.flow_from_directory(
    DATASET_PATH,
    target_size=(IMG_SIZE, IMG_SIZE),
    color_mode="grayscale",
    batch_size=BATCH_SIZE,
    class_mode="categorical",
    subset="training"
)

# Validation data
val_generator = train_datagen.flow_from_directory(
    DATASET_PATH,
    target_size=(IMG_SIZE, IMG_SIZE),
    color_mode="grayscale",
    batch_size=BATCH_SIZE,
    class_mode="categorical",
    subset="validation"
)

print("Classes:", train_generator.class_indices)

# Save class mapping
with open("class_indices.json", "w") as f:
    json.dump(train_generator.class_indices, f)

# Compute class weights (IMPORTANT)
labels = train_generator.classes

class_weights = compute_class_weight(
    class_weight="balanced",
    classes=np.unique(labels),
    y=labels
)

class_weights = dict(enumerate(class_weights))

print("Class Weights:", class_weights)

# Build model
model = build_fingerprint_model()

model.summary()

# Callbacks
early_stop = EarlyStopping(patience=6, restore_best_weights=True)

reduce_lr = ReduceLROnPlateau(
    monitor="val_loss",
    factor=0.3,
    patience=3,
    min_lr=0.000001
)

# Train model
history = model.fit(
    train_generator,
    validation_data=val_generator,
    epochs=EPOCHS,
    callbacks=[early_stop, reduce_lr],
    class_weight=class_weights
)

# Save model
MODEL_PATH = "fingerprint_bloodgroup_model.h5"
model.save(MODEL_PATH)

print("Model saved at:", MODEL_PATH)