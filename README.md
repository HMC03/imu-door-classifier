# IMU Door Classifier

This project uses a **Raspberry Pi 5** and an **IMU sensor** to classify whether a door is **open** or **closed** using real-time motion data and a **Support Vector Machine (SVM)** model.  
The Pi collects data from the IMU, classifies the door state with **LibSVM**, and publishes the result to **AWS IoT Core** via **MQTT**.  
A connected **user device** (web or mobile) subscribes to the MQTT topic to display the current door status in real time.


## System Overview

**Components**
- **Raspberry Pi 5** — runs IMU data collection, SVM classification, and MQTT publishing  
- **IMU (e.g., MPU6050)** — mounted on the door to measure acceleration and angular velocity  
- **AWS IoT Core** — handles MQTT message routing and storage  
- **User Device** — subscribes to the MQTT topic to visualize door state


## Hardware Setup

<img src="media/imu_circuit.png" width="80%" height="auto">

| IMU | RPi Pin | Function |
|-----|----------|----------|
| VCC | 5V | Power |
| GND | GND | Ground |
| SDA | GPIO 2 (Pin 3) | I²C Data |
| SCL | GPIO 3 (Pin 5) | I²C Clock |


## Software Overview

### Workflow
1. **Data Acquisition**  
   The Raspberry Pi reads IMU acceleration and gyro data via I²C at ~10 Hz.
2. **Feature Extraction & Classification**  
   The SVM model (via [LibSVM](https://www.csie.ntu.edu.tw/~cjlin/libsvm/)) processes the IMU data to predict whether the door is:
   - `open`
   - `closed`
3. **MQTT Publishing (Coming Soon)**  
   The predicted door state will be published to an AWS IoT Core topic `door/status`.
4. **User Interface (Future Work)**  
   A connected web or mobile client will subscribe to the MQTT topic and display the door’s state in real time.

---

## Repository Structure
```text
imu-door-classifier/
├── src/
│   ├── imu_read.py              # IMU data acquisition script
│   ├── classifier.py            # SVM classifier logic (LibSVM-based)
│   ├── mqtt_publisher.py        # Publishes door state to AWS MQTT (WIP)
│   └── main.py                  # Integrates all modules (WIP)
├── models/
│   └── svm_model.pkl            # Trained SVM model (placeholder)
├── media/
│   └── imu_circuit.png          # IMU-to-RPi wiring diagram
├── README.md
└── requirements.txt
```

## Instalation and Setup

1. Clone the Repository
    ```bash
    git clone https://github.com/<your-username>/imu-door-classifier.git
    cd imu-door-classifier
    ```
2. Create and Activate a Virtual Environment
    ```bash
    python3 -m venv .venv
    source .venv/bin/activate
    ```
3. Install Dependencies
    ```bash
    pip install -r requirements.txt
    ```

## Dependencies
| Package           | Purpose                                       |
| ----------------- | --------------------------------------------- |
| `numpy`           | Numeric operations and feature handling       |
| `libsvm-official` | Official Python bindings for LibSVM           |
| `scipy`           | Required by LibSVM for numerical optimization |
| `paho-mqtt`       | MQTT communication with AWS IoT     |
