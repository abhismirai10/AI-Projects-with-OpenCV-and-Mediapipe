import turtle
import cv2
import mediapipe as mp

# Set up the screen
win = turtle.Screen()
win.title("Pong Game with Hand Control")
win.bgcolor("black")
win.setup(width=800, height=600)
win.tracer(0)

# Paddle A
paddle_a = turtle.Turtle()
paddle_a.speed(0)
paddle_a.shape("square")
paddle_a.color("white")
paddle_a.shapesize(stretch_wid=6, stretch_len=2)
paddle_a.penup()
paddle_a.goto(-350, 0)

# Paddle B
paddle_b = turtle.Turtle()
paddle_b.speed(0)
paddle_b.shape("square")
paddle_b.color("white")
paddle_b.shapesize(stretch_wid=6, stretch_len=2)
paddle_b.penup()
paddle_b.goto(350, 0)

# Ball
ball = turtle.Turtle()
ball.speed(1)
ball.shape("square")
ball.color("white")
ball.penup()
ball.goto(0, 0)
ball.dx = 15.75  # Ball movement speed in the x-direction
ball.dy = 15.75  # Ball movement speed in the y-direction

# Score variables
score_a = 0
score_b = 0

# Score display
score_display = turtle.Turtle()
score_display.speed(0)
score_display.color("white")
score_display.penup()
score_display.hideturtle()
score_display.goto(0, 260)
score_display.write("Player A: 0  Player B: 0", align="center", font=("Courier", 24, "normal"))

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

# Function to move paddle A with left thumb position
def move_paddle_a_with_thumb():
    if hand_landmarks and len(hand_landmarks) >= 2:
        left_thumb_x, left_thumb_y = hand_landmarks[1][4]  # Get the position of the left thumb
        paddle_a.sety((webcam_height / 2 - left_thumb_y) * 2)  # Adjust the paddle A position based on left thumb position

# Function to move paddle B with right thumb position
def move_paddle_b_with_thumb():
    if hand_landmarks and len(hand_landmarks) >= 2:
        right_thumb_x, right_thumb_y = hand_landmarks[0][4]  # Get the position of the right thumb
        paddle_b.sety((webcam_height / 2 - right_thumb_y) * 2)  # Adjust the paddle B position based on right thumb position

# Main game loop
while True:
    # Capture frame from webcam
    ret, frame = webcam.read()

    # Flip the frame horizontally for a later selfie-view display
    flipped_frame = cv2.flip(frame, 1)

    # Get hand landmarks from the frame
    hand_landmarks = hand_detector.detect_and_draw_landmarks(flipped_frame)

    # use landMark positions to control paddle A and B
    move_paddle_a_with_thumb()
    move_paddle_b_with_thumb()

    # Move the ball
    ball.setx(ball.xcor() + ball.dx)
    ball.sety(ball.ycor() + ball.dy)

    # Border checking
    if ball.ycor() > 290 or ball.ycor() < -290:
        ball.dy *= -1

    # Paddle collisions
    if (ball.dx > 0) and (350 > ball.xcor() > 340) and (paddle_b.ycor() + 50 > ball.ycor() > paddle_b.ycor() - 50):
        ball.dx *= -1
        score_b += 1
        score_display.clear()
        score_display.write("Player A: {}  Player B: {}".format(score_a, score_b), align="center", font=("Courier", 24, "normal"))

    elif (ball.dx < 0) and (-350 < ball.xcor() < -340) and (paddle_a.ycor() + 50 > ball.ycor() > paddle_a.ycor() - 50):
        ball.dx *= -1
        score_a += 1
        score_display.clear()
        score_display.write("Player A: {}  Player B: {}".format(score_a, score_b), align="center", font=("Courier", 24, "normal"))

    # Reset ball position when it goes out of bounds
    if ball.xcor() > 390:
        ball.goto(0, 0)
        ball.dx *= -1

    elif ball.xcor() < -390:
        ball.goto(0, 0)
        ball.dx *= -1

    # Update the game window after moving the paddles and ball
    win.update()

    # Verify that frame has been successfully read
    if not ret:
        break

    # Display the resulting frame
    #cv2.imshow('Hand Detection Webcam Feed', flipped_frame)

    # If 'q' is pressed on the keyboard, break the loop and end the program
    if cv2.waitKey(1) & 0xFF == ord('q'):
        break

# After the loop, release the webcam object
webcam.release()

# Destroy all the windows
cv2.destroyAllWindows()

# Finish the game
win.bye()
