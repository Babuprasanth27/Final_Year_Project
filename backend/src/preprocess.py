import pandas as pd
from sklearn.model_selection import train_test_split
from sklearn.preprocessing import StandardScaler, LabelEncoder
from src.config import DATA_PATH, MODEL_SAVE_DIR
import os
import joblib

def preprocess_data(data_path=DATA_PATH):
    # Load CSV
    df = pd.read_csv(data_path)
    
    # Drop missing values if any
    df = df.dropna()

    # Separate features and label
    X = df.drop(columns=["label"])
    y = df["label"]

    # Encode labels (e.g., BENIGN -> 0, DrDoS_DNS -> 1)
    label_encoder = LabelEncoder()
    y = label_encoder.fit_transform(y)

    # Scale numerical features
    scaler = StandardScaler()
    X_scaled = scaler.fit_transform(X)

    # Split into train-test sets
    X_train, X_test, y_train, y_test = train_test_split(
        X_scaled, y, test_size=0.2, random_state=42, stratify=y
    )

    # Save encoders for future prediction
    os.makedirs(MODEL_SAVE_DIR, exist_ok=True)
    joblib.dump(label_encoder, os.path.join(MODEL_SAVE_DIR, "label_encoder.pkl"))
    joblib.dump(scaler, os.path.join(MODEL_SAVE_DIR, "scaler.pkl"))

    print("✅ Data preprocessing complete. Shapes:")
    print(f"   X_train: {X_train.shape}, X_test: {X_test.shape}")

    return X_train, X_test, y_train, y_test, label_encoder
