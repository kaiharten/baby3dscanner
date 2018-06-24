import cv2
import imageprocessor
import matplotlib.pyplot as plt

size = 256
x = 0
y = [0] * size
z = [0] * size
scanner = ImageProcessor()

img = cv2.imread("img/line0.jpeg")
x, y, z = scanner.getXYZ(img, 0)

plt.subplot(212)
plt.plot(y, z, 'ro')
plt.xlabel('')
plt.ylabel('Aantal pixels')
plt.show()

cv2.waitKey(0)

