# 🛡️ PhishGuard — AI-Powered Cybersecurity Detection System

PhishGuard is an AI-powered cybersecurity web application that uses Deep Learning to detect potentially harmful digital content.

The current application provides two AI-powered detection features:

* 🔗 **Phishing URL Detection**
* 📧 **Spam Email Classification**

## 🚀 Live Demo

Try the deployed application:

**Hugging Face Space:**
https://huggingface.co/spaces/Helanamagdy/phishguard

> The Hugging Face Space uses ZeroGPU. The demo may temporarily be unavailable when the available ZeroGPU quota is exhausted.

---

## ✨ Features

### 🔗 Phishing URL Detection

PhishGuard analyzes a submitted URL using an LSTM-based Deep Learning model and classifies it as potentially phishing or safe.

**Input:** URL
**Model:** LSTM
**Framework:** TensorFlow / Keras
**Output:** Phishing / Safe + confidence score

---

### 📧 Spam Email Classification

PhishGuard analyzes email content using an LSTM-based Deep Learning model and classifies the message as spam or safe.

**Input:** Email text
**Model:** LSTM
**Framework:** TensorFlow / Keras
**Output:** Spam / Safe + confidence score

---

## 🧠 AI Models

| Detection Task            | Model | Framework          |
| ------------------------- | ----- | ------------------ |
| Phishing URL Detection    | LSTM  | TensorFlow / Keras |
| Spam Email Classification | LSTM  | TensorFlow / Keras |

---

## 🛠️ Technologies

### Programming Languages

* Python
* HTML
* CSS
* JavaScript

### AI & Machine Learning

* TensorFlow
* Keras
* NumPy
* Joblib

### Natural Language Processing

* Tokenization
* Sequence Padding
* Text Preprocessing

### Backend

* FastAPI
* Uvicorn

### Frontend

* HTML
* CSS
* JavaScript

### Deployment

* Hugging Face Spaces
* GitHub
* Git LFS

---

## 📁 Project Structure

```text
Web Phishing Detection/
│
├── backend/
│   └── main.py
│
├── CSS/
│   └── style.css
│
├── HTML/
│   └── index (1).html
│
├── JS/
│   └── script.js
│
├── models/
│   │
│   ├── Phishing Links Detection/
│   │   ├── lstm_url_model.h5
│   │   ├── tokenizer.pkl
│   │   └── Phishing_Links_Detetction.ipynb
│   │
│   └── Spam Email Classification/
│       ├── spamclassification (1).h5
│       ├── tokenizer (1).pkl
│       └── Spam_Email_classification.ipynb
│
├── test_models.py
├── test_phishing_prediction.py
├── test_spam_prediction.py
├── .gitignore
├── .gitattributes
└── README.md
```

---

## ⚙️ Installation

### 1. Clone the repository

```bash
git clone https://github.com/helana-mmagdyy/helana-magdy.git
```

### 2. Navigate to the project

```bash
cd helana-magdy
```

### 3. Create a virtual environment

```bash
python -m venv venv
```

### 4. Activate the environment

On Windows:

```bash
venv\Scripts\activate
```

### 5. Install dependencies

```bash
pip install -r requirements.txt
```

---

## ▶️ Running the Backend

Start the FastAPI server:

```bash
uvicorn backend.main:app --reload
```

The API will be available at:

```text
http://127.0.0.1:8000
```

---

## 🧪 Testing

The repository includes test scripts for the trained models.

Run:

```bash
python test_models.py
```

Phishing URL model:

```bash
python test_phishing_prediction.py
```

Spam email model:

```bash
python test_spam_prediction.py
```

---

## 🔍 How It Works

### Phishing URL Detection

1. The user enters a URL.
2. The URL is processed using the trained tokenizer.
3. The sequence is padded to the required input length.
4. The processed input is passed to the LSTM model.
5. The model generates a prediction probability.
6. PhishGuard returns the classification and confidence score.

### Spam Email Classification

1. The user enters email content.
2. The text is cleaned and preprocessed.
3. The trained tokenizer converts the text into a sequence.
4. The sequence is padded to the required length.
5. The LSTM model generates a prediction.
6. PhishGuard returns the classification and confidence score.

---

## 🎯 Project Goals

PhishGuard demonstrates the practical application of Artificial Intelligence to cybersecurity.

The project combines:

* Artificial Intelligence
* Deep Learning
* Natural Language Processing
* Cybersecurity
* Web Development
* REST APIs
* Model Deployment

---

## 🔮 Future Improvements

Future versions may include:

* QR Code Detection integration
* Transformer-based models
* Improved model accuracy
* Explainable AI
* Security analytics dashboard
* User authentication
* Real-time threat intelligence
* Improved cloud deployment

---

## 📌 Project Status

| Component                 | Status      |
| ------------------------- | ----------- |
| Phishing URL Detection    | ✅ Completed |
| Spam Email Classification | ✅ Completed |
| Frontend                  | ✅ Completed |
| FastAPI Backend           | ✅ Completed |
| Hugging Face Deployment   | ✅ Deployed  |
| GitHub Repository         | ✅ Published |

---

## 👩‍💻 Author

**Helana Magdy Lamei**

Aspiring AI Engineer

Cairo, Egypt

📧 **Email:** [helanamagdylamei@gmail.com](mailto:helanamagdylamei@gmail.com)

💻 **GitHub:**
https://github.com/helana-mmagdyy

🔗 **LinkedIn:**
https://linkedin.com/in/helana-magdy-6b517a253

---

## 🔗 Links

**GitHub Repository:**
https://github.com/helana-mmagdyy/helana-magdy

**Live Demo:**
https://huggingface.co/spaces/Helanamagdy/phishguard

---

⭐ Thank You

Thank you for visiting **PhishGuard**.

Feel free to explore the repository and try the live demo.
