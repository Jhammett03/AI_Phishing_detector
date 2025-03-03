import re
import pickle
import nltk
import pandas as pd
import numpy as np
from bs4 import BeautifulSoup
from nltk.corpus import stopwords
from sklearn.feature_extraction.text import TfidfVectorizer
from sklearn.model_selection import train_test_split
from sklearn.linear_model import LogisticRegression
from sklearn.metrics import accuracy_score

# Download NLTK stopwords if not already downloaded
nltk.download('stopwords')

# Load dataset
def load_data():
    try:
        df = pd.read_csv("phishing_email.csv")

        # Rename 'text_combined' to 'email_text' if needed
        if "text_combined" in df.columns:
            df.rename(columns={"text_combined": "email_text"}, inplace=True)

        if "email_text" not in df.columns or "label" not in df.columns:
            raise ValueError("Dataset must contain 'email_text' and 'label' columns")

        # Sample balanced dataset
        phishing_samples = df[df["label"] == 1].sample(min(3000, len(df[df["label"] == 1])), random_state=42)
        normal_samples = df[df["label"] == 0].sample(min(3000, len(df[df["label"] == 0])), random_state=42)

        df = pd.concat([phishing_samples, normal_samples]).sample(frac=1, random_state=42).reset_index(drop=True)
        print(f"Dataset loaded: {df.shape[0]} emails")
        return df
    except Exception as e:
        print("Error loading dataset:", e)
        exit()

# Preprocessing function
def clean_email_text(text):
    text = BeautifulSoup(text, "html.parser").get_text()
    text = re.sub(r"http\S+", "", text)
    text = re.sub(r"[^a-zA-Z]", " ", text)
    text = text.lower().split()
    text = [word for word in text if word not in stopwords.words("english")]
    return " ".join(text)

# Load and preprocess data
df = load_data()
df["cleaned_text"] = df["email_text"].apply(clean_email_text)

# Feature extraction
vectorizer = TfidfVectorizer(max_features=10000)
X = vectorizer.fit_transform(df["cleaned_text"])
y = np.array(df["label"])

# Split dataset
X_train, X_test, y_train, y_test = train_test_split(X, y, test_size=0.2, random_state=42)

# Train model
model = LogisticRegression()
model.fit(X_train, y_train)

# Evaluate model
predictions = model.predict(X_test)
accuracy = accuracy_score(y_test, predictions)
print(f"Model Accuracy: {accuracy:.2f}")

# Save model and vectorizer
with open("phishing_model.pkl", "wb") as model_file:
    pickle.dump(model, model_file)

with open("vectorizer.pkl", "wb") as vec_file:
    pickle.dump(vectorizer, vec_file)

print("Training complete. Model and vectorizer saved.")
