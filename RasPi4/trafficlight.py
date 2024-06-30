#import RPi.GPIO as GPIO
import time

LATCH_PIN = 4  
CLOCK_PIN = 14 
DATA_PIN = 12  

# row:Den | collum: thoi gian tung trang thai
BCD = [
    0b00111111, 
    0b00000110, 
    0b01011011,  
    0b01001111, 
    0b01100110,  
    0b01101101,  
    0b01111101,  
    0b00000111,  
    0b01111111,  
    0b01101111   
]

LIGHT = [
    [0b01110111, 0b01111011, 0b01111101],
    [0b10110111, 0b10111011, 0b10111101],
    [0b11010111, 0b11011011, 0b11011101]
]
timeLeft_max = [
    [20,3,10+3+3+3],
    [10,3,20+3+3+3],
    [20,3,10+3+3+3],
    [10,3,20+3+3+3]]

state = [0, 2, 0, 2]

timeLeft = [
    timeLeft_max[0][0],
    timeLeft_max[1][2]-3,
    timeLeft_max[2][0],
    timeLeft_max[3][2]-3
    ]
"""
def setup():
    GPIO.setmode(GPIO.BCM)
    GPIO.setwarnings(False)
    GPIO.setup(LATCH_PIN, GPIO.OUT)
    GPIO.setup(CLOCK_PIN, GPIO.OUT)
    GPIO.setup(DATA_PIN, GPIO.OUT)

def shift_out(data_pin, clock_pin, value):
    for i in range(8):
        GPIO.output(data_pin, value & (1 << (7 - i)))
        GPIO.output(clock_pin, GPIO.HIGH)
        GPIO.output(clock_pin, GPIO.LOW)

def update_display():
    GPIO.output(LATCH_PIN, GPIO.LOW)
    shift_out(DATA_PIN, CLOCK_PIN, ~LIGHT[state[2]][state[3]])
    shift_out(DATA_PIN, CLOCK_PIN, ~LIGHT[state[0]][state[1]])
    for i in range(4):
        tens = timeLeft[i] // 10
        units = timeLeft[i] % 10
        shift_out(DATA_PIN, CLOCK_PIN, ~BCD[units])
        shift_out(DATA_PIN, CLOCK_PIN, ~BCD[tens])
    GPIO.output(LATCH_PIN, GPIO.HIGH)
"""
def update_timers():
    global timeLeft, state
    print('  -'.join([f'Den{i+1}:{timeLeft[i]}s {"Xanh" if state[i] == 0 else "Do" if state[i] == 2 else "Vang"}' for i in range(2)]))
    for i in range(4):
        timeLeft[i] -= 1
        if timeLeft[i] < 0:
            state[i] = (state[i]+1)% 3
            timeLeft[i] = timeLeft_max[i][state[i]]
def controlTrafficLight():
    #setup()
    try:
        while True:
            #update_display()
            update_timers()
            time.sleep(1)
    except KeyboardInterrupt:
        #GPIO.cleanup()
        pass

if __name__ == "__main__":
    controlTrafficLight()
