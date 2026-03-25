def build_retinal_model(input_shape=(224, 224, 3), num_classes=6):

    # ✅ Lazy import (deployment safe)
    import tensorflow as tf
    from tensorflow.keras.applications import MobileNetV2
    from tensorflow.keras.models import Model
    from tensorflow.keras.layers import Dense, GlobalAveragePooling2D, Dropout
    from tensorflow.keras.optimizers import Adam

    # ---------- BASE MODEL ----------
    base_model = MobileNetV2(
        weights='imagenet',
        include_top=False,
        input_shape=input_shape
    )

    # ---------- FREEZE / UNFREEZE ----------
    for layer in base_model.layers[:-30]:
        layer.trainable = False

    for layer in base_model.layers[-30:]:
        layer.trainable = True

    # ---------- CUSTOM HEAD ----------
    x = base_model.output
    x = GlobalAveragePooling2D()(x)

    x = Dense(128, activation='relu')(x)
    x = Dropout(0.5)(x)

    output = Dense(num_classes, activation='softmax')(x)

    # ---------- FINAL MODEL ----------
    model = Model(inputs=base_model.input, outputs=output, name="Retinal_Disease_Model")

    # ---------- COMPILE ----------
    model.compile(
        optimizer=Adam(learning_rate=0.00001),
        loss='categorical_crossentropy',
        metrics=['accuracy']
    )

    return model