import tensorflow as tf
import joblib
import numpy as np
from tensorflow.keras.preprocessing.sequence import pad_sequences

MODEL_PATH = r"models\Phishing Links Detection\lstm_url_model.h5"
TOKENIZER_PATH = r"models\Phishing Links Detection\tokenizer.pkl"

MAX_LEN = 200

print("Loading model...")

model = tf.keras.models.load_model(MODEL_PATH)

print("Loading tokenizer...")

tokenizer = joblib.load(TOKENIZER_PATH)

print("Model and tokenizer loaded successfully!")


def predict_url(url):

    sequence = tokenizer.texts_to_sequences([url])

    padded = pad_sequences(
        sequence,
        maxlen=MAX_LEN,
        padding="post"
    )

    probability = model.predict(
        padded,
        verbose=0
    )[0][0]

    # PhiUSIIL labels:
    # 1 = legitimate
    # 0 = phishing

    if probability >= 0.5:
        label = "legitimate"
    else:
        label = "phishing"

    return label, float(probability)


test_urls = [
    "https://www.google.com",
    "https://www.facebook.com",
    "http://example.com",
    "http://paypal-login-security.com"
]


print("\n" + "=" * 60)
print("PHISHING PREDICTION TEST")
print("=" * 60)

for url in test_urls:

    label, probability = predict_url(url)

    print(f"\nURL: {url}")
    print(f"Prediction: {label}")
    print(f"Probability: {probability:.4f}")