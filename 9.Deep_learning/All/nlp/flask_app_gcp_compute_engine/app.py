from flask import Flask, render_template, request
import pickle
import os
import pandas as pd
from cleaning import *
import warnings
warnings.simplefilter("ignore", UserWarning)
warnings.filterwarnings("ignore")

# Initialize Flask app
app = Flask(__name__)
# open the file
with open("vectorizer.pkl","rb") as f:
    vectorizer = pickle.load(f)

with open("model.pkl","rb") as f:
    model = pickle.load(f)
 

# Routes
@app.route("/")
def home(): 
    response = render_template("index.html", result=None)
    return response

@app.route("/predict", methods=["POST"])
def predict():
    text = request.form["text"]
    # Clean text
    df1 = pd.DataFrame({'review': [text]})

    df11 = normalize_text(df1)  # Apply your preprocessing pipeline
# Convert to features
    # Transform using the same vectorizer
    X_input = vectorizer.transform(df1['review'])
    # Predict
    result = model.predict(X_input)
    prediction = result[0]
    return render_template("index.html", result=prediction)

if __name__ == "__main__":
    # app.run(debug=True) # for local use
    app.run(debug=True, host="0.0.0.0", port=5000)  # Accessible from outside Docker

# flask 
# nltk
# scikit-learn
# pandas
