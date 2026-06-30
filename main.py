import cv2
import numpy as np

img = cv2.imread("1.jpg")

if img is None:
    raise FileNotFoundError("1.jpg not found.")

img = cv2.resize(img, (1280, 720))
orig = img.copy()

points = []


def mouse_click(event, x, y, flags, param):
    global img

    if event == cv2.EVENT_LBUTTONDOWN and len(points) < 4:

        points.append([x, y])

        cv2.circle(img, (x, y), 8, (0, 0, 255), -1)
        cv2.imshow("Select Points", img)

        print("Current Points:", points)

        if len(points) == 4:
            perspective_and_threshold()


def perspective_and_threshold():

    if len(points) != 4:
        print("Error: Exactly 4 points are required.")
        return

    pts1 = np.array(points, dtype=np.float32)

    print("Points:")
    print(pts1)

    print("Shape:", pts1.shape)
    print("Datatype:", pts1.dtype)

    width = 300
    height = 400

    pts2 = np.array(
        [
            [0, 0],
            [width, 0],
            [width, height],
            [0, height],
        ],
        dtype=np.float32,
    )

    try:
        matrix = cv2.getPerspectiveTransform(pts1, pts2)
    except cv2.error as e:
        print("\nOpenCV Error:")
        print(e)
        return

    warped = cv2.warpPerspective(orig, matrix, (width, height))

    gray = cv2.cvtColor(warped, cv2.COLOR_BGR2GRAY)

    thresh = cv2.adaptiveThreshold(
        gray,
        255,
        cv2.ADAPTIVE_THRESH_GAUSSIAN_C,
        cv2.THRESH_BINARY,
        25,
        15,
    )

    cv2.imshow("Perspective", warped)
    cv2.imshow("Adaptive", thresh)


cv2.namedWindow("Select Points")
cv2.imshow("Select Points", img)

cv2.setMouseCallback("Select Points", mouse_click)

print("Click 4 points in order:")
print("Top Left → Top Right → Bottom Right → Bottom Left")

cv2.waitKey(0)
cv2.destroyAllWindows()