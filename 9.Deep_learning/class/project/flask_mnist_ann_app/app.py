from flask import Flask, render_template, request, jsonify
import numpy as np
import cv2
import base64
import re
from tensorflow.keras.models import load_model
import matplotlib.pyplot as plt
import io
import os

app = Flask(__name__)
model = load_model("mnist_ann_model.h5")

@app.route("/")
def index():
    return render_template("index.html")

@app.route("/predict", methods=["POST"])
def predict():
    try:
        # Get base64 image data
        data_url = request.form["image"]
        encoded_data = re.sub('^data:image/.+;base64,', '', data_url)
        img_bytes = base64.b64decode(encoded_data)

        # Convert to NumPy array
        nparr = np.frombuffer(img_bytes, np.uint8)
        img = cv2.imdecode(nparr, cv2.IMREAD_UNCHANGED)  # RGBA

        # Preprocess
        img = cv2.cvtColor(img, cv2.COLOR_RGBA2GRAY)
        _, img = cv2.threshold(img, 100, 255, cv2.THRESH_BINARY)
        img = cv2.resize(img, (28, 28))

        # Center using bounding box
        contours, _ = cv2.findContours(img, cv2.RETR_EXTERNAL, cv2.CHAIN_APPROX_SIMPLE)
        if contours:
            x, y, w, h = cv2.boundingRect(contours[0])
            digit = img[y:y+h, x:x+w]
            padded = cv2.copyMakeBorder(digit, 10, 10, 10, 10, cv2.BORDER_CONSTANT, value=0)
            img = cv2.resize(padded, (28, 28))

        # Normalize
        img = img.astype("float32") / 255.0
        img_flat = img.reshape(1, 784)

        # Predict
        pred = model.predict(img_flat)
        pred_class = int(np.argmax(pred))
        pred_probs = pred[0].tolist()

        return jsonify({
            "prediction": pred_class,
            "probabilities": pred_probs
        })

    except Exception as e:
        return jsonify({"error": str(e)})

if __name__ == "__main__":
    app.run(debug=True)
