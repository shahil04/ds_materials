import tensorflow as tf
from tensorflow.keras.applications import ResNet50
from tensorflow.keras.layers import Dense, Flatten
from tensorflow.keras.models import Model
from tensorflow.keras.preprocessing.image import ImageDataGenerator

# Load pre-trained ResNet50
base_model = ResNet50(weights="imagenet", include_top=False, input_shape=(224, 224, 3))

# Freeze all layers in the base model
for layer in base_model.layers:
    layer.trainable = False

# Add custom classification head
x = Flatten()(base_model.output)
x = Dense(256, activation='relu')(x)
output = Dense(5, activation="softmax")(x)

model = Model(inputs=base_model.input, outputs=output)

#Compile the model
model.compile(optimizer='adam', loss="categorical_crossentropy", metrics=['accuracy'])

model.summary()

# Data Preparation
datagen = ImageDataGenerator(rescale=1./255, validation_split=0.2)

train_data = datagen.flow_from_directory(
    "PATH_TO_DATASET",
    target_size=(224, 224),
    batch_size=32,
    class_node="categorical",
    subset="training"
)

val_data = datagen.flow_from_directory(
    "PATH_TO_DATASET",
    target_size=(224, 224),
    batch_size=32,
    class_node="categorical",
    subset="validation"
)

# Train the model
history = model.fit(
    train_data,
    validation_data=val_data,
    epochs=10,
    steps_per_epoch=len(train_data),
    validation_steps=len(val_data)
)

for layer in base_model.layers[-5:]:
    layer.trainable = True
    
model.compile(optimizer=tf.keras.optimizers.Adam(learning_rate=1e-5), loss="categorical_crossentropy", metrics=["accuracy"])

val_loss, val_accuracy = model.evaluate(val_data)


