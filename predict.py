import pickle
import re
from bs4 import BeautifulSoup
from nltk.corpus import stopwords
import nltk
from flask import Flask, request, jsonify
from flask_cors import CORS

# Download NLTK stopwords if not available
nltk.download('stopwords')

# Load the trained model and vectorizer
with open("phishing_model.pkl", "rb") as model_file:
    model = pickle.load(model_file)

with open("vectorizer.pkl", "rb") as vec_file:
    vectorizer = pickle.load(vec_file)

# Preprocessing function
def clean_email_text(text):
    text = BeautifulSoup(text, "html.parser").get_text()
    text = re.sub(r"http\S+", "", text)
    text = re.sub(r"[^a-zA-Z]", " ", text)
    text = text.lower().split()
    text = [word for word in text if word not in stopwords.words("english")]
    return " ".join(text)

# Flask API
app = Flask(__name__)
CORS(app)

@app.route('/')
def home():
    return "Phishing Email Detector API is running. Use /predict for detection."

@app.route('/predict', methods=['POST'])
def predict():
    try:
        data = request.json.get("email_text", "")
        if not data:
            return jsonify({"error": "No email text provided"}), 400

        # Transform the input text using the saved vectorizer
        features = vectorizer.transform([clean_email_text(data)])
        prediction = model.predict(features)[0]

        return jsonify({"is_phishing": bool(prediction)})

    except Exception as e:
        return jsonify({"error": str(e)}), 500

if __name__ == '__main__':
    app.run(host="0.0.0.0", port=5000, debug=False)
