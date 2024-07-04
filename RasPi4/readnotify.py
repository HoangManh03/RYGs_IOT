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

class MyDelegate(btle.DefaultDelegate):
    def __init__(self):
        btle.DefaultDelegate.__init__(self)

    def handleNotification(self, cHandle, data):
        data = int.from_bytes(data, byteorder='little', signed=False)
        print(f"Notification received: {data}")


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
        time.sleep(10)
        


