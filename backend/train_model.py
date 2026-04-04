import numpy as np
from sklearn.ensemble import RandomForestClassifier
from sklearn.metrics import accuracy_score, classification_report
from sklearn.model_selection import train_test_split
import joblib
import os

# Load extracted features
X = np.load("X_train.npy")
y = np.load("y_train.npy")

print("Loaded features:", X.shape)
print("Loaded labels:", y.shape)

# Split into train & validation (extra safety)
X_train, X_val, y_train, y_val = train_test_split(
    X, y, test_size=0.2, random_state=42, stratify=y
)

# Initialize model
model = RandomForestClassifier(
    n_estimators=200,
    random_state=42,
    n_jobs=-1
)

# Train model
print("Training model...")
model.fit(X_train, y_train)

# Evaluate
y_pred = model.predict(X_val)

accuracy = accuracy_score(y_val, y_pred)
print(f"Validation Accuracy: {accuracy * 100:.2f}%")

print("\nClassification Report:")
print(classification_report(y_val, y_pred))

# Save model
os.makedirs("models", exist_ok=True)
joblib.dump(model, "models/deepfake_audio_model.pkl")

print("Model saved at models/deepfake_audio_model.pkl")
