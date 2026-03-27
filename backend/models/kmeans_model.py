import pickle
from sklearn.cluster import KMeans
from sklearn.metrics import silhouette_score


class KMeansModel:
    def __init__(self):
        """Initialize K-Means model with default parameters."""
        self.model = KMeans(n_clusters=2, random_state=42)

    def train(self, X):
        """Train the K-Means model and print silhouette score."""
        self.model.fit(X)
        labels = self.model.labels_
        score = silhouette_score(X, labels)
        print(f" K-Means Silhouette Score: {score:.4f}")
        return score

    def evaluate(self, X):
        """
        Evaluate K-Means using silhouette score.
        This method allows consistent use across models in train.py.
        """
        labels = self.model.predict(X)
        score = silhouette_score(X, labels)
        print(f"K-Means Evaluation Silhouette Score: {score:.4f}")
        return score

    def predict(self, X):
        """Predict cluster assignments for input data."""
        return self.model.predict(X)

    def save(self, path="backend/models/saved/kmeans.pkl"):
        """Save the trained K-Means model."""
        with open(path, "wb") as f:
            pickle.dump(self.model, f)
        print(f"K-Means model saved successfully at: {path}")

    def load(self, path="backend/models/saved/kmeans.pkl"):
        """Load a saved K-Means model."""
        with open(path, "rb") as f:
            self.model = pickle.load(f)
        print(f"K-Means model loaded successfully from: {path}")
