# Dynamic Knowledge Base Chatbot

## Overview

This project implements a Dynamic Knowledge Base Chatbot that automatically updates its knowledge base with new information from external sources. The system periodically collects new articles, generates embeddings, stores them in a vector database, and retrieves relevant information to answer user queries.

## Features

- Automatic data collection from external sources
- Dynamic knowledge base updates
- Vector similarity search using FAISS
- Sentence embeddings using Hugging Face models
- Streamlit-based user interface
- Retrieval of relevant documents for user queries

## Project Structure

Dynamic_Knowledge_Base_Chatbot/

├── app.py

├── requirements.txt

├── data/

│ └── articles.json

├── src/

│ ├── scraper.py

│ ├── embeddings.py

│ ├── vector_store.py

│ ├── updater.py

│ └── chatbot.py

├── test_embeddings.py

└── test_vector_store.py


## Technologies Used

- Python
- Streamlit
- FAISS
- Sentence Transformers
- Hugging Face Transformers
- Feedparser
- NumPy

## Workflow

1. Collect articles from external sources.
2. Store article data in JSON format.
3. Generate embeddings using a Sentence Transformer model.
4. Store embeddings in a FAISS vector database.
5. Convert user queries into embeddings.
6. Retrieve the most relevant articles using similarity search.
7. Display results through the Streamlit interface.
8. Update the knowledge base periodically with new information.

## Installation

### Clone Repository

```bash
git clone <repository-link>
cd Dynamic_Knowledge_Base_Chatbot
```

### Install Dependencies

```bash
pip install -r requirements.txt
```

## Run the Application

```bash
python -m streamlit run app.py
```

## Testing

### Test Embeddings

```bash
python test_embeddings.py
```

### Test Vector Store

```bash
python test_vector_store.py
```

## Sample Queries

- Artificial Intelligence
- Machine Learning
- Deep Learning
- Natural Language Processing
- Computer Vision

## Expected Outcome

The chatbot dynamically expands its knowledge base by incorporating newly collected information and retrieves relevant articles in response to user queries.

## Future Improvements

- Integration with Large Language Models (LLMs)
- OpenAI API support
- Advanced conversational memory
- Automated scheduling of updates
- Deployment on Streamlit Cloud

## Author

Sravya Reddy

## Internship Project

Dynamic Knowledge Base Chatbot – AI/Data Science Internship Project