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


current_dir = os.path.dirname(os.path.abspath(__file__))
module_dir = os.path.join(current_dir, 'modules')
if module_dir not in sys.path:
    sys.path.append(module_dir)
import deFuzzy
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
g_timeLeft_max = [#thoi gian max cac den
    [10,3,15+3+3+3],
    [15,3,10+3+3+3],
    [10,3,15+3+3+3],
    [15,3,10+3+3+3]]
g_defuzzy_timeLeft_max=[20,20,20,20]# thoi gian max cac den Xanh theo defuzzy
state = [0, 2, 0, 2]# trang thai bat dau cac den
timeLeft = [g_timeLeft_max[0][0],g_timeLeft_max[1][2]-3,g_timeLeft_max[2][0],g_timeLeft_max[3][2]-3]# thoi gian con lai cua cac den 
############################# defuzzy_timeleft function #############################
def reset_defuzzy_timeleft_max():
    global g_defuzzy_timeLeft_max
    g_defuzzy_timeLeft_max=[10,10,10,10]

def update_timeLeft_max():
    global g_timeLeft_max,g_defuzzy_timeLeft_max
    for i in range(2):
        g_defuzzy_timeLeft_max[i] =  max(g_defuzzy_timeLeft_max[i],g_defuzzy_timeLeft_max[i+2])
        g_defuzzy_timeLeft_max[i] =  max(g_defuzzy_timeLeft_max[i],g_defuzzy_timeLeft_max[i+2])
    g_timeLeft_max = [#thoi gian max cac den
    [g_defuzzy_timeLeft_max[0],3,g_defuzzy_timeLeft_max[1]+3+3+3],
    [g_defuzzy_timeLeft_max[1],3,g_defuzzy_timeLeft_max[0]+3+3+3],
    [g_defuzzy_timeLeft_max[0],3,g_defuzzy_timeLeft_max[1]+3+3+3],
    [g_defuzzy_timeLeft_max[1],3,g_defuzzy_timeLeft_max[0]+3+3+3]]
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
    global g_timeLeft_max,g_defuzzy_timeLeft_max
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
            print_number_objects = ""
            number_vehicle = 0
            for object in objects:#print_number_objects += f"  - {object}:{number_of_objects[object]}"
                number_vehicle+= number_of_objects[object]*multiplexer[object]
            print(print_number_objects)
            number_vehicle/=5
            timeleft = round(deFuzzy.deFuzzy(number_vehicle, max_distance))
            g_defuzzy_timeLeft_max[i] = timeleft
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
    shift_out(LIGHT[state[3]][state[2]],GPIO_PIN[2])
    shift_out(LIGHT[state[1]][state[0]],GPIO_PIN[2])
    for i in range(2):
        for j in reversed(range(2)):
            tens = timeLeft[i*2+j] // 10
            units = timeLeft[i*2+j] % 10
            shift_out(~BCD[units],GPIO_PIN[i])
            shift_out(~BCD[tens],GPIO_PIN[i])

def update_timers():
    global timeLeft, state
    #print('-'.join([f'Den{i+1}:{timeLeft[i]}s {"Xanh" if state[i] == 0 else "Do" if state[i] == 2 else "Vang"}' for i in range(2)]))
    for i in range(4):
        timeLeft[i] -= 1
        if timeLeft[i] < 0:
            state[i] = (state[i]+1)% 3
            timeLeft[i] = g_timeLeft_max[i][state[i]]
            if(state[i] == 0 and i >= 2):
                update_timeLeft_max()

def controlTrafficLight():
    global check_stop_program
    setup()
    try:
        while check_stop_program == False:
            update_display()
            update_timers()
            time.sleep(0.2)
    except KeyboardInterrupt:
        GPIO.cleanup()
        check_stop_program = True
        pass
##################################################################################
if __name__ == "__main__":
    detect_thread = threading.Thread(target=detect)
    detect_thread.start()
    controlTrafficLight_thread = threading.Thread(target=controlTrafficLight)
    controlTrafficLight_thread.start()
