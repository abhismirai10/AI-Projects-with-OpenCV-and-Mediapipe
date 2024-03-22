import cv2
import mediapipe as mp
import random
import turtle

# Set up the screen
win = turtle.Screen()
win.title("Fruit Ninja with Hand Control")
win.bgcolor("black")
win.setup(width=1280, height=720)
win.tracer(0)

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
                landmarks_coordinates = [(int(landmark.x * webcam_width), int(landmark.y * webcam_height)) for landmark in hand_landmark.landmark]
                hand_positions.append(landmarks_coordinates)
        return hand_positions

# Create a HandDetector object
hand_detector = HandDetector()

# Ball at Finger Position
ball = turtle.Turtle()
ball.shape("circle")
ball.color("white")
ball.shapesize(0.25, 0.25)  # Set the radius to make it smaller
ball.penup()
        
# Class for handling fruit objects
class Fruit:
    def __init__(self, shape, color, speed):
        self.fruit = turtle.Turtle()
        self.fruit.speed(0)
        self.fruit.shape(shape)
        self.fruit.color(color)
        self.fruit.penup()
        self.fruit.setposition(random.randint(-350, 350), 290)
        self.fruit.dy = -speed

# List to store fruit objects
fruits = []

# Function to spawn a new fruit
def spawn_fruit():
    shapes = ["circle", "triangle"]
    colors = ["red", "green", "blue", "yellow"]
    speed = random.randint(8, 10)
    fruit_shape = random.choice(shapes)
    fruit_color = random.choice(colors)
    new_fruit = Fruit(fruit_shape, fruit_color, speed)
    fruits.append(new_fruit)

# Function to detect slicing gesture and cut fruits
def detect_and_slice_fruits(hand_positions):
    for fruit in fruits:
        fruit_y = fruit.fruit.ycor()
        if fruit_y <= -290:
            fruits.remove(fruit)
            continue
        for hand_landmarks in hand_positions:
            hand_point_x, hand_point_y = hand_landmarks[8]
            hand_point_x = hand_point_x - webcam_width/2
            hand_point_y = -(hand_point_y - webcam_height/2)
            fruit_x, fruit_y = fruit.fruit.xcor(), fruit.fruit.ycor()

            if abs(hand_point_x - fruit_x) < 30 and abs(fruit_y - hand_point_y) < 30:
                fruit.fruit.hideturtle()
                fruits.remove(fruit)

# Main game loop
while True:
    # Capture frame from webcam
    ret, frame = webcam.read()

    # Flip the frame horizontally for a later selfie-view display
    flipped_frame = cv2.flip(frame, 1)

    # Get hand landmarks from the frame
    hand_landmarks = hand_detector.detect_and_draw_landmarks(flipped_frame)

    # Draw point at finger tip
    for hand_landmark in hand_landmarks:
        hand_point_x, hand_point_y = hand_landmark [8]
        hand_point_x = hand_point_x - webcam_width/2
        hand_point_y = -(hand_point_y - webcam_height/2)
            
        ball.setx (hand_point_x)
        ball.sety (hand_point_y)

    # Spawn a new fruit at random intervals
    if random.random() < 0.1:
        spawn_fruit()

    # Move the fruits and check for slicing gestures
    for fruit in fruits:
        fruit.fruit.sety(fruit.fruit.ycor() + fruit.fruit.dy)

    # Detect slicing gestures and cut fruits
    detect_and_slice_fruits(hand_landmarks)

    # Update the game window after moving the paddles, ball, and fruits
    win.update()

    # Verify that frame has been successfully read
    if not ret:
        break

    # If 'q' is pressed on the keyboard, break the loop and end the program
    if cv2.waitKey(1) & 0xFF == ord('q'):
        break

# After the loop, release the webcam object
webcam.release()

# Destroy all the windows
cv2.destroyAllWindows()

# Finish the game
win.bye()