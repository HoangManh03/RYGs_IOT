from imutils.video import VideoStream
import cv2
import time

for i in range(5):
    
    print("Cam1 begin")
    vs = VideoStream(src=1).start()
    frame = vs.read()
    cv2.imshow("Webcam 1", frame)
    vs.stop()
    print("Cam1 end")
    time.sleep(4)
    
    
   