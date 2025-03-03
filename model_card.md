# Model Card: Phishing Email Detection Model

# Overview

This document provides details about the phishing email detection model, including the dataset, training process, evaluation metrics, and known limitations.

---

# Dataset Information

Source: The dataset consists of phishing and non-phishing emails collected from Naser Abdullah Alam & Amith Khandakar's [Phishing Email Dataset](https://www.kaggle.com/datasets/naserabdullahalam/phishing-email-dataset?resource=download&select=phishing_email.csv) on Kaggle.
This project only uses data from the phishing_email.csv file.
Preprocessing: The dataset was preprocessed to remove HTML tags, URLs, and non-alphabetical characters. Stopwords were removed using the NLTK library.

---

# Dataset Splitting: 

## 1. Loading & Preprocessing the Data
   
#### Dataset source:

- We load phishing_email.csv and extract the "email_text" and "label" columns.
  
#### Balancing the dataset:

- We sample 3,000 phishing emails and 3,000 normal emails to ensure balanced data.
  
#### Preprocessing:

- Removing HTML tags, URLs, special characters, and stopwords from the email text

## 2. Feature Engineering

#### TF-IDF Vectorization:

- Converts email text into a numerical representation using a max of 10,000 features.

#### Labels (y) and Features (X)

- X → Transformed email text (numerical features).
- y → Binary labels (1 for phishing, 0 for normal emails).

## 3. Splitting the Dataset

#### We use train_test_split() from sklearn.model_selection:

```py
X_train, X_test, y_train, y_test = train_test_split(X, y, test_size=0.2, random_state=42)
```

#### Training Set (X_train, y_train)

- 80% of the dataset (4,800 emails).
- Used for training the Logistic Regression model.

#### Test Set (X_test, y_test)

- 20% of the dataset (1,200 emails).
- Used for evaluating model performance.

## 4. Model Training & Evaluation

#### Training:

- We fit the model on X_train and y_train:

```py
model = LogisticRegression()
model.fit(X_train, y_train)
```

#### Evaluation:

- We test the model on X_test and calculate accuracy:

```py
predictions = model.predict(X_test)
accuracy = accuracy_score(y_test, predictions)
print(f"Model Accuracy: {accuracy:.2f}")
```

# Model Details

- Algorithm: Logistic Regression

- Feature Engineering: TF-IDF vectorization with a maximum of 10,000 features

- Hyperparameters:

   - Default settings for Logistic Regression (no regularization tuning applied)

   - Random state set to 42 for reproducibility

# Performance Metrics

- Accuracy: Achieved an accuracy of approximately 96% on the test dataset.

- Precision: Measures the proportion of actual phishing emails among those predicted as phishing.

- Recall: Measures the proportion of phishing emails correctly identified.

# Model Training & Reproduction

To train the model from scratch:

- Ensure dependencies are installed (pip install -r requirements.txt)

- Run the training script:

``` py
python train.py
```

- The trained model and vectorizer will be saved as phishing_model.pkl and vectorizer.pkl.

# Inference & API Usage

Once the model is trained, you can use the prediction API:

1. Start the prediction service:

```py
python predict.py
```

2. Send a POST request to http://localhost:5000/predict with JSON data:

```js
{
  "email_text": "Your email content here"
}
```

3. The response will indicate whether the email is phishing (true/false).

# Known Failure Modes

- Edge Cases:

  - Emails with highly obfuscated phishing content may not be detected.

  - Non-English phishing emails are not supported.

- Generalization Issues:

  - Model performance may degrade on emails with significantly different wording than the training dataset.

- Mitigation Strategies:

  - Regularly retrain the model with new phishing email samples (the current dataset is updated about once a year so maybe try with different datasets).

  - Implement additional feature engineering techniques, such as metadata analysis.

