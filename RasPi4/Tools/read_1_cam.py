import cv2

check_stop_program = False

def capture_image_from_camera(cam_index):
    global check_stop_program
    for i in range(len(cam_index)):
        cv2.namedWindow(f"Webcam {cam_index[i]}")

    while check_stop_program == False:
        for i in range(len(cam_index)):
            
            cap = cv2.VideoCapture(cam_index[i])  
            if not cap.isOpened():
                print(f"Could not open webcam {cam_index[i]}")
                return
            ret, frame = cap.read()  
            cv2.resize(frame,(640,480))
            cv2.imshow(f'Webcam {cam_index[i]}', frame)
            cap.release() 
            if cv2.waitKey(1) != -1:
                print("Exit program")
                check_stop_program = True
                cv2.destroyAllWindows()  
                break

cam_index = [1]
capture_image_from_camera(cam_index)

