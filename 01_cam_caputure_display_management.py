import cv2

cam = cv2.VideoCapture(0)  # 0 is the camera index

# Handle camera not opening
if not cam.isOpened():
    raise IOError("Cannot open webcam")

# Set resolution 
width, height = 640, 360
cam.set(cv2.CAP_PROP_FRAME_WIDTH, width)
cam.set(cv2.CAP_PROP_FRAME_HEIGHT, height)

# Set window position 
# here we can set any location of frame's window even if extranal
# windows are available. to math using dispaly resolution
window_x, window_y = -1512, -500 

while True:
    ret, frame = cam.read()
    
    if not ret:
        break

    flip_frame = cv2.flip(frame, 1)

    cv2.imshow("webcam", frame)
    cv2.moveWindow("webcam", window_x, window_y)  # Move the window to (x, y)
    cv2.imshow("webcam1", flip_frame)
    cv2.moveWindow("webcam1", window_x + 640, window_y) 

    if cv2.waitKey(1) & 0xFF == ord('q'):
        break

cam.release()
cv2.destroyAllWindows()
