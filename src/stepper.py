import serial
import time
import threading

class Stepper:
    def __init__(self, port, baudrate=115200, timeout=2):
        self.com = serial.Serial(port=port, baudrate=baudrate,
        timeout=timeout, writeTimeout=timeout)

        if self.com.isOpen():
            print("Is Open")
            self.com.close()

        self.com.open()

    def moveStep(self):

        if not self.com.isOpen():
            self.com.open()
            time.sleep(0.08)
        bytesToRead = 0
        msg = []
        self.com.flushInput()
        self.com.flushOutput()
        #self.com.write(b'S\n')
        while bytesToRead is 0:
            self.com.write(b'S\n')
            bytesToRead = self.com.inWaiting()
            #print (bytesToRead)
            msg = self.com.read(bytesToRead)
            time.sleep(0.06)
        #print(msg.decod)
        msg = msg.decode('UTF-8')
        self.com.close()
        return msg

    def moveBack(self):
        if not self.com.isOpen():
            self.com.open()
            time.sleep(0.08)
            
        bytesToRead = 0
        msg = []
        #self.com.write(b'R\n')
        while bytesToRead is 0:
            self.com.write(b'R\n')
            bytesToRead = self.com.inWaiting()
            msg = self.com.read(bytesToRead)
            time.sleep(0.06)
        msg = msg.decode('UTF-8')
        self.com.close()
        return msg


def hello():
    print ("Hello")

#time.sleep(9)

#step.moveBack()
#time.sleep(9)
def main():
    step = Stepper("/dev/ttyACM0")
    time.sleep(0.5)
    msg = step.moveStep()
    time.sleep(12.5)
    step.moveBack()
    time.sleep(1)
    step.com.close()

#main()