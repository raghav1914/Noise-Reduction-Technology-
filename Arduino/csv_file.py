import serial
import pandas as pd
import re

# Replace 'COM6' with the appropriate serial port name for your Arduino
# On Windows, it will be like 'COM3', and on Linux or Mac, it will be like '/dev/ttyUSB0'
ser = serial.Serial('COM6', 9600)

# Create an empty DataFrame to store the frequency data
data_df = pd.DataFrame(columns=["Frequency"])

while True:
    try:
        # Read data from the Arduino
        raw_data = ser.readline()
        decoded_data = raw_data.decode('latin-1').strip()
        print("Received data from Arduino:", decoded_data)

        # Use regular expression to extract numeric value
        float_value_match = re.search(r'\d+\.\d+', decoded_data)
        if float_value_match:
            frequency = float(float_value_match.group())
            print("Received frequency:", frequency)

            # Add the frequency to the DataFrame
            
            data_df = data_df._append({"Frequency": frequency}, ignore_index=True)



    except KeyboardInterrupt:               #press ctrl+c to exit
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
