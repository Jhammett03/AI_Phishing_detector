import re
import pickle
import nltk
import pandas as pd
import numpy as np
from bs4 import BeautifulSoup
from flask import Flask, request, jsonify
from flask_cors import CORS  # Import Flask-CORS
from nltk.corpus import stopwords
from sklearn.feature_extraction.text import TfidfVectorizer
from sklearn.model_selection import train_test_split
from sklearn.linear_model import LogisticRegression
from sklearn.metrics import accuracy_score

# Download NLTK stopwords
nltk.download('stopwords')

# Load dataset (Replace this with actual phishing email dataset)
def load_data():
    try:
        # Load phishing dataset from CSV
        df = pd.read_csv("phishing_email.csv")  # Ensure this file exists

        # Print column names to confirm
        print("Columns in dataset:", df.columns)

        # Rename 'text_combined' to 'email_text' if needed
        if "text_combined" in df.columns:
            df.rename(columns={"text_combined": "email_text"}, inplace=True)

        # Ensure dataset has required columns
        if "email_text" not in df.columns or "label" not in df.columns:
            raise ValueError("Dataset must contain 'email_text' and 'label' columns")

        # Sample equal phishing and normal emails for balance
        phishing_samples = df[df["label"] == 1].sample(min(3000, len(df[df["label"] == 1])), random_state=42)
        normal_samples = df[df["label"] == 0].sample(min(3000, len(df[df["label"] == 0])), random_state=42)

        # Combine and shuffle dataset
        df = pd.concat([phishing_samples, normal_samples]).sample(frac=1, random_state=42).reset_index(drop=True)

        print(f"Dataset loaded: {df.shape[0]} emails")
        return df

    except Exception as e:
        print("Error loading dataset:", e)
        exit()

# Preprocessing: Clean email text
def clean_email_text(text):
    text = BeautifulSoup(text, "html.parser").get_text()  # Remove HTML tags
    text = re.sub(r"http\S+", "", text)  # Remove URLs
    text = re.sub(r"[^a-zA-Z]", " ", text)  # Keep only letters
    text = text.lower().split()
    text = [word for word in text if word not in stopwords.words("english")]
    return " ".join(text)

# Load and preprocess data
df = load_data()
df["cleaned_text"] = df["email_text"].apply(clean_email_text)

# Print dataset sample for debugging
print("Dataset Sample:")
print(df.head())

# Feature extraction (TF-IDF)
vectorizer = TfidfVectorizer(max_features=10000)  # Increased features
X = vectorizer.fit_transform(df["cleaned_text"])
y = np.array(df["label"])

# Print feature matrix size for debugging
print(f"Feature Matrix Size: {X.shape}")

# Split into training and testing sets
X_train, X_test, y_train, y_test = train_test_split(X, y, test_size=0.2, random_state=42)

# Train a Logistic Regression model (better than Naïve Bayes)
model = LogisticRegression()
model.fit(X_train, y_train)

# Evaluate accuracy
predictions = model.predict(X_test)
print(f"Model Accuracy: {accuracy_score(y_test, predictions):.2f}")

# Save model and vectorizer
with open("phishing_model.pkl", "wb") as model_file:
    pickle.dump(model, model_file)
with open("vectorizer.pkl", "wb") as vec_file:
    pickle.dump(vectorizer, vec_file)

# Flask API for real-time email classification
app = Flask(__name__)
CORS(app)  # Enable CORS for all routes

@app.route('/')
def home():
    return "Phishing Email Detector API is running. Use /predict for detection."

@app.route('/predict', methods=['POST'])
def predict():
    try:
        data = request.json.get("email_text", "")
        if not data:
            return jsonify({"error": "No email text provided"}), 400

        # Load model and vectorizer only once (better performance)
        features = vectorizer.transform([clean_email_text(data)])
        prediction = model.predict(features)[0]
        return jsonify({"is_phishing": bool(prediction)})

    except Exception as e:
        return jsonify({"error": str(e)}), 500

if __name__ == '__main__':
    app.run(host="0.0.0.0", port=5000, debug=False)
