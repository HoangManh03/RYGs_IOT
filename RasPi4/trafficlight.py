import RPi.GPIO as GPIO
import time

GPIO_PIN = [
    [4,3,2],   # CLOCK_TIME:0,1      -LATCH_TIME:0,1      -DATA_TIME:0,1
    [11,9,10], # CLOCK_TIME:2,3      -LATCH_TIME:2,3      -DATA_TIME:2,3
    [26,19,13] # CLOCK_LIGHT:0,1,2,3 -LATCH_LIGHT:0,1,2,3 -DATA_LIGHT:0,1,2,3
    ]
BCD = [0b11111100,0b01100000,0b11011010,0b11110010,0b01100110,0b10110110,0b10111110,0b11100000,0b11111110,0b11110110]
# Xanh Xanh, Xanh Vang, Xanh Do # Vang Xanh, Vang Vang, Vang Do # Do Xanh,   Do Vang,   Do Do
LIGHT = [[0b00010001, 0b00010010, 0b00010100], [0b00100001, 0b00100010, 0b00100100],[0b01000001, 0b01000010, 0b01000100]]
# thoi gian max cac den
g_timeLeft_max = [
    [20,3,10+3+3+3],
    [10,3,20+3+3+3],
    [20,3,10+3+3+3],
    [10,3,20+3+3+3]]
# trang thai bat dau cac den
state = [0, 2, 0, 2]
# thoi gian con lai cua cac den 
timeLeft = [g_timeLeft_max[0][0],g_timeLeft_max[1][2]-3,g_timeLeft_max[2][0],g_timeLeft_max[3][2]-3]

def setup():
    GPIO.setmode(GPIO.BCM)
    GPIO.setwarnings(False)
    for i in GPIO_PIN:
        for j in i:
            GPIO.setup(j, GPIO.OUT)
            
def pulse(pin):
    time.sleep(0.00001)
    GPIO.output(pin, GPIO.HIGH)
    time.sleep(0.00001)
    GPIO.output(pin, GPIO.LOW)
    
def shift_out(data,pin):
    for i in range(8):
        bit = (data >> i) & 0x01
        GPIO.output(pin[2], bit)
        pulse(pin[0])
    pulse(pin[1])

def update_display():
    shift_out(LIGHT[state[3]][state[2]],GPIO_PIN[2])
    shift_out(LIGHT[state[1]][state[0]],GPIO_PIN[2])
    for i in range(2):
        for j in range(2):
            tens = timeLeft[i*2+j] // 10
            units = timeLeft[i*2+j] % 10
            shift_out(~BCD[units],GPIO_PIN[i])
            shift_out(~BCD[tens],GPIO_PIN[i])

def update_timers():
    global timeLeft, state
    print('  -'.join([f'Den{i+1}:{timeLeft[i]}s {"Xanh" if state[i] == 0 else "Do" if state[i] == 2 else "Vang"}' for i in range(2)]))
    for i in range(4):
        timeLeft[i] -= 1
        if timeLeft[i] < 0:
            state[i] = (state[i]+1)% 3
            timeLeft[i] = g_timeLeft_max[i][state[i]]

def controlTrafficLight():
    setup()
    try:
        while True:
            update_display()
            update_timers()
            time.sleep(1)
    except KeyboardInterrupt:
        GPIO.cleanup()
        pass

if __name__ == "__main__":
    controlTrafficLight()
    
