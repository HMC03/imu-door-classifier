from pathlib import Path
import numpy as np
from libsvm.svmutil import svm_load_model, svm_predict

MODEL_PATH = Path(__file__).parent.parent / "models" / "svm_model.model"

class DoorClassifier:
    def __init__(self):
        """Load LIBSVM model or use placeholder heuristic."""
        if MODEL_PATH.exists():
            self.model = svm_load_model(str(MODEL_PATH))
            self.use_model = True
            print("[INFO] Loaded LIBSVM model.")
        else:
            self.model = None
            self.use_model = False
            print("[WARNING] No model found. Using heuristic classifier.")

    def extract_features(self, accel, gyro):
        """
        Convert raw IMU data (ax, ay, az, gx, gy, gz) to a feature vector.
        """
        ax, ay, az = accel
        gx, gy, gz = gyro

        accel_mag = np.sqrt(ax**2 + ay**2 + az**2)
        gyro_mag = np.sqrt(gx**2 + gy**2 + gz**2)

        # Feature vector for LIBSVM: simple 1D array
        return np.array([accel_mag, gyro_mag])

    def classify(self, accel, gyro):
        """
        Predicts the door state using the LIBSVM model.
        """
        features = self.extract_features(accel, gyro)

        if self.use_model:
            # LIBSVM expects a list of feature vectors
            p_label, p_acc, p_val = svm_predict([0], [features.tolist()], self.model, '-q')
            label = "open" if int(p_label[0]) == 1 else "closed"
        else:
            # Placeholder heuristic when model isn't available
            accel_mag = features[0]
            label = "open" if accel_mag > 1.1 else "closed"

        return label


if __name__ == "__main__":
    clf = DoorClassifier()

    # Simulated IMU samples
    accel_sample = (0.01, 0.05, 0.98)
    gyro_sample = (0.1, -0.3, 0.2)

    state = clf.classify(accel_sample, gyro_sample)
    print("Predicted door state:", state)