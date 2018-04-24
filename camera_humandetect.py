import time
from picamera import PiCamera
from picamera.array import PiRGBArray
import cv2

from imutils import contours
from skimage import measure
import numpy as np
import imutils

class Camera():

    def __init__(self):
        self.camera = PiCamera();
        self.camera.resolution = (640,480)
        self.camera.framerate = 30
        self.rawCapture = PiRGBArray(self.camera, size=(640, 480))
        self.image = []
        time.sleep(0.1)
    
    def grabImage(self):
        self.camera.capture(self.rawCapture, format="bgr")
        self.image = self.rawCapture.array

    def streamVideo(self):
        for frame in self.camera.capture_continuous(self.rawCapture, format="bgr", use_video_port=True):
            self.image = frame.array
            cv2.imshow("Frame", self.image)
            key = cv2.waitKey(1) & 0xFF
            self.rawCapture.truncate(0)

            if key == ord("q"):
                break


    def dispImage(self):
        cv2.imshow("Image", self.image)
        cv2.waitKey(0)

    def detectSingleBrightSpot(self):
        im = self.image
        orig = im.copy()
        gray_image = cv2.cvtColor(im, cv2.COLOR_BGR2GRAY)
        blurred = cv2.GaussianBlur(gray_image, (7, 7), 0)
        (minVal, maxVal, minLoc, maxLoc) = cv2.minMaxLoc(gray_image)
        im = orig.copy()
        cv2.circle(im, maxLoc, 7, (255,0,0), 2)
        
        cv2.imshow("Robust", im)
        cv2.waitKey(0)
        
        

    def detectBrightSpots(self):
        im = self.image
        gray_image = cv2.cvtColor(im, cv2.COLOR_BGR2GRAY)
        blurred = cv2.GaussianBlur(gray_image, (11, 11), 0)
        
        thresh = cv2.threshold(blurred, 240, 255, cv2.THRESH_BINARY)[1]
        thresh = cv2.erode(thresh, None, iterations=2)
        thresh = cv2.dilate(thresh, None, iterations=4)
        
        cv2.imshow("Thresh", thresh)
        cv2.waitKey(0)        
        
        labels = measure.label(thresh, neighbors=8, background=0)
        mask = np.zeros(thresh.shape, dtype="uint8")
        
        for label in np.unique(labels):
            if label==0:
                continue

            labelMask = np.zeros(thresh.shape, dtype="uint8")
            labelMask[labels == label] = 255
            numPixels = cv2.countNonZero(labelMask)

            if numPixels > 300:
                mask = cv2.add(mask, labelMask)
    
        cnts = cv2.findContours(mask.copy(), cv2.RETR_EXTERNAL, cv2.CHAIN_APPROX_SIMPLE)
        cnts = cnts[0] if imutils.is_cv2() else cnts[1]
        cnts = contours.sort_contours(cnts)[0]
        

        for (i,c) in enumerate(cnts):
            (x,y,w,h) = cv2.boundingRect(c)
            ((cX,cY), radius) = cv2.minEnclosingCircle(c)
            cv2.circle(im, (int(cX), int(cY)), int(radius), (0,0,255),3)
            cv2.putText(im, "#{}".format(i+1), (x,y-15), cv2.FONT_HERSHEY_SIMPLEX, 0.45, (0,0,255), 2)

        cv2.imshow("Image", im)
        cv2.waitKey(0)

    def detectHuman(self):
        from imutils.object_detection import non_max_suppression
        from imutils import paths
        import argparse

        hog = cv2.HOGDescriptor()
        hog.setSVMDetector(cv2.HOGDescriptor_getDefaultPeopleDetector())

        im = self.image
        im = imutils.resize(im, width=min(400, im.shape[1]))
        orig = im.copy()

        #detect peope in the image
        (rects, weights) = hog.detectMultiScale(im, winStride=(4, 4), padding=(8, 8), scale=1.05)
        
        # draw the original bounding boxes
        for (x, y, w, h) in rects:
            cv2.rectangle(orig, (x, y), (x + w, y + h), (0, 0, 255), 2)

        # apply non-maxima suppression to the bounding boxes using a fiarly large overlap threshold to try to maintain overlapping
        rects = np.array([[x, y, x + w, y + h] for (x, y, w, h) in rects])
        pick = non_max_suppression(rects, probs=None, overlapThresh=0.65)

        # draw final bounding boxes
        for (xA, yA, xB, yB) in pick:
            cv2.rectangle(im, (xA, yA), (xB, yB), (0, 255,0), 2)

        # show images
        cv2.imshow("Before", orig)
        cv2.imshow("After", im)
        cv2.waitKey(0)  

if __name__ == '__main__':
    cam = Camera()
    cam.streamVideo()
    cam.detectHuman()
    #cam.detectSingleBrightSpot()
