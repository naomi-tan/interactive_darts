import cv2 as cv


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
            cv.imwrite("calib/calibration_frame1.png", frame)
            break

    cap.release()
    cv.destroyAllWindows()


def main():
    print(cv.__version__)

    # camera_indexes = list_camera_indexes()
    # print(camera_indexes)

    capture_calibration_image(0)


if __name__ == "__main__":
    main()