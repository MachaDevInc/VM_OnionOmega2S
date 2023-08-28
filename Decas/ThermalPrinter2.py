import smbus
import time

# Define I2C bus number and device address of SC16IS752IPW
bus_num = 1
device_address = 0x4d

# Initialize I2C bus
bus = smbus.SMBus(bus_num)

# Set up printer
def setup_printer():
    # Send reset signal to printer
    bus.write_byte(device_address, 27)
    bus.write_byte(device_address, 64)

    # Set printing density and speed
    bus.write_byte(device_address, 18)
    bus.write_byte(device_address, 42)

    # Set character size
    bus.write_byte(device_address, 29)
    bus.write_byte(device_address, 33)
    bus.write_byte(device_address, 0)

# Print text
def print_text(text):
    # Convert text to byte array
    bytes_to_send = bytearray(text.encode())

    # Send bytes to printer
    for b in bytes_to_send:
        bus.write_byte(device_address, b)
        time.sleep(0.005) # Wait for printer to process data

# Example usage
setup_printer()
print_text("Hello, World!\n")