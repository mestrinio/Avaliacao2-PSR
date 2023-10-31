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


brush_stats = {'size':10,'color':(0,0,0),'previous_x': 0,'previous_y': 0}


def ArgumentS():

    """
    This function is only for creating the arguments which the user must input.
    """
    parser = argparse.ArgumentParser(description='Menu of Drawing Mode')
    parser.add_argument('-j', '--json', help='Full path to JSON file', required=True)
    args = parser.parse_args()
    return args


def KeyboardpresS(brush_stats,copypaint,img):
    quiting = 0
    cl = 0
    key_pressed = cv2.waitKey(50) & 0xFF

    if key_pressed == ord('q'):
        cv2.destroyAllWindows
        quiting = 1
        print('Exiting...')
    
        
    elif key_pressed == ord('r'):
        brush_stats['color'] = (0,0,255)
        print(Fore.RED+'Brush color set to red'+Style.RESET_ALL)
        
    elif key_pressed == ord('g'):
        brush_stats['color'] = (0,255,0)
        print(Fore.GREEN+'Brush color set to green'+Style.RESET_ALL)
            
    elif key_pressed == ord('b'):
        brush_stats['color'] = (255,0,0)
        print(Fore.BLUE+'Brush color set to blue'+Style.RESET_ALL)
    
    elif key_pressed == ord('p'):
        brush_stats['color'] = (0,0,0)
        print(Fore.LIGHTBLACK_EX+'Brush color set to black'+Style.RESET_ALL)
    
    elif key_pressed == ord('x'):
        brush_stats['color'] = (250,250,250)
        brush_stats['size'] = 30
        print(Fore.CYAN+'Ruber'+Style.RESET_ALL)
        
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
        print("Saving png image as " + Fore.LIGHTBLUE_EX + file_name + Style.RESET_ALL)

        cv2.imwrite(file_name , copypaint) #! Caso seja com o video pode ter de se mudar aqui
    
    
    return cl , quiting


def Shake_PreventioN(event, x, y, flags, param, copypain, drawing_data):

    
    drawing_data = {'pencil_down': False,'previous_x': 0,'previous_y': 0, 'color': (255,255,255)}

    if event == cv2.EVENT_LBUTTONDOWN:                  #Se acaso o botão do maouse for precionado.
        drawing_data['pencil_down'] = True              #Pencil_down tem q ser uma variável imutável e portanto leva [0].
        print('x = ' +str(x), ',y = '+str(y))

    elif event == cv2.EVENT_LBUTTONUP:
        drawing_data['pencil_down'] = False

    if drawing_data['pencil_down'] == True:
        cv2.line(copypaint, (drawing_data['previous_x'],drawing_data['previous_y']), (x,y), drawing_data['color'], 1)
                                                                                
    
    drawing_data['previous_x'] = x
    drawing_data['previous_y'] = y

    cv2.setMouseCallback(copypaint ,drawing_data)
            
    
    

def Show_webcaM(low_H, low_S, low_V, high_H, high_S, high_V ,brush_stats=brush_stats, mirror=False):

    cam = cv2.VideoCapture(0)
    ret_val, img = cam.read()
    paintWindow = np.zeros((img.shape)) + 255
    copypaint = deepcopy(paintWindow)

    

    while True:
        
        c, quiting = KeyboardpresS(brush_stats,copypaint,img)
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
            largest_component_label = np.argmax(stats[1:, cv2.CC_STAT_AREA]) + 1
        
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

            # CLEAR PAINT WINDOW            
            if c == 1: 
                c = 0
                paintWindow = np.zeros((img.shape)) + 255
                print("Clear all!")

            #Quiting Program
            if quiting == 1:
                break

            
           
            cv2.drawMarker(img, (cx, cy), color=[0, 0, 255], thickness=7,
                           markerType= cv2.MARKER_TILTED_CROSS, line_type=cv2.LINE_AA,markerSize=30)
            
            cv2.line(paintWindow,(brush_stats['previous_x'],brush_stats['previous_y']), 
                     (cx,cy), brush_stats['color'], brush_stats['size'])
            
            cv2.circle(hsv,(cx,cy),55,(0,0,255),-1)
            #cv2.circle(paintWindow,(cx,cy),brush_stats['size'],brush_stats['color'],-1)
            copypaint = deepcopy(paintWindow) 
            
            brush_stats['previous_x'] = cx
            brush_stats['previous_y'] = cy
        
            # Display the largest component mask and the image with the centroid
            #cv2.imshow('Largest Component Mask', largest_component_mask)
            
        cv2.imshow('mask',mask)
        cv2.imshow('Image with Centroid', img)
        cv2.imshow('drawing', paintWindow)
        
        
        if cv2.waitKey(1) == 27:
            break  # Close the window if the 'Esc' key is pressed

    cam.release()
    cv2.destroyAllWindows()

    return paintWindow
    
    

def LimitS(json_file):
 
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
    args = ArgumentS()
    json_file = args.json
    low_H, low_S, low_V, high_H, high_S, high_V= LimitS(json_file)
    Show_webcaM(low_H, low_S, low_V, high_H, high_S, high_V, mirror=True)
    
    

if __name__ == '__main__':
    main()