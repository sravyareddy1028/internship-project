# Sentiment Analysis using Machine Learning

## Project Overview

This project performs **Sentiment Analysis** on text by classifying user input as **Positive**, **Negative**, or **Neutral**. It uses Natural Language Processing (NLP) techniques and a Machine Learning model to analyze the sentiment expressed in reviews, comments, or other text data.

The application provides an easy-to-use interface where users can enter text and instantly receive the predicted sentiment.

---

## Features

* Predicts sentiment as Positive, Negative, or Neutral.
* Text preprocessing using NLP techniques.
* Machine Learning-based sentiment classification.
* Interactive web interface using Streamlit.
* Fast and easy-to-use application.

---

## Technologies Used

* Python
* Streamlit
* Scikit-learn
* Pandas
* NumPy
* NLTK
* Pickle (for saving the trained model)

---

## Dataset

The model is trained on a labeled sentiment dataset containing text samples and their corresponding sentiment labels.

Example labels:

* Positive
* Negative
* Neutral

---

## Project Structure

```text
sentiment-analysis/
│
├── app.py
├── sentiment_model.pkl
├── vectorizer.pkl
├── requirements.txt
├── README.md
└── dataset.csv
```

---

## Installation

### 1. Clone the repository

```bash
git clone <repository-url>
cd sentiment-analysis
```

### 2. Install the required libraries

```bash
pip install -r requirements.txt
```

---

## Running the Application

Start the Streamlit application using:

```bash
streamlit run app.py
```

The application will open automatically in your web browser.

---

## How It Works

1. The user enters a text message or review.
2. The text is preprocessed (cleaning, tokenization, etc.).
3. The trained vectorizer converts the text into numerical features.
4. The Machine Learning model predicts the sentiment.
5. The predicted sentiment is displayed to the user.

---

## Sample Inputs

| Input                           | Predicted Sentiment |
| ------------------------------- | ------------------- |
| I absolutely love this product! | Positive            |
| The service was terrible.       | Negative            |
| It is okay, nothing special.    | Neutral             |

---

## Future Enhancements

* Deep Learning models (LSTM/BERT).
* Emotion detection (Happy, Sad, Angry, etc.).
* Support for multiple languages.
* Sentiment confidence score.
* Batch prediction from CSV files.
* Visualization of sentiment distribution.

---

## Applications

* Product Review Analysis
* Social Media Monitoring
* Customer Feedback Analysis
* Movie and Book Review Classification
* Brand Reputation Monitoring

---

## Disclaimer

This project is developed for educational purposes. The predictions depend on the quality of the training data and the machine learning model used.

---

## Author

**Sravya Reddy Thumma**
