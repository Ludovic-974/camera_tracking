import cv2
import mediapipe as mp
from pymouse import PyMouse, PyMouseEvent
from pynput.mouse import Button,Controller

def init():
    mouse = Controller()
    cam = cv2.VideoCapture(0)
    if not cam.isOpened():
        print("Cannot open camera")
        exit()
    mpHands = mp.solutions.hands
    hands = mpHands.Hands()
    mpDraw =  mp.solutions.drawing_utils
    m = PyMouse()
    return mouse, cam, mpHands, hands, mpDraw, m

def get_hand_info(frame, hands):
    rbg = cv2.cvtColor(frame, cv2.COLOR_BGR2RGB)
    results = hands.process(rbg)
    return rbg, results

def get_hand_movement(results, m, mpDraw, frame, mpHands, mouse):
    if results.multi_hand_landmarks:
        for handLms in results.multi_hand_landmarks:
            for id, lm in enumerate(handLms.landmark):
                h, w, c = frame.shape
                cx, cy = int(lm.x*w), int(lm.y*h)
                if id == 4:
                    fingery = cy
                    fingerx = cx
                    cv2.circle(frame, (cx, cy), 20, (0, 255, 255), cv2.FILLED)
                if id == 8:
                    click = cy
                    cv2.circle(frame, (cx, cy), 20, (255, 0, 255), cv2.FILLED)
            if fingery < click:
               mouse.press(Button.left)
               mouse.release(Button.left)
            m.move(fingerx * 4, fingery * 4)
            mpDraw.draw_landmarks(frame, handLms, mpHands.HAND_CONNECTIONS)

def mouve_mouse():
    mouse, cam, mpHands, hands, mpDraw, m = init()
    while True:
        ret, frame = cam.read()
        rbg, results = get_hand_info(frame, hands)
        get_hand_movement(results, m, mpDraw, frame, mpHands, mouse)
        if not ret:
            print("Cannot read camera\n")
            break
        cv2.imshow("Cam", frame)
        if cv2.waitKey(1) == ord('q'):
            break
mouve_mouse()