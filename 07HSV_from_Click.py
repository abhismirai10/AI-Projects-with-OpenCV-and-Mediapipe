# Import required package
import cv2
import numpy as np

# Initialize global variables for mouse events and positions
Gevent, click_pos_x, click_pos_y = 0, 0, 0

# Define the properties of the Region Of Interest (ROI)
roi_thickness = 4
roi_color = (0, 0, 255)

# Define a callback function for mouse events
def mouse_event(event, x, y, flags, param):
    global Gevent, click_pos_x, click_pos_y

    if event == cv2.EVENT_LBUTTONDOWN or event == cv2.EVENT_LBUTTONUP:
        Gevent = event
        click_pos_x = x
        click_pos_y = y
        print(f'Mouse Event: {event} at Position {x}, {y}')

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

# to check above is done or not 
print(cam.get(cv2.CAP_PROP_FRAME_WIDTH))
print(cam.get(cv2.CAP_PROP_FRAME_HEIGHT))
print(cam.get(cv2.CAP_PROP_FPS))
print(cam.get(cv2.CAP_PROP_FOURCC))

# For mouse click 
cv2.namedWindow('frame01')
cv2.setMouseCallback('frame01', mouse_event)

# Main loop
while True:
    # Read a frame
    ret, frame = cam.read()

    # If a frame is not read correctly, then we break the loop
    if not ret:
        break

    # HSV frame
    HSVframe= cv2.cvtColor(frame,cv2.COLOR_BGR2HSV)

    # recode mouse click point and its color
    if Gevent == 1:
        x = np.zeros([250, 250, 3], dtype=np.uint8)
        click_color = HSVframe[click_pos_y, click_pos_x]
        x[:, :] = click_color
        x_BGR = cv2.cvtColor(x, cv2.COLOR_HSV2BGR)  # Convert to HSV color space
        cv2.putText(x_BGR,str(click_color),(0,50),cv2.FONT_HERSHEY_COMPLEX,1,(0,0,0),1)
        cv2.imshow('color picker', x_BGR)
        cv2.moveWindow('color picker', width, 0)

        # start listing for next time
        Gevent = 0

    # Display the frame
    cv2.imshow('frame01', frame)
    cv2.moveWindow('frame01', 0, 0)

    # If 'q' is pressed on the keyboard, then quit the program
    if cv2.waitKey(1) & 0xFF == ord('q'):
        break

# Release the webcam and destroy all windows
cam.release()
cv2.destroyAllWindows()
