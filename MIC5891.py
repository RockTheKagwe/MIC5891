import RPi.GPIO as GPIO
import time

# Define GPIO pins for Raspberry Pi
SDI = 17  # Serial data input
RCLK = 27  # Latch input
SRCLK = 22  # Clock input

# Define digits for 7-segment display (common cathode)
digits = {
    0: 0b00111111,
    1: 0b00000110,
    2: 0b01011011,
    3: 0b01001111,
    4: 0b01100110,
    5: 0b01101101,
    6: 0b01111101,
    7: 0b00000111,
    8: 0b01111111,
    9: 0b01101111
}

# Initialize GPIO
GPIO.setmode(GPIO.BCM)
GPIO.setup(SDI, GPIO.OUT)
GPIO.setup(RCLK, GPIO.OUT)
GPIO.setup(SRCLK, GPIO.OUT)

# Function to shift bits out to MIC5891
def shift_out(data):
    for i in range(8):
        GPIO.output(SDI, data & (1 << (7 - i)))
        GPIO.output(SRCLK, GPIO.HIGH)
        time.sleep(0.001)
        GPIO.output(SRCLK, GPIO.LOW)

# Function to latch data to MIC5891
def latch():
    GPIO.output(RCLK, GPIO.HIGH)
    time.sleep(0.001)
    GPIO.output(RCLK, GPIO.LOW)

# Function to display a number on the 7-segment display
def display_number(number):
    # Split number into tens and ones digits
    tens = number // 10
    ones = number % 10

    # Display tens digit
    shift_out(digits[tens])
    latch()

    # Display ones digit
    shift_out(digits[ones])
    latch()

# Main loop to count up to 99
try:
    while True:
        for i in range(100):
            display_number(i)
            time.sleep(1)

finally:
    GPIO.cleanup()
