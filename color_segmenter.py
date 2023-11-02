#!/usr/bin/env python3
#shebang line to inform the OS that the content is in python

from __future__ import print_function
import cv2
import argparse
from colorama import Fore, Back, Style
import json

max_value = 255

low_H = 0
low_S = 0
low_V = 0

high_H = max_value
high_S = max_value
high_V = max_value

window_capture_name = 'Video Capture'
window_detection_name = 'Object Detection'

low_H_name = 'Low H'
low_S_name = 'Low S'
low_V_name = 'Low V'

high_H_name = 'High H'
high_S_name = 'High S'
high_V_name = 'High V'



## [low H]
def on_low_H_thresh_trackbar(val):
    global low_H
    global high_H
    low_H = val
    low_H = min(low_H,high_H)
    cv2.setTrackbarPos(low_H_name, window_detection_name, low_H)
## [low H]

## [high H]
def on_high_H_thresh_trackbar(val):
    global low_H
    global high_H
    high_H = val
    high_H = max(high_H,low_H)
    cv2.setTrackbarPos(high_H_name, window_detection_name, high_H)
## [high H]

## [low S]
def on_low_S_thresh_trackbar(val):
    global low_S
    global high_S
    low_S = val
    low_S = min(high_S, low_S)
    cv2.setTrackbarPos(low_S_name, window_detection_name, low_S)
## [low S]

## [high S]
def on_high_S_thresh_trackbar(val):
    global low_S
    global high_S
    high_S = val
    high_S = max(high_S, low_S)
    cv2.setTrackbarPos(high_S_name, window_detection_name, high_S)
## [high S]

## [low V]
def on_low_V_thresh_trackbar(val):
    global low_V
    global high_V
    low_V = val
    low_V = min(high_V, low_V)
    cv2.setTrackbarPos(low_V_name, window_detection_name, low_V)
## [low V]

## [high V]
def on_high_V_thresh_trackbar(val):
    global low_V
    global high_V
    high_V = val
    high_V = max(high_V, low_V)
    cv2.setTrackbarPos(high_V_name, window_detection_name, high_V)
## [high V]


def main():

    parser = argparse.ArgumentParser('Menu of Saving limits')
    parser.add_argument('-c','--camera', help='', default=0, type=int, required=False)
    args = parser.parse_args()

    key_validation = 0

    ## [cap]
    cap = cv2.VideoCapture(args.camera)
    ## [cap]

    ## [window]
    cv2.namedWindow(window_capture_name)
    cv2.namedWindow(window_detection_name)
    ## [window]

    ## [trackbar]
    cv2.createTrackbar(low_H_name, window_detection_name , low_H, max_value, on_low_H_thresh_trackbar)
    cv2.createTrackbar(high_H_name, window_detection_name , high_H, max_value, on_high_H_thresh_trackbar)
    cv2.createTrackbar(low_S_name, window_detection_name , low_S, max_value, on_low_S_thresh_trackbar)
    cv2.createTrackbar(high_S_name, window_detection_name , high_S, max_value, on_high_S_thresh_trackbar)
    cv2.createTrackbar(low_V_name, window_detection_name , low_V, max_value, on_low_V_thresh_trackbar)
    cv2.createTrackbar(high_V_name, window_detection_name , high_V, max_value, on_high_V_thresh_trackbar)
    ## [trackbar]



    while True:
        ## [while]
        ret, frame = cap.read()
        key = cv2.waitKey(50)
        

        if frame is None:
            break

        #quit without saving
        elif key == ord('q') and key_validation ==0:
            print("Quiting Program without saving limits.")
            break
        
        #saving the paramiters of the color
        elif key == ord('w'):

            print('You have chosen:\n B- '+Fore.BLUE + str(low_H) 
                  + Fore.RESET +' min and ' +Fore.BLUE+ str(high_H)+Style.RESET_ALL+' max\n')
            
            print('You have chosen:\n G- '+Fore.GREEN + str(low_S) 
                  + Fore.RESET +' min and ' +Fore.GREEN+ str(high_S)+Style.RESET_ALL+' max\n')
            
            print('You have chosen:\n R- '+Fore.RED + str(low_V) 
                  + Fore.RESET +' min and ' +Fore.RED+ str(high_V)+Style.RESET_ALL+' max\n')


            dicio_limits = {'limits': {'B': {'max': high_H, 'min': low_H},
                                        'G': {'max': high_S, 'min': low_S},
                                        'R': {'max': high_V, 'min': low_V}}}
            
            file_name = 'limits.json'

            #dicio_json = json.dumps(dicio_limits, indent=1)
            #openFile = open(file_name,"w")

            #openFile.write(dicio_json)

            # openFile.close()
        
            key_validation += 1
                        
            with open(file_name, 'w') as file_handle:
                print('writing dictionary dicio_json to file ' + Fore.LIGHTYELLOW_EX+file_name+Style.RESET_ALL)
                {json.dump(dicio_limits, file_handle, indent='')}
        
        elif key == ord('q') and key_validation == 1:
            print("Quiting Program...\nYour limits has been saved!")
            break

            
        frame_HSV = cv2.cvtColor(frame, cv2.COLOR_BGR2HSV)
        frame_threshold = cv2.inRange(frame_HSV, (low_H, low_S, low_V), (high_H, high_S, high_V))
        ## [while]

        ## [show]
        cv2.imshow(window_capture_name, frame)
        cv2.imshow(window_detection_name, frame_threshold)
        ## [show]

if __name__ == '__main__':
    main()