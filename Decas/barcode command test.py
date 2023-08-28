import serial
import time

# Configure the serial port and baud rate
serial_port = "/dev/ttySC0"
baud_rate = 9600

# Command to be sent
reset_command = "7E 00 08 02 00 D9 50 AB CD"
command = "7E 00 08 01 00 02 01 AB CD"
command_bytes = bytes.fromhex(reset_command.replace(" ", ""))

def main():
    try:
        scanned = False
        # Open the serial port
        with serial.Serial(serial_port, baud_rate, timeout=1) as ser:
            print(f"Connected to {serial_port} at {baud_rate} baud rate.")

            # Send the command
            print(f"Sending command: {reset_command}")
            ser.write(command_bytes)

            while True:
                # Read data from the serial port
                data = ser.readline().decode("utf-8").strip()
                # If data is received, print it
                if data:
                    print(f"Received data: {data}")
                    break

                # Wait for a short period before reading the next data
                time.sleep(0.1)

    except KeyboardInterrupt:
        print("Exiting the program.")

    except Exception as e:
        print(f"Error: {e}")

if __name__ == "__main__":
    main()
