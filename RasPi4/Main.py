#11:01 24 jun 2024
import cv2
import numpy as np
from shapely.geometry import Polygon
from shapely.geometry.point import Point
from ultralytics import YOLO
from ultralytics.utils.files import increment_path
from ultralytics.utils.plotting import Annotator, colors
import json
import os

polygon_path = "polygon.json"
weights_path = 'custom3.pt'

objects = ["xe may", "oto", "xe bus", "xe tai"]  #################################### OBJECT NAME ########################

multiplexer = {
    "xe may": 1,
    "oto": 5,
    "xe bus": 10,
    "xe tai": 10,
}

check_stop_program = False

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
    current_dir = os.path.dirname(os.path.abspath(__file__))
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
                
            results = model.track(frame, persist=True, classes=None)#Predict
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
            countdown_time = 0
            
            for object in objects:
                print_number_objects += f"  - {object}:{number_of_objects[object]}"
                number_vehicle+= number_of_objects[object]*multiplexer[object]
            print(print_number_objects)
            print(f"Queue:{max_distance:.1f} m")
            print(f"Number:{number_vehicle}")
            print(f"Time:{countdown_time}s")
            
            frame = cv2.resize(frame, (640, 480))
            cv2.imshow(f"Webcam {i}",frame)
            cap.release()
            if cv2.waitKey(1) != -1:
                print("Exit program")
                check_stop_program = True
                cv2.destroyAllWindows()  
                break

def main():
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

if __name__ == "__main__":
    main()
