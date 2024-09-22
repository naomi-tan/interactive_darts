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


def detect_circles(img):
    # detect circles in calibration image
    cimg = cv.cvtColor(img, cv.COLOR_GRAY2BGR)

    circles  = cv.HoughCircles(img, cv.HOUGH_GRADIENT, 1, 20, param1=100, param2=60, minRadius=0, maxRadius=0)
    circles = np.uint16(np.around(circles))
    print(f'{len(circles[0])} circles image')

    for i in circles[0,:]:
        # draw outer circle
        cv.circle(cimg, (i[0], i[1]), i[2], (0, 255, 0), 2)
        # draw center
        cv.circle(cimg, (i[0], i[1]), 2, (0, 0, 255), 3)

    cv.imshow('detected circles', cimg)


def fit_ellipse(img):
    # fit ellipse to calibration image
    ret, thresh = cv.threshold(img, 150, 255, 0) # 111/227 200
    contours, hierarchy = cv.findContours(thresh, 1, 2)
    cnt = contours[0]
    m = cv.moments(cnt)
    # print(m)
    cv.imshow('calibration image', img)

    ellipse = cv.fitEllipse(cnt)
    cv.ellipse(img, ellipse, (255, 0, 0), 2)
    cv.imshow('ellipse image', img)
    print(ellipse)


def blob_detection(img):
    # detect circles and ellipses in calibration image
    params = cv.SimpleBlobDetector_Params()

    # params.filterByArea = True
    # params.minArea = 2000

    # params.filterByConvexity = True
    # params.minConvexity = 0.1

    params.filterByInertia = True
    params.minInertiaRatio = 0.01

    detector = cv.SimpleBlobDetector_create(params)
    keypoints = detector.detect(img)

    blank = np.zeros((1, 1))
    blobs = cv.drawKeypoints(img, keypoints, blank, (0, 0, 255), cv.DRAW_MATCHES_FLAGS_DRAW_RICH_KEYPOINTS)

    cv.imshow('blob detection', blobs)


def main():
    print(cv.__version__)

    # camera_indexes = list_camera_indexes()
    # print(camera_indexes)

    # capture_calibration_image(0)

    main_path = os.path.abspath(__file__)
    img_path = os.path.join(os.path.dirname(main_path), "calib\\calibration_frame1.png")
    print(img_path)

    img = cv.imread(img_path, cv.IMREAD_GRAYSCALE)  # Hough circle detection must be grayscale
    img = cv.medianBlur(img, 5)
    cv.imshow('calibration image', img)

    h, w = img.shape[:2]
    print(f'height: {h}, width: {w}')

    # this is not a good way to detect dart board circles at an angle as they will be an ellipse
    # detect_circles(img)

    # not sure how to set thresholds/parameters, not picking up the right ellipse
    # fit_ellipse(img)

    blob_detection(img)

    cv.waitKey(0)
    cv.destroyAllWindows()


if __name__ == "__main__":
    main()