import cv2

# to start capturing images
cam=cv2.VideoCapture(0)

# To handle no webcam or webcam access error
if not cam.isOpened():
    raise IOError("Cannot open webcam")
 
#standard size for webcam 1280*720
width  = 640
height = 360

cam.set(cv2.CAP_PROP_FRAME_WIDTH, 1280)
cam.set(cv2.CAP_PROP_FRAME_HEIGHT, 720)
cam.set(cv2.CAP_PROP_FPS, 30)   #FPS is 30 max I think
cam.set(cv2.CAP_PROP_FOURCC, cv2.VideoWriter_fourcc(*'MJPG'))   #this is not working

while True:

    #to read a frame
    ret, frame = cam.read()

    # Verify that frame has been read
    if not ret:
        break

    # Resize the frame
    frame = cv2.resize(frame, (width, height))

    # Convert to grayscale
    gray_frame = cv2.cvtColor(frame, cv2.COLOR_BGR2GRAY)

    # Extract Blue Channel
    blue_channel = frame.copy()
    blue_channel[:, :, 1] = 0
    blue_channel[:, :, 2] = 0

    # Extract Red Channel
    red_channel = frame.copy()
    red_channel[:, :, 0] = 0
    red_channel[:, :, 1] = 0

    # Extract green Channel
    green_channel = frame.copy()
    green_channel[:, :, 0] = 0
    green_channel[:, :, 2] = 0

    # Display the resulting frames side by side
    cv2.imshow('normal frame01', frame)
    cv2.moveWindow('normal frame01',0,0)

    cv2.imshow('blue frame02', blue_channel)
    cv2.moveWindow('blue frame02',width+5,0)

    cv2.imshow('red frame03', red_channel)
    cv2.moveWindow('red frame03',0,height+30)

    cv2.imshow('green frame04',gray_frame)
    cv2.moveWindow('green frame04',width+5,height+30)

    # If 'q' is pressed, break the loop
    if cv2.waitKey(1) & 0xFF == ord('q'):
        break

# Release the VideoCapture and destroy windows
cam.release()
cv2.destroyAllWindows()
