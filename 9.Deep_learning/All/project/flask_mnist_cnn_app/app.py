# 🌐 PART 2: Flask App with CNN Model
from flask import Flask, render_template, request, jsonify
import numpy as np
import base64
import cv2
import re
from tensorflow.keras.models import load_model

app = Flask(__name__)
model = load_model("mnist_cnn_model.h5")

@app.route("/")
def index():
    return render_template("index.html")

@app.route("/predict", methods=["POST"])
def predict():
    try:
        data_url = request.form["image"]
        encoded = re.sub('^data:image/.+;base64,', '', data_url)
        img_bytes = base64.b64decode(encoded)
        nparr = np.frombuffer(img_bytes, np.uint8)
        img = cv2.imdecode(nparr, cv2.IMREAD_UNCHANGED)  # RGBA

        # Preprocess
        img = cv2.cvtColor(img, cv2.COLOR_RGBA2GRAY)
        img = cv2.resize(img, (28, 28))
        img = cv2.bitwise_not(img)
        img = img.astype("float32") / 255.0
        img = img.reshape(1, 28, 28, 1)

        # Predict
        pred = model.predict(img)
        pred_class = int(np.argmax(pred))
        probs = pred[0].tolist()

        return jsonify({
            "prediction": pred_class,
            "probabilities": probs
        })
    except Exception as e:
        return jsonify({"error": str(e)})

if __name__ == "__main__":
    app.run(debug=True)
