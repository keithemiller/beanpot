#!/usr/bin/python
"""
Did they blink?!?!?
"""
import os, sys
import cv2
import numpy as np
from image_processing import show_image

def blink_detect(pix_path):
    if os.path.isfile('haarcascade_eye.xml'):
        eye_cascade = cv2.CascadeClassifier('2split_eye.xml')#'haarcascade_eye_glasses.xml')#'haarcascade_eye.xml')
        if eye_cascade == "":
            sys.exit(234)
    
    # Do the stufpixpix__f
    files = [f for f in os.listdir(pix_path) if os.path.isfile(os.path.join(pix_path, f))]
    print files

    status = "NO EYES"

    for f in files:
        p = os.path.join(pix_path, f)
        img = cv2.imread(p)
        
        #print img
        gray_img = cv2.cvtColor(img, cv2.COLOR_BGR2GRAY)
        gray_img2 = cv2.GaussianBlur(gray_img, (9,9),2,2)
        
        eyes = eye_cascade.detectMultiScale(gray_img)#eye_detect(gray_img)
        frame = gray_img
        detected = eyes
        for (ex,ey,ew,eh) in eyes:
            cv2.rectangle(img,(ex,ey),(ex+ew,ey+eh),(0,255,0),2)

            """
        circles = cv2.HoughCircles(gray_img, cv2.cv.CV_HOUGH_GRADIENT, 1.2, 10)
    
        if circles is not None:
            circles = np.round(circles[0, :]).astype("int")

            for (x, y, radius) in circles:
                cv2.circle(img, (x, y), radius, (0, 255, 0), 4)

        """



            pupilFrame = frame
            pupilO = frame
            windowClose = np.ones((5,5),np.uint8)
            windowOpen = np.ones((2,2),np.uint8)
            windowErode = np.ones((2,2),np.uint8)
    
            #draw square
            for (x,y,w,h) in detected:
                cv2.rectangle(frame, (x,y), ((x+w),(y+h)), (0,0,255),1) 
                cv2.line(frame, (x,y), ((x+w,y+h)), (0,0,255),1)
                cv2.line(frame, (x+w,y), ((x,y+h)), (0,0,255),1)
                pupilFrame = cv2.equalizeHist(frame[y+(h*.25):(y+h), x:(x+w)])
                pupilO = pupilFrame
                ret, pupilFrame = cv2.threshold(pupilFrame,55,255,cv2.THRESH_BINARY)        #50 ..nothin 70 is better
                pupilFrame = cv2.morphologyEx(pupilFrame, cv2.MORPH_CLOSE, windowClose)
                pupilFrame = cv2.morphologyEx(pupilFrame, cv2.MORPH_ERODE, windowErode)
                pupilFrame = cv2.morphologyEx(pupilFrame, cv2.MORPH_OPEN, windowOpen)
    
                #so above we do image processing to get the pupil..
                #now we find the biggest blob and get the centriod
                
                threshold = cv2.inRange(pupilFrame,250,255)     #get the blobs
                contours, hierarchy = cv2.findContours(threshold,cv2.RETR_LIST,cv2.CHAIN_APPROX_SIMPLE)
                
                #if there are 3 or more blobs, delete the biggest and delete the left most for the right eye
                #if there are 2 blob, take the second largest
                #if there are 1 or less blobs, do nothing
                
                if len(contours) >= 2:
                    #find biggest blob
                    maxArea = 0
                    MAindex = 0         #to get the unwanted frame 
                    distanceX = []      #delete the left most (for right eye)
                    currentIndex = 0 
                    for cnt in contours:
                        area = cv2.contourArea(cnt)
                        center = cv2.moments(cnt)
                        cx,cy = int(center['m10']/center['m00']), int(center['m01']/center['m00'])
                        distanceX.append(cx)    
                        if area > maxArea:
                            maxArea = area
                            MAindex = currentIndex
                        currentIndex = currentIndex + 1
            
                    del contours[MAindex]       #remove the picture frame contour
                    del distanceX[MAindex]
                
                eye = 'right'
    
                if len(contours) >= 2:      #delete the left most blob for right eye
                    if eye == 'right':
                        edgeOfEye = distanceX.index(min(distanceX))
                    else:
                        edgeOfEye = distanceX.index(max(distanceX)) 
                    del contours[edgeOfEye]
                    del distanceX[edgeOfEye]
    
                if len(contours) >= 1:      #get largest blob
                    maxArea = 0
                    for cnt in contours:
                        area = cv2.contourArea(cnt)
                        if area > maxArea:
                            maxArea = area
                            largeBlob = cnt
                        
                if len(largeBlob) > 0:  
                    center = cv2.moments(largeBlob)
                    cx,cy = int(center['m10']/center['m00']), int(center['m01']/center['m00'])
                    cv2.circle(pupilO,(cx,cy),5,255,-1)
    
        
            #show picture
            cv2.imshow('frame',pupilO)
            cv2.imshow('frame2',pupilFrame)
            if cv2.waitKey(1) & 0xFF == ord('q'):
                break




        
        show_image(img)
        
    print "DONE DETECT"       

#def eye_detect(gray_img):
    

if __name__=='__main__':
    print "starting"
    import argparse
    parser = argparse.ArgumentParser(description="Detects Blinks")
    parser.add_argument('path', type=str, help="Path to pics")

    args = parser.parse_args()

    print "Directory is ", args.path

    PATH_TO_PICS = args.path

    path_exists = os.path.isdir(PATH_TO_PICS)
    
    print "exists?", path_exists

    if not path_exists:
        print "PATH DOESN'T EXIST"
        sys.exit(1234)

    else:
        blink_detect(PATH_TO_PICS)
