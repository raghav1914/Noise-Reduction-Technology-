import serial

# Replace 'COMX' with the appropriate serial port name for your Arduino
# On Windows, it will be like 'COM3', and on Linux or Mac, it will be like '/dev/ttyUSB0'
ser = serial.Serial('COM4', 9600) 

while True:
    try:
        # Read data from the Arduino
        data = ser.readline().decode().strip()
        print("Received data from Arduino:", data)

    except KeyboardInterrupt:
        print("Exiting...")
        break

ser.close() # Close the serial connection when done