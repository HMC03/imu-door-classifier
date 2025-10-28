import os
import numpy as np
from libsvm.svmutil import svm_train, svm_save_model, svm_load_model, svm_predict
from pathlib import Path

CONFIG_DIR = Path(__file__).parent / "configs"
MODEL_FILE = CONFIG_DIR / "model.libsvm"
TRAINING_FILE = CONFIG_DIR / "training_data.csv"
os.makedirs(CONFIG_DIR, exist_ok=True)

def save_training_sample(feature, label):
    """Append a new sample to training data."""
    with open(TRAINING_FILE, "a") as f:
        f.write(f"{feature},{label}\n")

def load_training_data():
    if not TRAINING_FILE.exists():
        return [], []
    data = np.loadtxt(TRAINING_FILE, delimiter=",")
    if data.ndim == 1:
        data = np.expand_dims(data, axis=0)
    X = data[:, 0].tolist()
    y = data[:, 1].astype(int).tolist()
    return X, y

def train_model():
    """Train an SVM model from stored samples (0=closed, 1=open, 2=idle)."""
    X, y = load_training_data()
    if len(X) < 3:
        print("Not enough samples to train (need at least one per class).")
        return
    model = svm_train(y, [[x] for x in X], "-t 0 -c 1")  # linear kernel
    svm_save_model(str(MODEL_FILE), model)
    print(f"Model trained and saved to {MODEL_FILE}")

def load_model():
    if not MODEL_FILE.exists():
        print("Model not found. Train it first.")
        return None
    return svm_load_model(str(MODEL_FILE))

def predict(feature):
    model = load_model()
    if model is None:
        return None
    label, _, _ = svm_predict([0], [[feature]], model, "-q")
    return int(label[0])
