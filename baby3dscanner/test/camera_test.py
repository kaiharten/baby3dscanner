import cv2
from camera import CameraStream

if __name__ == "__main__":
    cam = CameraStream().start()
    while True:
        frame = cam.read()
        cv2.imshow('webcam', frame)
        if cv2.waitKey(1) == 27:
            break
    
    cam.stop()
    cv2.destroyAllWindows()