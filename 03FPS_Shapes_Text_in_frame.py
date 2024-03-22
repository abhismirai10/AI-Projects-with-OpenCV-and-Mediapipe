import cv2
import time

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

#for calculation of FPS
ltime=time.time()
time.sleep(.1)

avg_fps = 0
while True:

    # time delay count
    dt=time.time()-ltime
    fps = 1/dt
    print(fps)
    avg_fps=0.9 * avg_fps + 0.1 * (fps)
    ltime=time.time()

    #to read a frame
    ret, frame = cam.read()

    # Verify that frame has been read
    if not ret:
        break
    
    # putting rectangle and circle
    cv2.rectangle(frame,(int((width/2)-30),int((height/2)-20)),(int((width/2)+30),int((height/2)+20)),(255,0,0),2)
    cv2.circle(frame,(640,360),50,(0,0,0),3)

    # Text
    cv2.putText(frame,"FPS = {}" .format(int(avg_fps)),(0,50),cv2.FONT_HERSHEY_COMPLEX,2,(255,0,0),2)

    # Display the resulting frames
    cv2.imshow('frame01', frame)

    # If 'q' is pressed, break the loop
    if cv2.waitKey(1) & 0xFF == ord('q'):
        break

# Release the VideoCapture and destroy windows
cam.release()
cv2.destroyAllWindows()
