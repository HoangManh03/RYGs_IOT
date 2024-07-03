from bluepy import btle
from bluepy.btle import Scanner, DefaultDelegate
import time
import threading
import json
import os

ble_devices_path = r'ble_devices.json'

current_dir = os.path.dirname(os.path.abspath(__file__))
ble_devices_path = os.path.join(current_dir , 'data' , ble_devices_path)
addr_devices_in_processes = []
addr_select_devices = []
addr_scanned_devices = []
stop_BLEDeviceThread = True
data_int = None
##########################################
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
##############################################

def update_timers():
    global timeLeft, state
    print('  -'.join([f'Den{i+1}:{timeLeft[i]}s {"Xanh" if state[i] == 0 else "Do" if state[i] == 2 else "Vang"}' for i in range(2)]))
    for i in range(4):
        timeLeft[i] -= 1
        if timeLeft[i] < 0:
            state[i] = (state[i]+1)% 3
            timeLeft[i] = timeLeft_max[i][state[i]]

def controlTrafficLight():

    global data_int
    #setup()
    try:
        while True:
            if data_int == 0:
                print("data received = 0")
                # Decrease red light timer (logic depends on your notify script)
                timeLeft[0] = max(10, timeLeft[0] - 5)  # Adjust time decrease value as needed
            elif data_int == 1:
                print("data received = 1")
                # Increase green light timer (logic depends on your notify script)
                timeLeft[2] = min(timeLeft_max[2][2], timeLeft[2] + 5)
            #update_display()
            update_timers()
            data_int = None
            time.sleep(1)
    except KeyboardInterrupt:
        #GPIO.cleanup()
        pass
##########################################


class MyDelegate(btle.DefaultDelegate):
    def __init__(self):
        btle.DefaultDelegate.__init__(self)

    def handleNotification(self, cHandle, data):
        global data_int
        data_int = int.from_bytes(data, byteorder='little', signed=False)
        print(f"Notification received: {data_int}")

def BLEDeviceThread(addr,name):
    global addr_devices_in_processes
    global addr_select_devices
    global stop_BLEDeviceThread
    addr_devices_in_processes.append(addr)
    try:
        peripheral = btle.Peripheral(addr)
        print(f"Connected to device {name} | {addr}")
        peripheral.setDelegate(MyDelegate())
        service_uuid = btle.UUID("12345678-1234-1234-1234-123456789123")
        characteristic_uuid = btle.UUID("12345678-1234-1234-1234-123456789012")
        service = peripheral.getServiceByUUID(service_uuid)
        characteristic = service.getCharacteristics(characteristic_uuid)[0]
        peripheral.writeCharacteristic(characteristic.valHandle + 1, b'\x01\x00', withResponse=True)
        while addr in addr_select_devices:
            if stop_BLEDeviceThread == True:
                break
            else:
                if peripheral.waitForNotifications(1.5):
                    pass
    except btle.BTLEDisconnectError:
        print(f"BTLEDisconnectError to Device {name} | {addr}")

    except Exception as e:
        print(f"Cant to Device {name} | {addr}")  
        #print(f"An error occurred: {e}")
    finally:
        addr_devices_in_processes.remove(addr)
        try:
            peripheral.disconnect()
            return 
        except:
            pass

def get_select_devices():
    try:
        with open(ble_devices_path, 'r') as f:
            devices = json.load(f)
        return devices
    except FileNotFoundError:
        print("File 'ble_devices.json' not found. Exiting.")
        return []
    except json.JSONDecodeError:
        print("Error decoding JSON from 'ble_devices.json'. Exiting.")
        return []

def scan_ble_devices():
    global addr_scanned_devices
    scanner = Scanner().withDelegate(MyDelegate())
    devices = scanner.scan(0.5)
    addr_scanned_devices = [dev.addr for dev in devices]


if __name__ == "__main__":
    control_traffic_light = threading.Thread(target=controlTrafficLight)
    control_traffic_light.start()
    addr_select_devices = []
    while True:
        print(f"Stop Device For Scanning")
        stop_BLEDeviceThread = True
        time.sleep(2)
        scanthread = threading.Thread(target=scan_ble_devices)
        scanthread.start()
        scanthread.join()
        print(addr_scanned_devices)
        time.sleep(0.1)
        stop_BLEDeviceThread = False
        select_devices = get_select_devices()
        addr_select_devices = [addr for addr, name in select_devices]
        for select_address, name in select_devices:
            if select_address in addr_scanned_devices:
                if select_address not in addr_devices_in_processes:
                    thread = threading.Thread(target=BLEDeviceThread, args = (select_address,name,))
                    thread.start()
                    time.sleep(0.1)
        time.sleep(30)

        



