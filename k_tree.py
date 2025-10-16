#Knowing Tree
import gpiod
import time
import random
from gpiod.line import Direction
from gpiod.line import Bias,Edge,Value

import pygame
import cv2
import numpy as np
 
# Initialize video capture
capture = cv2.VideoCapture(0)
capture.set(cv2.CAP_PROP_FRAME_WIDTH, 1024)
capture.set(cv2.CAP_PROP_FRAME_HEIGHT, 576)
capture.set(cv2.CAP_PROP_FPS, 30)  # Requesting 30 FPS from the camera
#This camera does not seem to support Exposure control. It always does auto-exposure
#capture.set(cv2.CAP_PROP_AUTO_EXPOSURE, 1) #Trying to turn off auto-exposure
#capture.set(cv2.CAP_PROP_EXPOSURE, -10) #Set the exposure (Whats the unit for exposure?)
#print("CAP_PROP_AUTO_EXPOSURE  : '{}'".format(capture.get(cv2.CAP_PROP_AUTO_EXPOSURE)))
#print("CAP_PROP_EXPOSURE  : '{}'".format(capture.get(cv2.CAP_PROP_EXPOSURE)))

# Background subtractor
bg_subtractor = cv2.createBackgroundSubtractorMOG2()
 
# Current mode
#mode = "test"	#In this mode, the candy ID data will be displayed on screen
mode = "normal"

#Global parameters begin
initFramesNum = 60  #The number of frames captured on startup to set the autoexposure
binaryThreshValue = 100
roiYStart=95	#Region of interest (Y is vertical axis in image)
roiYEnd=400
roiXStart=140	#Region of interest (X is horizontal axis in image)
roiXEnd=450
#Global parameters end


#Configure the blob detector
# Setup SimpleBlobDetector parameters
params = cv2.SimpleBlobDetector_Params()

def init_auto_exposure():
    #On startup, capture some images to allow the automatic exposure to adjust. 
    for x in range(initFramesNum):
        #Capture an image
        ret, frame = capture.read()
        #Check for an error during capture
        if not ret:
            break
        #Display the images if we are running in test mode
        #Note: This assumes the window "InputImage" was already created
        if mode == "test":
            #Display the current frame number
            cv2.putText(frame, f"{int(x)}", (10, 30), cv2.FONT_HERSHEY_SIMPLEX, 1, (0, 255, 0), 2)
            # Show image
            cv2.imshow("InputImage", frame)
    
def detect_candy():
    #Capture an image
    ret, frame = capture.read()
    #Check for an error during capture
    if not ret:
        print("Error capturing image in detect_candy()")
        return
    
    #Convert the image to grayscale
    gray = cv2.cvtColor(frame, cv2.COLOR_BGR2GRAY)
    #Binarize the image
    ret, bin_img = cv2.threshold(gray, binaryThreshValue, 255, cv2.THRESH_BINARY_INV)
    bin_img_ROI=bin_img[roiYStart:roiYEnd,roiXStart:roiXEnd]
    contours,hierarchy = cv2.findContours(bin_img_ROI, cv2.RETR_LIST, method=cv2.CHAIN_APPROX_NONE,offset=(roiXStart,roiYStart))
    cv2.drawContours(frame, contours, -1, (0,255,0), 3)
    
    print( "Blobs detected: ", len(contours))
    if len(contours) > 0:
        #Get the blob with the largest area
        c = max(contours, key = cv2.contourArea)            
        rect = cv2.minAreaRect(c)  #Find the min area rectangle
        box = cv2.boxPoints(rect)	#Convert the rect to points            
        #Extract features from blob
        blobArea = cv2.contourArea(c)	#area
        (x, y), (width, height), angle = rect
        blobAspect = min(width, height) / max(width, height)
        #blobAspect = max(box[0,0],box[1,0],box[2,0],box[3,0])/min(box[0,1],box[1,1],box[2,1],box[3,1])
        print( blobArea , blobAspect)
        box = np.int32(box)		#Convert points to integers
        # draw the min area react in red
        cv2.drawContours(frame, [box], 0, (0,0,255), 2)
        #Classify the candy
        if blobArea>3800 and blobArea<5000 and blobAspect>0.5: #Starburst
            print("Starburst")
        elif blobArea>6000 and blobArea<12000 and blobAspect<0.5: #Smartie
            print("Smartie")
        elif blobArea>3000 and blobArea<5700 and blobAspect<0.5: #Tootsie roll
            print("Tootsie roll")
        else:
            print("Chocolate covered tree frog")
    #Display the images if we are running in test mode
    if mode == "test":
        # Show image in color window
        cv2.imshow("InputImage", frame)
        #Display the binarized image
        cv2.imshow("OutputImage", bin_img_ROI)
        
#^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^

def run_test_mode():
    #Create window for displaying images
    cv2.namedWindow("InputImage")
    cv2.moveWindow("InputImage",20,20)
    cv2.namedWindow("OutputImage")
    cv2.moveWindow("OutputImage",600,20)
    #Let the camera adjust the autoexposure
    init_auto_exposure()
    #Loop until the "q" key is pressed.
    while True:
        
        detect_candy()
        #Check for a keypress
        key = cv2.waitKey(1) & 0xFF
        if key == ord("q"):
            break            
    #End while
    # Clean up
    capture.release()
    cv2.destroyAllWindows()
#*********************************************************************

def run_normal_mode():
    #Let the camera adjust the autoexposure
    init_auto_exposure()
    #Capture the frame that will be used for candy detection
    ret, frame = capture.read()
    if not ret:
        print("Error capturing image in run_normal_mode()")
        return
 
    detect_candy()    
        
      
#*********************************************************************

def get_line_value(chip_path, line_offset):
    with gpiod.request_lines(
        chip_path,
        consumer="get-line-value",
        config={line_offset: gpiod.LineSettings(direction=Direction.INPUT,bias=Bias.PULL_UP)},
    ) as request:
        value = request.get_value(line_offset)
        print("{}={}".format(line_offset, value))
        return value
    
#*********************************************************************

def play_idle_sound():
    sound = pygame.mixer.Sound('/home/rpi/Documents/knowledgetree/sounds/snore_x.wav')
    rnd_val = random.randint(1,3)
    if rnd_val == 1:
        sound = pygame.mixer.Sound('/home/rpi/Documents/knowledgetree/sounds/flush_y.wav')
    elif rnd_val == 2:
        sound = pygame.mixer.Sound('/home/rpi/Documents/knowledgetree/sounds/ufo_x.wav')
    
    playing = sound.play()
    while playing.get_busy():
        pygame.time.delay(10)
        
#*********************************************************************

if __name__ == "__main__":
    try:
        pygame.mixer.init()
        
        if mode == "normal":
            play_idle_sound()  #Testing
            #Begin polling for a button press
            while True:
                num_loops=600
                for i in range(num_loops):
                    btn_state = get_line_value("/dev/gpiochip0", 17)
                    if btn_state == Value.INACTIVE:
                        print("Button pressed")
                        run_normal_mode()
                        i=0
                    #endif        
                    time.sleep(0.1)
                #end for
                play_idle_sound()
            #end while
        elif mode == "test": #Data collection & testing mode
            run_test_mode()
        else: 
            print("Invalid run mode")
            
        
    except OSError as ex:
        print(ex, "\n Error in k_tree.py")