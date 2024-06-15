import serial
import pynmea2

# Configuration for the serial connection
SERIAL_PORT = '/dev/ttyUSB0'  # Adjust based on your GPS module connection
BAUD_RATE = 4800  # Common baud rate for GPS devices

def read_gps_data(port):
    """
    Reads data from the GPS device over serial port.
    
    Args:
        port (serial.Serial): The serial port connected to the GPS device.
    
    Returns:
        str: Raw NMEA sentence or None if no data is available.
    """
    try:
        data = port.readline().decode('utf-8')
        if data:
            return data.strip()
        return None
    except serial.SerialException as e:
        print(f"Error reading data: {e}")
        return None

def parse_gps_data(nmea_sentence):
    """
    Parses NMEA sentence and extracts GPS data.
    
    Args:
        nmea_sentence (str): NMEA sentence.
    
    Returns:
        pynmea2.Msg: Parsed NMEA object or None if parsing fails.
    """
    try:
        msg = pynmea2.parse(nmea_sentence)
        return msg
    except pynmea2.ParseError as e:
        print(f"Error parsing NMEA sentence: {e}")
        return None

def main():
    # Setup serial connection
    with serial.Serial(SERIAL_PORT, BAUD_RATE, timeout=1) as ser:
        try:
            while True:
                nmea_data = read_gps_data(ser)
                if nmea_data:
                    gps_info = parse_gps_data(nmea_data)
                    if gps_info:
                        print(f"Latitude: {gps_info.latitude}, Longitude: {gps_info.longitude}")
        except KeyboardInterrupt:
            print("Program terminated by user.")

if __name__ == "__main__":
    main()
