import cv2

# to start capturing images
cam=cv2.VideoCapture(0)

# To handle no webcam or webcam access error
if not cam.isOpened():
    raise IOError("Cannot open webcam")
 
#standard size for webcam 1280*720
width  = 1280
height = 720

cam.set(cv2.CAP_PROP_FRAME_WIDTH, width)
cam.set(cv2.CAP_PROP_FRAME_HEIGHT, height)
cam.set(cv2.CAP_PROP_FPS, 30)   #FPS is 30 max I think
cam.set(cv2.CAP_PROP_FOURCC, cv2.VideoWriter_fourcc(*'MJPG'))   #this is not working

# Define Region of Interest (ROI) dimensions
ROI_w, ROI_h = 200, 120

# Starting point for the ROI box
x, y = int((1280 - ROI_w)/2), int((720 - ROI_h)/2)

# Define speed of movement for the ROI box
dx, dy = 5, 5

while True:

    #to read a frame
    ret, frame = cam.read()

    # Verify that frame has been read
    if not ret:
        break

    # If ROI box reaches frame boundaries, change direction
    if x <= 0 or x + ROI_w >= frame.shape[1]:
        dx = -dx
    if y <= 0 or y + ROI_h >= frame.shape[0]:
        dy = -dy

    # Adjust position of ROI box
    x += dx
    y += dy

    # Extract ROI from the frame
    ROI_frame = frame[y:y+ROI_h, x:x+ROI_w]

    # Copy the frame and keep only the red channel
    red_frame = frame.copy()
    red_frame[:, :, 0] = 0
    red_frame[:, :, 1] = 0

    # Replace the red channel ROI with the original colored ROI
    red_frame[y:y+ROI_h, x:x+ROI_w] = ROI_frame

    # Display the frames
    cv2.imshow('Red Channel', red_frame)

    # If 'q' is pressed, break the loop
    if cv2.waitKey(1) & 0xFF == ord('q'):
        break

# Release the VideoCapture and destroy windows
cam.release()
cv2.destroyAllWindows()
