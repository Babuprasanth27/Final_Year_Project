import os
import pickle
import joblib
import numpy as np
import tensorflow as tf
from pathlib import Path

_MODEL_CACHE = {"loaded": False, "models": None, "scaler": None, "encoder": None}

def find_model_dir():
    base_dir = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
    candidates = [
        os.path.join(base_dir, "models", "saved"),
        os.path.join(base_dir, "backend", "models", "saved"),
        os.path.join(base_dir, "..", "backend", "models", "saved"),
    ]
    for c in candidates:
        if os.path.isdir(c):
            return os.path.normpath(c)
    for root, dirs, files in os.walk(base_dir):
        if "saved" in dirs and os.path.basename(root) == "models":
            return os.path.normpath(os.path.join(root, "saved"))
    return None

def _load_pickle_safe(path):
    try:
        with open(path, 'rb') as f:
            return pickle.load(f)
    except Exception as e:
        print(f"⚠️ pickle failed for {os.path.basename(path)}: {e}\nTrying joblib...")
        return joblib.load(path)

def _load_all_models():
    if _MODEL_CACHE["loaded"]:
        return _MODEL_CACHE["models"], _MODEL_CACHE["scaler"], _MODEL_CACHE["encoder"]

    MODEL_DIR = find_model_dir()
    if MODEL_DIR is None:
        raise FileNotFoundError("❌ Could not find models directory.")

    print("✅ MODEL_DIR:", MODEL_DIR)

    paths = {
        "random_forest": os.path.join(MODEL_DIR, "random_forest.pkl"),
        "svm": os.path.join(MODEL_DIR, "svm.pkl"),
        "xgboost": os.path.join(MODEL_DIR, "xgboost.pkl"),
        "kmeans": os.path.join(MODEL_DIR, "kmeans.pkl"),
        "ann": os.path.join(MODEL_DIR, "ann_model.h5"),
        "scaler": os.path.join(MODEL_DIR, "scaler.pkl"),
        "encoder": os.path.join(MODEL_DIR, "label_encoder.pkl"),
    }

    missing = [k for k, v in paths.items() if not os.path.exists(v)]
    if missing:
        raise FileNotFoundError(f"❌ Missing files: {missing}")

    models = {}
    for name in ["random_forest", "svm", "xgboost", "kmeans"]:
        print(f"🔄 Loading {name.upper()}...")
        models[name] = _load_pickle_safe(paths[name])

    print("🔄 Loading ANN (Keras model)...")
    models["ann"] = tf.keras.models.load_model(paths["ann"])

    print("🔄 Loading Scaler...")
    scaler = _load_pickle_safe(paths["scaler"])
    print(f"Scaler loaded: {type(scaler)}")

    print("🔄 Loading Encoder...")
    encoder = _load_pickle_safe(paths["encoder"])

    _MODEL_CACHE.update({
        "loaded": True,
        "models": models,
        "scaler": scaler,
        "encoder": encoder,
    })

    print("✅ All models loaded successfully.")
    return models, scaler, encoder

def predict_attack(input_features):
    models, scaler, encoder = _load_all_models()
    X_input = np.array(input_features).reshape(1, -1)

    try:
        expected_n = scaler.mean_.shape[0]
    except Exception:
        raise RuntimeError("Scaler invalid or corrupted.")

    if X_input.shape[1] != expected_n:
        raise ValueError(f"Input features: {X_input.shape[1]} ≠ expected {expected_n}")

    X_scaled = scaler.transform(X_input)

    preds = {
        "rf": int(models["random_forest"].predict(X_scaled)[0]),
        "svm": int(models["svm"].predict(X_scaled)[0]),
        "xgb": int(models["xgboost"].predict(X_scaled)[0]),
    }

    ann_probs = models["ann"].predict(X_scaled, verbose=0)
    preds["ann"] = int(np.argmax(ann_probs, axis=1)[0])

    votes = list(preds.values())
    final_pred_index = max(set(votes), key=votes.count)

    try:
        final_label = encoder.inverse_transform([final_pred_index])[0]
    except Exception:
        final_label = str(final_pred_index)

    print("🔍 Predictions:", preds)
    print("✅ Final Label:", final_label)
    return {"preds": preds, "label": final_label}

if __name__ == "__main__":
    print("🚀 Starting Prediction Test...")
    sample_input = [18, 0.002, 2, 1, 10, 120, 90, 60, 50, 80, 0.1, 0.15, 1.12, 180, 3000]
    try:
        out = predict_attack(sample_input)
        print("🧠 Predicted Attack Type:", out["label"])
    except Exception as e:
        print("❗ Prediction failed:", e)
        mdl = find_model_dir()
        if mdl:
            print("Model dir contents:", os.listdir(mdl))