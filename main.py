import cv2 as cv
import os
import numpy as np

def list_camera_indexes(limit = 10):
    # return valid camera indexes, limit 10
    camera_indexes = []

    for i in range(limit):
        cap = cv.VideoCapture(i)
        if cap.read()[0]:
            camera_indexes.append(i)
            cap.release()
    return camera_indexes


def capture_calibration_image(index = 0):
    # open camera session and save image to file on key press
    cap = cv.VideoCapture(index)
    if not cap.isOpened():
        print("Cannot open camera")
        exit()

    while True:
        ret, frame = cap.read()
        cv.imshow('frame', frame)

        if not ret:
            print("Can't receive frame")
            break

        if cv.waitKey(1) == ord('q'):
            break

        if cv.waitKey(1) == ord('c'):
            cv.imwrite("calib\\calibration_frame1.png", frame)
            break

    cap.release()
    cv.destroyAllWindows()


def circle_detection():
    # detect circles in calibration image
    main_path = os.path.abspath(__file__)
    img_path = os.path.join(os.path.dirname(main_path), "calib\\calibration_frame1.png")
    print(img_path)

    img = cv.imread(img_path, cv.IMREAD_GRAYSCALE) # Hough circle detection must be grayscale
    cv.imshow('calibration image', img)

    cimg = cv.cvtColor(img, cv.COLOR_GRAY2BGR)

    circles  = cv.HoughCircles(img, cv.HOUGH_GRADIENT, 1, 20, param1=100, param2=90, minRadius=0, maxRadius=0)
    circles = np.uint16(np.around(circles))
    print(f'{len(circles[0])} circles detected')

    for i in circles[0,:]:
        # draw outer circle
        cv.circle(cimg, (i[0], i[1]), i[2], (0, 255, 0), 2)
        # draw center
        cv.circle(cimg, (i[0], i[1]), 2, (0, 0, 255), 3)

    cv.imshow('detected circles', cimg)

    cv.waitKey(0)
    cv.destroyAllWindows()


def main():
    print(cv.__version__)

    # camera_indexes = list_camera_indexes()
    # print(camera_indexes)

    # capture_calibration_image(0)

    circle_detection()


if __name__ == "__main__":
    main()