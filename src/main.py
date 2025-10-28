import time
from imu_read import read_window, calibrate
from classifier import predict, save_training_sample, train_model

def main():
    print("\nIMU Door Classifier")
    print("===================")
    print("Options:")
    print("1. Calibrate IMU")
    print("2. Train Model")
    print("3. Run Detection")
    choice = input("Select an option: ")

    if choice == "1":
        calibrate()
    elif choice == "2":
        while True:
            label = input("Label this state (0=closed, 1=open, q=quit): ")
            if label.lower() == "q":
                break
            print("Recording window...")
            feature = read_window(1.0)
            save_training_sample(feature, label)
            print(f"Saved sample: feature={feature:.3f}, label={label}")
        train_model()
    elif choice == "3":
        prev_state = None
        while True:
            feature = read_window(1.0)
            state = predict(feature)
            if state is not None and state != prev_state:
                if state == 1:
                    print("Door opened!")
                else:
                    print("Door closed!")
                prev_state = state
            time.sleep(0.5)
    else:
        print("Invalid option.")

if __name__ == "__main__":
    main()