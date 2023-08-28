
import smbus
import time

SC16IS752_ADDRESS = 0x4D

WRITE_BIT = 0x00
READ_BIT = 0x01

RHR = 0x00
THR = 0x00
IER = 0x01
FCR = 0x02
IIR = 0x02
LCR = 0x03
MCR = 0x04
LSR = 0x05
MSR = 0x06
SPR = 0x07
TCR = 0x06
TLR = 0x07
EFR = 0x02

LCR_8BIT = 0x03
LCR_ENHANCED_REGISTER = 0x80
FCR_ENABLE_FIFO = 0x01
MCR_LOOPBACK_MODE = 0x10

bus = smbus.SMBus(1)

def write_register(reg, data):
    bus.write_i2c_block_data(SC16IS752_ADDRESS, (reg << 3) | WRITE_BIT, [data])

def read_register(reg):
    bus.write_byte(SC16IS752_ADDRESS, (reg << 3) | READ_BIT)
    return bus.read_byte(SC16IS752_ADDRESS)

def configure_sc16is752():
    write_register(LCR, LCR_ENHANCED_REGISTER)
    write_register(EFR, 0x10)
    write_register(LCR, LCR_8BIT)
    write_register(FCR, FCR_ENABLE_FIFO)
    write_register(MCR, MCR_LOOPBACK_MODE)
    write_register(IER, 0x01)
    received_byte1 = read_register(LCR)
    print(hex(received_byte1))
    received_byte1 = read_register(FCR)
    print(hex(received_byte1))
    received_byte1 = read_register(MCR)
    print(hex(received_byte1))

def loopback_test():
    test_byte = 0xA0
    write_register(THR, test_byte)
    time.sleep(0.1)

    while ((read_register(IIR) & 0x0C) != 0x0C):
        print(bin(read_register(IIR)))
        time.sleep(0.1)

    received_byte = read_register(RHR)
    print(hex(received_byte))
    if received_byte == test_byte:
        print("Loopback test successful!")
    else:
        print("Loopback test failed. Mismatched data.")

    
#    while ((status & 0x01) == 0):
#        time.sleep(0.1)
#    if (status & 0x01):
#        received_byte = read_register(RHR)
#        if received_byte == test_byte:
#            print("Loopback test successful!")
#        else:
#            print("Loopback test failed. Mismatched data.")
#    else:
#        print("Loopback test failed. No data received.")

print("SC16IS752 Self Test")
configure_sc16is752()
loopback_test()
