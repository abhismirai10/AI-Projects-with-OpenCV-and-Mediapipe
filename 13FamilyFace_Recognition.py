import cv2
import face_recognition as fr

# Open the webcam
webcam = cv2.VideoCapture(0)

# Check if webcam is opened correctly
if not webcam.isOpened():
    raise IOError("Cannot open webcam")

# Set the webcam resolution
webcam.set(cv2.CAP_PROP_FRAME_WIDTH, 1280)
webcam.set(cv2.CAP_PROP_FRAME_HEIGHT, 720)
webcam.set(cv2.CAP_PROP_FPS, 30)

# Setup font for text in video
font = cv2.FONT_HERSHEY_SIMPLEX

# Function to load and encode faces
def load_and_encode_face(image_path):
    image = fr.load_image_file(image_path)
    if image is None:
        raise IOError(f"Cannot open image at {image_path}")
    face_locations = fr.face_locations(image)
    if len(face_locations) == 0:
        raise ValueError(f"No face detected in the image at {image_path}")
    face_encoding = fr.face_encodings(image, face_locations)[0]
    return face_encoding

# Load and encode known faces
known_faces = {
    "Abhi": load_and_encode_face('Family/known/Abhi.jpg'),
    "Dada": load_and_encode_face('Family/known/Dada.jpeg'),
    "Pooja": load_and_encode_face('Family/known/Didi.jpeg'),
    "Prabha": load_and_encode_face('Family/known/Mummy.jpeg'),
    "Bakul": load_and_encode_face('Family/known/Papa.jpeg'),
}

# Main loop to read and process frames
while True:
    ret, frame = webcam.read()

    # If the frame was not read correctly, then we break the loop
    if not ret:
        break

    # Convert the image from BGR color to RGB color
    rgb_frame = cv2.cvtColor(frame, cv2.COLOR_BGR2RGB)

    # Find all face locations and face encodings in the current frame
    face_locations = fr.face_locations(rgb_frame)
    face_encodings = fr.face_encodings(rgb_frame, face_locations)

    # Process each face in the frame
    for face_location, face_encoding in zip(face_locations, face_encodings):
        # Draw a rectangle around the face
        top, right, bottom, left = face_location
        #cv2.rectangle(frame, (left, top), (right, bottom), (255, 0, 0), 3)

        # Default face name to "Unknown" if no match found
        face_name = "Unknown Person"

        # Check if this face matches any known faces
        for known_name, known_encoding in known_faces.items():
            match = fr.compare_faces([known_encoding], face_encoding, tolerance=0.50)
            if match[0]:                            
                # If a match was found, set face_name to the known name
                face_name = known_name
                break

        # Display the face name on the frame
        #cv2.putText(frame, face_name, (left, top), font, .75, (0, 0, 255), 2)
        cv2.putText(frame, "hey {} whats up!, abhi talks about you a lot!".format(face_name), (50, 50), font, .75, (255, 0, 0), 2)
        if face_name == "Pooja":
            cv2.putText(frame, "have you appied for your visa?".format(face_name), (50, 700), font, .75, (0, 255, 0), 2)
        if face_name == "Prabha":
            cv2.putText(frame, "how was your teaching today?".format(face_name), (50, 700), font, .75, (0, 255, 0), 2)
        if face_name == "Bakul":
            cv2.putText(frame, "how is the crop in your farm?".format(face_name), (50, 700), font, .75, (0, 255, 0), 2)
      
    # Display the resulting frame
    cv2.imshow('Face Recognition', frame)

    # If 'q' is pressed, break the loop
    if cv2.waitKey(1) & 0xFF == ord('q'):
        break

# Release the VideoCapture and destroy all windows
webcam.release()
cv2.destroyAllWindows()
