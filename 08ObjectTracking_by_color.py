# Import required package
import cv2
import numpy as np

# Initialize global variables for trackbar positions
huelow, huehigh = 26, 83
satlow, sathigh = 28, 130
vallow, valhigh = 82, 177

# Define a callback function for trackbar events
def onTrack1(val):
    global huelow
    huelow = val
    print('huelow', huelow)

def onTrack2(val):
    global huehigh
    huehigh = val
    print('huehigh', huehigh)

def onTrack3(val):
    global satlow
    satlow = val
    print('satlow', satlow)

def onTrack4(val):
    global sathigh
    sathigh = val
    print('sathigh', sathigh)

def onTrack5(val):
    global vallow
    vallow = val
    print('vallow', vallow)

def onTrack6(val):
    global valhigh
    valhigh = val
    print('valhigh', valhigh)

# Open the webcam
cam = cv2.VideoCapture(0)

# Check if the webcam is opened correctly
if not cam.isOpened():
    raise IOError("Cannot open webcam")

# Standard size for webcam 1280*960
width, height = 640, 480

# Set webcam properties
cam.set(cv2.CAP_PROP_FRAME_WIDTH, width)
cam.set(cv2.CAP_PROP_FRAME_HEIGHT, height)
cam.set(cv2.CAP_PROP_FPS, 30)   # FPS is typically 30 max
cam.set(cv2.CAP_PROP_FOURCC, cv2.VideoWriter_fourcc(*'MJPG'))   # this might not work for all webcams

# For track bar movement
cv2.namedWindow('MyTrackbar')
cv2.imshow('MyTrackbar', np.zeros((1, 1)))  # Display an extremely small image otherwise not moving
cv2.moveWindow('MyTrackbar', 2*(width+5), 0)

cv2.createTrackbar('Hue Low', 'MyTrackbar', 26, 179, onTrack1)
cv2.createTrackbar('Hue High', 'MyTrackbar', 83, 179, onTrack2)
cv2.createTrackbar('Sat Low', 'MyTrackbar', 28, 255, onTrack3)
cv2.createTrackbar('Sat High', 'MyTrackbar', 130, 255, onTrack4)
cv2.createTrackbar('Val Low', 'MyTrackbar', 82, 255, onTrack5)
cv2.createTrackbar('Val High', 'MyTrackbar', 177, 255, onTrack6)

# Main loop
while True:
    # Read a frame
    ret, frame = cam.read()

    # If a frame is not read correctly, then we break the loop
    if not ret:
        break

    # Convert to HSV frame
    HSV_frame = cv2.cvtColor(frame, cv2.COLOR_BGR2HSV)

    # bounds and mask to find color of objects
    lowwerbound=np.array([huelow,satlow,vallow])
    upperbound=np.array([huehigh,sathigh,valhigh])

    myMask=cv2.inRange(HSV_frame,lowwerbound,upperbound)
    myMask_small=cv2.resize(myMask,(320,240))

    # myMask is a single channel image, convert it to 3-channel image for bitwise_and operation
    #myMask_color = cv2.cvtColor(myMask, cv2.COLOR_GRAY2BGR)
    #myObject = cv2.bitwise_and(frame, myMask_color)
    
    myObject = cv2.bitwise_and(frame, frame, mask= myMask)
    myObject_small=cv2.resize(myObject,(320,240))

    #display the mask which would be black and white
    cv2.imshow('myMask',myMask_small)
    cv2.moveWindow('myMask',width,0)

    # display object of interest
    cv2.imshow('Object found',myObject_small)
    cv2.moveWindow('Object found',width,210)

    # Display the frame
    cv2.imshow('frame01', frame)
    cv2.moveWindow('frame01',0,0)

    # If 'q' is pressed on the keyboard, then quit the program
    if cv2.waitKey(1) & 0xFF == ord('q'):
        break

# Release the webcam and destroy all windows
cam.release()
cv2.destroyAllWindows()