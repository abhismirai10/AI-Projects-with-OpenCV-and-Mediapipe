# Import required package
import cv2
import numpy as np

# Initialize global variables for trackbar positions
pos_x, pos_y = 0, 0
xsize, ysize = 100, 100  # Initialize to a visible size

# Define the properties of the Region Of Interest (ROI)
roi_thickness = 4
roi_color = (0, 0, 255)

# Define a callback function for trackbar events
def trackbar01 (value):
    global pos_x
    pos_x = min(max(value, xsize // 2), width - xsize // 2)

def trackbar02 (value):
    global pos_y
    pos_y = min(max(value, ysize // 2), height - ysize // 2)
    
def trackbar03 (value):
    global xsize
    xsize = max(value, 10)  # Prevent size from being too small

def trackbar04 (value):
    global ysize
    ysize = max(value, 10)  # Prevent size from being too small

# Open the webcam
cam = cv2.VideoCapture(0)

# Check if the webcam is opened correctly
if not cam.isOpened():
    raise IOError("Cannot open webcam")

# Standard size for webcam 1280*720
width, height = 640, 360

# Set webcam properties
cam.set(cv2.CAP_PROP_FRAME_WIDTH, width)
cam.set(cv2.CAP_PROP_FRAME_HEIGHT, height)
cam.set(cv2.CAP_PROP_FPS, 30)   # FPS is typically 30 max
cam.set(cv2.CAP_PROP_FOURCC, cv2.VideoWriter_fourcc(*'MJPG'))   # this might not work for all webcams

# For track bar movement
cv2.namedWindow('trackbar')
cv2.imshow('trackbar', np.zeros((1, 1)))  # Display an extremely small image otherwise not moving
cv2.moveWindow('trackbar', width+5, 0)

cv2.createTrackbar("xpos","trackbar",int(width/2),width,trackbar01)
cv2.createTrackbar("ypos","trackbar",int(height/2),height,trackbar02)
cv2.createTrackbar("xsize","trackbar",xsize,width,trackbar03)
cv2.createTrackbar("ysize","trackbar",ysize,height,trackbar04)

# Main loop
while True:
    # Read a frame
    ret, frame = cam.read()

    # If a frame is not read correctly, then we break the loop
    if not ret:
        break

    # Draw the rectangle for the ROI
    cv2.rectangle(frame,(int(pos_x - xsize/2),int(pos_y - ysize/2)),(int(pos_x + xsize/2),int(pos_y + ysize/2)),roi_color,roi_thickness)

    #roi frame 
    roi_frame = frame [int(pos_y - ysize/2):int(pos_y + ysize/2),int(pos_x - xsize/2):int(pos_x + xsize/2)]
    
    # Display the frame
    cv2.imshow('frame01', frame)
    cv2.moveWindow('frame01',0,0)

    cv2.imshow('roi frame',roi_frame)
    cv2.moveWindow('roi frame',0,height+30)

    # If 'q' is pressed on the keyboard, then quit the program
    if cv2.waitKey(1) & 0xFF == ord('q'):
        break

# Release the webcam and destroy all windows
cam.release()
cv2.destroyAllWindows()
