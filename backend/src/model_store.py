import os
import pickle
import tensorflow as tf
from src.config import MODEL_SAVE_DIR


def save_model(model, filename):
    """Save a model (Keras or traditional ML) to the specified directory."""
    os.makedirs(MODEL_SAVE_DIR, exist_ok=True)
    path = os.path.join(MODEL_SAVE_DIR, filename)

    if filename.endswith(".h5"):
        # Save Keras/TensorFlow models
        model.save(path)
    else:
        # Save traditional ML models
        with open(path, "wb") as f:
            pickle.dump(model, f)

    print(f"✅ Model saved successfully: {path}")


def load_model(filename):
    """Load a saved model (Keras or traditional ML) from the directory."""
    path = os.path.join(MODEL_SAVE_DIR, filename)

    if not os.path.exists(path):
        raise FileNotFoundError(f"❌ Model file not found: {path}")

    if filename.endswith(".h5"):
        # Load Keras/TensorFlow models
        return tf.keras.models.load_model(path)
    else:
        # Load traditional ML models
        with open(path, "rb") as f:
            return pickle.load(f)
