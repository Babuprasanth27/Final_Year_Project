# from fastapi import FastAPI, HTTPException
# from pydantic import BaseModel
# import numpy as np
# import joblib
# import os
# from src.config import MODEL_SAVE_DIR, LABEL_MAP
# from src.model_store import load_model
# from models.ensemble_model import EnsembleModel

# app = FastAPI(title="Network Attack Detection API 🚀")

# # =========================
# #  Define Input Schema
# # =========================
# class PredictRequest(BaseModel):
#     protocol: int
#     flow_duration: float
#     total_forward_packets: int
#     total_backward_packets: int
#     total_forward_packets_length: float
#     total_backward_packets_length: float
#     forward_packet_length_mean: float
#     backward_packet_length_mean: float
#     forward_packets_per_second: float
#     backward_packets_per_second: float
#     forward_iat_mean: float
#     backward_iat_mean: float
#     flow_iat_mean: float
#     flow_packets_per_seconds: float
#     flow_bytes_per_seconds: float


# # =========================
# # Load Models and Scaler
# # =========================
# try:
#     rf = load_model("random_forest.pkl")
#     svm = load_model("svm.pkl")
#     xgb = load_model("xgboost.pkl")
#     ann = load_model("ann_model.h5")
#     scaler = joblib.load(os.path.join(MODEL_SAVE_DIR, "scaler.pkl"))
#     ensemble = EnsembleModel(models=[rf, svm, xgb])
#     print("✅ Models and scaler loaded successfully.")
# except Exception as e:
#     raise RuntimeError(f"❌ Failed to load models: {e}")


# @app.get("/")
# def root():
#     """Check API status."""
#     return {"message": "✅ Network Attack Detector is running 🚀"}


# # =========================
# # Prediction Endpoint
# # =========================
# @app.post("/predict")
# def predict(request: PredictRequest):
#     """Predict network attack type using ensemble model."""
#     try:
#         features = np.array([[
#             request.protocol,
#             request.flow_duration,
#             request.total_forward_packets,
#             request.total_backward_packets,
#             request.total_forward_packets_length,
#             request.total_backward_packets_length,
#             request.forward_packet_length_mean,
#             request.backward_packet_length_mean,
#             request.forward_packets_per_second,
#             request.backward_packets_per_second,
#             request.forward_iat_mean,
#             request.backward_iat_mean,
#             request.flow_iat_mean,
#             request.flow_packets_per_seconds,
#             request.flow_bytes_per_seconds,
#         ]])

#         # Scale features
#         features_scaled = scaler.transform(features)

#         # Predict with ensemble
#         preds = ensemble.predict(features_scaled)
#         pred_label = int(preds[0])
#         label = LABEL_MAP.get(pred_label, "Unknown Attack")

#         return {
#             "prediction": label,
#             "predicted_class": pred_label,
#             "status": "success"
#         }

#     except Exception as e:
#         raise HTTPException(status_code=400, detail=f"Prediction error: {e}")

# from fastapi import FastAPI, HTTPException
# from pydantic import BaseModel
# import numpy as np
# import joblib
# import os
# from src.config import MODEL_SAVE_DIR, LABEL_MAP
# from src.model_store import load_model
# from models.ensemble_model import EnsembleModel
# import tensorflow as tf

# app = FastAPI(title="🚀 Network Attack Detection API")

# # =========================
# #  Define Input Schema
# # =========================
# class PredictRequest(BaseModel):
#     protocol: int
#     flow_duration: float
#     total_forward_packets: int
#     total_backward_packets: int
#     total_forward_packets_length: float
#     total_backward_packets_length: float
#     forward_packet_length_mean: float
#     backward_packet_length_mean: float
#     forward_packets_per_second: float
#     backward_packets_per_second: float
#     forward_iat_mean: float
#     backward_iat_mean: float
#     flow_iat_mean: float
#     flow_packets_per_seconds: float
#     flow_bytes_per_seconds: float


# # =========================
# # Load Models and Scaler
# # =========================
# try:
#     print("🔄 Loading models and scaler...")

#     rf = load_model("random_forest.pkl")
#     svm = load_model("svm.pkl")
#     xgb = load_model("xgboost.pkl")

#     ann_path = os.path.join(MODEL_SAVE_DIR, "ann_model.h5")
#     ann = tf.keras.models.load_model(ann_path)

#     scaler_path = os.path.join(MODEL_SAVE_DIR, "scaler.pkl")
#     scaler = joblib.load(scaler_path)

#     ensemble = EnsembleModel(models=[rf, svm, xgb])

#     print("✅ Models and scaler loaded successfully.")
# except Exception as e:
#     raise RuntimeError(f"❌ Failed to load models: {e}")


# # =========================
# # Root Endpoint
# # =========================
# @app.get("/")
# def root():
#     """Check API status."""
#     return {"message": "✅ Network Attack Detector API is running 🚀"}


# # =========================
# # Prediction Endpoint
# # =========================
# @app.post("/predict")
# def predict(request: PredictRequest):
#     """Predict network attack type using ensemble model."""
#     try:
#         # Convert incoming JSON to NumPy array
#         features = np.array([[
#             request.protocol,
#             request.flow_duration,
#             request.total_forward_packets,
#             request.total_backward_packets,
#             request.total_forward_packets_length,
#             request.total_backward_packets_length,
#             request.forward_packet_length_mean,
#             request.backward_packet_length_mean,
#             request.forward_packets_per_second,
#             request.backward_packets_per_second,
#             request.forward_iat_mean,
#             request.backward_iat_mean,
#             request.flow_iat_mean,
#             request.flow_packets_per_seconds,
#             request.flow_bytes_per_seconds,
#         ]])

#         # Scale input features
#         features_scaled = scaler.transform(features)

#         # Ensemble model prediction (RF + SVM + XGBoost)
#         ensemble_pred = ensemble.predict(features_scaled)
#         ensemble_label = int(ensemble_pred[0])
#         ensemble_attack = LABEL_MAP.get(ensemble_label, "Unknown Attack")

#         # ANN model prediction
#         ann_pred = ann.predict(features_scaled)
#         ann_label = int(np.argmax(ann_pred, axis=1)[0])
#         ann_attack = LABEL_MAP.get(ann_label, "Unknown Attack")

#         # Combine results
#         result = {
#             "ensemble_prediction": ensemble_attack,
#             "ensemble_label": ensemble_label,
#             "ann_prediction": ann_attack,
#             "ann_label": ann_label,
#             "status": "success"
#         }

#         return result

#     except Exception as e:
#         raise HTTPException(status_code=400, detail=f"Prediction error: {str(e)}")
from fastapi import FastAPI, Query
from pydantic import BaseModel
import numpy as np
import joblib
import os
import socket

from src.config import MODEL_SAVE_DIR, LABEL_MAP
from src.model_store import load_model
from models.ensemble_model import EnsembleModel
from agent.live_capture import capture_live_flow
from ml.firewall import traffic_firewall

app = FastAPI(title="Network Attack Detection API 🚀")


class PredictRequest(BaseModel):
    src_ip: str
    dst_ip: str
    protocol: int
    flow_duration: float
    total_forward_packets: int
    total_backward_packets: int
    total_forward_packets_length: float
    total_backward_packets_length: float
    forward_packet_length_mean: float
    backward_packet_length_mean: float
    forward_packets_per_second: float
    backward_packets_per_second: float
    forward_iat_mean: float
    backward_iat_mean: float
    flow_iat_mean: float
    flow_packets_per_seconds: float
    flow_bytes_per_seconds: float


rf = load_model("random_forest.pkl")
svm = load_model("svm.pkl")
xgb = load_model("xgboost.pkl")
ann = load_model("ann_model.h5")
scaler = joblib.load(os.path.join(MODEL_SAVE_DIR, "scaler.pkl"))
ensemble = EnsembleModel(models=[rf, svm, xgb])


@app.get("/")
def root():
    return {"message": "Network Attack Detector running"}


# ================= MANUAL =================
@app.post("/predict/manual")
def predict_manual(request: PredictRequest):

    fw = traffic_firewall(request)
    if fw:
        fw["mode"] = "manual"
        fw["confidence"] = 0.55
        return fw

    features = np.array([[  
        request.protocol,
        request.flow_duration,
        request.total_forward_packets,
        request.total_backward_packets,
        request.total_forward_packets_length,
        request.total_backward_packets_length,
        request.forward_packet_length_mean,
        request.backward_packet_length_mean,
        request.forward_packets_per_second,
        request.backward_packets_per_second,
        request.forward_iat_mean,
        request.backward_iat_mean,
        request.flow_iat_mean,
        request.flow_packets_per_seconds,
        request.flow_bytes_per_seconds
    ]])

    features_scaled = scaler.transform(features)

    # FIXED PART
    rf_pred = int(rf.predict(features_scaled)[0])
    svm_pred = int(svm.predict(features_scaled)[0])
    xgb_pred = int(xgb.predict(features_scaled)[0])

    votes = [rf_pred, svm_pred, xgb_pred]
    final_pred = max(set(votes), key=votes.count)

    dist = float(np.linalg.norm(features_scaled))
    confidence = round(0.5 + (np.log1p(dist) / np.log1p(50)) * 0.49, 3)

    return {
        "mode": "manual",
        "prediction": LABEL_MAP.get(final_pred, "Unknown"),
        "predicted_class": int(final_pred),
        "confidence": confidence,
        "status": "success"
    }


# ================= LIVE =================
@app.get("/predict/live")
def predict_live(duration: int = Query(5, ge=2, le=30)):

    local_ip = socket.gethostbyname(socket.gethostname())
    result = capture_live_flow(duration=duration, filter_ip=local_ip, return_meta=True)

    features = result["features"]
    meta = result["meta"]

    # ----- SAFE MANUAL BUILD OF REQUEST OBJECT -----
    vals = features.flatten().tolist()

    d = PredictRequest(
        src_ip = meta.get("src_ip") or "LIVE",
        dst_ip = meta.get("dst_ip") or "NETWORK",
        protocol = int(vals[0]),
        flow_duration = float(vals[1]),
        total_forward_packets = int(vals[2]),
        total_backward_packets = int(vals[3]),
        total_forward_packets_length = float(vals[4]),
        total_backward_packets_length = float(vals[5]),
        forward_packet_length_mean = float(vals[6]),
        backward_packet_length_mean = float(vals[7]),
        forward_packets_per_second = float(vals[8]),
        backward_packets_per_second = float(vals[9]),
        forward_iat_mean = float(vals[10]),
        backward_iat_mean = float(vals[11]),
        flow_iat_mean = float(vals[12]),
        flow_packets_per_seconds = float(vals[13]),
        flow_bytes_per_seconds = float(vals[14])
    )

    # ----- FIREWALL FILTER -----
    fw = traffic_firewall(d)
    if fw:
        fw["mode"] = "live_capture"
        fw["meta"] = meta
        fw["confidence"] = 0.55
        return fw

    # ----- ML PIPELINE -----
    features_scaled = scaler.transform(features)

    rf_pred = int(rf.predict(features_scaled)[0])
    svm_pred = int(svm.predict(features_scaled)[0])
    xgb_pred = int(xgb.predict(features_scaled)[0])

    votes = [rf_pred, svm_pred, xgb_pred]
    final_pred = max(set(votes), key=votes.count)

    ann_probs = ann.predict(features_scaled)[0]
    ann_conf = float(max(ann_probs))

    calibrated = 0.5 + (ann_conf - 0.5) * 0.6
    vote_strength = votes.count(final_pred) / len(votes)
    confidence = round(calibrated * (0.6 + 0.4 * vote_strength), 3)

    return {
        "mode": "live_capture",
        "prediction": LABEL_MAP.get(final_pred),
        "predicted_class": final_pred,
        "confidence": confidence,
        "meta": meta,
        "status": "success"
    }

# ================= DEBUG =================
@app.get("/predict/debug")
def predict_debug(duration: int = Query(5, ge=2, le=30)):

    local_ip = socket.gethostbyname(socket.gethostname())
    result = capture_live_flow(duration=duration, filter_ip=local_ip, return_meta=True)
    features = result["features"]
    meta = result["meta"]

    d = PredictRequest(**dict(zip(PredictRequest.__fields__.keys(), features.flatten().tolist())))

    fw = traffic_firewall(d)
    if fw:
        fw["mode"] = "debug"
        fw["meta"] = meta
        fw["confidence"] = 0.55
        return fw

    features_scaled = scaler.transform(features)

    rf_pred = int(rf.predict(features_scaled)[0])
    svm_pred = int(svm.predict(features_scaled)[0])
    xgb_pred = int(xgb.predict(features_scaled)[0])
    ann_probs = ann.predict(features_scaled)[0].tolist()
    ann_label = int(np.argmax(ann_probs))

    votes = [rf_pred, svm_pred, xgb_pred]
    ensemble_vote = max(set(votes), key=votes.count)

    return {
        "mode": "debug",
        "rf_pred": rf_pred,
        "svm_pred": svm_pred,
        "xgb_pred": xgb_pred,
        "ann_probs": ann_probs,
        "ann_label": ann_label,
        "ensemble_vote": ensemble_vote,
        "ensemble_label": LABEL_MAP.get(ensemble_vote),
        "raw_features": features.tolist(),
        "meta": meta,
        "status": "success"
    }
