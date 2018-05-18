import sys
import time
from gpiozero import PWMOutputDevice
from gpiozero import DigitalOutputDevice
from imutils.object_detection import non_max_suppression
import numpy  as np
import imutils
import cv2

from state import State
from RobotState import Idle
from microphone import Microphone
from camera import Camera
import signal

## Motor Driver GPIO Pins
# Motor A, Left Side GPIO CONSTANTS
PWM_DRIVE_LEFT   = 21
FORWARD_LEFT_PIN = 26
REVERSE_LEFT_PIN = 19
# Motor B, Right Side GPIO CONSTANTS
PWM_DRIVE_RIGHT   = 5
FORWARD_RIGHT_PIN = 13
REVERSE_RIGHT_PIN = 6

class Robot(State):
    def __init__(self):
        self.sig_hndlr = signal.signal(signal.SIGINT, self.exit_gracefully)

        #set up GPIO
        self.driveLeft  = PWMOutputDevice(PWM_DRIVE_LEFT, True, 0, 1000)
        self.driveRight = PWMOutputDevice(PWM_DRIVE_RIGHT, True, 0, 1000)

        self.forwardLeft  = DigitalOutputDevice(FORWARD_LEFT_PIN)
        self.reverseLeft  = DigitalOutputDevice(REVERSE_LEFT_PIN)
        self.forwardRight = DigitalOutputDevice(FORWARD_RIGHT_PIN)
        self.reverseRight = DigitalOutputDevice(REVERSE_RIGHT_PIN)
        
        # Set up sensors
        self.camera = Camera()
        self.microphone = Microphone()

        self.state = Idle()

    def on_event(self, event):
        self.state = self.state.on_event(event)

    def allStop(self):
        self.forwardLeft.value = False
        self.reverseLeft.value = False
        self.forwardRight.value = False
        self.reverseRight.value = False
        self.driveLeft.value = 0
        self.driveRight.value = 0
        
    def goForward(self):
        self.forwardLeft.value = True
        self.reverseLeft.value = False
        self.forwardRight.value = True
        self.reverseRight.value = False
        self.driveLeft.value = 1.0
        self.driveRight.value = 1.0

    def goBackward(self):
        self.forwardLeft.value = False
        self.everseLeft.value = True
        self.orwardRight.value = False
        self.reverseRight.value = True
        self.driveLeft.value = 1.0
        self.driveRight.value = 1.0

    def rotateRight(self):
        self.forwardLeft.value = True
        self.reverseLeft.value = False
        self.forwardRight.value = False
        self.reverseRight.value = True
        self.driveLeft.value = 0.8
        self.driveRight.value = 0.8

    def rotateLeft(self):
        self.forwardLeft.value = False
        self.reverseLeft.value = True
        self.forwardRight.value = True
        self.reverseRight.value = False
        self.driveLeft.value = 0.8
        self.driveRight.value = 0.8

    def bankRight(self):
        self.forwardLeft.value = True
        self.reverseLeft.value = False
        self.forwardRight.value = True
        self.reverseRight.value = False
        self.driveLeft.value = 0.8
        self.driveRight.value = 0.2

    def bankLeft(self):
        self.forwardLeft.value = True
        self.reverseLeft.value = False
        self.forwardRight.value = True
        self.reverseRight.value = False
        self.driveLeft.value = 0.2
        self.driveRight.value = 0.8
            
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
        bounded_box = None
        for (xA, yA, xB, yB) in pick:
            # here we assume one person is in the frame
            bounded_box = (xA, yA, xB, yB)
            cv2.rectangle(im, (xA, yA), (xB, yB), (0, 255,0), 2)
            

        # show images
        #cv2.imshow("Before", orig)
        cv2.imshow("After", im)
        print bounded_box
        return bounded_box
        
        

    def followHuman(self):
        # Variables to Change
        binsize = 17
        turningTime = 0.2
        midrange_L = 7
        midrange_R = 11
        bounded_box = self.detectHuman()
        if bounded_box == None:
            return
        mid_pt = (bounded_box[0] + bounded_box[2]) / 2
        if (mid_pt > (400*midrange_L) / binsize and mid_pt < (400*midrange_R) / binsize):
            self.goForward()
            time.sleep(1.0)
            self.allStop()
            print "human in view"
        elif (mid_pt < (400*midrange_L) / binsize):
            print "left side"        
            self.rotateLeft()
            time.sleep(turningTime)
            self.allStop()
        else:
            print "right side"
            self.rotateRight()
            time.sleep(turningTime)
            self.allStop()
    
    def startupSensors(self):
        self.camera.startStream()
        self.microphone.startRecording()
        time.sleep(1)

    def quit(self):
        self.camera.close()
        self.microphone.close()
        self.allStop() 
    
    def runStateMachine(self):
        Thread(target=self.stateMachine, args=()).start()
   
    def runRobot(self):
        while True:
            print "Recording"
            
            if (self.microphone.startRecording()):
                print "Done Recording"
                self.on_event(self.microphone.read())
                print self.state.__str__()
                print self.state.__str__() == 'Idle' 
                if (self.state.__str__() == 'Idle'):
                    self.allStop()
                elif (self.state.__str__() == 'FollowHumanIdle'):
                    #self.camera.startStream()
                    self.allStop()
                elif (self.state.__str__() == 'FollowHuman'):
                    self.followHuman()
                elif (self.state.__str__() == 'VoiceControlIdle'):
                    print "VCIdle"
                    self.allStop()
                elif (self.state.__str__() == 'Forward'):
                    print "for"
                    self.goForward()
                elif (self.state.__str__() == 'RotateLeft'):
                    print "RLeft"
                    self.rotateLeft()
                elif (self.state.__str__() == 'RotateRight'):
                    self.rotateRight()
                elif (self.state.__str__() == 'QuitApp'):
                    self.quit()
                    return
    
                time.sleep(2.0)

    def followSpeech(self):
        while True:
            if (self.microphone.startRecording()):
                print "Done Recording"
                print self.microphone.read()
                self.state = self.microphone.read()
                if (self.state.__str__() == "go"):
                    self.goForward()
                elif(self.state.__str__() == "left"):
                    self.rotateLeft()
                elif(self.state.__str__() == "right"):
                    self.rotateRight()
                time.sleep(1.0)
                self.allStop()
                return
 
    def stateMachine(self):
        print "Starting recording"
        prevState = None 
        self.microphone.startRecording()
        time.sleep(1.0)
        while True:
            if prevState != self.microphone.read():
                prevState = self.microphone.read()
                self.on_event(self.microphone.read())
            time.sleep(1.0)
            if (self.state.__str__() == "Idle"):
                continue
                #self.allStop()
            elif (self.state.__str__() == "FollowHumanIdle"):
                self.camera.startStream()
                self.allStop()
            elif (self.state.__str__() == "FollowHuman"):
                self.followHuman()
            elif (self.state.__str__() == "VoiceControlIdle"):
                self.allStop()
            elif (self.state.__str__() == "RotateLeft"):
                self.rotateLeft()
            elif (self.state.__str__() == "RotateRight"):
                self.rotateRight()
            elif (self.state.__str__() == "QuitApp"):
                self.quit()
                return
             
    def exit_gracefully(self, signal, frame):
        print('Trying to exit gracefully...')
        self.quit()
        sys.exit(0)
     

if __name__ == '__main__':
    rob = Robot()
    time.sleep(1.0)

    if (sys.argv[1] = "-H"):
        rob.camera.startStream()
        time.sleep(1.0)
    while True:
        if (sys.argv[1] == "-S"):
            rob.followSpeech()
        elif (sys.argv[1] == "-H"):
            rob.followHuman()
        else:
            sys.exit(0)

    
        
