import serial
import time

# Configure the serial port and baud rate
serial_port = "/dev/ttySC0"
baud_rate = 9600

# Command to be sent
uart_output_command = "7E000801000D00ABCD"
single_scanning_time_command = "7E000801000600ABCD"
command_mode_command = "7E0008010000D5ABCD"
reset_command = "7E00080100D950ABCD"

def main():
    try:
        scanned = False
        # Open the serial port
        with serial.Serial(serial_port, baud_rate, timeout=1) as ser:
            print(f"Connected to {serial_port} at {baud_rate} baud rate.")

            # Send the command
            print(f"Sending command: {command_mode_command}")
            ser.write(bytes.fromhex(command_mode_command))

            while True:
                # Read data from the serial port
                data = ser.readline().decode("utf-8").strip()
                # If data is received, print it
                if data:
                    print(f"Received data: {data}")
                    break

                # Wait for a short period before reading the next data
                time.sleep(0.1)

            # Send the command
            print(f"Sending command: {single_scanning_time_command}")
            ser.write(bytes.fromhex(single_scanning_time_command))

            while True:
                # Read data from the serial port
                data = ser.readline().decode("utf-8").strip()
                # If data is received, print it
                if data:
                    print(f"Received data: {data}")
                    break

                # Wait for a short period before reading the next data
                time.sleep(0.1)

            # Send the command
            print(f"Sending command: {uart_output_command}")
            ser.write(bytes.fromhex(uart_output_command))

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
