import cv2 as cv


def list_camera_indexes(limit: int = 5) -> list[int]:
    """
    get list of valid indexes of cameras connected
    :param limit: search camera index limit, default value 10
    :return: valid camera indexes
    """
    camera_indexes: list[int] = []

    for i in range(limit):
        try:
            cap = cv.VideoCapture(i)
            if cap.read()[0]:
                camera_indexes.append(i)
                cap.release()
            break
        except:
            # suppress errors on output for camera index out of range
            break

    return camera_indexes


def capture_calibration_image(camera_index: int = 0) -> None:
    """
    capture calibration image on 'c' keypress, quit on 'q' keypress
    :param camera_index: index of camera to capture calibration image from
    :return: none, image is saved to file
    """
    cap = cv.VideoCapture(camera_index)

    if not cap.isOpened():
        print("Cannot open camera")

    while True:
        ret, frame = cap.read()
        cv.imshow('frame', frame)

        if not ret:
            print("Can't receive frame")
            break

        if cv.waitKey(1) == ord('q'):
            break

        if cv.waitKey(1) == ord('c'):
            cv.imwrite("calib/calibration_frame.png", frame)
            break

    cap.release()
    cv.destroyAllWindows()


def get_calibration_image(path: str = "calib/calibration_frame.png") -> []:
    image = cv.imread(path)
    return image


def circle_detection() -> None:
    print('circle detection function')


def main():
    print(cv.__version__)

    camera_indexes = list_camera_indexes()
    print(camera_indexes)

    # capture_calibration_image(0)

    calibration_image = get_calibration_image()

    while True:
        cv.imshow('cal_frame', calibration_image)
        if cv.waitKey(1) == ord('q'):
            break


if __name__ == "__main__":
    main()