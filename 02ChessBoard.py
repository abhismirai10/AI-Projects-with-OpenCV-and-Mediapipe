import cv2
import numpy as np

# Generate the entire checkerboard at once before entering the while loop.
blockSize = 160
size = 8 * blockSize
frame = np.zeros((size, size, 3), dtype=np.uint8)

for i in range(8):
    for j in range(8):
        if (i + j) % 2 == 0:
            frame[i*blockSize:(i+1)*blockSize, j*blockSize:(j+1)*blockSize] = (255, 255, 255)

cv2.imshow('my image', frame)

while True:

    # If 'q' is pressed, break the loop
    if cv2.waitKey(1) & 0xFF == ord('q'):
        break

# destroy windows
cv2.destroyAllWindows()
