import os
import pickle
import numpy as np
import tensorflow as tf
from xgboost import XGBClassifier
from sklearn.ensemble import RandomForestClassifier
from sklearn.svm import SVC
from sklearn.cluster import KMeans

# =====================================================
# ✅ Model Directory Paths
# Adjust according to your folder layout
# =====================================================
BASE_DIR = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
MODEL_DIR = os.path.join(BASE_DIR, "backend", "models", "saved")

# Print to verify
print("✅ MODEL_DIR:", MODEL_DIR)

MODEL_PATHS = {
    "random_forest": os.path.join(MODEL_DIR, "random_forest.pkl"),
    "svm": os.path.join(MODEL_DIR, "svm.pkl"),
    "xgboost": os.path.join(MODEL_DIR, "xgboost.pkl"),
    "kmeans": os.path.join(MODEL_DIR, "kmeans.pkl"),
    "ann": os.path.join(MODEL_DIR, "ann_model.h5"),
}

SCALER_PATH = os.path.join(MODEL_DIR, "scaler.pkl")
ENCODER_PATH = os.path.join(MODEL_DIR, "label_encoder.pkl")

# =====================================================
# ✅ Load Models
# =====================================================
def load_models():
    print("🔄 Loading models...")
    models = {}

    with open(MODEL_PATHS["random_forest"], "rb") as f:
        models["rf"] = pickle.load(f)

    with open(MODEL_PATHS["svm"], "rb") as f:
        models["svm"] = pickle.load(f)

    with open(MODEL_PATHS["xgboost"], "rb") as f:
        models["xgb"] = pickle.load(f)

    with open(MODEL_PATHS["kmeans"], "rb") as f:
        models["kmeans"] = pickle.load(f)

    models["ann"] = tf.keras.models.load_model(MODEL_PATHS["ann"])

    with open(SCALER_PATH, "rb") as f:
        scaler = pickle.load(f)

    with open(ENCODER_PATH, "rb") as f:
        encoder = pickle.load(f)

    print("✅ All models, scaler, and encoder loaded successfully.")
    return models, scaler, encoder


# =====================================================
# ✅ Predict Function
# =====================================================
def predict_attack(input_features):
    """
    input_features: list of feature values in same order as training columns
    """
    models, scaler, encoder = load_models()

    # Reshape input
    X_input = np.array(input_features).reshape(1, -1)
    X_scaled = scaler.transform(X_input)

    # Predict with ensemble
    preds = {
        "rf": models["rf"].predict(X_scaled)[0],
        "svm": models["svm"].predict(X_scaled)[0],
        "xgb": models["xgb"].predict(X_scaled)[0],
        "ann": np.argmax(models["ann"].predict(X_scaled), axis=1)[0],
    }

    # Take majority vote
    votes = list(preds.values())
    final_pred = max(set(votes), key=votes.count)

    # Decode label (if encoder is available)
    if hasattr(encoder, "inverse_transform"):
        try:
            final_label = encoder.inverse_transform([final_pred])[0]
        except Exception:
            final_label = str(final_pred)
    else:
        final_label = str(final_pred)

    print("🔍 Individual Model Predictions:", preds)
    print("✅ Final Predicted Label:", final_label)
    return final_label


# =====================================================
# ✅ Example Usage
# =====================================================
if __name__ == "__main__":
    # Example input (replace with actual values)
    sample_input = [
        17,  # protocol
        0.002,  # flow_duration
        2,  # total_forward_packets
        1,  # total_backward_packets
        180,  # total_forward_packets_length
        120,  # total_backward_packets_length
        90,  # forward_packet_length_mean
        60,  # backward_packet_length_mean
        100,  # forward_packets_per_second
        80,  # backward_packets_per_second
        0.1,  # forward_iat_mean
        0.15,  # backward_iat_mean
        0.12,  # flow_iat_mean
        180,  # flow_packets_per_seconds
        300,  # flow_bytes_per_seconds
    ]

    result = predict_attack(sample_input)
    print("🧠 Predicted Attack Type:", result)
