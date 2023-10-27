#!/usr/bin/env python3


# Imports -------------------------------------------------
import numpy as np
import cv2
from collections import deque


# Init ----------------------------------------------------
vid = cv2.VideoCapture(0)
vid.set(3,1280)
vid.set(4,720)

def main():
    while(True): 
      
        # Capture the video frame 
        # by frame 
        ret, frame = vid.read() 
        frame = cv2.flip(frame, 1)
        # Display the resulting frame 
        cv2.imshow('frame', frame) 
      
        # the 'q' button is set as the quitting button you may use any desired button of your choice 
        if cv2.waitKey(1) & 0xFF == ord('q'): 
            break
  

        kernel = np.ones((5,5),np.uint8)
        # Initializing the canvas on which we will draw upon
        canvas = None   # Initilize x1,y1 points
        x1,y1 = 0,0   # Threshold for noise
        noiseth = 800


        if canvas is None:
            canvas = np.ones_like(frame)


        hsv = cv2.cvtColor(frame, cv2.COLOR_BGR2HSV)


        # If you're reading from memory then load the upper and lower ranges 
        # from there
        #f load_from_disk:
        #lower_range = hsv_value[0]
        #upper_range = hsv_value[1]


        # Otherwise define your own custom values for upper and lower range.
        # else:

        lower_range  = np.array([134, 20, 204])
        upper_range = np.array([179, 255, 255])



        mask = cv2.inRange(hsv, lower_range, upper_range)

        mask = cv2.erode(mask,kernel,iterations = 1)
        mask = cv2.dilate(mask,kernel,iterations = 2)



        contours, hierarchy = cv2.findContours(mask, cv2.RETR_EXTERNAL, cv2.CHAIN_APPROX_SIMPLE)

        if contours and cv2.contourArea(max(contours, key = cv2.contourArea)) > noiseth:
            c = max(contours, key = cv2.contourArea)    
            x2,y2,w,h = cv2.boundingRect(c)

            # If there were no previous points then save the detected x2,y2 
            # coordinates as x1,y1. 
            # This is true when we writing for the first time or when writing 
            # again when the pen had disappeared from view.
            if x1 == 0 and y1 == 0:
                x1,y1= x2,y2

            else:
                # Draw the line on the canvas
                canvas = cv2.line(canvas, (x1,y1),(x2,y2), [255,0,0], 4)

            # After the line is drawn the new points become the previous points.
            x1,y1= x2,y2    

        else:
            # If there were no contours detected then make x1,y1 = 0
            x1,y1 =0,0

        # Merge the canvas and the frame.
        frame = cv2.add(frame,canvas)


        k = cv2.waitKey(1) & 0xFF
        if k == 27:
            break
        
        # When c is pressed clear the canvas
        if k == ord('c'):
            canvas = None


    # After the loop release the cap object 
    vid.release() 
    # Destroy all the windows 
    cv2.destroyAllWindows() 

    

if __name__ == "__main__":
    main()