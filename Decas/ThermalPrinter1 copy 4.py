import Adafruit_Thermal
import time
import smbus

# Set up I2C bus
bus = smbus.SMBus(1)  # Use I2C bus 1

# Set up UART-B over SC16IS752IPW
SC16IS752_ADDRESS = 0x4D  # Address of SC16IS752IPW on I2C bus
SC16IS752_LCR = 0x03  # Line Control Register for 8N1 mode
SC16IS752_DLL = 0x00  # Divisor Latch LSB for 9600 baud rate
SC16IS752_DLM = 0x03  # Divisor Latch MSB for 9600 baud rate
bus.write_byte_data(SC16IS752_ADDRESS, 0x00, 0x80)  # Enable access to configuration registers
bus.write_byte_data(SC16IS752_ADDRESS, 0x06, SC16IS752_LCR)  # Set 8N1 mode
bus.write_byte_data(SC16IS752_ADDRESS, 0x00, SC16IS752_DLL)  # Set DLL for 9600 baud rate
bus.write_byte_data(SC16IS752_ADDRESS, 0x01, SC16IS752_DLM)  # Set DLM for 9600 baud rate

# Initialize thermal printer
printer = Adafruit_Thermal.Adafruit_Thermal("/dev/ttySC0", 9600)

# Print some text
printer.println("Hello, world!")
printer.println("This is a thermal printer connected to a Raspberry Pi via I2C to TTL bridge.")
printer.println("Thanks for using this code!")
printer.feed(3)

# Wait for printing to complete
time.sleep(2)