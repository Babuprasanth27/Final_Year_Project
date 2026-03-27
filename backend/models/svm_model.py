import pickle
from sklearn.svm import SVC
from sklearn.metrics import accuracy_score, classification_report


class SVMModel:
    def __init__(self):
        """Initialize the Support Vector Machine model."""
        self.model = SVC(
            kernel='rbf',
            C=1,
            gamma='scale',
            probability=True,
            random_state=42
        )

    def train(self, X_train, y_train):
        """Train the SVM model."""
        self.model.fit(X_train, y_train)
        print(" SVM training completed.")

    def evaluate(self, X_test, y_test):
        """Evaluate the SVM model on test data."""
        y_pred = self.model.predict(X_test)
        acc = accuracy_score(y_test, y_pred)
        print(f" SVM Accuracy: {acc:.4f}")
        print(" Classification Report:\n", classification_report(y_test, y_pred))
        return acc

    def predict(self, X):
        """Predict class labels for input data."""
        return self.model.predict(X)

    def save(self, path="backend/models/saved/svm.pkl"):
        """Save the trained SVM model."""
        with open(path, "wb") as f:
            pickle.dump(self.model, f)
        print(f" SVM model saved successfully at: {path}")

    def load(self, path="backend/models/saved/svm.pkl"):
        """Load a saved SVM model."""
        with open(path, "rb") as f:
            self.model = pickle.load(f)
        print(f" SVM model loaded successfully from: {path}")
