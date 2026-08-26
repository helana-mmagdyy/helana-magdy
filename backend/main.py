from fastapi import FastAPI, HTTPException
from fastapi.middleware.cors import CORSMiddleware
from pydantic import BaseModel

from tensorflow.keras.models import load_model
from tensorflow.keras.preprocessing.sequence import pad_sequences

import joblib
import numpy as np
import os
import re


# ============================================================
# APP
# ============================================================

app = FastAPI(
    title="PhishGuard API",
    description="AI-powered phishing link and spam email detection",
    version="1.0.0"
)


# ============================================================
# CORS
# ============================================================

app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)


# ============================================================
# PATHS
# ============================================================

# Current file:
# D:\Web Phishing Detection\backend\main.py

BASE_DIR = os.path.dirname(
    os.path.dirname(
        os.path.abspath(__file__)
    )
)

MODELS_DIR = os.path.join(
    BASE_DIR,
    "models"
)


# ============================================================
# PHISHING URL MODEL PATHS
# ============================================================

URL_MODEL_PATH = os.path.join(
    MODELS_DIR,
    "Phishing Links Detection",
    "lstm_url_model.h5"
)

URL_TOKENIZER_PATH = os.path.join(
    MODELS_DIR,
    "Phishing Links Detection",
    "tokenizer.pkl"
)


# ============================================================
# SPAM EMAIL MODEL PATHS
# ============================================================

EMAIL_MODEL_PATH = os.path.join(
    MODELS_DIR,
    "Spam Email Classification",
    "spamclassification (1).h5"
)

EMAIL_TOKENIZER_PATH = os.path.join(
    MODELS_DIR,
    "Spam Email Classification",
    "tokenizer (1).pkl"
)


# ============================================================
# MODEL CONFIGURATION
# ============================================================

MAX_LEN = 200

URL_THRESHOLD = 0.5

EMAIL_THRESHOLD = 0.5


# ============================================================
# GLOBAL MODELS
# ============================================================

url_model = None
url_tokenizer = None

email_model = None
email_tokenizer = None


# ============================================================
# STARTUP / MODEL LOADING
# ============================================================

print("=" * 70)
print("PHISHGUARD API")
print("Loading AI Models...")
print("=" * 70)


# ============================================================
# LOAD PHISHING URL MODEL
# ============================================================

try:

    print("\n[1/4] Loading phishing URL model...")

    if not os.path.exists(URL_MODEL_PATH):
        raise FileNotFoundError(
            f"URL model not found:\n{URL_MODEL_PATH}"
        )

    url_model = load_model(
        URL_MODEL_PATH,
        compile=False
    )

    print("✓ Phishing URL model loaded successfully")

except Exception as e:

    print("✗ Phishing URL model failed")
    print("Error:", e)


# ============================================================
# LOAD PHISHING URL TOKENIZER
# ============================================================

try:

    print("\n[2/4] Loading phishing URL tokenizer...")

    if not os.path.exists(URL_TOKENIZER_PATH):
        raise FileNotFoundError(
            f"URL tokenizer not found:\n{URL_TOKENIZER_PATH}"
        )

    url_tokenizer = joblib.load(
        URL_TOKENIZER_PATH
    )

    print("✓ Phishing URL tokenizer loaded successfully")

except Exception as e:

    print("✗ Phishing URL tokenizer failed")
    print("Error:", e)


# ============================================================
# LOAD SPAM EMAIL MODEL
# ============================================================

try:

    print("\n[3/4] Loading spam email model...")

    if not os.path.exists(EMAIL_MODEL_PATH):
        raise FileNotFoundError(
            f"Email model not found:\n{EMAIL_MODEL_PATH}"
        )

    email_model = load_model(
        EMAIL_MODEL_PATH,
        compile=False
    )

    print("✓ Spam email model loaded successfully")

except Exception as e:

    print("✗ Spam email model failed")
    print("Error:", e)


# ============================================================
# LOAD SPAM EMAIL TOKENIZER
# ============================================================

try:

    print("\n[4/4] Loading spam email tokenizer...")

    if not os.path.exists(EMAIL_TOKENIZER_PATH):
        raise FileNotFoundError(
            f"Email tokenizer not found:\n{EMAIL_TOKENIZER_PATH}"
        )

    email_tokenizer = joblib.load(
        EMAIL_TOKENIZER_PATH
    )

    print("✓ Spam email tokenizer loaded successfully")

except Exception as e:

    print("✗ Spam email tokenizer failed")
    print("Error:", e)


# ============================================================
# MODEL LOADING SUMMARY
# ============================================================

print("\n" + "=" * 70)
print("MODEL LOADING SUMMARY")
print("=" * 70)

print(
    f"Phishing URL Model:     "
    f"{'LOADED ✓' if url_model is not None else 'FAILED ✗'}"
)

print(
    f"Phishing URL Tokenizer: "
    f"{'LOADED ✓' if url_tokenizer is not None else 'FAILED ✗'}"
)

print(
    f"Spam Email Model:       "
    f"{'LOADED ✓' if email_model is not None else 'FAILED ✗'}"
)

print(
    f"Spam Email Tokenizer:   "
    f"{'LOADED ✓' if email_tokenizer is not None else 'FAILED ✗'}"
)

print("=" * 70)


# ============================================================
# REQUEST SCHEMAS
# ============================================================

class LinkRequest(BaseModel):

    url: str


class EmailRequest(BaseModel):

    text: str


# ============================================================
# ROOT ENDPOINT
# ============================================================

@app.get("/")
def root():

    return {

        "message": "PhishGuard API is running",

        "version": "1.0.0",

        "models": {

            "phishing_link":
                url_model is not None
                and url_tokenizer is not None,

            "spam_email":
                email_model is not None
                and email_tokenizer is not None
        }
    }


# ============================================================
# HEALTH ENDPOINT
# ============================================================

@app.get("/health")
def health():

    return {

        "status": "ok",

        "phishing_link": {

            "model_loaded":
                url_model is not None,

            "tokenizer_loaded":
                url_tokenizer is not None
        },

        "spam_email": {

            "model_loaded":
                email_model is not None,

            "tokenizer_loaded":
                email_tokenizer is not None
        }
    }


# ============================================================
# URL PREPROCESSING
# ============================================================

def preprocess_url(url: str):

    if url_tokenizer is None:

        raise RuntimeError(
            "URL tokenizer is not loaded"
        )

    # Character-level tokenization
    sequence = url_tokenizer.texts_to_sequences(
        [url]
    )

    # Same max_len used during training
    padded = pad_sequences(
        sequence,
        maxlen=MAX_LEN,
        padding="post"
    )

    return np.array(padded)


# ============================================================
# EMAIL CLEANING
# ============================================================

def clean_email_text(text: str):

    # EXACT SAME CLEANING USED DURING TRAINING

    text = text.lower()

    # Remove URLs
    text = re.sub(
        r'https?://\S+|www\.\S+',
        '',
        text
    )

    # Keep only English letters and spaces
    text = re.sub(
        r'[^a-zA-Z\s]',
        '',
        text
    )

    # Remove extra spaces
    text = re.sub(
        r'\s+',
        ' ',
        text
    ).strip()

    return text


# ============================================================
# EMAIL PREPROCESSING
# ============================================================

def preprocess_email(text: str):

    if email_tokenizer is None:

        raise RuntimeError(
            "Email tokenizer is not loaded"
        )

    cleaned_text = clean_email_text(
        text
    )

    sequence = email_tokenizer.texts_to_sequences(
        [cleaned_text]
    )

    padded = pad_sequences(
        sequence,
        maxlen=MAX_LEN,
        padding="post"
    )

    return np.array(padded)


# ============================================================
# PHISHING LINK SCAN
# ============================================================

@app.post("/api/scan/link")
def scan_link(request: LinkRequest):

    # --------------------------------------------------------
    # CHECK MODEL
    # --------------------------------------------------------

    if url_model is None:

        raise HTTPException(
            status_code=500,
            detail="Phishing URL model is not loaded"
        )

    if url_tokenizer is None:

        raise HTTPException(
            status_code=500,
            detail="Phishing URL tokenizer is not loaded"
        )

    # --------------------------------------------------------
    # VALIDATE URL
    # --------------------------------------------------------

    url = request.url.strip()

    if not url:

        raise HTTPException(
            status_code=400,
            detail="URL cannot be empty"
        )

    try:

        # ----------------------------------------------------
        # PREPROCESS
        # ----------------------------------------------------

        X = preprocess_url(
            url
        )

        # ----------------------------------------------------
        # MODEL PREDICTION
        # ----------------------------------------------------

        probability = float(
            url_model.predict(
                X,
                verbose=0
            )[0][0]
        )

        # ----------------------------------------------------
        # IMPORTANT:
        #
        # PhiUSIIL DATASET LABELS:
        #
        # 0 = PHISHING
        # 1 = LEGITIMATE
        #
        # Therefore:
        #
        # probability < 0.5
        #       => PHISHING
        #
        # probability >= 0.5
        #       => LEGITIMATE
        # ----------------------------------------------------

        is_phishing = (
            probability < URL_THRESHOLD
        )

        # ----------------------------------------------------
        # LABEL + CONFIDENCE
        # ----------------------------------------------------

        if is_phishing:

            label = "Phishing"

            confidence = (
                1 - probability
            ) * 100

        else:

            label = "Safe"

            confidence = (
                probability
            ) * 100

        # ----------------------------------------------------
        # RESPONSE
        # ----------------------------------------------------

        return {

            "isThreat":
                bool(is_phishing),

            "label":
                label,

            "confidence":
                round(
                    confidence,
                    2
                ),

            "model":
                "LSTM · url-sequence",

            "probability":
                round(
                    probability,
                    6
                ),

            "label_mapping": {

                "0":
                    "Phishing",

                "1":
                    "Legitimate"
            }
        }

    except Exception as e:

        print(
            "URL prediction error:",
            e
        )

        raise HTTPException(
            status_code=500,
            detail=f"URL prediction failed: {str(e)}"
        )


# ============================================================
# SPAM EMAIL SCAN
# ============================================================

@app.post("/api/scan/email")
def scan_email(request: EmailRequest):

    # --------------------------------------------------------
    # CHECK MODEL
    # --------------------------------------------------------

    if email_model is None:

        raise HTTPException(
            status_code=500,
            detail="Spam email model is not loaded"
        )

    if email_tokenizer is None:

        raise HTTPException(
            status_code=500,
            detail="Spam email tokenizer is not loaded"
        )

    # --------------------------------------------------------
    # VALIDATE EMAIL
    # --------------------------------------------------------

    text = request.text.strip()

    if not text:

        raise HTTPException(
            status_code=400,
            detail="Email text cannot be empty"
        )

    try:

        # ----------------------------------------------------
        # CLEAN EMAIL
        # ----------------------------------------------------

        cleaned_text = clean_email_text(
            text
        )

        # ----------------------------------------------------
        # PREPROCESS
        # ----------------------------------------------------

        X = preprocess_email(
            cleaned_text
        )

        # ----------------------------------------------------
        # MODEL PREDICTION
        # ----------------------------------------------------

        probability = float(
            email_model.predict(
                X,
                verbose=0
            )[0][0]
        )

        # ----------------------------------------------------
        # IMPORTANT:
        #
        # YOUR SPAM DATASET:
        #
        # 0 = SPAM
        # 1 = HAM / SAFE
        #
        # Therefore:
        #
        # probability < 0.5
        #       => SPAM
        #
        # probability >= 0.5
        #       => SAFE
        # ----------------------------------------------------

        is_spam = (
            probability < EMAIL_THRESHOLD
        )

        # ----------------------------------------------------
        # LABEL + CONFIDENCE
        # ----------------------------------------------------

        if is_spam:

            label = "Spam"

            confidence = (
                1 - probability
            ) * 100

        else:

            label = "Safe"

            confidence = (
                probability
            ) * 100

        # ----------------------------------------------------
        # RESPONSE
        # ----------------------------------------------------

        return {

            "isThreat":
                bool(is_spam),

            "label":
                label,

            "confidence":
                round(
                    confidence,
                    2
                ),

            "model":
                "Bi-LSTM · email",

            "probability":
                round(
                    probability,
                    6
                ),

            "label_mapping": {

                "0":
                    "Spam",

                "1":
                    "Safe"
            }
        }

    except Exception as e:

        print(
            "Email prediction error:",
            e
        )

        raise HTTPException(
            status_code=500,
            detail=f"Email prediction failed: {str(e)}"
        )


# ============================================================
# MODELS INFORMATION
# ============================================================

@app.get("/api/models")
def models_info():

    return {

        "phishing_link": {

            "loaded":
                url_model is not None,

            "tokenizer_loaded":
                url_tokenizer is not None,

            "model":
                "LSTM",

            "tokenizer":
                "Character-level",

            "max_words":
                50000,

            "max_length":
                MAX_LEN,

            "threshold":
                URL_THRESHOLD,

            "labels":
                {
                    "0":
                        "phishing",

                    "1":
                        "legitimate"
                }
        },

        "spam_email": {

            "loaded":
                email_model is not None,

            "tokenizer_loaded":
                email_tokenizer is not None,

            "model":
                "Bidirectional LSTM",

            "tokenizer":
                "Character-level",

            "max_words":
                50000,

            "max_length":
                MAX_LEN,

            "threshold":
                EMAIL_THRESHOLD,

            "labels":
                {
                    "0":
                        "spam",

                    "1":
                        "safe"
                }
        }
    }