import serial

def setup():
    global port
    global baudrate
    global serial_connection
    # Configure the serial connection
    port = "/dev/cu.usbmodem11201"  # Adjust the port to match your setup
    baudrate = 115200
    serial_connection = serial.Serial(port, baudrate)

# Read data from the Pico and write it directly to your program
while True:
    data = serial_connection.read(128)  # Adjust the buffer size as needed
    if data:
        # Process the data in your program (e.g., store it in a list, analyze it, etc.)
        print(data.decode())  # Example: Print the received data
