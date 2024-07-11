import RPi.GPIO as GPIO
import cv2
import numpy as np
from shapely.geometry import Polygon
from shapely.geometry.point import Point
from ultralytics import YOLO
from ultralytics.utils.files import increment_path
from ultralytics.utils.plotting import Annotator, colors
import json
import os
import sys
import threading
import time
from bluepy import btle
from bluepy.btle import Scanner, DefaultDelegate

current_dir = os.path.dirname(os.path.abspath(__file__))
module_dir = os.path.join(current_dir, 'modules')
if module_dir not in sys.path:
    sys.path.append(module_dir)
import deFuzzy
############################# BLE constant variable #############################
ble_devices_path = r'ble_devices.json'
current_dir = os.path.dirname(os.path.abspath(__file__))
ble_devices_path = os.path.join(current_dir , 'data' , ble_devices_path)
addr_devices_in_processes = []
addr_select_devices = []
addr_scanned_devices = []
stop_BLEDeviceThread = True
data_int = None
############################# Detect and defuzzy constant variable #############################
polygon_path = "polygon.json"
weights_path = 'saban.pt'
objects = ["xe may", "oto", "xe bus", "xe tai"] 
multiplexer = {
    "xe may": 1,
    "oto": 5,
    "xe bus": 10,
    "xe tai": 10,
}
############################# Detect and defuzzy variable #############################
check_stop_program = False
############################# Control light constant variable ##############################
GPIO_PIN = [
    [4,3,2],   # CLOCK_TIME:0,1      -LATCH_TIME:0,1      -DATA_TIME:0,1
    [11,9,10], # CLOCK_TIME:2,3      -LATCH_TIME:2,3      -DATA_TIME:2,3
    [26,19,13] # CLOCK_LIGHT:0,1,2,3 -LATCH_LIGHT:0,1,2,3 -DATA_LIGHT:0,1,2,3
    ]
BCD = [0b11111100,0b01100000,0b11011010,0b11110010,0b01100110,0b10110110,0b10111110,0b11100000,0b11111110,0b11110110]
# Xanh Xanh, Xanh Vang, Xanh Do # Vang Xanh, Vang Vang, Vang Do # Do Xanh,   Do Vang,   Do Do
LIGHT = [[0b00010001, 0b00010010, 0b00010100], [0b00100001, 0b00100010, 0b00100100],[0b01000001, 0b01000010, 0b01000100]]
############################# Control light variable ##############################
g_phase = 0
g_state = [0, 2, 2, 2]# trang thai bat dau cac den
g_timeLeft_max = [10,15,20,25]#thoi gian max cac den
timeLeft = [g_timeLeft_max[0],g_timeLeft_max[1],g_timeLeft_max[2],g_timeLeft_max[3]]# thoi gian con lai cua cac den
g_yellow_timeleft = 5
g_red_timeLeft_max = 99
decrease_time_left = 5
increase_time_left = 10
############################# defuzzy_timeleft function #############################

############################# Detect and defuzzy function #############################
def convert_to_real_world_coordinates(point, H):
    point = np.array([point[0], point[1], 1.0], dtype="float64")
    real_point = np.dot(H, point)
    real_point = real_point / real_point[2]
    return real_point[:2]

def distance_point_to_line(point, line_start, line_end):
    point = np.array(point, dtype="float64")
    line_start = np.array(line_start, dtype="float64")
    line_end = np.array(line_end, dtype="float64")
    vector_start_to_point = point - line_start
    vector_line = line_end - line_start
    t = np.dot(vector_start_to_point, vector_line) / np.dot(vector_line, vector_line)
    closest_point = line_start + t * vector_line
    distance = np.linalg.norm(point - closest_point)
    return distance

def run(cam_index_list, image_points_array, stop_line_real_array, H_array):
    ###Change parameter in Here ####
    global objects
    global weights_path
    global g_timeLeft_max
    global current_dir 
    weights_path = os.path.join(current_dir, 'data' ,weights_path)
    number_of_objects = {}
    model = YOLO(weights_path)
    model.to("cpu")
    names = model.model.names
    global check_stop_program
    for i in range(len(cam_index_list)):
        cv2.namedWindow(f"Webcam {i}")
    while check_stop_program == False:
        for i,cam_index in enumerate(cam_index_list):
            polygon = Polygon([(image_points_array[i][0][0],image_points_array[i][0][1]),(image_points_array[i][1][0],image_points_array[i][1][1]), (image_points_array[i][2][0],image_points_array[i][2][1]), (image_points_array[i][3][0],image_points_array[i][3][1] )]) # Polygon points
            cap = cv2.VideoCapture(cam_index)  
            if not cap.isOpened():
                print(f"Could not open webcam {cam_index}")
                return
            ret, frame = cap.read()  
            
            max_distance = 0
            for key in objects:#Set number of object = 0
                number_of_objects[key] = 0    
                
            results = model.track(frame)#Predict
            print(results)
            if results[0].boxes.id is not None:#Check if there is any object
                boxes = results[0].boxes.xyxy.cpu()#Get bounding box
                track_ids = results[0].boxes.id.int().cpu().tolist()#Get track id
                clss = results[0].boxes.cls.cpu().tolist()#Get class
                annotator = Annotator(frame, line_width=1, example=str(names))#Annotator
                
                for box, track_id, cls in zip(boxes, track_ids, clss):#Draw bounding box
                    bbox_center = (box[0] + box[2]) / 2, box[3]  # Bbox center
                    bbox_center_real = convert_to_real_world_coordinates(bbox_center, H_array[i])
                    distance=distance_point_to_line((bbox_center_real[0], bbox_center_real[1]),(stop_line_real_array[i][0][0], stop_line_real_array[i][0][1]),(stop_line_real_array[i][1][0], stop_line_real_array[i][1][1]))
                    if distance > max_distance:
                        max_distance = distance
                    annotator.box_label(box, f"{names[cls]}:{distance:.1f}", color=colors(cls, True))#Draw label
                    if polygon.contains(Point((bbox_center[0], bbox_center[1]))) and names[cls] in number_of_objects:
                        number_of_objects[names[cls]] += 1
                        
            polygon_coords = np.array(polygon.exterior.coords, dtype=np.int32)
            cv2.polylines(frame, [polygon_coords], isClosed=True, color=(0, 247, 0), thickness=3)
            number_vehicle = 0
            for object in objects:#print_number_objects += f"  - {object}:{number_of_objects[object]}"
                number_vehicle+= number_of_objects[object]*multiplexer[object]
            number_vehicle/=5
            timeleft = round(deFuzzy.deFuzzy(number_vehicle, max_distance))
            g_timeLeft_max[i] = timeleft
            #print(f"Queue:{max_distance:.1f}m")  #print(f"Number:{number_vehicle}")  #print(f"Duration:{timeleft} s")
            cv2.putText(frame, f"Queue:{max_distance:.1f}m", (10,30), cv2.FONT_HERSHEY_SIMPLEX, 1, (255,0,0), 2)
            cv2.putText(frame, f"Number:{number_vehicle}", (10,60), cv2.FONT_HERSHEY_SIMPLEX, 1, (255,0,0), 2)
            cv2.putText(frame, f"Duration:{timeleft} s", (10,90), cv2.FONT_HERSHEY_SIMPLEX, 1, (255,0,0), 2)
            cv2.imshow(f"Webcam {i}",frame)
            cap.release()
            if cv2.waitKey(1) != -1:
                print("Exit program")
                check_stop_program = True
                cv2.destroyAllWindows()  
                break

def detect():
    global polygon_path
    current_dir = os.path.dirname(os.path.abspath(__file__))
    polygon_path = os.path.join(current_dir, 'data' ,polygon_path)
    with open(polygon_path, 'r') as f:
        data = json.load(f)
    polygons = data['polygons']
    cam_index_list = []
    image_points_list = []
    H_list = []
    stop_line_real_list = []
    for i in range(len(polygons)):
        cam_index_list.append(polygons[i]['index_camera'])
        real_points = np.array(polygons[i]['real'], dtype="int32")
        image_points = np.array(polygons[i]['camera'], dtype="int32")
        H, _ = cv2.findHomography(image_points, real_points)
        if H is not None:
            H_list.append(H)
            image_points_list.append(image_points)
            stop_line = [(image_points[3][0], image_points[3][1]), (image_points[2][0], image_points[2][1])]
            stop_line_real = [
                convert_to_real_world_coordinates(stop_line[0], H),
                convert_to_real_world_coordinates(stop_line[1], H)
            ]
            stop_line_real_list.append(stop_line_real)
        else:
            print(f"Warning: Homography could not be computed for polygon {i}")
    image_points_array = np.array(image_points_list)
    stop_line_real_array = np.array(stop_line_real_list)
    H_array = np.array(H_list)
    run(cam_index_list, image_points_array, stop_line_real_array, H_array)
####################### Code control lights ############################
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
        for j in reversed(range(2)):
            tens = timeLeft[i*2+j] // 10
            units = timeLeft[i*2+j] % 10
            shift_out(~BCD[units],GPIO_PIN[i])
            shift_out(~BCD[tens],GPIO_PIN[i])

def update_timers():
    global timeLeft, g_state, g_phase
    print('-'.join([f'Den{i+1}:{timeLeft[i]}s {"Xanh " if g_state[i] == 0 else "Do " if g_state[i] == 2 else "Vang "}' for i in range(4)]))
    timeLeft[g_phase] -= 1
    timeLeft[(g_phase+1)%4] -= 1
    if timeLeft[g_phase] < 0:
        if(g_state[g_phase]==1):
            g_phase = (g_phase+1)%4
            g_state[g_phase] = 0
            g_state[(g_phase-1)%4] = 2
            timeLeft[(g_phase-1)%4] = g_red_timeLeft_max
            timeLeft[g_phase] = g_timeLeft_max[g_phase]
            timeLeft[(g_phase+1)%4] = g_timeLeft_max[g_phase]+g_yellow_timeleft+1
        elif(g_state[g_phase]==0):
            g_state[g_phase] = 1
            timeLeft[g_phase] = g_yellow_timeleft

def controlTrafficLight():
    global check_stop_program,data_int
    setup()
    try:
        while check_stop_program == False:
            if data_int == 0:
                if(timeLeft[g_phase] > decrease_time_left and g_state[g_phase] == 0):
                    print("Giam thoi gian den")# Decrease red light timer (logic depends on your notify script)
                    timeLeft[g_phase] = decrease_time_left  # Adjust time decrease value as needed
                    timeLeft[(g_phase+1)%4] = decrease_time_left+g_yellow_timeleft+1
            elif data_int == 1:
                if(g_state[g_phase] == 0):
                    print("Tang thoi gian den")# Decrease red light timer (logic depends on your notify script)
                    timeLeft[g_phase] += increase_time_left  # Adjust time decrease value as needed
                    timeLeft[(g_phase+1)%4] += increase_time_left
            data_int = None
            update_display()
            update_timers()
            time.sleep(0.3)
    except KeyboardInterrupt:
        GPIO.cleanup()
        check_stop_program = True
        pass
############################# BLE function #############################
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
################################   MAIN  #######################
if __name__ == "__main__":
    detect_thread = threading.Thread(target=detect)
    detect_thread.start()
    controlTrafficLight_thread = threading.Thread(target=controlTrafficLight)
    controlTrafficLight_thread.start()
    addr_select_devices = []
    while check_stop_program == False:
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
