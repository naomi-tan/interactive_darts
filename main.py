import cv2 as cv

print(cv.__version__)

cap = cv.VideoCapture(0)

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