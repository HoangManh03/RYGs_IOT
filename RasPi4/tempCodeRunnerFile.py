
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
    shift_out(LIGHT[g_state[3]][g_state[2]],GPIO_PIN[2])
    shift_out(LIGHT[g_state[1]][g_state[0]],GPIO_PIN[2])
    for i in range(2):
            tens = timeLeft[i*2+j] // 10
            units = timeLeft[i*2+j] % 10
            shift_out(~BCD[units],GPIO_PIN[i])
            shift_out(~BCD[tens],GPIO_PIN[i])
