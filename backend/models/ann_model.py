import tensorflow as tf
from tensorflow.keras import layers, models
import numpy as np
from sklearn.metrics import accuracy_score, classification_report

class ANNModel:
    def __init__(self, input_dim, num_classes):
        """Initialize the Artificial Neural Network model."""
        self.model = models.Sequential([
            layers.Dense(128, activation='relu', input_shape=(input_dim,)),
            layers.Dropout(0.3),
            layers.Dense(64, activation='relu'),
            layers.Dense(num_classes, activation='softmax')
        ])

        self.model.compile(
            optimizer='adam',
            loss='sparse_categorical_crossentropy',
            metrics=['accuracy']
        )

    def train(self, X_train, y_train, X_test, y_test, epochs=20, batch_size=32):
        """Train the ANN model and evaluate accuracy."""
        history = self.model.fit(
            X_train, y_train,
            validation_data=(X_test, y_test),
            epochs=epochs,
            batch_size=batch_size,
            verbose=1
        )

        _, acc = self.model.evaluate(X_test, y_test, verbose=0)
        print(f" ANN Accuracy: {acc:.4f}")
        return acc, history

    def evaluate(self, X_test, y_test):
        """Evaluate ANN model and print accuracy + classification report."""
        y_pred_prob = self.model.predict(X_test)
        y_pred = np.argmax(y_pred_prob, axis=1)
        acc = accuracy_score(y_test, y_pred)

        print(f" ANN Accuracy: {acc:.4f}")
        print(" Classification Report:")
        print(classification_report(y_test, y_pred))

        return acc

    def predict(self, X):
        """Predict the class labels for input data."""
        preds = self.model.predict(X)
        return preds.argmax(axis=1)

    def save(self, path="backend/models/saved/ann_model.h5"):
        """Save the trained ANN model."""
        self.model.save(path)
        print(f" ANN model saved successfully at: {path}")

    def load(self, path="backend/models/saved/ann_model.h5"):
        """Load a saved ANN model."""
        self.model = tf.keras.models.load_model(path)
        print(f" ANN model loaded successfully from: {path}")
