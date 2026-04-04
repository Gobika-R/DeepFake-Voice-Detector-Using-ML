import librosa
import numpy as np
import os

def extract_mfcc(file_path, n_mfcc=40):
    try:
        audio, sr = librosa.load(file_path, sr=None)
        mfcc = librosa.feature.mfcc(y=audio, sr=sr, n_mfcc=n_mfcc)
        mfcc_mean = np.mean(mfcc.T, axis=0)
        return mfcc_mean
    except Exception as e:
        print(f"Error processing {file_path}: {e}")
        return None


def load_dataset(dataset_path):
    X = []
    y = []

    for label, folder in enumerate(["real", "fake"]):
        folder_path = os.path.join(dataset_path, folder)

        for file in os.listdir(folder_path):
            if file.endswith(".wav"):
                file_path = os.path.join(folder_path, file)
                features = extract_mfcc(file_path)

                if features is not None:
                    X.append(features)
                    y.append(label)

    return np.array(X), np.array(y)


if __name__ == "__main__":
    dataset_dir = "../dataset/for-2seconds/training"
    X, y = load_dataset(dataset_dir)

    np.save("X_train.npy", X)
    np.save("y_train.npy", y)

    print("Training features saved!")
    print("X shape:", X.shape)
    print("y shape:", y.shape)

