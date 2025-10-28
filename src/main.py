import time
from imu_read import read_window, calibrate
from classifier import predict, save_training_sample, train_model
from mqtt_publisher import connect_mqtt, publish_door_state

# Window and sample settings
WINDOW_DURATION = 3.0  # seconds, change to 2.0 or 3.0 if desired
SAMPLE_RATE = 50       # samples per second

def main():
    print("\nIMU Door Classifier")
    print("===================")
    print("Options:")
    print("1. Calibrate IMU")
    print("2. Train Model")
    print("3. Run Detection")
    choice = input("Select an option: ")

    if choice == "1":
        calibrate(WINDOW_DURATION)

    elif choice == "2":
        print("Training mode: label states as 0=closed, 1=open, 2=idle, q=quit")
        while True:
            label = input("Label this state (0/1/2/q): ")
            if label.lower() == "q":
                break
            print("Recording window...")
            feature = read_window(window_sec=WINDOW_DURATION, sample_rate=SAMPLE_RATE)
            save_training_sample(feature, int(label))
            print(f"Saved sample: feature={feature:.3f}, label={label}")
        train_model()

    elif choice == "3":
        # Connect to AWS MQTT
        mqtt_connection = connect_mqtt()
        prev_state = None

        while True:
            feature = read_window(window_sec=WINDOW_DURATION, sample_rate=SAMPLE_RATE)
            state = predict(feature)
            if state is None:
                continue

            # Only announce transitions (ignore 'idle')
            if state != prev_state and state != 2:
                if state == 1:
                    print("Door opened!")
                    publish_door_state(mqtt_connection, "open")
                elif state == 0:
                    print("Door closed!")
                    publish_door_state(mqtt_connection, "closed")
                prev_state = state

            time.sleep(0.5)
    else:
        print("Invalid option.")

if __name__ == "__main__":
    main()