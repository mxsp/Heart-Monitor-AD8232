import time
import spidev

# Initialize SPI communication
spi = spidev.SpiDev()
spi.open(0, 0)  # Use SPI bus 0, device 0
spi.max_speed_hz = 500000  # Set SPI speed (adjust as needed)

def read_ecg_value():
    # Read raw ECG data from AD8232
    raw_data = spi.xfer2([0x00, 0x00])
    ecg_value = (raw_data[0] << 8) | raw_data[1]
    return ecg_value

try:
    while True:
        timestamp = int(time.time())  # Get current timestamp
        ecg_value = read_ecg_value()
        print(f"Timestamp: {timestamp}, ECG Value: {ecg_value}")
        time.sleep(1)  # Read data every second

except KeyboardInterrupt:
    print("Exiting...")

finally:
    spi.close()  # Close SPI communication
