import tensorflow as tf
import joblib
import re
from tensorflow.keras.preprocessing.sequence import pad_sequences

MODEL_PATH = r"models\Spam Email Classification\spamclassification (1).h5"
TOKENIZER_PATH = r"models\Spam Email Classification\tokenizer (1).pkl"

MAX_LEN = 200

print("Loading spam model...")

model = tf.keras.models.load_model(MODEL_PATH)

print("Loading spam tokenizer...")

tokenizer = joblib.load(TOKENIZER_PATH)

print("Spam model and tokenizer loaded successfully!")


def clean_text(text):
    text = text.lower()
    text = re.sub(r'https?://\S+|www\.\S+', '', text)
    text = re.sub(r'[^a-zA-Z\s]', '', text)
    text = re.sub(r'\s+', ' ', text).strip()
    return text


def predict_email(email):

    cleaned = clean_text(email)

    sequence = tokenizer.texts_to_sequences([cleaned])

    padded = pad_sequences(
        sequence,
        maxlen=MAX_LEN,
        padding="post"
    )

    probability = model.predict(
        padded,
        verbose=0
    )[0][0]

    # Spam dataset labels:
    # 0 = spam
    # 1 = ham

    if probability >= 0.5:
        label = "ham"
    else:
        label = "spam"

    return label, float(probability)


test_emails = [

    # HAM
    "Hey, are we still meeting tomorrow?",
    "Can you send me the project report today?",
    "I'll call you when I get home.",

    # SPAM
    "WINNER!! You have won a £1000 prize! Call now to claim your prize!",
    "Congratulations! You have been selected to receive a FREE prize. Text WIN to 80082.",
    "URGENT! You have won $100000. Claim your reward immediately!",
    "FREE entry in 2 a weekly competition to win FA Cup final tickets. Text FA to 87121.",
    "You have been specially selected for a cash prize. Call now to claim!",
    "Claim your FREE gift now! Click here to receive your reward!"
]


print("\n" + "=" * 60)
print("SPAM EMAIL PREDICTION TEST")
print("=" * 60)

for email in test_emails:

    label, probability = predict_email(email)

    print("\nEmail:")
    print(email)

    print(f"Prediction: {label}")
    print(f"Probability: {probability:.4f}")