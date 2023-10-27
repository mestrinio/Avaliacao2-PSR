#!/usr/bin/env python3
import cv2
import numpy as np



def show_webcam(mirror=False):
    cam = cv2.VideoCapture(0)
    while True:
        ret_val, img = cam.read()
        
        if mirror: 
            img = cv2.flip(img, 1)
            cv2.imshow('my webcam', img)
            
        gray_image = cv2.cvtColor(img, cv2.COLOR_BGR2GRAY)
        
        # Convert BGR to HSV
        hsv = cv2.cvtColor(img, cv2.COLOR_BGR2HSV)

        #define range of blue color in HSV
        lower_yellow = np.array([15,50,180])
        upper_yellow = np.array([40,255,255])
        mask = cv2.inRange(hsv, lower_yellow, upper_yellow)
    

        # display the mask and masked image
        cv2.imshow('Mask',mask)
        
        ret, thresh1 = cv2.threshold(mask,127,255,cv2.THRESH_BINARY)
        cv2.imshow('thresh',thresh1)
        #ret, thresh = cv2.threshold(gray_image, 50, 255, cv2.THRESH_BINARY)
        #im, contours = cv2.findContours(thresh, cv2.RETR_EXTERNAL, cv2.CHAIN_APPROX_NONE)
        #cv2.drawContours(img, contours, 0, (0, 255, 0), 2)
        #M = cv2.moments(contours[0])
        
        #print("center X : '{}'".format(round(M['m10'] / M['m00'])))
        #print("center Y : '{}'".format(round(M['m01'] / M['m00'])))

        # Draw a circle based centered at centroid coordinates
        #cv2.circle(img, (round(M['m10'] / M['m00']), round(M['m01'] / M['m00'])), 5, (0, 255, 0), -1)
        
        
        if cv2.waitKey(1) == 27: 
            break  # esc to quit
    cv2.destroyAllWindows()


def main():
    show_webcam(mirror=True)

    



if __name__ == "__main__":
    main()