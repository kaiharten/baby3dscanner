import cv2
import numpy as np
import math

# This class takes an image with a red laser line and 
# calculates the height 
class ImageProcessor:

    def __init__(self, size = 256,
                rpc = 0.0014,
                ro = 0.2686,
                d_cam_laser = 13, 
                d_laser_surface = 46.5):

        self.size = size
        self.radians_per_pixel_pitch = rpc
        self.radian_offset = ro
        self.distance_cam_laser = d_cam_laser
        self.distance_laser_surface = d_laser_surface

    def getXYZ(self, image, x_frame):

        x_laser = [0] * self.size
        y_laser = [0] * self.size

        #Perform grayscale and OtsuFilter and get laser coordinates
        img = self.__performThreshold(image)
        x_laser, y_laser = self.__getLaserCoordinates(img)

        y1 = y_laser[0]
        y2 = y_laser[255]
        x1 = x_laser[0]
        x2 = x_laser[255]

        #y = ax + b
        a, b = self.__getLinearCoeff(y1, y2, x1, x2)

        y = [0] * self.size
        z = [0] * self.size
        y, z = self.__calculateYZ(x_laser, y_laser, a, b)

        return x_frame, y, z

    def __performThreshold(self, image):
        cv_img = cv2.cvtColor(image, cv2.COLOR_BGR2GRAY)
        ret, img = cv2.threshold(cv_img, 0, 255, cv2.THRESH_OTSU)

        return img

    def __getLaserCoordinates(self, image):
        j = 0
        prev = 5

        y_laser = [0] * self.size
        x_laser = [0] * self.size

        for i in range(0, 1280, 5):
            crop_img = image[0:720, i:prev]
            prev = prev + 5

            white_pixels_matrix = np.argwhere(crop_img == 255)

            x_val = [pos[0] for pos in white_pixels_matrix]
            y_val = [pos[1] for pos in white_pixels_matrix]
                
            x_val_e = -1 * np.median(x_val) # this is y
            y_val_e = np.median(y_val)  

            y_laser[j] = x_val_e
            x_laser[j] = (y_val_e + i)
            j = j + 1

        return x_laser, y_laser

    # gets coefficients from y = ax + b  to calculate baseline  
    def __getLinearCoeff(self, y_1, y_2, x_1, x_2):
        a = (y_2 - y_1) /(x_2 - x_1)
        b = (y_1) - (a* x_1)

        return a, b
    
    def __calculateYZ(self, x, y, a, b):
        base_line = [0] * self.size
        pfc = [0] * self.size

        y = [0] * self.size
        z = [0] * self.size

        for k in range(0, self.size, 1):
            #calculate baseline with coefficients
            base_line[k] = (a * x[k]) + b

            #subtract baseline from measured pixel line
            pfc[k] = y[k] - base_line[k]

            # theta = rpp * pfc + ro
            theta = self.radians_per_pixel_pitch * abs(pfc[k]) + self.radian_offset

            # D =  h / (tan(pfc & rpc + ro))
            tan_theta = math.tan(theta)

            # calculate z in millimeters
            z[k] = (self.distance_laser_surface - (self.distance_cam_laser/tan_theta)) * 10
            if z[k] <= 0:
                z[k] = 0

            # Calculate y in millimeters
            y[k] = (x[k] * (56/1280)) * 10
        
        return y, z
    