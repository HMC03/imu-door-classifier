# IMU Door Classifier 🚪📈

This project uses a **Raspberry Pi 5** and an **IMU sensor** to classify whether a door is **open** or **closed** using real-time motion data and a machine learning model. The Pi collects data from the IMU, classifies door state with an **SVM (Support Vector Machine)** model, and publishes the result to an **AWS IoT MQTT** endpoint.  
A connected **user device** (web app or mobile app) subscribes to this MQTT topic to display the current door status in real time.

---

## 🧩 System Overview

**Components:**
- **Raspberry Pi 5** — runs the data collection, classification, and MQTT publishing code
- **IMU (MPU6050)** — mounted on the door to measure motion and orientation
- **AWS IoT Core** — handles MQTT communication and data storage
- **User Device** — subscribes to the MQTT topic to visualize the door state

---

## 🔌 Hardware Setup


<img src="media/imu_circuit.png" width=80% height="auto">

| IMU | RPI | Function |
|------------|-----|----------|
| VCC | 5V | Power |
| GND | GND | Ground |
| SDA | GPIO 2 (Pin 3) | I²C data |
| SCL | GPIO 3 (Pin 5) | I²C clock |

---

## ⚙️ Software Overview

### Process Flow
1. **Data Acquisition**  
   The Pi continuously reads IMU acceleration and gyro data via I²C.
2. **Feature Extraction & Classification**  
   A trained **SVM model** processes IMU data to classify door state:
   - `open`
   - `closed`
3. **MQTT Publishing**  
   The result is published to an AWS IoT Core MQTT topic (e.g., `door/status`).
4. **User Interface**  
   The user device subscribes to the topic and updates the display in real time.

---

## 📦 Repository Structure
```text
imu-door-classifier/
├── src/
│   ├── imu_read.py              # IMU data acquisition script
│   ├── classifier.py            # SVM classifier logic
│   ├── mqtt_publisher.py        # Publishes messages to AWS MQTT
│   └── main.py                  # Combines all modules
├── models/
│   └── svm_model.pkl            # Trained SVM model
├── media/
│   └── connection_diagram.png   # Hardware connection diagram
├── README.md
└── requirements.txt
```
