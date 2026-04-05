import librosa
import numpy as np

def preprocess_audio(file_path, target_sr=16000, duration=3):
    """
    Preprocess audio:
    - Load audio
    - Normalize
    - Trim silence
    - Pad / truncate to fixed duration
    """

    # Load audio
    audio, sr = librosa.load(file_path, sr=target_sr)

    # Trim silence
    audio, _ = librosa.effects.trim(audio)

    # Normalize safely (avoid division by zero on near-silent clips)
    peak = np.max(np.abs(audio))
    if peak > 0:
        audio = audio / peak

    # Fix length (padding or truncating)
    max_length = target_sr * duration

    if len(audio) > max_length:
        audio = audio[:max_length]
    else:
        padding = max_length - len(audio)
        audio = np.pad(audio, (0, padding), mode='constant')

    return audio
