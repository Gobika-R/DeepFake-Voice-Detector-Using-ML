import librosa
import numpy as np
import joblib
import os

BASE_DIR = os.path.dirname(os.path.abspath(__file__))
MODEL_PATH = os.path.join(BASE_DIR, "models", "deepfake_audio_model.pkl")
model = None


def get_model():
    global model
    if model is None:
        model = joblib.load(MODEL_PATH)
    return model

def extract_mfcc(file_path, n_mfcc=40):
    audio, sr = librosa.load(file_path, sr=None)
    mfcc = librosa.feature.mfcc(y=audio, sr=sr, n_mfcc=n_mfcc)
    mfcc_mean = np.mean(mfcc.T, axis=0)
    return mfcc_mean.reshape(1, -1)


def predict_audio(file_path):
    features = extract_mfcc(file_path)
    loaded_model = get_model()
    prediction = loaded_model.predict(features)[0]
    probability = loaded_model.predict_proba(features)[0]

    label = "FAKE" if prediction == 1 else "REAL"
    confidence = max(probability) * 100

    return label, round(confidence, 2)
