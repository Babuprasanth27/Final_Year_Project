import os
from src.preprocess import preprocess_data
from src.config import DATA_PATH
from models.random_forest_model import RandomForestModel
from models.svm_model import SVMModel
from models.xgboost_model import XGBoostModel
from models.kmeans_model import KMeansModel
from models.ann_model import ANNModel
from models.ensemble_model import EnsembleModel
from src.utils import log_time
from sklearn.metrics import accuracy_score
import pandas as pd


@log_time
def main():
    # Step 1: Preprocess data (this also saves scaler.pkl & label_encoder.pkl)
    X_train, X_test, y_train, y_test, _ = preprocess_data(DATA_PATH)
    input_dim = X_train.shape[1]
    num_classes = len(set(y_train))
    print(f"✅ Data preprocessing complete. Shapes:\n   X_train: {X_train.shape}, X_test: {X_test.shape}")

    # Step 2: Initialize models
    rf = RandomForestModel()
    svm = SVMModel()
    xgb = XGBoostModel()
    km = KMeansModel()
    ann = ANNModel(input_dim=input_dim, num_classes=num_classes)

    print("\n🚀 Training models...\n")

    # Step 3: Train models
    rf.train(X_train, y_train)
    print("✅ Random Forest training completed.")

    svm.train(X_train, y_train)
    print("✅ SVM training completed.")

    xgb.train(X_train, y_train)
    print("✅ XGBoost training completed.")

    km.train(X_train)
    print("✅ KMeans training completed.")

    ann.train(X_train, y_train, X_test, y_test)
    print("✅ ANN training completed.")

    # Step 4: Evaluate models
    results = {}

    rf_acc = rf.evaluate(X_test, y_test) * 100
    results["Random Forest"] = round(rf_acc, 2)

    svm_acc = svm.evaluate(X_test, y_test) * 100
    results["SVM"] = round(svm_acc, 2)

    xgb_acc = xgb.evaluate(X_test, y_test) * 100
    results["XGBoost"] = round(xgb_acc, 2)

    ann_acc = ann.evaluate(X_test, y_test) * 100
    results["ANN"] = round(ann_acc, 2)

    km_score = km.evaluate(X_train)
    results["KMeans (Silhouette Score)"] = round(km_score, 4)

    # Step 5: Create Ensemble
    ensemble = EnsembleModel(models=[rf.model, svm.model, xgb.model])
    print("✅ Ensemble created successfully.")

    # Step 6: Ensure save directory exists
    os.makedirs("backend/models/saved", exist_ok=True)

    # Step 7: Save all models
    rf.save("backend/models/saved/random_forest.pkl")
    svm.save("backend/models/saved/svm.pkl")
    xgb.save("backend/models/saved/xgboost.pkl")
    km.save("backend/models/saved/kmeans.pkl")
    ann.save("backend/models/saved/ann_model.h5")

    # Step 8: Save results summary
    report_path = "backend/reports"
    os.makedirs(report_path, exist_ok=True)
    df = pd.DataFrame(list(results.items()), columns=["Model", "Score"])
    df.to_csv(os.path.join(report_path, "model_accuracy_summary.csv"), index=False)

    print("\n✅ Model Accuracy Summary:")
    for model, acc in results.items():
        print(f"   {model}: {acc}")

    print("\n✅ All models and reports saved successfully!")


if __name__ == "__main__":
    main()
