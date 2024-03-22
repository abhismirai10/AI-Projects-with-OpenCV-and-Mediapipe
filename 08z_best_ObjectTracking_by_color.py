import cv2
import numpy as np

class TrackbarHandler:
    def __init__(self):
        self.hue_low = 0
        self.hue_high = 14
        self.sat_low = 59
        self.sat_high = 180
        self.val_low = 68
        self.val_high = 178

    def on_hue_low(self, val):
        self.hue_low = val
        print('Hue Low', self.hue_low)

    def on_hue_high(self, val):
        self.hue_high = val
        print('Hue High', self.hue_high)

    def on_sat_low(self, val):
        self.sat_low = val
        print('Saturation Low', self.sat_low)

    def on_sat_high(self, val):
        self.sat_high = val
        print('Saturation High', self.sat_high)

    def on_val_low(self, val):
        self.val_low = val
        print('Value Low', self.val_low)

    def on_val_high(self, val):
        self.val_high = val
        print('Value High', self.val_high)

def initialize_trackbars(trackbar_handler):
    cv2.namedWindow('MyTrackbar')
    cv2.imshow('MyTrackbar', np.zeros((1, 1)))  
    cv2.moveWindow('MyTrackbar', 2*(width+5), 0)

    cv2.createTrackbar('Hue Low', 'MyTrackbar', 0, 179, trackbar_handler.on_hue_low)
    cv2.createTrackbar('Hue High', 'MyTrackbar', 14, 179, trackbar_handler.on_hue_high)
    cv2.createTrackbar('Sat Low', 'MyTrackbar', 59, 255, trackbar_handler.on_sat_low)
    cv2.createTrackbar('Sat High', 'MyTrackbar', 180, 255, trackbar_handler.on_sat_high)
    cv2.createTrackbar('Val Low', 'MyTrackbar', 68, 255, trackbar_handler.on_val_low)
    cv2.createTrackbar('Val High', 'MyTrackbar', 178, 255, trackbar_handler.on_val_high)

def main():
    trackbar_handler = TrackbarHandler()
    
    # webcam settings
    cam = cv2.VideoCapture(0)
    if not cam.isOpened():
        raise IOError("Cannot open webcam")
    global width, height
    width, height = 640, 360
    cam.set(cv2.CAP_PROP_FRAME_WIDTH, width)
    cam.set(cv2.CAP_PROP_FRAME_HEIGHT, height)
    cam.set(cv2.CAP_PROP_FPS, 30)   
    cam.set(cv2.CAP_PROP_FOURCC, cv2.VideoWriter_fourcc(*'MJPG'))   

    initialize_trackbars(trackbar_handler)
    
    # Main loop
    while True:
        #to read a frame and flip it
        ret, flipped_frame = cam.read()
        frame = cv2.flip(flipped_frame, 1)

        if not ret:
            break

        HSV_frame = cv2.cvtColor(frame, cv2.COLOR_BGR2HSV)

        # define color bounds and create mask to isolate objects of specified color
        lower_bound = np.array([trackbar_handler.hue_low, trackbar_handler.sat_low, trackbar_handler.val_low])
        upper_bound = np.array([trackbar_handler.hue_high, trackbar_handler.sat_high, trackbar_handler.val_high])
        
        mask = cv2.inRange(HSV_frame, lower_bound, upper_bound)
        mask_small = cv2.resize(mask, (320, 180))
        
        # apply mask to original frame to isolate object of interest
        object_of_interest = cv2.bitwise_and(frame, frame, mask=mask)
        object_of_interest_small = cv2.resize(object_of_interest, (320, 180))

        # display the mask, object of interest, and the original frame
        cv2.imshow('myMask', mask_small)
        cv2.moveWindow('myMask', width, 0)
        cv2.imshow('Object found', object_of_interest_small)
        cv2.moveWindow('Object found', width, 210)
        cv2.imshow('frame01', frame)
        cv2.moveWindow('frame01', 0, 0)

        # exit program on 'q' key press
        if cv2.waitKey(1) & 0xFF == ord('q'):
            break

    # clean up
    cam.release()
    cv2.destroyAllWindows()

if __name__ == "__main__":
    main()