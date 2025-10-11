#Knowing Tree

import cv2
import numpy as np
import time
 
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
mode = "data"	#In this mode, the candy ID data will be saved to a file
#mode = "normal"

#Global parameters begin
initFramesNum = 60  #The number of frames captured on startup to set the autoexposure
binaryThreshValue = 100
roiYStart=95	#Region of interest (Y is vertical axis in image)
roiYEnd=400
roiXStart=140	#Region of interest (X is horizontal axis in image)
roiXEnd=450
#Global parameters end

#Create window for displaying images
cv2.namedWindow("InputImage")
cv2.moveWindow("InputImage",20,20)
cv2.namedWindow("OutputImage")
cv2.moveWindow("OutputImage",600,20)
#Configure the blob detector
# Setup SimpleBlobDetector parameters
params = cv2.SimpleBlobDetector_Params()

#On startup, capture some images to allow the automatic exposure to adjust. 
for x in range(initFramesNum):
    #Capture an image
    ret, frame = capture.read()
    #Check for an error during capture
    if not ret:
        break
    #Display the current frame number
    cv2.putText(frame, f"{int(x)}", (10, 30), cv2.FONT_HERSHEY_SIMPLEX, 1, (0, 255, 0), 2)
    # Show image
    cv2.imshow("InputImage", frame)

if mode == "data":
    while True:
        #Capture an image
        ret, frame = capture.read()
        #Check for an error during capture
        if not ret:
            break
        
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
        # Show image in color window
        cv2.imshow("InputImage", frame)
        #Display the binarized image
        cv2.imshow("OutputImage", bin_img_ROI)
        
        #Check for a keypress
        key = cv2.waitKey(1) & 0xFF
        if key == ord("d"):
            mode = "threshold"
        elif key == ord("q"):
            break            

if mode == "normal":
    while True:
        ret, frame = capture.read()
        if not ret:
            break
     
        frame = cv2.flip(frame, 1)
        display_frame = frame.copy()
     
        if mode == "threshold":
            gray = cv2.cvtColor(frame, cv2.COLOR_BGR2GRAY)
            _, display_frame = cv2.threshold(gray, 127, 255, cv2.THRESH_BINARY)
            display_frame = cv2.cvtColor(display_frame, cv2.COLOR_GRAY2BGR)
     
        elif mode == "edge":
            gray = cv2.cvtColor(frame, cv2.COLOR_BGR2GRAY)
            edges = cv2.Canny(gray, 100, 200)
            display_frame = cv2.cvtColor(edges, cv2.COLOR_GRAY2BGR)
     
        elif mode == "bg_sub":
            fg_mask = bg_subtractor.apply(frame)
            display_frame = cv2.bitwise_and(frame, frame, mask=fg_mask)
     
        elif mode == "contour":
            gray = cv2.cvtColor(frame, cv2.COLOR_BGR2GRAY)
            _, thresh = cv2.threshold(gray, 127, 255, cv2.THRESH_BINARY)
            contours, _ = cv2.findContours(thresh, cv2.RETR_TREE, cv2.CHAIN_APPROX_SIMPLE)
            display_frame = cv2.drawContours(frame.copy(), contours, -1, (0, 255, 0), 2)
     
        # Calculate actual processing FPS
        curr_time = time.time()
        processing_fps = 1 / (curr_time - prev_time)
        prev_time = curr_time
     
        # Display actual processing FPS
        cv2.putText(
            display_frame, f"FPS: {int(processing_fps)} Mode: {mode}", (10, 30), cv2.FONT_HERSHEY_SIMPLEX, 1, (0, 255, 0), 2
        )
     
        # Write frame to video
        #out.write(display_frame)
     
        # Show video
        cv2.imshow("Live Video", display_frame)
     
        key = cv2.waitKey(1) & 0xFF
        if key == ord("t"):
            mode = "threshold"
        elif key == ord("e"):
            mode = "edge"
        elif key == ord("b"):
            mode = "bg_sub"
        elif key == ord("c"):
            mode = "contour"
        elif key == ord("n"):
            mode = "normal"
        elif key == ord("q"):
            break
     
# Clean up
capture.release()
cv2.destroyAllWindows()