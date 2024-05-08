import RPi.GPIO as GPIO
import time

# Define GPIO pins for Raspberry Pi
DATA_PIN = 17  # Connect to MIC5891 pin 3
CLOCK_PIN = 27  # Connect to MIC5891 pin 2
LATCH_PIN = 22  # Connect to MIC5891 pin 4
OE_PIN = 18  # Connect to MIC5891 pin 14

# Global variables
decimalPt = True  # Decimal point display flag
pwmValue = 0      # PWM brightness value

# Segment patterns for hexadecimal digits (0-F)
segments = {
    0: 0b00111111, 1: 0b00000110, 2: 0b01011011, 3: 0b01001111,
    4: 0b01100110, 5: 0b01101101, 6: 0b01111101, 7: 0b00000111,
    8: 0b01111111, 9: 0b01101111, 10: 0b01110111, 11: 0b01111100,
    12: 0b00111001, 13: 0b01011110, 14: 0b01111001, 15: 0b01110001
}

# Initialize GPIO
GPIO.setmode(GPIO.BCM)
GPIO.setup(DATA_PIN, GPIO.OUT)
GPIO.setup(CLOCK_PIN, GPIO.OUT)
GPIO.setup(LATCH_PIN, GPIO.OUT)
GPIO.setup(OE_PIN, GPIO.OUT)

# Enable MIC5891 outputs
GPIO.output(OE_PIN, GPIO.LOW)

# Function to shift data out to MIC5891
def shift_out(data):
    for bit in range(7, -1, -1):
        GPIO.output(DATA_PIN, (data >> bit) & 1)
        GPIO.output(CLOCK_PIN, GPIO.HIGH)
        GPIO.output(CLOCK_PIN, GPIO.LOW)

# Function to latch data to MIC5891
def latch():
    GPIO.output(LATCH_PIN, GPIO.HIGH)
    GPIO.output(LATCH_PIN, GPIO.LOW)

# Function to display a number on the 7-segment display
def display_number(number):
    global decimalPt, pwmValue
    decimalPt = not decimalPt  # Display decimal point every other pass through loop
    
    for i in range(16):  # Generate Hex characters to display (0 to F)
        bits = segments[i]
        if decimalPt:
            bits |= 0b10000000  # Add decimal point on every other pass
        shift_out(bits)  # Display alphanumeric digit
        latch()
        time.sleep(1)  # Pause for 1 second
        pwmValue += 5
        if pwmValue > 255:
            pwmValue = 0  # Reset PWM brightness value
        print(pwmValue)
        GPIO.output(OE_PIN, pwmValue)  # Change brightness of display

# Main loop
try:
    while True:
        display_number(0)  # Start with 0
finally:
    GPIO.cleanup()
