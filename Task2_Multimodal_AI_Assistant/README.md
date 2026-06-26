# 🤖 Multi Modal AI Assistant

## 📌 Project Overview

The **Multi Modal AI Assistant** is an AI-powered application built using **Python**, **Streamlit**, and the **BLIP (Bootstrapping Language-Image Pre-training)** model from Hugging Face.

The application allows users to upload an image, automatically generates a description of the image using a pre-trained deep learning model, and answers simple questions related to the uploaded image.

---

## 🚀 Features

* Upload JPG, JPEG, and PNG images.
* Automatic image caption generation using BLIP.
* Ask questions related to the uploaded image.
* Displays AI-generated image description.
* Maintains conversation history.
* Clear conversation option.
* Simple and interactive Streamlit interface.

---

## 🛠 Technologies Used

* Python
* Streamlit
* Hugging Face Transformers
* BLIP Image Captioning Model
* Pillow (PIL)

---

## 📂 Project Structure

```
Multi_Modal_AI_Assistant/
│
├── app.py
├── requirements.txt
├── README.md
└── images/ (optional)
```

---

## 📦 Installation

Clone the repository:

```bash
git clone https://github.com/yourusername/Multi_Modal_AI_Assistant.git
```

Move into the project folder:

```bash
cd Multi_Modal_AI_Assistant
```

Install dependencies:

```bash
pip install -r requirements.txt
```

---

## ▶️ Run the Application

Start the Streamlit server:

```bash
streamlit run app.py
```

or

```bash
python -m streamlit run app.py
```

The application will open in your browser at:

```
http://localhost:8501
```

---

## 📸 How It Works

1. Launch the application.
2. Upload an image.
3. Click **Analyze Image**.
4. The BLIP model generates an image description.
5. Ask questions about the uploaded image.
6. The assistant provides responses based on the generated caption.
7. Previous conversations are stored during the session.

---

## 📚 Libraries Used

```
streamlit
transformers
torch
Pillow
```

---

## 🤖 Model Used

**Model Name**

```
Salesforce/blip-image-captioning-base
```

The BLIP model is used for generating natural language descriptions of uploaded images.

---

## 🎯 Example

### Input

Upload an image of a dog playing with a ball.

### Generated Caption

```
A dog playing with a ball in the grass.
```

### User Question

```
What is in the image?
```

### Assistant Response

```
The image appears to contain a dog playing with a ball in the grass.
```

---

## 🔮 Future Enhancements

* Support voice-based questions.
* Add speech output.
* Integrate Large Language Models (LLMs) for more intelligent responses.
* Support multiple image uploads.
* Improve visual question answering accuracy.
* Deploy the application on Streamlit Cloud.

---

## 👩‍💻 Author

**Sravya Reddy Thumma**

B.Tech Student

AI & Machine Learning Enthusiast

---

## 📄 License

This project is developed for educational and internship purposes.
