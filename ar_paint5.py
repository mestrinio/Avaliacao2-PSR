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
from functools import partial
from collections import namedtuple
#import imutils


brush_stats = {'size':10,'color':(0,0,0),'previous_x': 0,'previous_y': 0}
centroid_tuple = namedtuple('centroid_tuple',['x','y'])
usp_sensitivity = 100

def ArgumentS():

    """
    This function is only for creating the arguments which the user must input.
    """
    parser = argparse.ArgumentParser(description='Menu of Drawing Mode')
    parser.add_argument('-j', '--json', help='Full path to JSON file', required=True)
    parser.add_argument('-usp','--use_shake_prevention', action='store_true',default = False ,help='Activate shake prevention mode')
    
    args = parser.parse_args()
    return args

# NEEDS CORRECTION
def KeyboardpresS(brush_stats,copypaint,img):
    key_pressed = cv2.waitKey(50) & 0xFF

    if key_pressed == ord('q'):
        #cv2.destroyAllWindows
        print('Exiting...')
        exit()
        
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
        print(Fore.CYAN+'Rubber'+Style.RESET_ALL)
        
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
        shape = copypaint.shape
        copypaint = np.zeros((shape)) + 255
        centroids['x'] = []
        centroids['y'] = []
        print('Cleared Canvas')
        

    elif key_pressed == ord('w'):
        date = time.ctime(time.time())
        file_name = "Drawing " + date +".png"
        print("Saving png image as " + Fore.LIGHTBLUE_EX + file_name + Style.RESET_ALL)

        cv2.imwrite(file_name , copypaint) #! Caso seja com o video pode ter de se mudar aqui
    
    
    return 

def mouseCallback(event,x,y,flag,param,points):

    if event == cv2.EVENT_LBUTTONDOWN:
        points['x'].append(x)
        points['y'].append(y)
    return

def drawLine(copypaint,points,brush_stats,usp):

    if points['x'] == []: # without points just skip
        return

    # If cant do a line, does a circle
    if len(points['x']) < 2: 
        cv2.circle(copypaint, (points['x'][-1],points['y'][-1]) , brush_stats['size'] //2 ,brush_stats['color'], -1)

        return
    

    # If can do a line goes here
    initial_point = (points['x'][-2],points['y'][-2] )
    final_point = (points['x'][-1],points['y'][-1] )
    
    # using shake protection
    if usp: 
        distance = round(sqrt((initial_point[0]-final_point[0])**2+(initial_point[1]-final_point[1])**2))
        if distance > usp_sensitivity:
            cv2.circle(copypaint, (points['x'][-1],points['y'][-1]) , brush_stats['size'] //2 ,brush_stats['color'], -1) # !!!!!!!!!!!! //2
            return


def Shake_PreventioN(event, x, y, flags, param, copypaint, drawing_data):

    
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
            
    
    
# LEGACY
#def Show_webcaM(low_H, low_S, low_V, high_H, high_S, high_V ,brush_stats=brush_stats, mirror=False):
#
#    cam = cv2.VideoCapture(0)
#    ret_val, img = cam.read()
#    paintWindow = np.zeros((img.shape)) + 255
#    copypaint = deepcopy(paintWindow)
#
#    
#
#    while True:
#        
#        c, quiting = KeyboardpresS(brush_stats,copypaint,img)
#        ret_val, img = cam.read()
#        
#        if mirror:
#            img = cv2.flip(img, 1)
#        
#        hsv = cv2.cvtColor(img, cv2.COLOR_BGR2HSV)
#        
#        # Define the range of yellow color in HSV
#        #print(type(high_H))
#        upper_yellow = np.array([high_H, high_S, high_V])
#        lower_yellow = np.array([low_H,low_S,low_V])
#        
#        #print(upper_yellow,lower_yellow)
#        mask = cv2.inRange(hsv, lower_yellow, upper_yellow)
#        
#        
#        # Find connected components in the binary mask
#        num_labels, labels, stats, centroids = cv2.connectedComponentsWithStats(mask, connectivity=4)
#        #print(num_labels)
#        
#        
#        # Find the label (component) with the largest area
#        if num_labels > 1:
#            largest_component_label = np.argmax(stats[1:, cv2.CC_STAT_AREA]) + 1
#        
#            # Create a mask containing only the largest component
#            largest_component_mask = np.uint8(labels == largest_component_label) * 255
#        
#            # Calculate moments of the largest component
#            moments = cv2.moments(largest_component_mask)
#
#            # Calculate the centroid coordinates
#            if moments["m00"] != 0:
#                cx = int(moments["m10"] / moments["m00"])
#                cy = int(moments["m01"] / moments["m00"])
#                #print("Centroid X:", cx)
#                #print("Centroid Y:", cy)
#                
#            else:
#                print("No centroid found (division by zero)")
#
#            # CLEAR PAINT WINDOW            
#            if c == 1: 
#                c = 0
#                paintWindow = np.zeros((img.shape)) + 255
#                print("Clear all!")
#
#            #Quiting Program
#            if quiting == 1:
#                break
#
#            
#           
#            cv2.drawMarker(img, (cx, cy), color=[0, 0, 255], thickness=7,
#                           markerType= cv2.MARKER_TILTED_CROSS, line_type=cv2.LINE_AA,markerSize=30)
#            
#            cv2.line(paintWindow,(brush_stats['previous_x'],brush_stats['previous_y']), 
#                     (cx,cy), brush_stats['color'], brush_stats['size'])
#            
#            cv2.circle(hsv,(cx,cy),55,(0,0,255),-1)
#            #cv2.circle(paintWindow,(cx,cy),brush_stats['size'],brush_stats['color'],-1)
#            copypaint = deepcopy(paintWindow) 
#            
#            brush_stats['previous_x'] = cx
#            brush_stats['previous_y'] = cy
#        
#            # Display the largest component mask and the image with the centroid
#            #cv2.imshow('Largest Component Mask', largest_component_mask)
#            
#        cv2.imshow('mask',mask)
#        cv2.imshow('Image with Centroid', img)
#        cv2.imshow('drawing', paintWindow)
#        
#        
#        if cv2.waitKey(1) == 27:
#            break  # Close the window if the 'Esc' key is pressed
#
#    cam.release()
#    cv2.destroyAllWindows()
#
#    return paintWindow
    
    

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



def connectedcomponents(mask):
    
    shape = mask.shape
    cc_output_matrix = cv2.connectedComponentsWithStats(mask,connectivity =4)
    num_labels, labels, stats, centroids = cv2.connectedComponentsWithStats(mask, connectivity=4)
    if num_labels > 1:
            #print('video ativo aqui 2')
            largest_component_label = np.argmax(stats[1:, cv2.CC_STAT_AREA]) + 1
            #print('video ativo aqui 3')
        
            # Create a mask containing only the largest component
            largest_component_mask = np.uint8(labels == largest_component_label) * 255
            
            #! TODO PAINT THE OBJECT IN GREEN ON THE MASK IMSHOW    
            
            # Calculate moments of the largest component
            moments = cv2.moments(largest_component_mask)

            # Calculate the centroid coordinates
            if moments["m00"] != 0:
                cx = int(moments["m10"] / moments["m00"])
                cy = int(moments["m01"] / moments["m00"])
                centroid = centroid_tuple(x= int(x), y=int(y))
                #print("Centroid X:", cx)
                #print("Centroid Y:", cy)
                return centroid
                
            else:
                print("No centroid found (division by zero)")


def drawingCore(img, mask,copypaint,centroids,brush_stats,usp):

        # find centroid in img

        cccentroid = connectcomponents(mask)
        #cc_mask = np.where(cc_mask,mask,0)  
        
        #mark with red x
        cv2.drawMarker(img, cccentroid, color=[0, 0, 255], thickness=7,markerType= cv2.MARKER_TILTED_CROSS, line_type=cv2.LINE_AA,markerSize=30)


        # recording centroids
        centroids['x'].append(cccentroid.x) # cccentroid is a namedTuple
        centroids['y'].append(cccentroid.y)
        
        if len(centroids['x']) >= 5 :
            centroids['x'] = centroids['x'][-2:] # If the list gets too big, cleans it back to the last 2, which are needed for drawing
            centroids['y'] = centroids['y'][-2:] 
    
        drawLine(copypaint,centroids,brush_stats,usp)

        # show biggest object in mask

        #! This is here because cc_mask is only relevant inside this fc and didn't want to have it as output
        #cv2.imshow("Biggest Object in Mask",cc_mask)



#def main():
#    
#    global drawing_data
#    global brush_stats
#    global copypaint
#    args = ArgumentS()
#    usp = args.use_shake_prevention
#    json_file = args.json
#    low_H, low_S, low_V, high_H, high_S, high_V= LimitS(json_file)
#    Show_webcaM(low_H, low_S, low_V, high_H, high_S, high_V, mirror=True)
    
    
def main():
    global usp_sensitivity
    ArgumentS()
    parser = argparse.ArgumentParser(description='Menu of Drawing Mode')
    parser.add_argument('-j', '--json', help='Full path to JSON file', required=True)
    parser.add_argument('-usp','--use_shake_prevention', action='store_true',default = False ,help='Activate shake prevention mode')
    args = parser.parse_args()
    json_file = args.json
    low_H, low_S, low_V, high_H, high_S, high_V= LimitS(json_file)
    

    # Camera and paint window
    cam = cv2.VideoCapture(0)
    ret_val, img = cam.read()
    img = cv2.flip(img, 1)
    
    
    windowsize = img.shape
    centroids = { 'x' : [], 'y' : []}
    
    paintWindow = np.zeros((img.shape)) + 255
    
    usp = args.use_shake_prevention
    copypaint = deepcopy(img)

    brush_stats = {'size' : 10, 'color' : (0,0,0)}
    
   

    cv2.namedWindow("Drawing")
    cv2.setMouseCallback("Drawing",partial(mouseCallback,points = centroids))

   ##* ---Adding trackbar to change usp sensibility if on---
#
   # if usp:
   #     if puzzle_mode:
   #         cv2.createTrackbar("Usp_sensibility","Puzzle",usp_sensitivity,400,lambda x:x)
   #     elif normal_mode:
   #         cv2.createTrackbar("Usp_sensibility","Drawing",usp_sensitivity,400,lambda x:x)

   
    while(1):
        ##* ---Updating usp sensibility---
#
        #
        #if puzzle_mode:
        #    usp_sensitivity = cv2.getTrackbarPos("Usp_sensibility","Puzzle")
        #elif normal_mode:
        #    usp_sensitivity = cv2.getTrackbarPos("Usp_sensibility","Drawing")


        # atualizar camara
        
        ret_val, img = cam.read()
        img = cv2.flip(img, 1)

        # mask
        hsv = cv2.cvtColor(img, cv2.COLOR_BGR2HSV)
        upper = np.array([high_H, high_S, high_V])
        lower = np.array([low_H,low_S,low_V])
        mask = cv2.inRange(hsv, lower, upper)
        
        
        num_labels, labels, stats, centroids = cv2.connectedComponentsWithStats(mask, connectivity=4)
        
        
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
                
            else:
                print("No centroid found (division by zero)")
        

        # drawingCore(img, mask,src_copypaint,centroids,brush_stats,usp,flip_flop,shape_points,puzzle_mode)

        try:
            drawingCore(img, mask,copypaint,centroids,brush_stats,usp)
            
        cv2.imshow('mask',mask)
        cv2.imshow('Image with Centroid', img)
        KeyboardpresS(brush_stats,copypaint,centroids)
        
        

    
    

if __name__ == '__main__':
    main()