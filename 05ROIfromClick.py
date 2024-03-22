# Import required package
import cv2

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
width, height = 1280, 720

# Set webcam properties
cam.set(cv2.CAP_PROP_FRAME_WIDTH, width)
cam.set(cv2.CAP_PROP_FRAME_HEIGHT, height)
cam.set(cv2.CAP_PROP_FPS, 30)   # FPS is typically 30 max
cam.set(cv2.CAP_PROP_FOURCC, cv2.VideoWriter_fourcc(*'MJPG'))   # this might not work for all webcams

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

    # recode a upper left and lowwer right corners
    if Gevent == cv2.EVENT_LBUTTONDOWN:
        upper_left = [click_pos_x, click_pos_y]

    if Gevent == cv2.EVENT_LBUTTONUP:
        lowwer_right = [click_pos_x, click_pos_y]

        #creating ROI
        cv2.rectangle(frame,upper_left,lowwer_right,roi_color,roi_thickness)

        #new window for ROI
        roi_frame = frame[upper_left[1]:lowwer_right[1], upper_left[0]:lowwer_right[0]]

        # Display the frame of ROI
        cv2.imshow('ROI frame', roi_frame)
        cv2.moveWindow('ROI frame',width,0)

    # Display the frame
    cv2.imshow('frame01', frame)

    # If 'q' is pressed on the keyboard, then quit the program
    if cv2.waitKey(1) & 0xFF == ord('q'):
        break

# Release the webcam and destroy all windows
cam.release()
cv2.destroyAllWindows()
