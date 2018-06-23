import serial
import time
import threading

# This class controlls the stepper motor via a serial connection.
# Use moveStep to move the scanner forward
# Use moveBack to move the scanner back to its start position

class Stepper:
    def __init__(self, port, baudrate=115200, timeout=2):
        self.com = serial.Serial(port=port, baudrate=baudrate,
        timeout=timeout, writeTimeout=timeout)

        # check if serial port is open
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

        # Send 'S' and wait for acknowledge from the stepper controller 
        while bytesToRead is 0:
            self.com.write(b'S\n')
            bytesToRead = self.com.inWaiting()

            msg = self.com.read(bytesToRead)
            time.sleep(0.06)

        msg = msg.decode('UTF-8')
        self.com.close()
        return msg

    def moveBack(self):
        if not self.com.isOpen():
            self.com.open()
            time.sleep(0.08)
            
        bytesToRead = 0
        msg = []

        # Send 'R' and wait for acknowledge from the stepper controller 
        while bytesToRead is 0:
            self.com.write(b'R\n')
            bytesToRead = self.com.inWaiting()
            msg = self.com.read(bytesToRead)
            time.sleep(0.06)
        msg = msg.decode('UTF-8')
        self.com.close()
        return msg