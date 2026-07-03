from http.server import BaseHTTPRequestHandler, HTTPServer
import sqlite3

HOST_NAME = '0.0.0.0'
PORT_NUMBER = 8080
DB_FILE = 'data.db'

class DataHandler(BaseHTTPRequestHandler):
    def do_GET(self):
        content_length = int(self.headers['Content-Length'])
        data = self.rfile.read(content_length).decode('utf-8')
        
        if data.startswith("SOUND:"):
            sound_value, latitude, longitude = parse_data(data)
            self.store_data(sound_value, latitude, longitude)
            self.send_response(200)
            self.end_headers()
            self.wfile.write(b'Data received and stored successfully')
        else:
            self.send_response(400)
            self.end_headers()
            self.wfile.write(b'Invalid data format')

    def store_data(self, sound_value, latitude, longitude):
        conn = sqlite3.connect(DB_FILE)
        cursor = conn.cursor()
        cursor.execute('''CREATE TABLE IF NOT EXISTS sensor_data
                          (id INTEGER PRIMARY KEY AUTOINCREMENT, sound INTEGER, latitude REAL, longitude REAL)''')
        cursor.execute('''INSERT INTO sensor_data (sound, latitude, longitude) VALUES (?, ?, ?)''', (sound_value, latitude, longitude))
        conn.commit()
        conn.close()

def parse_data(data):
    sound_str, gps_str = data.split(',')
    sound_value = int(sound_str.split(':')[1])
    latitude = float(gps_str.split(':')[1])
    longitude = float(gps_str.split(':')[2])
    return sound_value, latitude, longitude

if __name__ == '__main__':
    http_server = HTTPServer((HOST_NAME, PORT_NUMBER), DataHandler)
    print("Server started on http://{}:{}/".format(HOST_NAME, PORT_NUMBER))
    http_server.serve_forever()
