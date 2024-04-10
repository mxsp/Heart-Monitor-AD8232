
def get_data():
    import serial
    import subprocess
    import time
    # Configure serial port (adjust port name as needed)
    ser = serial.Serial('COM7', 9600)

    # Wait for the serial connection to establish
    ser.timeout = 2

    #ser.write(b'testcom.py\n')  # Send command to start the script

    while True:
        data = ser.readline().decode().strip()
        timestamp = time.time()
        return data, timestamp
    
print(get_data())