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
from math import sqrt

import tkinter as tk
from tkinter import messagebox, Tk, Frame, Menu, ttk

#import imutils


brush_stats = {'pencil_down': False,'size':10,'color':(0,0,0),'previous_x': 0,'previous_y': 0}
centroid_tuple = namedtuple('centroid_tuple',['x','y'])
usp_sensitivity = 200



def KeyboardpresS(img,brush_stats,copypaint,copyimg,centroids,switch,mouse):
    key_pressed = cv2.waitKey(50) & 0xFF

    if key_pressed == ord('q'):
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
        copyimg = deepcopy(img)
        centroids['x'] = []
        centroids['y'] = []
        print('Cleared Canvas')
        

    elif key_pressed == ord('w'):
        date = time.ctime(time.time())
        file_name = "Drawing " + date +".png"
        print("Saving png image as " + Fore.LIGHTBLUE_EX + file_name + Style.RESET_ALL)

        cv2.imwrite(file_name , copypaint) 
    
    elif key_pressed == ord('j'):
        print(switch)
        switch = (0) if switch == 1 else 1
        print(switch)
    
    elif key_pressed == ord('m'):
        mouse = True
        print('Mouse Mode selected')
    
    elif key_pressed == ord('i'):
        mouse = False
        print('Vídeo Mode selected')
    
    
    
    
    return copyimg,copypaint,centroids,switch, mouse


def mouseCallback(event,x,y,flag,param,copypaint,brush_stats):


    if event == cv2.EVENT_LBUTTONDOWN:                  #Se acaso o botão do maouse for precionado.
        brush_stats['pencil_down'] = True              #Pencil_down tem q ser uma variável imutável e portanto leva [0].
        print('x = ' +str(x), ',y = '+str(y))

    elif event == cv2.EVENT_LBUTTONUP:
        brush_stats['pencil_down'] = False

    if brush_stats['pencil_down'] == True:
        cv2.line(copypaint, (brush_stats['previous_x'],brush_stats['previous_y']),
                 (x,y), brush_stats['color'],brush_stats['size'], 1)
                                                                                
    
    brush_stats['previous_x'] = x
    brush_stats['previous_y'] = y



def SelectingMode (img,mask,copypaint,copyimg,centroids,brush_stats,usp,switch,mouse):


    if mouse == True:
        cv2.setMouseCallback('paintwindow',partial(mouseCallback,copypaint=copypaint,brush_stats=brush_stats))

    elif mouse ==False:
        draw(img,mask,copypaint,copyimg,centroids,brush_stats,usp,switch)


def drawLine(copyimg,copypaint,points,brush_stats,usp,switch):

    if points['x'] == []: # without points just skip
        return

    # If cant do a line, does a circle
    if len(points['x']) < 2: 
        cv2.circle(copypaint if switch == 0 else copyimg, (points['x'][-1],points['y'][-1]) ,
                   brush_stats['size'] //2 ,brush_stats['color'], -1)

        return
    

    # If can do a line goes here
    initial_point = (points['x'][-2],points['y'][-2] )
    final_point = (points['x'][-1],points['y'][-1] )
    
    # using shake protection
    if usp: 
        distance = round(sqrt((initial_point[0]-final_point[0])**2+(initial_point[1]-final_point[1])**2))
        if distance > usp_sensitivity:
            cv2.circle(copypaint if switch == 0 else copyimg, (points['x'][-1],points['y'][-1]),
                       brush_stats['size'] //2 ,brush_stats['color'], -1) 
            return

    cv2.line(copypaint if switch == 0 else copyimg, initial_point, final_point, brush_stats['color'], brush_stats['size'])
   

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
        largest_component_label = np.argmax(stats[1:, cv2.CC_STAT_AREA]) + 1
    
        # Create a mask containing only the largest component
        largest_component_mask = np.uint8(labels == largest_component_label) * 255
        
        #! TODO PAINT THE OBJECT IN GREEN ON THE MASK IMSHOW    
        
        # Calculate moments of the largest component
        moments = cv2.moments(largest_component_mask)

        # Calculate the centroid coordinates
        if moments["m00"] != 0:
            cx = int(moments["m10"] / moments["m00"])
            cy = int(moments["m01"] / moments["m00"])
            centroid = centroid_tuple(x= int(cx), y=int(cy))

            return centroid
                
        else:
            print("No centroid found (division by zero)")
                
    
    elif num_labels == 1:
        centroid = centroid_tuple(x= -50,y=-50) 
        return centroid
        

def draw(img, mask,copypaint,copyimg,centroids,brush_stats,usp,switch):

        # find centroid in img

        cccentroid = connectedcomponents(mask)
        
        #mark with red x
        cv2.drawMarker(img, cccentroid, color=[0, 0, 255], thickness=3,
                       markerType= cv2.MARKER_TILTED_CROSS, line_type=cv2.LINE_AA,markerSize=25)


        # recording centroids
        
        centroids['x'].append(cccentroid.x) 
        centroids['y'].append(cccentroid.y)
        
        if len(centroids['x']) >= 4 :
            centroids['x'] = centroids['x'][-2:] # If the list gets too big, cleans it back to the last 2, which are needed for drawing
            centroids['y'] = centroids['y'][-2:] 

        
            drawLine(copyimg,copypaint,centroids,brush_stats,usp,switch)


def Menu_interface():

    # root window
    root = tk.Tk()
    root.title('Menu Demo')
    root.geometry("500x500")
    root.resizable(0,0)

    # configure the grid
    root.columnconfigure(0, weight=1)
    root.columnconfigure(1, weight=3)

    # Informatinos about the keys
    username_label = ttk.Label(root, text="Funcionalidades:")
    username_label.grid(column=0, row=0, sticky=tk.W, padx=5, pady=5)
    
    password_label = ttk.Label(root, text="Q - Quitting program")
    password_label.grid(column=0, row=1, sticky=tk.W, padx=5, pady=5)

    password_label = ttk.Label(root, text="R - Red color")
    password_label.grid(column=0, row=2, sticky=tk.W, padx=5, pady=5)
    
    password_label = ttk.Label(root, text="B - Blue color")
    password_label.grid(column=0, row=3, sticky=tk.W, padx=5, pady=5)
    
    password_label = ttk.Label(root, text="G - Green color")
    password_label.grid(column=0, row=4, sticky=tk.W, padx=5, pady=5)

    password_label = ttk.Label(root, text="P - Black color")
    password_label.grid(column=0, row=5, sticky=tk.W, padx=5, pady=5)

    password_label = ttk.Label(root, text="M - Mouse mode")
    password_label.grid(column=0, row=6, sticky=tk.W, padx=5, pady=5)

    password_label = ttk.Label(root, text="I - Image Mode")
    password_label.grid(column=0, row=7, sticky=tk.W, padx=5, pady=5)

    password_label = ttk.Label(root, text="X - Rubber")
    password_label.grid(column=1, row=1, sticky=tk.W, padx=5, pady=5)

    password_label = ttk.Label(root, text="C - Clear cavas")
    password_label.grid(column=1, row=2, sticky=tk.W, padx=5, pady=5)

    password_label = ttk.Label(root, text="W - Saving Draw")
    password_label.grid(column=1, row=3, sticky=tk.W, padx=5, pady=5)

    password_label = ttk.Label(root, text="+ - Increasing size")
    password_label.grid(column=1, row=4, sticky=tk.W, padx=5, pady=5)

    password_label = ttk.Label(root, text="- - Decreasing size")
    password_label.grid(column=1, row=5, sticky=tk.W, padx=5, pady=5)

    password_label = ttk.Label(root, text="J - Draw on video window")
    password_label.grid(column=1, row=6, sticky=tk.W, padx=5, pady=5)

    
    # create a menubar
    menubar = Menu(root)
    root.config(menu=menubar)
    # create a menu
    file_menu = Menu(menubar)
    # add a menu item to the menu
    file_menu.add_command(label='Exit',command=root.destroy)
    # add the File menu to the menubar
    menubar.add_cascade(label="File",menu=file_menu)
    root.mainloop()


    
def main():
    global usp_sensitivity
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
    switch = 0
    
    windowsize = img.shape
    centroids = { 'x' : [], 'y' : []}
    copyimg = deepcopy(img)
    paintWindow = np.zeros((img.shape)) + 255
    
    usp = args.use_shake_prevention
    copypaint = deepcopy(paintWindow)

    brush_stats = {'size' : 10, 'color' : (0,0,0)}
    
    mouse =False
    alpha = 0.2
    beta = (1.0 - alpha)

    Menu_interface()

    while(1):

        # atualizar camara
        
        ret_val, img = cam.read()
        img = cv2.flip(img, 1)

        # mask
        hsv = cv2.cvtColor(img, cv2.COLOR_BGR2HSV)
        upper = np.array([high_H, high_S, high_V])
        lower = np.array([low_H,low_S,low_V])
        mask = cv2.inRange(hsv, lower, upper)
        img2 = deepcopy(img)

        copyimg, copypaint, centroids, switch, mouse = KeyboardpresS(img,brush_stats,copypaint,copyimg,centroids,switch, mouse) 
        SelectingMode(img,mask,copypaint,copyimg,centroids,brush_stats,usp,switch, mouse)
        img2 = cv2.addWeighted(copyimg,alpha,img2,beta,0.0)
       
        cv2.imshow('mask',mask)
        
        cv2.imshow('Image with Centroid', img)
        if switch == 0:
            cv2.imshow('paintwindow',copypaint)
        else:
            cv2.imshow('paintCam',img2)



if __name__ == '__main__':
    main()
