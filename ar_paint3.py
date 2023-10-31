#!/usr/bin/env python3
#shebang line to inform the OS that the content is in python

from __future__ import print_function
from copy import deepcopy
import time
import cv2
import argparse
from colorama import Fore, Back, Style
import json
import color_segmenter1
import numpy as np
import linecache
import os
import readchar

#import imutils

##arguments
import argparse

brush_stats = {'size':10,'color':(0,0,0)}


def arguments():
    parser = argparse.ArgumentParser(description='Menu of Drawing Mode')
    parser.add_argument('-j', '--json', help='Full path to JSON file', required=True)
    args = parser.parse_args()
    return args







def keyboardpress(brush_stats,copypaint,img):
    cl = 0
    key_pressed = cv2.waitKey(50) & 0xFF
    if key_pressed == ord('q'):
        cv2.destroyAllWindows
        print('Exiting...')
        exit
        
    elif key_pressed == ord('r'):
        brush_stats['color'] = (0,0,255)
        print('Brush color set to red')
        
    elif key_pressed == ord('g'):
        brush_stats['color'] = (0,255,0)
        print('Brush color set to green')
            
    elif key_pressed == ord('b'):
        brush_stats['color'] = (255,0,0)
        print('Brush color set to blue')
        
    elif key_pressed == ord('+'):
        
        if brush_stats['size'] < 50:
            brush_stats['size'] += 1
            print('Increased size +1')
        else:
            print('Max size reached')
            
    elif key_pressed == ord('-'):
        
        if brush_stats['size'] > 1:
            brush_stats['size'] -= 1
            print('Decreased size -1')
        else:
            print('Min size reached')
            
    elif key_pressed == ord('c'):
        cl = 1
        print('Cleared Canvas')
        

    elif key_pressed == ord('w'):
        date = time.ctime(time.time())
        file_name = "Drawing " + date +".png"
        print("Saving png image as " + file_name)

        cv2.imwrite(file_name , copypaint) #! Caso seja com o video pode ter de se mudar aqui

    return cl
            
    
    

def show_webcam(low_H, low_S, low_V, high_H, high_S, high_V ,brush_stats=brush_stats, mirror=False):
    cam = cv2.VideoCapture(0)
    ret_val, img = cam.read()
    paintWindow = np.zeros((img.shape)) + 255
    copypaint = deepcopy(paintWindow)
    
    while True:
        c = keyboardpress(brush_stats,copypaint,img)
        ret_val, img = cam.read()
        
        if mirror:
            img = cv2.flip(img, 1)
            
        
          
        
        hsv = cv2.cvtColor(img, cv2.COLOR_BGR2HSV)
        
        # Define the range of yellow color in HSV
        #print(type(high_H))
        upper_yellow = np.array([high_H, high_S, high_V])
        lower_yellow = np.array([low_H,low_S,low_V])
        
        #print(upper_yellow,lower_yellow)
        mask = cv2.inRange(hsv, lower_yellow, upper_yellow)
        
        
        # Find connected components in the binary mask
        num_labels, labels, stats, centroids = cv2.connectedComponentsWithStats(mask, connectivity=4)
        #print(num_labels)
        
        
        # Find the label (component) with the largest area
        
        if num_labels > 1:
            #print('video ativo aqui 2')
            largest_component_label = np.argmax(stats[1:, cv2.CC_STAT_AREA]) + 1
            #print('video ativo aqui 3')
        
            # Create a mask containing only the largest component
            largest_component_mask = np.uint8(labels == largest_component_label) * 255
        
            # Calculate moments of the largest component
            moments = cv2.moments(largest_component_mask)

            # Calculate the centroid coordinates
            if moments["m00"] != 0:
                cx = int(moments["m10"] / moments["m00"])
                cy = int(moments["m01"] / moments["m00"])
                #print("Centroid X:", cx)
                #print("Centroid Y:", cy)
                
            else:
                print("No centroid found (division by zero)")

            
            
            if c == 1: # CLEAR PAINT WINDOW
                c = 0
                paintWindow = np.zeros((img.shape)) + 255
            
            cv2.drawMarker(img, (cx, cy), color=[0, 0, 255], thickness=7,markerType= cv2.MARKER_TILTED_CROSS, line_type=cv2.LINE_AA,markerSize=30)
            cv2.circle(hsv,(cx,cy),55,(0,0,255),-1)
            cv2.circle(paintWindow,(cx,cy),brush_stats['size'],brush_stats['color'],-1)
            copypaint = deepcopy(paintWindow) 
            
        
            # Display the largest component mask and the image with the centroid
            #cv2.imshow('Largest Component Mask', largest_component_mask)
        cv2.imshow('mask',mask)
        cv2.imshow('Image with Centroid', img)
        cv2.imshow('drawing', paintWindow)
        
        
        if cv2.waitKey(1) == 27:
            break  # Close the window if the 'Esc' key is pressed

    cam.release()
    cv2.destroyAllWindows()
    
    


def limits(json_file):
 
    """
    This function is only for reading the values of the json file.
    """
    
    #Reading Values from limits.json
    with open(json_file, 'r') as file_handle:
        load_file = json.load(file_handle)
           

    limits_file = load_file['limits']
    print('Carregou o dcio...')

    #loading Limits B
    B_limits = limits_file['B']
    low_H = B_limits['min']
    print("B min " + str(low_H))

    high_H = B_limits['max']
    print("B min " + str(high_H))

    #loading Limits G 
    G_limits = limits_file['G']
    low_S = G_limits['min']
    print("G max " + str(low_S))

    high_S = G_limits['max']
    print("G max " + str(high_S))

    #loading Limits R
    R_limits = limits_file['R']
    low_V = R_limits['min']
    print("R max " + str(low_V))

    high_V = R_limits['max']
    print("R max " + str(high_V))
    
    return low_H, low_S, low_V, high_H, high_S, high_V

def main():
    global brush_stats
    global copypaint
    args = arguments()
    json_file = args.json
    low_H, low_S, low_V, high_H, high_S, high_V= limits(json_file)
    show_webcam(low_H, low_S, low_V, high_H, high_S, high_V, mirror=True)
    
    

if __name__ == '__main__':
    main()
