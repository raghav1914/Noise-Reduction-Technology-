import serial
import pandas as pd
from twilio.rest import Client
import re

# Replace 'COM6' with the appropriate serial port name for your Arduino
# On Windows, it will be like 'COM3', and on Linux or Mac, it will be like '/dev/ttyUSB0'
ser = serial.Serial('COM6', 9600)

# Create an empty DataFrame to store the frequency data
data_df = pd.DataFrame(columns=["Frequency"])

# Set the frequency limit for sending SMS warnings
frequency_limit = 7000.0

# Twilio Account SID and Auth Token (replace with your own values)
twilio_account_sid = "AC3e0df36d720c75cb8e99fb9c6c75d9a2"
twilio_auth_token = "dfcff7747f27f01ac64d4f921ebd0d14"

# Twilio phone numbers (replace with your Twilio phone number and recipient phone number)
twilio_phone_number = "+15188737089"
recipient_phone_number = "+918005757690"

# Create a Twilio client
client = Client(twilio_account_sid, twilio_auth_token)

def is_float(value):
    try:
        float(value)
        return True
    except (ValueError, TypeError):
        return False

while True:
    try:
        # Read data from the Arduino
        raw_data = ser.readline()  # Read the raw bytes

        # Decode the raw data using 'latin-1' encoding
        decoded_data = raw_data.decode('latin-1').strip()
        print("Received raw data:", decoded_data)

        # Extract numeric frequency value from decoded_data using regular expression
        frequency_match = re.search(r'\d+\.\d+', decoded_data)
        
        if frequency_match:
            frequency = float(frequency_match.group())
            print("Received frequency:", frequency)

            # Add the frequency to the DataFrame
            data_df = data_df._append({"Frequency": frequency}, ignore_index=True)

            # Check if the frequency exceeds the limit
            if frequency > frequency_limit:
                # Send an SMS warning
                warning_message = f"Warning: Frequency exceeded {frequency_limit} Hz: {frequency} Hz!"
                client.messages.create(body=warning_message, from_=twilio_phone_number, to=recipient_phone_number)
                print("Warning SMS sent!")
        else:
            print("Invalid data received. Skipping this data point.")

    except KeyboardInterrupt:
        print("Exiting...")
        break

ser.close()  # Close the serial connection when done

# Save the DataFrame to a CSV file
data_df.to_csv("frequency_data.csv", index=False)

# Optional: Open the CSV file using Excel (requires Excel to be installed on your system)
try:
    import os
    os.system("start excel frequency_data.csv")
except:
    print("Unable to open the CSV file with Excel.")