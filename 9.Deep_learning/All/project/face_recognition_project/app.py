# face_recognition_project

# ----------------------
# collect_faces.py
# ----------------------
import cv2
import os

face_cascade = cv2.CascadeClassifier(cv2.data.haarcascades + 'haarcascade_frontalface_default.xml')
person_name = input("Enter person name: ")
data_path = f"dataset/{person_name}"
os.makedirs(data_path, exist_ok=True)

cap = cv2.VideoCapture(0)
count = 0
while True:
    ret, frame = cap.read()
    if not ret:
        break
    gray = cv2.cvtColor(frame, cv2.COLOR_BGR2GRAY)
    faces = face_cascade.detectMultiScale(gray, 1.3, 5)
    for (x, y, w, h) in faces:
        face = frame[y:y+h, x:x+w]
        face = cv2.resize(face, (100, 100))
        cv2.imwrite(f"{data_path}/{count}.jpg", face)
        count += 1
        cv2.rectangle(frame, (x, y), (x+w, y+h), (255, 0, 0), 2)
    cv2.imshow('Collecting Faces', frame)
    if cv2.waitKey(1) == 27 or count >= 100:
        break
cap.release()
cv2.destroyAllWindows()

# ----------------------
# preprocess_and_train.py
# ----------------------
import os
import cv2
import numpy as np
import pickle
from sklearn.model_selection import train_test_split
from tensorflow.keras.models import Sequential
from tensorflow.keras.layers import Conv2D, MaxPooling2D, Flatten, Dense

# Load images and labels
data = []
labels = []
label_map = {}
label_id = 0

for person in os.listdir('dataset'):
    person_path = os.path.join('dataset', person)
    if os.path.isdir(person_path):
        label_map[label_id] = person
        for img_name in os.listdir(person_path):
            img_path = os.path.join(person_path, img_name)
            img = cv2.imread(img_path)
            img = cv2.resize(img, (100, 100))
            data.append(img)
            labels.append(label_id)
        label_id += 1

# Save label map
with open("label_map.pkl", "wb") as f:
    pickle.dump(label_map, f)

data = np.array(data) / 255.0
labels = np.array(labels)
X_train, X_test, y_train, y_test = train_test_split(data, labels, test_size=0.2, stratify=labels)

# Build CNN model
model = Sequential([
    Conv2D(32, (3,3), activation='relu', input_shape=(100, 100, 3)),
    MaxPooling2D(2, 2),
    Conv2D(64, (3,3), activation='relu'),
    MaxPooling2D(2,2),
    Flatten(),
    Dense(128, activation='relu'),
    Dense(len(label_map), activation='softmax')
])

model.compile(optimizer='adam', loss='sparse_categorical_crossentropy', metrics=['accuracy'])
model.fit(X_train, y_train, validation_data=(X_test, y_test), epochs=10)
model.save("face_recognition_model.h5")

# ----------------------
# realtime_recognition.py
# ----------------------
import cv2
import numpy as np
import pickle
from tensorflow.keras.models import load_model

model = load_model("face_recognition_model.h5")
with open("label_map.pkl", "rb") as f:
    label_map = pickle.load(f)

face_cascade = cv2.CascadeClassifier(cv2.data.haarcascades + 'haarcascade_frontalface_default.xml')
cap = cv2.VideoCapture(0)

while True:
    ret, frame = cap.read()
    if not ret:
        break
    gray = cv2.cvtColor(frame, cv2.COLOR_BGR2GRAY)
    faces = face_cascade.detectMultiScale(gray, 1.3, 5)
    for (x, y, w, h) in faces:
        face = frame[y:y+h, x:x+w]
        face = cv2.resize(face, (100, 100)) / 255.0
        face = np.expand_dims(face, axis=0)
        pred = model.predict(face)
        label = label_map[np.argmax(pred)]
        confidence = np.max(pred)
        cv2.putText(frame, f"{label} ({confidence:.2f})", (x, y-10), cv2.FONT_HERSHEY_SIMPLEX, 0.9, (0,255,0), 2)
        cv2.rectangle(frame, (x, y), (x+w, y+h), (0,255,0), 2)
    cv2.imshow("Real-time Face Recognition", frame)
    if cv2.waitKey(1) == 27:
        break
cap.release()
cv2.destroyAllWindows()

# ----------------------
# app.py (Streamlit app)
# ----------------------
import streamlit as st
import cv2
import numpy as np
import pickle
from tensorflow.keras.models import load_model
from PIL import Image

model = load_model("face_recognition_model.h5")
with open("label_map.pkl", "rb") as f:
    label_map = pickle.load(f)

face_cascade = cv2.CascadeClassifier(cv2.data.haarcascades + 'haarcascade_frontalface_default.xml')

st.title("Face Recognition App")
mode = st.radio("Choose Mode", ["Webcam", "Upload Image"])

def predict_face(img):
    face = cv2.resize(img, (100, 100)) / 255.0
    face = np.expand_dims(face, axis=0)
    pred = model.predict(face)
    return label_map[np.argmax(pred)], np.max(pred)

if mode == "Upload Image":
    uploaded_file = st.file_uploader("Upload an image")
    if uploaded_file is not None:
        img = Image.open(uploaded_file)
        img_np = np.array(img.convert("RGB"))
        gray = cv2.cvtColor(img_np, cv2.COLOR_RGB2GRAY)
        faces = face_cascade.detectMultiScale(gray, 1.3, 5)
        for (x, y, w, h) in faces:
            face_img = img_np[y:y+h, x:x+w]
            label, conf = predict_face(face_img)
            cv2.rectangle(img_np, (x, y), (x+w, y+h), (0,255,0), 2)
            cv2.putText(img_np, f"{label} ({conf:.2f})", (x, y-10), cv2.FONT_HERSHEY_SIMPLEX, 0.8, (255,0,0), 2)
        st.image(img_np, caption="Predicted Image")

elif mode == "Webcam":
    st.warning("To use webcam, run this app locally with: streamlit run app.py")

# ----------------------
# requirements.txt
# ----------------------
opencv-python
numpy
tensorflow
streamlit
scikit-learn
pillow

# ----------------------
# README.md
# ----------------------
# Face Recognition Project

## Features:
- Face detection using Haar Cascade
- Face classification using CNN
- Real-time recognition
- Streamlit UI with webcam and image upload

## Usage
1. Run `collect_faces.py` to collect images for each person.
2. Run `preprocess_and_train.py` to train the CNN.
3. Use `realtime_recognition.py` or `streamlit run app.py` for live recognition.
