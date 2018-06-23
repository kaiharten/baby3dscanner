import cv2
import numpy as np
from picamera.array import PiRGBArray
from picamera import PiCamera
import time
import math

# initialize the camera and grab a reference to the raw camera capture
camera = PiCamera()
rawCapture = PiRGBArray(camera)
 
# allow the camera to warmup
time.sleep(0.3)
 
# grab an image from the camera
camera.capture(rawCapture, format="bgr")
image = rawCapture.array
cv2.imshow('Captured Foto', image)
a = cv2.cvtColor(image, cv2.COLOR_BGR2GRAY)
cv2.imshow('Filter(GrayScale)', a)

outfile = 'fotoo.jpg'
cv2.imwrite(outfile, a)

ret, thr = cv2.threshold(a, 0, 255, cv2.THRESH_OTSU)
cv2.imshow('Filter(Black/White)', thr)

#imagem = cv2.bitwise_not(thr)
#cv2.imshow('win2', imagem)

#sum_pxl1 = cv2.countNonZero(imagem)
#print('Aantal pixel1:' + str(sum_pxl1))

outfile = 'fotoo_thr.jpg'
cv2.imwrite(outfile, thr)

sum_pxl = cv2.countNonZero(a)
print('Aantal pixel:' + str(sum_pxl))

#n_white_pix = np.sum(thr == 255)
#print('Number of white pixels:', n_white_pix)

prev = 5
t = np.zeros(257)
t2 = np.zeros(257)
a = 0
b = 1

for i in range(0, 1280, 5):
    crop_img = thr[0:720, i:prev]
    t2[b] = prev
    b = b + 1
    prev = prev + 5
    sum_pxl2 = cv2.countNonZero(crop_img)
    t[a] = sum_pxl2
    a = a + 1
    print('The number of white pixels is: '+ str(sum_pxl2))
    outfile2 = '%s.jpg' % i
    cv2.imwrite(outfile2, crop_img)

l = np.mean(t)
print('Gemiddelde', l)



cv2.waitKey(0)
cv2.destroyAllWindows()

