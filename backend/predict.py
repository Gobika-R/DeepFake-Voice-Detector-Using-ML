import librosa
import numpy as np
import joblib
import os

try:
    from preprocessing.audio_preprocess import preprocess_audio
except ModuleNotFoundError as exc:
    if exc.name != "preprocessing":
        raise
    from backend.preprocessing.audio_preprocess import preprocess_audio

BASE_DIR = os.path.dirname(os.path.abspath(__file__))
MODEL_PATH = os.path.join(BASE_DIR, "models", "deepfake_audio_model.pkl")
model = None


def get_model():
    global model
    if model is None:
        if not os.path.exists(MODEL_PATH):
            raise FileNotFoundError(f"Model not found at {MODEL_PATH}")
        model = joblib.load(MODEL_PATH)
    return model

def extract_mfcc(file_path, n_mfcc=40):
    if not os.path.exists(file_path):
        raise FileNotFoundError(f"Audio file not found: {file_path}")

    # Keep inference bounded and consistent on cloud instances.
    sr = 16000
    audio = preprocess_audio(file_path, target_sr=sr, duration=3)

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
