import pickle
from sklearn.ensemble import RandomForestClassifier
from sklearn.metrics import accuracy_score, classification_report


class RandomForestModel:
    def __init__(self):
        """Initialize the Random Forest classifier."""
        self.model = RandomForestClassifier(
            n_estimators=200,
            max_depth=12,
            random_state=42
        )

    def train(self, X_train, y_train):
        """Train the Random Forest model."""
        self.model.fit(X_train, y_train)
        print(" Random Forest training completed.")

    def evaluate(self, X_test, y_test):
        """Evaluate the model on test data."""
        y_pred = self.model.predict(X_test)
        acc = accuracy_score(y_test, y_pred)
        print(f" Random Forest Accuracy: {acc:.4f}")
        print(" Classification Report:\n", classification_report(y_test, y_pred))
        return acc

    def predict(self, X):
        """Predict class labels for input data."""
        return self.model.predict(X)

    def save(self, path="backend/models/saved/random_forest.pkl"):
        """Save the trained model."""
        with open(path, "wb") as f:
            pickle.dump(self.model, f)
        print(f" Random Forest model saved successfully at: {path}")

    def load(self, path="backend/models/saved/random_forest.pkl"):
        """Load a saved Random Forest model."""
        with open(path, "rb") as f:
            self.model = pickle.load(f)
        print(f" Random Forest model loaded successfully from: {path}")
