import cv2
import time
Known_distance = 30
Known_width = 5.7
GREEN = (0, 255, 0)
RED = (0, 0, 255)
BLACK = (0, 0, 0)
YELLOW = (0, 255, 255)
WHITE = (255, 255, 255)
CYAN = (255, 255, 0)
MAGENTA = (255, 0, 242)
GOLDEN = (32, 218, 165)
LIGHT_BLUE = (255, 9, 2)
PURPLE = (128, 0, 128)
CHOCOLATE = (30, 105, 210)
PINK = (147, 20, 255)
ORANGE = (0, 69, 255)
fonts = cv2.FONT_HERSHEY_COMPLEX
fonts2 = cv2.FONT_HERSHEY_SCRIPT_SIMPLEX
fonts3 = cv2.FONT_HERSHEY_COMPLEX_SMALL
fonts4 = cv2.FONT_HERSHEY_TRIPLEX
capID = 0
cap = cv2.VideoCapture(capID)  # Number According to your Camera
Distance_level = 0
travedDistance = 0
changeDistance = 0
velocity = 0
fourcc = cv2.VideoWriter_fourcc(*'XVID')
out = cv2.VideoWriter('output21.mp4', fourcc, 30.0, (640, 480))
face_detector = cv2.CascadeClassifier("E:\mini project\haarcascade_frontalface_default.xml")
def FocalLength(measured_distance, real_width, width_in_rf_image):
    focal_length = (10 * measured_distance) / real_width
    return focal_length
def Distance_finder(Focal_Length, real_face_width, face_width_in_frame):
    distance = (real_face_width * Focal_Length) / face_width_in_frame
    return distance
def speedFinder(distance, takenTime):
    speed = distance / takenTime
    return speed
def face_data(image, CallOut, Distance_level):
    face_width = 0
    face_x, face_y = 0, 0
    face_center_x = 0
    face_center_y = 0
    gray_image = cv2.cvtColor(image, cv2.COLOR_BGR2GRAY)
    faces = face_detector.detectMultiScale(gray_image, 1.2, 5)
    for (x, y, h, w) in faces:
        line_thickness = 1
        LLV = int(h * 0.12)
        cv2.line(image, (x, y + LLV), (x + w, y + LLV), (LIGHT_BLUE), line_thickness)
        cv2.line(image, (x, y + h), (x + w, y + h), (LIGHT_BLUE), line_thickness)
        cv2.line(image, (x, y + LLV), (x, y + LLV + LLV), (LIGHT_BLUE), line_thickness)
        cv2.line(image, (x + w, y + LLV), (x + w, y + LLV + LLV),
                 (LIGHT_BLUE), line_thickness)
        cv2.line(image, (x, y + h), (x, y + h - LLV), (LIGHT_BLUE), line_thickness)
        cv2.line(image, (x + w, y + h), (x + w, y + h - LLV), (LIGHT_BLUE), line_thickness)
        face_width = w
        face_center_x = int(w / 2) + x
        face_center_y = int(h / 2) + y
        if Distance_level < 10:
            Distance_level = 10
        if CallOut == True:
            cv2.line(image, (x, y - 11), (x + 180, y - 11), (WHITE), 20)
    return face_width, faces, face_center_x, face_center_y
def averageFinder(valuesList, numberElements):
    sizeOfList = len(valuesList)
    lastMostElement = sizeOfList - numberElements
    lastPart = valuesList[lastMostElement:]
    average = sum(lastPart) / (len(lastPart))
    return average
ref_image = cv2.imread("E:\mini project\Screenshot (37).png")
ref_image_face_width = face_data(ref_image, False, Distance_level)
Focal_length_found = FocalLength(Known_distance, Known_width, ref_image_face_width)
print(Focal_length_found)
cv2.imshow("ref_image", ref_image)
speedList = []
DistanceList = []
averageSpeed = 0
intialDisntace = 0
while True:
    _, frame = cap.read()
    intialTime = time.time()
    face_width_in_frame, Faces, FC_X, FC_Y = face_data(
        frame, True, Distance_level)
    # finding the distance by calling function Distance finder
    for (face_x, face_y, face_w, face_h) in Faces:
        if face_width_in_frame != 0:
            Distance = Distance_finder(
                Focal_length_found, Known_width, face_width_in_frame)
            DistanceList.append(Distance)
            avergDistnce = averageFinder(DistanceList, 6)
            roundedDistance = round((avergDistnce * 0.0254), 2)
            Distance_level = int(Distance)
            if intialDisntace != 0:
                changeDistance = Distance - intialDisntace
                distanceInMeters = changeDistance * 0.0254
                velocity = speedFinder(distanceInMeters, changeInTime)
                speedList.append(velocity)
                averageSpeed = averageFinder(speedList, 6)
            intialDisntace = avergDistnce
            changeInTime = time.time() - intialTime
            # cv2.line(frame, (25, 45), (180, 45), (BLACK), 26)
            cv2.line(frame, (25, 45), (180, 45), (WHITE), 20)
            if averageSpeed < 0:
                averageSpeed = averageSpeed * -1
            cv2.putText(
                frame, f"Speed: {round(averageSpeed, 2)} m/s", (30, 50), fonts, 0.5, BLACK, 2)
            cv2.putText(frame, f"Distance {roundedDistance} meter",
                        (face_x - 6, face_y - 6), fonts, 0.5, (BLACK), 2)
    cv2.imshow("frame", frame)
    out.write(frame)
    if cv2.waitKey(1) == ord("q"):
        break
cap.release()
cv2.destroyAllWindows()
