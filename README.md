# 🐟 AI Phishing Email Detector
🚀 **A Chrome extension that detects phishing emails using AI and warns users directly in Gmail.**  

---

## 📌 Overview
The **AI Phishing Email Detector** is a **Chrome/Edge extension** that **automatically analyzes emails** in Gmail and detects potential phishing attempts using **machine learning**.  

💡 **Why?** Phishing scams are becoming more sophisticated. This tool helps users avoid malicious emails by highlighting suspicious content **before clicking on links**.

🔹Note: I am currently working on getting the extension released on the Chrome/Edge webstores, but for now only local instances of the program are supported.


---

## ✨ Features
✅ **Real-time Email Analysis**: Automatically scans opened Gmail emails.  
✅ **AI-Powered Detection**: Uses **Natural Language Processing (NLP)** to classify emails as phishing or safe.  
✅ **Warning Banners**: Adds **alert messages** inside Gmail for suspicious emails.  
✅ **Keyword Highlighting**: Flags phishing-related words like `"click here"`, `"urgent"`, `"bank details"`, etc.  
✅ **"Check Page" Button**: Allows users to manually check an email without pasting content.  
✅ **Privacy Focused**: No data is stored—everything is analyzed locally on your machine.  

---

## 🛠 Tech Stack
🔹 **Frontend**: Chrome/Edge Extension (JavaScript, HTML, CSS)  
🔹 **Backend**: Flask (Python)  
🔹 **Machine Learning**: Logistic Regression (Scikit-learn, NLTK, TF-IDF)  
🔹 **Data Storage**: Pickle (for model persistence)  
🔹 **Deployment**: Render.com (for Flask backend)  

---
### 📊 Training Data  
We use a dataset containing phishing and non-phishing emails from [Kaggle Phishing Email Dataset](https://www.kaggle.com/datasets/naserabdullahalam/phishing-email-dataset?resource=download&select=phishing_email.csv)
specifically from phishing_email.csv.  
- **Data Preprocessing:** Emails are cleaned, stopwords removed, and text converted to TF-IDF features.  
- **Train/Test Split:**  
  - **80% (4,800 emails)** → Training data  
  - **20% (1,200 emails)** → Test data  
  - Balanced dataset: 3,000 phishing emails + 3,000 normal emails

  #### See model_card.md for more information about the dataset and how it is manipulated.

--- 

### Model Persistence
Once trained, the model is stored in `phishing_model.pkl` and the vectorizer in `vectorizer.pkl`.  
- **You do not need to retrain each time you use the API**  
- If you want to update the model with new data, re-run `train.py`

---

## 📥 Installation
To run the AI Phishing Detector **locally**, follow these steps:

### 1️⃣ Clone the Repository
```sh
git clone https://github.com/Jhammett03/AI_Phishing_detector.git
cd AI_Phishing_detector
```
2️⃣ Backend Setup  
The backend Flask API handles email classification.

🔹 Set up a virtual environment (optional)
```sh
python -m venv venv
source venv/bin/activate   # (Mac/Linux)
venv\Scripts\activate      # (Windows)
```
🔹 Install dependencies
```sh
pip install -r requirements.txt
```
🔹 Train the Model
```sh
python train.py
```
- This will generate phishing_model.pkl and vectorizer.pkl.

🔹 Run the Flask Server
```sh
python predict.py
```
By default, the API runs at: http://127.0.0.1:5000

### 3️⃣ Chrome Extension Setup
1. Open Chrome → Navigate to chrome://extensions/.
2. Enable "Developer mode" (top right).
3. Click "Load unpacked" and select the phishing-detector-extension folder.

The extension should now be active! 🎉

### 🛠 Usage
1. Open Gmail.
2. Click on an email—the extension will scan it automatically.
3. If a phishing attempt is detected, a warning banner will appear.
4. Suspicious words will be highlighted in yellow.
5. Click "Check Page" in the extension popup to manually scan an email.
