import smbus
import time

# Initialize I2C bus
bus = smbus.SMBus(1)
address = 0x68  # Default I2C address for MPU6050

# MPU6050 register addresses
PWR_MGMT_1 = 0x6B
ACCEL_XOUT_H = 0x3B
GYRO_XOUT_H = 0x43

# Wake up the MPU6050 (it starts in sleep mode)
bus.write_byte_data(address, PWR_MGMT_1, 0)

def read_word_2c(adr):
    high = bus.read_byte_data(address, adr)
    low = bus.read_byte_data(address, adr + 1)
    val = (high << 8) + low
    if val >= 0x8000:
        val = -((65535 - val) + 1)
    return val

try:
    while True:
        # Read accelerometer values
        accel_x = read_word_2c(ACCEL_XOUT_H) / 16384.0
        accel_y = read_word_2c(ACCEL_XOUT_H + 2) / 16384.0
        accel_z = read_word_2c(ACCEL_XOUT_H + 4) / 16384.0

        # Read gyroscope values
        gyro_x = read_word_2c(GYRO_XOUT_H) / 131.0
        gyro_y = read_word_2c(GYRO_XOUT_H + 2) / 131.0
        gyro_z = read_word_2c(GYRO_XOUT_H + 4) / 131.0

        print(f"Accel (g): X={accel_x:.2f}, Y={accel_y:.2f}, Z={accel_z:.2f} | "
              f"Gyro (°/s): X={gyro_x:.2f}, Y={gyro_y:.2f}, Z={gyro_z:.2f}")
        time.sleep(0.1)

except KeyboardInterrupt:
    print("\nStopped.")