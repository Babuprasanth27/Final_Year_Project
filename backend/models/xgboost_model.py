import pickle
from xgboost import XGBClassifier
from sklearn.metrics import accuracy_score, classification_report


class XGBoostModel:
    def __init__(self):
        """Initialize the XGBoost classifier with tuned hyperparameters."""
        self.model = XGBClassifier(
            n_estimators=300,
            learning_rate=0.05,
            max_depth=8,
            subsample=0.8,
            colsample_bytree=0.8,
            random_state=42,
            use_label_encoder=False,
            eval_metric="logloss"
        )

    def train(self, X_train, y_train):
        """Train the XGBoost model."""
        self.model.fit(X_train, y_train)
        print(" XGBoost training completed.")

    def evaluate(self, X_test, y_test):
        """Evaluate the model on test data."""
        y_pred = self.model.predict(X_test)
        acc = accuracy_score(y_test, y_pred)
        print(f"XGBoost Accuracy: {acc:.4f}")
        print(" Classification Report:\n", classification_report(y_test, y_pred))
        return acc

    def predict(self, X):
        """Predict class labels for input data."""
        return self.model.predict(X)

    def save(self, path="backend/models/saved/xgboost.pkl"):
        """Save the trained XGBoost model."""
        with open(path, "wb") as f:
            pickle.dump(self.model, f)
        print(f" XGBoost model saved successfully at: {path}")

    def load(self, path="backend/models/saved/xgboost.pkl"):
        """Load a saved XGBoost model."""
        with open(path, "rb") as f:
            self.model = pickle.load(f)
        print(f" XGBoost model loaded successfully from: {path}")
