import os

# Babyscan specific modules
import userinterface as gui
import stepper as step
import camera as cam
from imageprocessor import ImageProcessor

# The flag for when the interval function needs to stop
global stopFlag
stopFlag = True


global count
count = 0

class BabyScannerApp():

    def __init__(self, *args, **kwargs):

        # Create camera and start stream
        self.cam = cam.CameraStream().start()

        # Create user interface
        self.userinterface = gui.UserInterface(self)

        # Add  RUN function to button 1 to start Scan
        self.start_page = self.userinterface.frames[self.userinterface.StartPage]
        self.start_page.add_function_to_button1(self.run)
        self.shot_frame = [[] for x in range(200)]

        # Create Stepper and add function to button 4
        self.stepper = step.Stepper("/dev/ttyACM0")
        self.start_page.add_function_to_button4(self.stepper.moveBack)
        self.stepper_set = 0
        
        self.start_page.add_function_to_button2(self.stepper.moveStep)
        
        # Create image processor
        self.img_proc = ImageProcessor()
            
    def restart(self):
        global stopFlag
        stopFlag = True

    def run(self):
        global count
        global stopFlag

        self.start_page.start_cam_button.config(state='disabled')
        self.start_page.update_idletasks()
        stopFlag = True

        if stopFlag is True:

            # Set interval  of 90ms for calling this function again
            after_id = self.userinterface.after(90, self.run)

            #If stepper hasnt been called to move, call to move
            if self.stepper_set is 0:
                step_status = self.stepper.moveStep()
                self.stepper_set = 1
                print(step_status)

        
                if "MOVE CMD" in step_status:
                    print ("Stepper is moving...")
                    self.stepper_set = 2

            # If stepper asnwered to the move call, start taking pictures with interval
            if self.stepper_set is 2:

                # Update gui
                self.start_page.label.config(text="Retrieving frame %d of 140" % (count) )
                self.start_page.update_idletasks()

                # Store frame from camera
                self.shot_frame[count] = self.cam.read()
                count = count + 1

            # 140 is the max count of frames until stepper is near the end point
            if count == 140:
                self.stepper_set = 0
                self.userinterface.after_cancel(after_id)
                self.process()


    
    def process(self):
        global stopFlag
        stopFlag = False
        global count
        x = 0

        # Check if there is already a coordinates file, if so: delete to make a new one
        coord_filename = "data/coordinates.csv"
        try:
            os.remove(coord_filename)
        except OSError:
            pass
        my_file = open(coord_filename, "w")

        # Lists to store every coordinate in
        z_coord = [[] for x in range(200)]
        x_coord = [0] * 200
        y_coord = [[] for x in range(200)]

        # Go through all photo frames
        for n in list(range(count)):

            # Add 3 millimeters after every photo
            x_coord[n] = x
            x = x + 3

            # Update Gui with status
            self.start_page.label.config(text="Processing image %d of 140" % (n + 1))
            self.start_page.update_idletasks()

            # Get XYZ coords
            image = self.shot_frame[n]
            x_coord[n], y_coord[n], z_coord[n] = self.img_proc.getXYZ(image, n)

            # Write XYZ coords to CSV file
            for h in range(0, 256, 1):
                my_file.write(str(x_coord[n]) + ',' + str(y_coord[n][h]) + ',' + str(z_coord[n][h]) + '\n')
                
            print ("Processing image %d of 130\r" % (n))
            
        print ("\n")         
        print("Scanning done")

        # Update GUI with button states
        self.start_page.start_cam_button.config(state='normal')
        self.start_page.but3_cam.config(state='normal')
        self.start_page.update_idletasks()
        self.start_page.label.config(text="done - idle")
        self.start_page.update_idletasks()

        # Reset the taken frames count for next scan
        count = 0

def main():
    app = BabyScannerApp()
    try:
        app.userinterface.mainloop()

    except:
        app.cam.stop()
        quit()

if __name__ == "__main__":
    main()