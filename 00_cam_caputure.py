import cv2

cam = cv2.VideoCapture(0) # 0 is the number for port inwhich cam is connected

#to handel cam not detection error
if not cam.isOpened:
    raise IOError("cannot open webcam")

# #standard size for webcam 1280*720
# width = 1280
# height = 720

# cam.set(cv2.CAP_PROP_FRAME_WIDTH, width)
# cam.set(cv2.CAP_PROP_FRAME_HEIGHT, height)
# cam.set(cv2.CAP_PROP_FPS, 30)

while True:
    ret, frame = cam.read()
    
    if not ret:
        break

    cv2.imshow("webcam", frame)

    if cv2.waitKey(1) & 0xFF == ord('q'):
        break

cam.release()
cv2.destroyAllWindows()