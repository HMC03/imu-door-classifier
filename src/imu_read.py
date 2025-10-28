import smbus
import time
import json
import numpy as np
import os

# MPU6050 registers
PWR_MGMT_1 = 0x6B
GYRO_YOUT_H = 0x45

ADDRESS = 0x68
bus = smbus.SMBus(1)

# Initialize IMU
bus.write_byte_data(ADDRESS, PWR_MGMT_1, 0)

CALIBRATION_FILE = "configs/calibration.json"

def read_word_2c(adr):
    high = bus.read_byte_data(ADDRESS, adr)
    low = bus.read_byte_data(ADDRESS, adr + 1)
    val = (high << 8) + low
    if val >= 0x8000:
        val = -((65535 - val) + 1)
    return val

def read_gyro_y():
    """Reads the Y-axis gyro value (°/s)."""
    raw_gyro_y = read_word_2c(GYRO_YOUT_H)
    return raw_gyro_y / 131.0  # MPU6050 scale factor

def calibrate(duration=3.0):
    """Averages gyro_y over duration seconds and saves calibration offset."""
    print(f"Calibrating for {duration}s...")
    start = time.time()
    samples = []
    while time.time() - start < duration:
        samples.append(read_gyro_y())
        time.sleep(0.01)
    offset = float(np.mean(samples))
    os.makedirs("configs", exist_ok=True)
    with open(CALIBRATION_FILE, "w") as f:
        json.dump({"gyro_y_offset": offset}, f)
    print(f"Calibration complete. Offset: {offset:.4f}")

def load_calibration():
    if os.path.exists(CALIBRATION_FILE):
        with open(CALIBRATION_FILE, "r") as f:
            return json.load(f)
    return {"gyro_y_offset": 0.0}

def read_window(window_time=1.0, calibration=None):
    """Accumulates gyro_y readings over a window_time period."""
    if calibration is None:
        calibration = load_calibration()
    offset = calibration["gyro_y_offset"]

    start = time.time()
    readings = []
    while time.time() - start < window_time:
        gyro_y = read_gyro_y() - offset
        readings.append(gyro_y)
        time.sleep(0.01)
    return np.sum(readings)