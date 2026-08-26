import tensorflow as tf
import pickle
import joblib
print("=" * 50)
print("TESTING PHISHING MODEL")
print("=" * 50)

phishing_model = tf.keras.models.load_model(
    r"models\Phishing Links Detection\lstm_url_model.h5"
)

print("Phishing LSTM loaded successfully!")

with open(
    r"models\Phishing Links Detection\tokenizer.pkl",
    "rb"
) as f:
    phishing_tokenizer = pickle.load(f)

print("Phishing tokenizer loaded successfully!")

print("=" * 50)
print("PHISHING MODEL TEST PASSED!")
print("=" * 50)

# Load spam model
spam_model = tf.keras.models.load_model(
    r"models\Spam Email Classification\spamclassification (1).h5"
)

# Load spam tokenizer
with open(
    r"models\Spam Email Classification\tokenizer (1).pkl",
    "rb"
) as f:
    spam_tokenizer = pickle.load(f)

print("Spam LSTM loaded successfully!")
print("Spam tokenizer loaded successfully!")


print("\n" + "=" * 50)
print("TESTING QR MODEL")
print("=" * 50)

