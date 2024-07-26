#11:01 24 jun 2024
import cv2
import json
import os
import sys

index_cameras = [0,2,4,6]
polygon_path = "polygon.json"

current_dir = os.path.dirname(os.path.abspath(__file__))
polygon_path = os.path.join(current_dir , 'data' , polygon_path)
module_dir = os.path.join(current_dir, 'modules')
if module_dir not in sys.path:
    sys.path.append(module_dir)

import PolygonEntryDisplay

g_camera_coordinates = []
g_camera_index = 0
g_img = None
g_camera_coordinates_list = []


def read_imgs_from_cams(index_cameras):
    imgs = []
    for i in index_cameras:
        cap = cv2.VideoCapture(i)
        if not cap.isOpened():
            print(f"Cant open webcam {i}")
            continue
        ret, img = cap.read()
        imgs.append(img)
        cap.release()
    return imgs

def click_event(event, x, y, flags, param):
    global g_camera_coordinates, g_camera_index
    if event == cv2.EVENT_LBUTTONDOWN:
        g_camera_coordinates.append([x, y])
        print(f"Coordinate {len(g_camera_coordinates)}: [{x}, {y}]")
        cv2.circle(g_img, (x, y), 5, (0, 0, 255), -1)
        cv2.imshow(f'Camera {g_camera_index}', g_img)
        if len(g_camera_coordinates) == 4:
            cv2.line(g_img, g_camera_coordinates[0], g_camera_coordinates[1], (0, 255, 0), 2)
            cv2.line(g_img, g_camera_coordinates[1], g_camera_coordinates[2], (0, 255, 0), 2)
            cv2.line(g_img, g_camera_coordinates[2], g_camera_coordinates[3], (0, 255, 0), 2)
            cv2.line(g_img, g_camera_coordinates[3], g_camera_coordinates[0], (0, 255, 0), 2)
            cv2.imshow(f'Camera {g_camera_index}', g_img)
            

def process_image(i,img):
    global g_img, g_camera_coordinates, g_camera_index
    g_camera_coordinates = []
    g_img = img
    g_camera_index = i
    cv2.imshow(f'Camera {g_camera_index}', g_img)
    cv2.setMouseCallback(f'Camera {g_camera_index}', click_event)
    while(len(g_camera_coordinates) != 4):
        cv2.waitKey(1)
    cv2.destroyAllWindows()

    
def main():
    global index_cameras, polygon_path
    with open(polygon_path, 'r') as f:
        data = json.load(f)        
    polygons = data['polygons']
    # Write Camera indexs
    for i,index_camera in enumerate(index_cameras):
        polygons[i]['index_camera']=index_camera
    imgs = read_imgs_from_cams(index_cameras)
    # Write Camera coordinates
    for i,img in enumerate(imgs):
        process_image(i,img)
        polygons[i]['camera']=g_camera_coordinates
    # Write Real coordinates
    read_real_coordinates = PolygonEntryDisplay.RealCoordinatesInputApp()
    
    if read_real_coordinates:
        for i,img in enumerate(read_real_coordinates):
            for j in range(4):
                for k in range(2):
                    polygons[i]['real'][j][k]=int(read_real_coordinates[i][j*2+k])
    print(read_real_coordinates)
    with open(polygon_path, 'w') as f:
        json.dump(data, f, indent=4)
        
        
if __name__ == '__main__':
    main()
    
