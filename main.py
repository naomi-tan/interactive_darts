import cv2 as cv
import os
import numpy as np
import re

def list_camera_indexes(limit = 10):
    # return valid camera indexes, limit 10
    camera_indexes = []

    for i in range(limit):
        print(i)
        cap = cv.VideoCapture(i)
        print('@')
        if cap.read()[0]:
            print('?')
            camera_indexes.append(i)
            cap.release()
        print('!')
    return camera_indexes


def capture_calibration_image(index: int = 0) -> str:
    # open camera session and save image to file on key press
    cal_imgs = os.listdir('calib')
    img_num = 0
    for img in cal_imgs:
        # i = int(img.split('calibration_frame')[1].split(''))
        i = int(img.split('calibration_frame')[1].split('.png')[0])
        if i > img_num:
            img_num = i
    img_path = f'calib\\calibration_frame{img_num + 1}.png'

    cap = cv.VideoCapture(index)
    if not cap.isOpened():
        print("Cannot open camera")
        exit()

    while True:
        ret, frame = cap.read()
        gray = cv.cvtColor(frame, cv.COLOR_BGR2GRAY)
        cv.imshow('frame', gray)

        if not ret:
            print("Can't receive frame")
            break

        if cv.waitKey(1) & 0xFF == ord('q'):
            img_path = f'calib\\{cal_imgs[-1]}'
            break

        if cv.waitKey(1) & 0xFF == ord('c'):
            cv.imwrite(img_path, frame)
            break

    cap.release()
    cv.destroyAllWindows()
    return img_path


def detect_circles(img):
    # detect circles in calibration image
    cimg = cv.cvtColor(img, cv.COLOR_GRAY2BGR)

    # circles  = cv.HoughCircles(img, cv.HOUGH_GRADIENT, 1, 20, param1=100, param2=60, minRadius=0, maxRadius=0)
    circles  = cv.HoughCircles(img, cv.HOUGH_GRADIENT, 1, 20, param1=100, param2=60, minRadius=190, maxRadius=0)
    circles = np.uint16(np.around(circles))
    print(f'{len(circles[0])} circles image')

    max_radius = 0
    max_i = []

    for i in circles[0,:]:
        if i[2] > max_radius:
            max_radius = i[2]
            max_i = i

    # draw outer circle
    cv.circle(cimg, (max_i[0], max_i[1]), max_i[2], (0, 255, 0), 2)
    # draw center
    cv.circle(cimg, (max_i[0], max_i[1]), 2, (0, 0, 255), 3)
    return cimg


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

    params.filterByArea = True
    params.minArea = 2000

    params.filterByConvexity = True
    params.minConvexity = 0.5

    params.filterByInertia = True
    params.minInertiaRatio = 0.1

    detector = cv.SimpleBlobDetector_create(params)
    # detector = cv.SimpleBlobDetector()
    keypoints = detector.detect(img)

    blank = np.zeros((1, 1))
    blobs = cv.drawKeypoints(img, keypoints, blank, (0, 0, 255), cv.DRAW_MATCHES_FLAGS_DRAW_RICH_KEYPOINTS)
    return blobs


def edge_detection(img):
    edge_img = cv.Canny(img, 300, 350)
    return edge_img


def adjust_image(img):
    # adjust image brightness and contrast
    new_img = np.zeros(img.shape, img.dtype)

    alpha = 3  # contrast
    beta = 0  # brightness

    for y in range(img.shape[0]):
        for x in range(img.shape[1]):
            for c in range(img.shape[2]):
                new_img[y, x, c] = np.clip(alpha*img[y, x, c] + beta, 0, 255)

    cv.imshow('adjusted image', new_img)
    return new_img


def main():
    print(cv.__version__)

    # img_path = capture_calibration_image(0)
    img_path = f'calib\\calibration_frame2.png'
    print(img_path)

    img = cv.imread(img_path)  # Hough circle detection must be grayscale
    img = cv.imread(img_path, cv.IMREAD_GRAYSCALE)  # Hough circle detection must be grayscale
    # img = cv.medianBlur(img, 5)
    cv.imshow('calibration image', img)

    # h, w = img.shape[:2]
    # print(f'height: {h}, width: {w}')

    # new_img = adjust_image(img)

    edge_img = edge_detection(img)
    cv.imshow('edges', edge_img)
    # blobs = blob_detection(edge_img)
    # cv.imshow('blob detection', blobs)
    # not sure how to set thresholds/parameters, not picking up the right ellipse
    # fit_ellipse(edge_img)
    # this is not a good way to detect dart board circles at an angle as they will be an ellipse
    cimg = detect_circles(edge_img)
    cv.imshow('detected circles', cimg)

    cv.waitKey(0)
    cv.destroyAllWindows()


if __name__ == "__main__":
    main()