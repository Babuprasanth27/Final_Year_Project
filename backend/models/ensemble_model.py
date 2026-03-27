import numpy as np
from scipy.stats import mode


class EnsembleModel:
    def __init__(self, models):
        """Initialize the ensemble with a list of trained models."""
        self.models = models

    def predict(self, X):
        """Predict using majority voting across all models."""
        preds = [m.predict(X) for m in self.models]
        preds = np.array(preds)

        # Use scipy's mode to get majority prediction
        final_pred, _ = mode(preds, axis=0, keepdims=True)

        return final_pred.flatten()
