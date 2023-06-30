import cv2
import numpy as np

def save_blank_test():
    # Create a blank test image
    blank_test = 255 * np.ones((1600, 1400), dtype=np.uint8)  # Increase the size to fit larger markers and the shifted squares

    # Define the locations of the answer regions for the student ID
    id_locs = [(y, x) for y in range(200, 300, 50) for x in range(250, 1250, 100)]  # Shift ID locations
    # Define the locations of the answer regions for each question
    question_locs = [(y, x) for y in range(400, 1400, 100) for x in range(250, 750, 100)]  # Shift question locations

    # Define the size of the markers
    marker_size = 150  # The marker size remains the same

    # Define the locations of the markers
    marker_locs = [(10, 10), (10, blank_test.shape[1] - marker_size - 10), 
                   (blank_test.shape[0] - marker_size - 10, 10), 
                   (blank_test.shape[0] - marker_size - 10, blank_test.shape[1] - marker_size - 10)]
    
    # Draw the ID squares
    for y, x in id_locs:
        cv2.rectangle(blank_test, (x, y), (x+50, y+50), (0), 2)

    # Draw the answer squares
    for y, x in question_locs:
        cv2.rectangle(blank_test, (x, y), (x+50, y+50), (0), 2)

    # Draw the markers
    for y, x in marker_locs:
        cv2.rectangle(blank_test, (x, y), (x+marker_size, y+marker_size), (0), -1)

    # Save the blank test image
    cv2.imwrite('blank_testMK6.png', blank_test)

if __name__ == "__main__":
    save_blank_test()
