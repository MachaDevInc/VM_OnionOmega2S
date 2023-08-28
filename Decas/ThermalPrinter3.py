import smbus2
import time

# I2C address of the SC16IS752IPW
I2C_ADDRESS = 0x4d

# Register addresses for the second UART of SC16IS752IPW
LSR_REG = 0x0d
THR_REG = 0x0b

# Open an I2C connection to the SC16IS752IPW
i2c = smbus2.SMBus(1)

def write_to_printer(data):
    # Write data to the second UART of SC16IS752IPW
    i2c.write_byte_data(I2C_ADDRESS, THR_REG, data)

    # Wait for the data to be sent to the printer
    while i2c.read_byte_data(I2C_ADDRESS, LSR_REG) & 0x20 == 0:
        time.sleep(0.001)

# Example usage
write_to_printer(b'Hello, world!\n')