import numpy as np
import joblib
import os

from sklearn.model_selection import train_test_split
from sklearn.metrics import accuracy_score, classification_report

from sklearn.ensemble import RandomForestClassifier
from sklearn.linear_model import LogisticRegression

from xgboost import XGBClassifier


# Load dataset
X = np.load("X_train.npy")
y = np.load("y_train.npy")

print("Dataset Loaded:", X.shape)


# Split data
X_train, X_val, y_train, y_val = train_test_split(
    X, y,
    test_size=0.2,
    random_state=42,
    stratify=y
)


# Create models
models = {

    "RandomForest": RandomForestClassifier(
        n_estimators=200,
        random_state=42,
        n_jobs=-1
    ),

    "LogisticRegression": LogisticRegression(
        max_iter=500
    ),

    "XGBoost": XGBClassifier(
        n_estimators=200,
        learning_rate=0.1,
        max_depth=6,
        eval_metric="logloss"
    )

}


# Create models folder
os.makedirs("models", exist_ok=True)


# Train and evaluate
for name, model in models.items():

    print("\n=======================")
    print("Training", name)
    print("=======================")

    model.fit(X_train, y_train)

    y_pred = model.predict(X_val)

    acc = accuracy_score(y_val, y_pred)

    print("Accuracy:", acc * 100)

    print(classification_report(y_val, y_pred))


    # Save model
    joblib.dump(model, f"models/{name}_model.pkl")

print("\nAll models trained and saved.")