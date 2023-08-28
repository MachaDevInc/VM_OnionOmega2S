import time
import smbus2
import serial
from smbus2 import SMBusWrapper

# SC16IS752 I2C address and registers
I2C_ADDR = 0x4D
REG_LCR = 0x03
REG_DLL = 0x00
REG_DLH = 0x01
REG_FCR = 0x02
REG_EFR = 0x02
REG_MCR = 0x04

# I2C bus and UART channel
I2C_BUS = 1
UART_CHANNEL = 1

# Baud rate for thermal printer
BAUD_RATE = 9600

def write_register(bus, register, value):
    bus.write_byte_data(I2C_ADDR, (UART_CHANNEL << 7) | register, value)

def setup_uart(bus):
    # Enable enhanced functions
    write_register(bus, REG_LCR, 0xBF)
    write_register(bus, REG_EFR, 0x10)
    
    # Set baud rate
    write_register(bus, REG_LCR, 0x80)
    baud_divisor = int(14745600 / (BAUD_RATE * 16))
    write_register(bus, REG_DLL, baud_divisor & 0xFF)
    write_register(bus, REG_DLH, (baud_divisor >> 8) & 0xFF)
    
    # Set 8N1 frame format
    write_register(bus, REG_LCR, 0x03)
    
    # Enable FIFO
    write_register(bus, REG_FCR, 0x07)
    
    # Set flow control
    write_register(bus, REG_EFR, 0x90)
    
    # Enable UART
    write_register(bus, REG_MCR, 0x0B)

def main():
    with SMBusWrapper(I2C_BUS) as bus:
        setup_uart(bus)
        ser = serial.Serial('/dev/ttySC1', BAUD_RATE)
        ser.write(b'\x1B\x40')  # Initialize printer
        time.sleep(0.5)

        # Print text
        ser.write(b'Hello, world!\n')
        
        # Print a barcode
        ser.write(b'\x1D\x6B\x02')  # Barcode type: CODE93
        ser.write(b'12345678')       # Barcode data
        ser.write(b'\x00')           # Null terminator
        
        ser.write(b'\n\n\n')         # Feed paper
        ser.close()

if __name__ == "__main__":
    main()