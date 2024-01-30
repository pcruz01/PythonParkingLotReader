import cv2
import pickle
import cvzone
import numpy as np
import time
from db_module import connect_to_db, perform_query

# Video feed
cap = cv2.VideoCapture('carPark.mp4')

with open('CarParkPos', 'rb') as f:
    posList = pickle.load(f)

width, height = 107, 48

def checkParkingSpace(imgPro):

    spaceCounter = 0
    lotID = '19Y'

    for pos in posList:
        x, y = pos

        imgCrop = imgPro[y:y+height, x:x+width]
        count = cv2.countNonZero(imgCrop)
        cvzone.putTextRect(img, str(count), (x, y+height-3), scale=1, 
                           thickness=2, offset=0, colorR=(0, 0, 255))

        if count < 850:
            color = (0, 255, 0)
            thickness = 5
            spaceCounter += 1
        else:
            color = (0, 0, 255)
            thickness = 2
        cv2.rectangle(img, pos, (pos[0]+width, pos[1]+height), color, thickness)

    cvzone.putTextRect(img, f'Free: {spaceCounter}/{len(posList)}', (100, 50), scale=3, 
            thickness=5, offset=20, colorR=(0, 200, 0))

    return spaceCounter, lotID

start_time = time.time()  # Record the start time
interval_time = 3

while True:
    if cap.get(cv2.CAP_PROP_POS_FRAMES) == cap.get(cv2.CAP_PROP_FRAME_COUNT):
        cap.set(cv2.CAP_PROP_POS_FRAMES, 0)
    success, img = cap.read()
    imgGray = cv2.cvtColor(img, cv2.COLOR_BGR2GRAY)
    imgBlur = cv2.GaussianBlur(imgGray, (3, 3), 1)
    imgThreshold = cv2.adaptiveThreshold(imgBlur, 255, cv2.ADAPTIVE_THRESH_GAUSSIAN_C,
                                         cv2.THRESH_BINARY_INV, 25, 16)
    imgMedian = cv2.medianBlur(imgThreshold, 5)
    kernel = np.ones((3, 3), np.uint8)
    imgDilate = cv2.dilate(imgMedian, kernel, iterations=1)

    spaceCounter, lotID = checkParkingSpace(imgDilate)

    cv2.imshow("Image", img)
    cv2.waitKey(10)

    # Calculate elapsed time
    elapsed_time = time.time() - start_time

    # Print something every 10 seconds
    if elapsed_time >= interval_time:
        connection = connect_to_db()
        perform_query(connection, lotID, spaceCounter)
        connection.close()

        print(f'{lotID} has {spaceCounter} spots available')
        # Reset the start time for the next interval
        start_time = time.time()
