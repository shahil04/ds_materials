#  complete end-to-end implementation of a CNN-based MNIST Digit Recognizer, including:

# ✅ 1. Model Creation: Load → Train → Save
# ✅ 2. Flask App: Draw → Predict → Display Result
# Let’s break it into two parts:
# 🧠 PART 1: Create & Train CNN Model on MNIST
# cnn_mnist_train.py
import numpy as np
from tensorflow.keras.datasets import mnist
from tensorflow.keras.models import Sequential
from tensorflow.keras.layers import Conv2D, MaxPooling2D, Flatten, Dense, Dropout
from tensorflow.keras.utils import to_categorical

# Load data
(x_train, y_train), (x_test, y_test) = mnist.load_data()

# Reshape for CNN input (28, 28, 1)
x_train = x_train.reshape(-1, 28, 28, 1).astype("float32") / 255.0
x_test = x_test.reshape(-1, 28, 28, 1).astype("float32") / 255.0

# One-hot encode labels
y_train_cat = to_categorical(y_train, 10)
y_test_cat = to_categorical(y_test, 10)

# Build CNN
model = Sequential([
    Conv2D(32, kernel_size=(3,3), activation='relu', input_shape=(28,28,1)),
    MaxPooling2D(pool_size=(2,2)),
    Conv2D(64, kernel_size=(3,3), activation='relu'),
    MaxPooling2D(pool_size=(2,2)),
    Flatten(),
    Dense(128, activation='relu'),
    Dropout(0.25),
    Dense(10, activation='softmax')
])

model.compile(optimizer='adam', loss='categorical_crossentropy', metrics=['accuracy'])
model.summary()

# Train
model.fit(x_train, y_train_cat, batch_size=128, epochs=5, verbose=1, validation_split=0.1)

# Evaluate
loss, acc = model.evaluate(x_test, y_test_cat, verbose=0)
print(f"Test Accuracy: {acc:.4f}")

# Save model
model.save("mnist_cnn_model.h5")
