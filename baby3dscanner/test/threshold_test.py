#Hierin wordt een foto van de camera gepakt en komt er een filter erover heen.
#Verder wordt de totale witte pixels gemeten, door CountNonZero

import cv2
import numpy as np
from picamera.array import PiRGBArray
from picamera import PiCamera
import time
 
# initialize the camera and grab a reference to the raw camera capture
camera = PiCamera()
rawCapture = PiRGBArray(camera)
 
# allow the camera to warmup
time.sleep(0.3)
 
# grab an image from the camera
camera.capture(rawCapture, format="bgr")
image = rawCapture.array
cv2.imshow('win3', image)
a = cv2.cvtColor(image, cv2.COLOR_BGR2GRAY)
cv2.imshow('win2', a)

outfile = 'fotoo.jpg'
cv2.imwrite(outfile, a)

ret, thr = cv2.threshold(a, 0, 255, cv2.THRESH_OTSU)
cv2.imshow('win1', thr)

imagem = cv2.bitwise_not(thr)
cv2.imshow('win2', imagem)

#sum_pxl1 = cv2.countNonZero(imagem)
#print('Aantal pixel1:' + str(sum_pxl1))

outfile = 'fotoo_thr.jpg'
cv2.imwrite(outfile, thr)

sum_pxl = cv2.countNonZero(a)
print('Aantal pixel:' + str(sum_pxl))

#n_white_pix = np.sum(thr == 255)
#print('Number of white pixels:', n_white_pix)

cv2.waitKey(0)
cv2.destroyAllWindows()