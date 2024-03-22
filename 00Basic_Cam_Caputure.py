import cv2

# to start capturing images
cam=cv2.VideoCapture(0)

# To handle no webcam or webcam access error
if not cam.isOpened():
    raise IOError("Cannot open webcam")
 
#standard size for webcam 1280*720
width  = 640
height = 360

cam.set(cv2.CAP_PROP_FRAME_WIDTH, width)
cam.set(cv2.CAP_PROP_FRAME_HEIGHT, height)
cam.set(cv2.CAP_PROP_FPS, 30)   #FPS is 30 max I think
cam.set(cv2.CAP_PROP_FOURCC, cv2.VideoWriter_fourcc(*'MJPG'))   #this is not working

# # to check above is done or not 
# print(cam.get(cv2.CAP_PROP_FRAME_WIDTH))
# print(cam.get(cv2.CAP_PROP_FRAME_HEIGHT))
# print(cam.get(cv2.CAP_PROP_FPS))
# print(cam.get(cv2.CAP_PROP_FOURCC))

while True:

    #to read a frame and flip it
    ret, flipped_frame = cam.read()
    frame = cv2.flip(flipped_frame, 1)

    # Verify that frame has been read
    if not ret:
        break

    # Display the resulting frames
    cv2.imshow('frame01', frame)
    # If 'q' is pressed, break the loop
    if cv2.waitKey(1) & 0xFF == ord('q'):
        break

# Release the VideoCapture and destroy windows
cam.release()
cv2.destroyAllWindows()
