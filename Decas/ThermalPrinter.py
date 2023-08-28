import smbus
import time

# define the I2C address of the TTL bridge
SC16IS752_ADDRESS = 0x4D

# define the commands for the thermal printer
INIT_COMMANDS = [
    27, 64,   # initialize printer
    27, 33, 0 # set character size to 12x24
]
PRINT_COMMANDS = [
    10 # print and feed line
]

# initialize the I2C bus and the SC16IS752 chip
bus = smbus.SMBus(1)
bus.write_byte_data(SC16IS752_ADDRESS, 0x06, 0x04) # enable I2C mode
bus.write_byte_data(SC16IS752_ADDRESS, 0xE3, 0x05) # set baud rate to 19200

# send the initialization commands to the thermal printer
bus.write_i2c_block_data(SC16IS752_ADDRESS, 0x00, INIT_COMMANDS)

# print some text
text = "Hello, world!"
bus.write_i2c_block_data(SC16IS752_ADDRESS, 0x00, bytearray(text, "ascii"))
bus.write_i2c_block_data(SC16IS752_ADDRESS, 0x00, PRINT_COMMANDS)

# wait for the printer to finish
time.sleep(0.5)