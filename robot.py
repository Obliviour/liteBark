import time
from gpiozero import PWMOutputDevice
from gpiozero import DigitalOutputDevice
from camera import Camera
from imutils.object_detection import non_max_suppression
import numpy  as np
import imutils
import cv2

from RobotState import WaitingForKeywordState
## Motor Driver GPIO Pins
# Motor A, Left Side GPIO CONSTANTS
PWM_DRIVE_LEFT   = 21
PWM_LEFT_PIN     = 26
REVERSE_LEFT_PIN = 19
# Motor B, Right Side GPIO CONSTANTS
PWM_DRIVE_RIGHT   = 5
FORWARD_RIGHT_PIN = 13
REVERSE_RIGHT_PIN = 6




class robot(State):
    def __init__(self):
        #set up GPIO
        self.driveLeft  = PWMOutputDevice(PWM_DRIVE_LEFT, True, 0, 1000)
        self.driveRight = PWMOutputDevice(PWM_DRIVE_RIGHT, True, 0 1000)

        self.forwardLeft  = DigitalOutputDevice(FORWARD_LEFT_PIN)
        self.reverseLeft  = DigitalOutputDevice(REVERSE_LEFT_PIN)
        self.forwardRight = DigitalOutputDevice(FORWARD_RIGHT_PIN)
        self.reverseRight = DigitalOutputDevice(REVERSE_RIGHT_PIN)
        
        self.camera = Camera()
        # Microphone class not yet implemented
        #self.microphone = microphone()

        self.state = WaitingForKeywordState()

    def on_event(self, event)
        self.state = self.state.on_event(event)

    def allStop():
        forwardLeft.value = False
        reverseLeft.value = False
        forwardRight.value = False
        reverseRight.value = False
        driveLeft.value = 0
        driveRight.value = 0
        
    def goForward():
        forwardLeft.value = True
        reverseLeft.value = False
        forwardRight.value = True
        reverseRight.value = False
        driveLeft.value = 1.0
        driveRight.value = 1.0

    def goBackward():
        forwardLeft.value = False
        reverseLeft.value = True
        forwardRight.value = False
        reverseRight.value = True
        driveLeft.value = 1.0
        driveRight.value = 1.0

    def rotateRight():
        forwardLeft.value = True
        reverseLeft.value = False
        forwardRight.value = False
        reverseRight.value = True
        driveLeft.value = 1.0
        driveRight.value = 1.0

    def rotateLeft():
        forwardLeft.value = False
        reverseLeft.value = True
        forwardRight.value = True
        reverseRight.value = False
        driveLeft.value = 1.0
        driveRight.value = 1.0

    def bankRight():
        forwardLeft.value = True
        reverseLeft.value = False
        forwardRight.value = True
        reverseRight.value = False
        driveLeft.value = 0.8
        driveRight.value = 0.2

    def bankLeft():
        forwardLeft.value = True
        reverseLeft.value = False
        forwardRight.value = True
        reverseRight.value = False
        driveLeft.value = 0.2
        driveRight.value = 0.8


    
            
    def detectHuman(self):
        hog = cv2.HOGDescriptor()
        hog.setSVMDetector(cv2.HOGDescriptor_getDefaultPeopleDetector())

        im = self.camera.read()
        im = imutils.resize(im, width=min(400, im.shape[1]))
        orig = im.copy()

        #detect peope in the image
        (rects, weights) = hog.detectMultiScale(im, winStride=(4, 4), padding=(8, 8), scale=1.05)
        
        # draw the original bounding boxes
        for (x, y, w, h) in rects:
            cv2.rectangle(orig, (x, y), (x + w, y + h), (0, 0, 255), 2)

        # apply non-maxima suppression to the bounding boxes using a fiarly large overlap
        # threshold to try to maintain overlapping
        rects = np.array([[x, y, x + w, y + h] for (x, y, w, h) in rects])
        pick = non_max_suppression(rects, probs=None, overlapThresh=0.65)

        # draw final bounding boxes
        for (xA, yA, xB, yB) in pick:
            # here we assume one person is in the frame
            
            cv2.rectangle(im, (xA, yA), (xB, yB), (0, 255,0), 2)
            

        # show images
        #cv2.imshow("Before", orig)
        #cv2.imshow("After", im)
        
        return (xA, yA, xB, yB)
        
        
    def startRobot(self):
        Thread(target=self.moveRobot, args=()).start()
        return self

    def followHuman(self):
        bounded_box = self.detectHuman()
        mid_pt = ((bounded_box[0] + bounded_box[2]) / 2, (bounded_box[1] + bounded_box[3]) / 2)
        if (mid_pt > self.camera.resolution[0] / 3 and mid_pt > (self.camera.resolution[1] * 2) / 3):
            self.goForward()
        else (mid_pt < self.camera.resolution[0] / 3):
            self.bankLeft()
        else:
            self.bankRight()
    
        
        
        
        
