import smbus
import time
import json
from pathlib import Path
import numpy as np
import os

# Paths
CONFIG_DIR = Path(__file__).parent / "configs"
CALIBRATION_FILE = CONFIG_DIR / "calibration.json"
os.makedirs(CONFIG_DIR, exist_ok=True)

# MPU6050 setup
bus = smbus.SMBus(1)
ADDRESS = 0x68
PWR_MGMT_1 = 0x6B
GYRO_YOUT_H = 0x45
bus.write_byte_data(ADDRESS, PWR_MGMT_1, 0)

def read_word_2c(adr):
    high = bus.read_byte_data(ADDRESS, adr)
    low = bus.read_byte_data(ADDRESS, adr + 1)
    val = (high << 8) + low
    if val >= 0x8000:
        val = -((65535 - val) + 1)
    return val

def read_gyro_y():
    """Read raw Y-axis gyro value in °/s."""
    raw = read_word_2c(GYRO_YOUT_H)
    return raw / 131.0

def calibrate(duration=3.0):
    """Calibrate IMU by averaging gyro_y over duration seconds."""
    print(f"Calibrating for {duration:.1f}s...")
    samples = []
    start = time.time()
    while time.time() - start < duration:
        samples.append(read_gyro_y())
        time.sleep(0.01)
    offset = float(np.mean(samples))
    with open(CALIBRATION_FILE, "w") as f:
        json.dump({"gyro_y_offset": offset}, f)
    print(f"Calibration complete. Offset: {offset:.4f}")

def load_calibration():
    if CALIBRATION_FILE.exists():
        with open(CALIBRATION_FILE, "r") as f:
            return json.load(f).get("gyro_y_offset", 0.0)
    return 0.0

def read_window(window_sec=1.0, sample_rate=50):
    """Sum of calibrated gyro_y values over a window."""
    offset = load_calibration()
    num_samples = int(window_sec * sample_rate)
    total = 0.0
    for _ in range(num_samples):
        gyro_y = read_gyro_y() - offset
        total += gyro_y
        time.sleep(1 / sample_rate)
    return total