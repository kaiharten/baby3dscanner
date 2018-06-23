import cv2
import numpy as np
import math
import os
import userinterface as gui
#import imageprocessor as scan
import stepper as step
import camera as cam

global stopFlag
stopFlag = True

global count
count = 0

class BabyScannerApp():

    def __init__(self, *args, **kwargs):
        self.cam = cam.CameraStream().start()
        self.userinterface = self.create_ui()

        self.start_page = self.userinterface.frames[self.userinterface.StartPage]
        self.start_page.add_function_to_button1(self.run)
        self.shot_frame = [[] for x in range(200)]

        self.stepper = step.Stepper("/dev/ttyACM0")
        self.start_page.add_function_to_button4(self.stepper.moveBack)
        self.stepper_set = 0
        
        self.start_page.add_function_to_button2(self.stepper.moveStep)
        
        
        self.z = [[] for x in range(200)]
        self.x = [0] * 200
        self.y = [[] for x in range(200)]
        
    def create_ui(self):
        return gui.UserInterface(self)
    
    def restart(self):
        global stopFlag
        stopFlag = True

    def run(self):
        global count
        global stopFlag

        self.start_page.start_cam_button.config(state='disabled')
        self.start_page.update_idletasks()
        stopFlag = True
        d = 0
        if stopFlag is True:
            after_id = self.userinterface.after(90, self.run)
            if self.stepper_set is 0:
                step_status = self.stepper.moveStep()
                self.stepper_set = 1
                print(step_status)
                if "MOVE CMD" in step_status:
                    print ("Stepper is moving...")
                    self.stepper_set = 2

            if self.stepper_set is 2:
                self.start_page.label.config(text="Retrieving frame %d of 140" % (count) )
                self.start_page.update_idletasks()
                #print(count)
                self.shot_frame[count] = self.cam.read()
                count = count + 1

            if count == 140:
                self.stepper_set = 0
                self.userinterface.after_cancel(after_id)
                self.process()


    
    def process(self):
        global stopFlag
        stopFlag = False
        global count
        x = 0
        coord_filename = "data/coordinates.csv"
        try:
            os.remove(coord_filename)
        except OSError:
            pass
        my_file = open(coord_filename, "w")
        for n in list(range(count)):
            self.x[n] = x
            x = x + 3
            self.start_page.label.config(text="Processing image %d of 140" % (n + 1))
            self.start_page.update_idletasks()
            filename = "img/scan_images/image_%d.jpg" % (n)
            image = self.shot_frame[n]

            cv_img = cv2.cvtColor(image, cv2.COLOR_BGR2GRAY)
            ret, img = cv2.threshold(cv_img, 0, 255, cv2.THRESH_OTSU)

            prev = 5
            t = [0] * 256
            t2 = [0] * 256
            t3 = [0] * 256
            t4 = [0] * 256
            
            j = 0
            for i in range(0, 1280, 5):
                crop_img = img[0:720, i:prev]
                prev = prev + 5
                
                white_pixels_matrix = np.argwhere(crop_img == 255)
                
                x_val = [pos[0] for pos in white_pixels_matrix]
                y_val = [pos[1] for pos in white_pixels_matrix]
                
                x_val_e = -1 * np.median(x_val) # this is y
                y_val_e = np.median(y_val)
                
                t[j] = x_val_e
                t2[j] = (y_val_e + i)
                j = j + 1
                
            y_1 = t[0]
            y_2 = t[255]
            
            x_1 = t2[0]
            x_2 = t2[255]
            
            #y = ax + b 
            a = (y_2 - y_1)/(x_2 - x_1)
            b = y_1 - (a * x_1)
            
            t5 = [0] * 256
            
            # subtract baseline from actual white pixel line
            for k in range(0, 256, 1):
                t5[k] = k
                t3[k] = (a * t2[k]) + b
                t4[k] = t[k] - t3[k]
                
            z = [0] * 256
            
            for h in range(0, 256, 1):
                theta = 0.0014 * abs(t4[h]) + 0.2686
                tan_theta = math.tan(theta)
                z[h] = (46.5 - (13/tan_theta)) * 10
                if z[h] <= 0:
                    depth = 0
                else:
                    depth = z[h]
                
                y_in_mm = (t2[h] * (56/1280)) * 10
                my_file.write(str(self.x[n]) + ',' + str(y_in_mm) + ',' + str(depth) + '\n')
                

            print ("Processing image %d of 130\r" % (n))
            
        print ("\n") 
        
        print("Scanning done")
        self.start_page.start_cam_button.config(state='normal')
        self.start_page.but3_cam.config(state='normal')
        self.start_page.update_idletasks()
        self.start_page.label.config(text="done - idle")
        self.start_page.update_idletasks()
        count = 0
