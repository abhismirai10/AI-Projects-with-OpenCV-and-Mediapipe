import cv2

# to start capturing images
cam = cv2.VideoCapture(0)

# To handle no webcam or webcam access error
if not cam.isOpened():
    raise IOError("Cannot open webcam")

# standard size for webcam 1280*720
width  = 640
height = 360

cam.set(cv2.CAP_PROP_FRAME_WIDTH, width)
cam.set(cv2.CAP_PROP_FRAME_HEIGHT, height)
cam.set(cv2.CAP_PROP_FPS, 30)  # FPS is 30 max I think
cam.set(cv2.CAP_PROP_FOURCC, cv2.VideoWriter_fourcc(*'MJPG'))  # this is not working

# file for face detection 
faceCascade = cv2.CascadeClassifier('haar/haarcascade_frontalface_default.xml')
smileCascade = cv2.CascadeClassifier('haar/haarcascade_smile.xml')

while True:
    # to read a frame and flip it
    ret, flipped_frame = cam.read()

    # Verify that frame has been read
    if not ret:
        break

    frame = cv2.flip(flipped_frame, 1)

    # Convert to grayscale
    gray_frame = cv2.cvtColor(frame, cv2.COLOR_BGR2GRAY)

    # face detection
    faces = faceCascade.detectMultiScale(gray_frame, 1.3, 5)
    for (x, y, w, h) in faces:
        roi_gray = gray_frame[y:y+h, x:x+w] # Region of Interest
        smiles = smileCascade.detectMultiScale(roi_gray, 1.3, 50)
        for (x1, y1, w1, h1) in smiles:
            cv2.rectangle(frame, (x + x1, y + y1), (x + x1 + w1, y + y1 + h1), (255, 0, 0), 2)
        #cv2.rectangle(frame, (x, y), (x+w, y+h), (0, 255, 0), 2)  # green rectangle for faces

    # Display the resulting frames
    cv2.imshow('frame01', frame)

    # If 'q' is pressed, break the loop
    if cv2.waitKey(1) & 0xFF == ord('q'):
        break

# Release the VideoCapture and destroy windows
cam.release()
cv2.destroyAllWindows()
