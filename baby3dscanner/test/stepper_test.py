from stepper import Stepper
import time
# Move the stepper from start point to end point
step = Stepper("/dev/ttyACMA0")
time.sleep(0.5)
step.moveStep()
time.sleep(12.5)
step.moveBack()
time.sleep(1)
step.com.close()