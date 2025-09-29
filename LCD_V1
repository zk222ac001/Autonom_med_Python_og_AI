#smbus2 — Python library that provides I²C (SMBus) functions to send bytes over the Raspberry Pi I²C bus.
import smbus2, time

'''
ADDR is the I²C address of the PCF8574 backpack on the LCD. Common values: 0x27 or 0x3f. 
Use i2cdetect -y 1 to confirm.nbus = smbus2.SMBus(1) opens I²C bus number 1
(the standard bus on modern Raspberry Pi models). bus is used to write bytes to the device.'''

ADDR = 0x27          # LCD I2C address (use i2cdetect -y 1 to check)
bus = smbus2.SMBus(1)

'''
LCD_CHR = 1 and LCD_CMD = 0 are used as the RS bit: 1 = data/character, 0 = command.
LINE1 (0x80) and LINE2 (0xC0) are DDRAM addresses that position the cursor to the start of line 1 and line 2.
BACKLIGHT = 0x08 is the bit used by many PCF8574 backpacks to keep the backlight on
(OR this into every byte you send). If your module maps backlight differently, you may need another value.
ENABLE = 0b00000100 is the bit mask for the LCD’s EN (enable) line — toggling this latches data into the LCD.
'''
LCD_CHR, LCD_CMD = 1, 0
LINE1, LINE2 = 0x80, 0xC0
BACKLIGHT, ENABLE = 0x08, 0b00000100

'''
toggle(b) pulses the ENABLE bit high then low to tell the LCD to read the current data/command lines.
b | ENABLE sets EN = 1 (write); small delay; then b & ~ENABLE clears EN (write 0).
The delays ensure the LCD sees the pulse.
'''
def toggle(b):
    bus.write_byte(ADDR, b | ENABLE); time.sleep(0.0005)
    bus.write_byte(ADDR, b & ~ENABLE); time.sleep(0.0005)

'''
send(val, mode) sends an 8-bit val to the LCD in 4-bit mode (PCF8574 uses only 4 data lines).
(val & 0xF0) extracts the high nibble (upper 4 bits) already positioned in the high bits.
((val << 4) & 0xF0) shifts the low nibble into the high nibble position so it can be sent next.
For each nibble b, d = mode | b | BACKLIGHT combines the RS bit (mode), the nibble, and turns the backlight on.
bus.write_byte(ADDR, d) sends that byte to the PCF8574, then toggle(d) 
pulses EN so the LCD latches the nibble. Two nibble transfers = one full 8-bit transfer.
'''
def send(val, mode):
    for b in [(val & 0xF0), ((val << 4) & 0xF0)]:
        d = mode | b | BACKLIGHT
        bus.write_byte(ADDR, d); toggle(d)

# Init LCD
for cmd in (0x33,0x32,0x28,0x0C,0x06,0x01): send(cmd, LCD_CMD)

# Write two lines
send(LINE1, LCD_CMD)
for c in "Hello, World!   ": send(ord(c), LCD_CHR)

send(LINE2, LCD_CMD)
for c in "I2C LCD Module    ": send(ord(c), LCD_CHR)

time.sleep(5)
