import librosa
import numpy as np

def extract_mfcc(audio, sr=16000, n_mfcc=40):
    """
    Extract MFCC features from preprocessed audio
    """

    mfcc = librosa.feature.mfcc(
        y=audio,
        sr=sr,
        n_mfcc=n_mfcc
    )

    # Normalize MFCC
    mfcc = (mfcc - np.mean(mfcc)) / np.std(mfcc)

    return mfcc
