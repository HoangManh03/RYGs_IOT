from bluepy import btle
from bluepy.btle import Peripheral, UUID, DefaultDelegate, BTLEDisconnectError, Scanner
import time
import threading
import json

devices_in_processes = []
addr_select_devices = []

class MyDelegate(btle.DefaultDelegate):
    def __init__(self):
        btle.DefaultDelegate.__init__(self)

    def handleNotification(self, cHandle, data):
        data = int.from_bytes(data, byteorder='little', signed=False)
        print(f"Notification received: {data}")

def BLEDeviceThread(addr,name):
    global devices_in_processes
    global addr_select_devices
    devices_in_processes.append(addr)
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
            if peripheral.waitForNotifications(1.0):
                pass
            
    except btle.BTLEDisconnectError:
        print(f"Cant to Device {name} | {addr}")
    
    except Exception as e:
        print(f"Cant to Device {name} | {addr}")
        #print(f"An error occurred: {e}")
        
    finally:
        devices_in_processes.remove(addr)
        try:
            peripheral.disconnect()
        except:
            pass

def get_select_devices():
    try:
        with open(r'/home/pi41/Main/ble_devices.json', 'r') as f:
            devices = json.load(f)
        return devices
    except FileNotFoundError:
        print("File 'ble_devices.json' not found. Exiting.")
        return []
    except json.JSONDecodeError:
        print("Error decoding JSON from 'ble_devices.json'. Exiting.")
        return []

if __name__ == "__main__":
    devices_in_processes = []
    while True:
        select_devices= get_select_devices()
        addr_select_devices = [device[0] for device in select_devices]
        for select_address, name in select_devices:
            if select_address not in devices_in_processes:
                thread = threading.Thread(target=BLEDeviceThread, args = (select_address,name,))
                thread.start()
                time.sleep(1)
        time.sleep(1)


