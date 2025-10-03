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

#Create window for displaying images
cv2.namedWindow("InputImage")
cv2.moveWindow("InputImage",20,20)
cv2.namedWindow("OutputImage")
cv2.moveWindow("OutputImage",600,20)
#Configure the blob detector
# Setup SimpleBlobDetector parameters
params = cv2.SimpleBlobDetector_Params()
# Thresholds for binarization
#params.minThreshold = 10
#params.maxThreshold = 50
#Detect dark blobs
params.blobColor = 0
# Filter by Area
params.filterByArea = True
params.minArea = 1000
params.maxArea = 100000
params.filterByInertia = False
params.filterByConvexity = False
# Create a detector with the parameters
detector = cv2.SimpleBlobDetector_create(params)

#On startup, capture some images to allow the automatic exposure to adjust. 
for x in range(60):
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
        # Show image in color window
        cv2.imshow("InputImage", frame)
        #Convert the image to grayscale
        gray = cv2.cvtColor(frame, cv2.COLOR_BGR2GRAY)
        # Detect blobs
        keypoints = detector.detect(gray)
        # Draw blobs as red circles
        output = cv2.drawKeypoints(gray, keypoints, np.array([]), (0, 0, 255),
                           cv2.DRAW_MATCHES_FLAGS_DRAW_RICH_KEYPOINTS)
        cv2.imshow("OutputImage", output)
        #Binarize the image
        #_, bin_frame = cv2.threshold(gray, 127, 255, cv2.THRESH_BINARY)
        #Display the binarized image
        #cv2.imshow("OutputImage", bin_frame)
        
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