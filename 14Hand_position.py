# Import required libraries
import cv2
import mediapipe as mp

# Create a VideoCapture object for webcam feed
webcam = cv2.VideoCapture(0)

# If webcam fails to open, raise an error
if not webcam.isOpened():
    raise IOError("Cannot open webcam")

# Standard size for webcam
webcam_width = 1280
webcam_height = 720

# Set webcam resolution and FPS
webcam.set(cv2.CAP_PROP_FRAME_WIDTH, webcam_width)
webcam.set(cv2.CAP_PROP_FRAME_HEIGHT, webcam_height)
webcam.set(cv2.CAP_PROP_FPS, 30)  # Set frames per second to 30
webcam.set(cv2.CAP_PROP_FOURCC, cv2.VideoWriter_fourcc(*'MJPG'))  # Set MJPG as video codec

# Class for handling hand detection and landmark detection
class HandDetector:
    def __init__(self, static_image_mode=False, max_num_hands=2, min_detection_confidence=0.5, min_tracking_confidence=0.5):
        self.mp = mp.solutions
        self.hand_detector = self.mp.hands.Hands(static_image_mode=False, max_num_hands=2, min_detection_confidence=0.5, min_tracking_confidence=0.5)
        self.landmark_drawer = self.mp.drawing_utils

    # Method to process a frame, detect hands and draw landmarks
    def detect_and_draw_landmarks(self, frame):
        hand_positions = []

        # Convert BGR image to RGB before processing
        rgb_frame = cv2.cvtColor(frame, cv2.COLOR_BGR2RGB)

        # Process the frame to find hand landmarks
        hand_landmarks_result = self.hand_detector.process(rgb_frame)

        # If hand landmarks are detected, draw them on the frame
        if hand_landmarks_result.multi_hand_landmarks:
            for hand_landmark in hand_landmarks_result.multi_hand_landmarks:
                self.landmark_drawer.draw_landmarks(frame, hand_landmark, self.mp.hands.HAND_CONNECTIONS)
                landmarks_coordinates = [(int(landmark.x * webcam_width), int(landmark.y * webcam_height)) for landmark in hand_landmark.landmark]
                hand_positions.append(landmarks_coordinates)
        return hand_positions

# Create a HandDetector object
hand_detector = HandDetector()

# Start webcam feed and continue until 'q' is pressed
while True:
    # Capture frame from webcam
    ret, frame = webcam.read()

    # Flip the frame horizontally for a later selfie-view display
    flipped_frame = cv2.flip(frame, 1)

    # Get hand landmarks from the frame
    hand_landmarks = hand_detector.detect_and_draw_landmarks(flipped_frame)    

    # use landMark positions
    for hand_landmark in hand_landmarks:
        for point in [0,4,20]:
            cv2.circle(flipped_frame,hand_landmark[point],25,(255,0,0),-1)
    
    # Verify that frame has been successfully read
    if not ret:
        break

    # Display the resulting frame
    cv2.imshow('Hand Detection Webcam Feed', flipped_frame)

    # If 'q' is pressed on the keyboard, break the loop and end the program
    if cv2.waitKey(1) & 0xFF == ord('q'):
        break

# After the loop, release the webcam object
webcam.release()

# Destroy all the windows
cv2.destroyAllWindows()
