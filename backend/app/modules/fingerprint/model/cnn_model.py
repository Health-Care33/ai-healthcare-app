def build_fingerprint_model(input_shape=(128, 128, 1), num_classes=8):

    # ✅ Lazy import (important for deployment environments)
    import tensorflow as tf
    from tensorflow.keras import layers, models

    model = models.Sequential(name="Fingerprint_BloodGroup_Model")

    # ---------- BLOCK 1 ----------
    model.add(layers.Conv2D(32, (3, 3), activation='relu', input_shape=input_shape))
    model.add(layers.MaxPooling2D((2, 2)))
    model.add(layers.BatchNormalization())

    # ---------- BLOCK 2 ----------
    model.add(layers.Conv2D(64, (3, 3), activation='relu'))
    model.add(layers.MaxPooling2D((2, 2)))
    model.add(layers.BatchNormalization())

    # ---------- BLOCK 3 ----------
    model.add(layers.Conv2D(128, (3, 3), activation='relu'))
    model.add(layers.MaxPooling2D((2, 2)))

    # ---------- BLOCK 4 ----------
    model.add(layers.Conv2D(256, (3, 3), activation='relu'))
    model.add(layers.MaxPooling2D((2, 2)))

    # ---------- CLASSIFIER ----------
    model.add(layers.Flatten())

    model.add(layers.Dense(256, activation='relu'))
    model.add(layers.Dropout(0.5))

    model.add(layers.Dense(num_classes, activation='softmax'))

    # ---------- COMPILE ----------
    model.compile(
        optimizer=tf.keras.optimizers.Adam(),
        loss='categorical_crossentropy',
        metrics=['accuracy']
    )

    return model