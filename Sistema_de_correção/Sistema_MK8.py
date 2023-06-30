import cv2
import numpy as np

def process_test(image, answer_key):

    def preprocess_image(image):
        # Convert the image to grayscale
        gray = cv2.cvtColor(image, cv2.COLOR_BGR2GRAY)

        # Threshold the image
        _, thresh = cv2.threshold(gray, 100, 255, cv2.THRESH_BINARY_INV)

        # Find contours in the thresholded image
        contours, _ = cv2.findContours(thresh, cv2.RETR_EXTERNAL, cv2.CHAIN_APPROX_SIMPLE)

        # Visualize all contours found
        #cv2.drawContours(image, contours, -1, (0,255,0), 3)
        #cv2.imshow("Contours", image)
        #cv2.waitKey(0)
        #cv2.destroyAllWindows()

        # Find the four largest contours - these should be the corner markers
        contours = sorted(contours, key=cv2.contourArea, reverse=True)[:4]

        if len(contours) != 4:
            print('Error: not exactly four contours found.')
            return None, None

        # Compute the centroid of each contour
        centers = []
        for contour in contours:
            M = cv2.moments(contour)
            cX = int(M["m10"] / M["m00"])
            cY = int(M["m01"] / M["m00"])
            centers.append((cX, cY))

        # Sort the contours/centers by their position (top-left, top-right, bottom-left, bottom-right)
        # Top-left corner will have the smallest sum, bottom-right corner will have the largest sum.
        contours = [x for _,x in sorted(zip([c[0]+c[1] for c in centers], contours), key=lambda pair: pair[0])]

        # Define 4 corner points of the new perspective
        dst_pts = np.float32([(0, 0), (image.shape[1] - 1, 0), (0, image.shape[0] - 1), (image.shape[1] - 1, image.shape[0] - 1)])

        # Determine 4 corresponding points from the original image
        src_pts = np.float32([cv2.minAreaRect(contour)[0] for contour in contours])

        # Compute the perspective transform matrix
        M = cv2.getPerspectiveTransform(src_pts, dst_pts)

        # Apply the perspective transformation
        corrected = cv2.warpPerspective(image, M, (image.shape[1], image.shape[0]))

        return thresh, corrected




    def get_id_digits(id_locs, thresh):
        id_digits = []
        for i in range(20):
            y, x = id_locs[i]
            answer_region = thresh[y:y+50, x:x+50]
            ink_amount = cv2.countNonZero(answer_region)
            
            if ink_amount > ink_threshold:
                id_digits.append(i%10)
        
        return id_digits

    def get_answers(question_locs, thresh):
        answers = []
        for i in range(10):
            ink_amounts = []
            for j in range(5):
                y, x = question_locs[i*5 + j]
                answer_region = thresh[y:y+50, x:x+50]
                ink_amount = cv2.countNonZero(answer_region)
                ink_amounts.append(ink_amount)

            marked_answers = [amt > ink_threshold for amt in ink_amounts]
            if marked_answers.count(True) != 1:
                answers.append(None)
            else:
                answers.append(np.argmax(ink_amounts))

        return answers

    


    thresh, image = preprocess_image(image)

    # Check if thresh and image are None
    if thresh is None or image is None:
        print("Image preprocessing failed.")
        return None, None

    # Define the locations of the answer regions for the student ID
    id_locs = [(y, x) for y in range(200, 300, 50) for x in range(250, 1250, 100)]  # shift ID locations
    # Define the locations of the answer regions for each question
    question_locs = [(y, x) for y in range(400, 1400, 100) for x in range(250, 750, 100)]  # shift question locations
    
    
        # Draw rectangles around ID locations
    for loc in id_locs:
        y, x = loc
        cv2.rectangle(image, (x, y), (x+50, y+50), (0,255,0), 2)

    # Draw rectangles around answer locations
    for loc in question_locs:
        y, x = loc
        cv2.rectangle(image, (x, y), (x+50, y+50), (0,255,0), 2)

    # Show the image with the rectangles
    #cv2.imshow("Regions", image)
    #cv2.waitKey(0)
    #cv2.destroyAllWindows()


    ink_threshold = 500
    id_digits = get_id_digits(id_locs, thresh)
    answers = get_answers(question_locs, thresh)

    # Determine test ID
    id = id_digits[0]*10 + id_digits[1] if len(id_digits) == 2 else None

    # Score the test
    score = sum(a == b for a, b in zip(answers, answer_key) if a is not None)

    return id, score

if __name__ == "__main__":
    image = cv2.imread('testMK6-distorcido.jpg')  # replace with your actual image path
    answer_key = [0, 1, 2, 3, 4, 3, 2, 1, 0, 1]  # replace with your actual answer key
    id, score = process_test(image, answer_key)
    print(f'The test ID is {id}, the test score is {score} out of 10')