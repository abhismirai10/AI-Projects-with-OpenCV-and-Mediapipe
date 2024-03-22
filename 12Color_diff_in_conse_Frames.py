import cv2
import numpy as np
import mediapipe as mp
# Define a function that calculates color difference
def color_difference(old_frame, new_frame):
    # convert the images to the Lab color space
    old_frame_lab = cv2.cvtColor(old_frame, cv2.COLOR_BGR2Lab)
    new_frame_lab = cv2.cvtColor(new_frame, cv2.COLOR_BGR2Lab)

    # compute the color difference
    diff = cv2.absdiff(old_frame_lab, new_frame_lab)
    return diff

# Initialize video stream (0 for webcam, or replace with video file path)
cap = cv2.VideoCapture(0)

# Initialize the first frame
ret, old_frame = cap.read()

while True:
    # read the next frame from the video stream
    ret, new_frame = cap.read()

    # if the frame could not be grabbed, then we have reached the end of the video
    if not ret:
        break

    # calculate the color difference
    diff = color_difference(old_frame, new_frame)
    BGR_frame = cv2.cvtColor(diff,cv2.COLOR_LAB2BGR)

    # show the difference
    cv2.imshow("Color Difference LAB", diff)
    cv2.imshow("Color Difference BGR", BGR_frame)
    
    # break if 'q' is pressed
    key = cv2.waitKey(1) & 0xFF
    if key == ord("q"):
        break

    # Update old_frame
    old_frame = new_frame

cap.release()
cv2.destroyAllWindows()
