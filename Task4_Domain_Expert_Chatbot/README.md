# ArXiv Expert Chatbot

## Overview

This project is an AI-powered chatbot that helps users search and explore research papers from the arXiv dataset.

## Features

* Search research papers using natural language queries
* Retrieve relevant papers using semantic similarity
* Uses Sentence Transformers for embeddings
* Uses FAISS for fast vector search
* Interactive user interface built with Streamlit

## Technologies Used

* Python
* Streamlit
* Sentence Transformers
* FAISS
* Pandas

## Dataset

The project uses the arXiv dataset from Kaggle.

Dataset download:
https://www.kaggle.com/datasets/Cornell-University/arxiv

Note: The dataset is not included in this repository because of its large size.

## Installation

```bash
pip install -r requirements.txt
```

## Run the Application

```bash
streamlit run app.py
```

## Project Structure

```text
ARXIV_EXPERT_CHATBOT
├── app.py
├── requirements.txt
├── README.md
├── src
│   ├── data_loader.py
│   ├── embeddings.py
│   ├── retriever.py
│   └── chatbot.py
```

## Author

Sravya Reddy
