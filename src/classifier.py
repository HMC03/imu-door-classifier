import os
import numpy as np
from libsvm.svmutil import svm_train, svm_save_model, svm_load_model, svm_predict

MODEL_FILE = "configs/model.libsvm"
TRAINING_FILE = "configs/training_data.csv"

def save_training_sample(feature, label):
    """Append a new sample to training data."""
    os.makedirs("configs", exist_ok=True)
    with open(TRAINING_FILE, "a") as f:
        f.write(f"{feature},{label}\n")

def load_training_data():
    if not os.path.exists(TRAINING_FILE):
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
    os.makedirs("configs", exist_ok=True)
    svm_save_model(MODEL_FILE, model)
    print(f"Model trained and saved to {MODEL_FILE}")

def load_model():
    if not os.path.exists(MODEL_FILE):
        print("Model not found. Train it first.")
        return None
    return svm_load_model(MODEL_FILE)

def predict(feature):
    model = load_model()
    if model is None:
        return None
    label, _, _ = svm_predict([0], [[feature]], model, "-q")
    return int(label[0])