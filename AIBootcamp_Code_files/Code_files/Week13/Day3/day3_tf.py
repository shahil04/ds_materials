import tensorflow as tf
from tensorflow.keras.applications import MobileNetV2
from tensorflow.keras.layers import Dense, GlobalAveragePooling2D
from tensorflow.keras.models import Model
from tensorflow.keras.preprocessing.image import ImageDatagenerator

# Load pretrained MobileNetV2
base_model = MobileNetV2(weights="imagenet", include_top=False, input_shape=(224, 224, 3))

# Freeze all layers
for layer in base_model.layers:
    layer.trainable = False

# Add Classification head
x = GlobalAveragePooling2D()(base_model.output)
output = Dense(5, activation="softmax")(x)
model = Model(inputs=base_model.input, outputs=output)

# Define data augmentation
datagen = ImageDatagenerator(
    rescale=1./255,
    rotation_range=20,
    width_shape_range=0.2,
    height_shift_range=0.2,
    shear_range=0.2,
    zoom_range=0.2,
    horizontal_flip=True,
    validation_split=0.2
)

train_data = datagen.flow_from_directory(
    "PATH_TO_DATASET",
    target_size=(224, 224),
    batch_size=32,
    class_mode="categorical",
    subset="training"
)

val_data = datagen.flow_from_directory(
    "PATH_TO_DATASET",
    target_size=(224, 224),
    batch_size=32,
    class_mode="categorical",
    subset="validation"
)

# Compile the model
model.compile(optimizer=tf.keras.optimizers.Adam(lerarning_rate=1e-5), loss="categorical_crossentropy", metrics=["accuracy"])

# Train the model
history = model.fit(
    train_data, validation_data= val_data, epochs=10, steps_per_epoch=len(train_data),
    validation_steps=len(val_data)
)

