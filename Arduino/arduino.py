import serial.tools.list_ports
import sqlite3

# Find the Arduino Uno's serial port
def find_arduino_port():
    ports = list(serial.tools.list_ports.comports())
    for port in ports:
        if "Arduino Uno" in port.description:
            return port.device
    return None

# Establish a connection to the Arduino via serial port
arduino_port = find_arduino_port()
if arduino_port is None:
    print("Arduino Uno not found.")
    exit()

ser = serial.Serial(arduino_port, 9600)

# Connect to the SQLite database (you can replace 'frequency_data.db' with your preferred database name)
conn = sqlite3.connect('frequency_data.db')
cursor = conn.cursor()

# Create a table to store the data if it doesn't exist
cursor.execute('''CREATE TABLE IF NOT EXISTS frequency_data (
                    id INTEGER PRIMARY KEY AUTOINCREMENT,
                    frequency INTEGER,
                    latitude FLOAT,
                    longitude FLOAT)''')

def parse_data(data):
    parts = data.split(',')
    freq = int(parts[0].split(':')[1])
    lat = float(parts[1].split(':')[1])
    lon = float(parts[2].split(':')[1])
    return freq, lat, lon

while True:
    try:
        data = ser.readline().decode().strip()
        if data.startswith('FREQ:') and 'LAT:' in data and 'LON:' in data:
            freq, lat, lon = parse_data(data)
            print(f"Received: Frequency={freq}, Latitude={lat}, Longitude={lon}")
            
            # Insert the data into the database
            cursor.execute("INSERT INTO frequency_data (frequency, latitude, longitude) VALUES (?, ?, ?)", (freq, lat, lon))
            conn.commit()
    except KeyboardInterrupt:
        break

# Close the connection to the database and serial port
cursor.close()
conn.close()
ser.close()
