import time
from gpiozero import PWMOutputDevice
from gpiozero import DigitalOutputDevice
from camera import Camera
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
            
    
        
        
        
        
        
        
        
        
        
