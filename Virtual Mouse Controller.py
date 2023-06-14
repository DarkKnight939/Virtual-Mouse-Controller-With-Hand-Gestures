import cv2
import math
import mediapipe as mp
import pyautogui
import time

mp_drawing = mp.solutions.drawing_utils
mp_hands = mp.solutions.hands

# For webcam input:
cap = cv2.VideoCapture(0)

cap.set(cv2.CAP_PROP_FPS, 30)
start_time = 0
start_time1 = 0
start_time2 = 0
prev_time = 0

with mp_hands.Hands(
        min_detection_confidence=0.6,
        min_tracking_confidence=0.6, static_image_mode=False,
        max_num_hands=2, ) as hands:

    initial_distance = 0
    while cap.isOpened():

        curr_time = time.time()
        fps = 1 / (curr_time - prev_time)
        prev_time = curr_time
        print(fps)

        success, img = cap.read()
        if not success:
            print("Ignoring empty camera frame.")
            continue

        # Flip the image horizontally for a later selfie-view display, and convert
        # the BGR image to RGB.
        img = cv2.cvtColor(cv2.flip(img, 1), cv2.COLOR_BGR2RGB)
        # To improve performance, optionally mark the image as not writeable to
        # pass by reference.
        img.flags.writeable = False
        results = hands.process(img)
        # Draw the hand annotations on the image.
        img.flags.writeable = True
        img = cv2.cvtColor(img, cv2.COLOR_RGB2BGR)
        if results.multi_hand_landmarks:
            for handLms in results.multi_hand_landmarks:
                # Draw hand landmarks
                mp_drawing.draw_landmarks(img, handLms, mp_hands.HAND_CONNECTIONS)

                fingers = [0, 0, 0, 0, 0]
                for id, lm in enumerate(handLms.landmark):
                    h, w, c = img.shape
                    cx, cy = int(lm.x * w), int(lm.y * h)
                    if id == 0:
                        x0, y0 = cx, cy
                    if id == 2:
                        x2, y2 = cx, cy
                    if id == 4:
                        x4, y4 = cx, cy
                    if id == 5:
                        x5, y5 = cx, cy
                    if id == 8:
                        x8, y8 = cx, cy
                    if id == 9:
                        x9, y9 = cx, cy
                    if id == 12:
                        x12, y12 = cx, cy
                    if id == 13:
                        x13, y13 = cx, cy
                    if id == 16:
                        x16, y16 = cx, cy
                    if id == 17:
                        x17, y17 = cx, cy
                    if id == 20:
                        x20, y20 = cx, cy

                        if math.dist([x8, y8], [x0, y0]) > math.dist([x5, y5], [x0, y0]):
                            fingers[1] = 1
                        if math.dist([x12, y12], [x0, y0]) > math.dist([x9, y9], [x0, y0]):
                            fingers[2] = 1
                        if math.dist([x16, y16], [x0, y0]) > math.dist([x13, y13], [x0, y0]):
                            fingers[3] = 1
                        if math.dist([x20, y20], [x0, y0]) > math.dist([x17, y17], [x0, y0]):
                            fingers[4] = 1

                        count1 = fingers.count(1)
                if count1 == 0:
                    print(start_time)
                    start_time += 1
                    starttime = time.time()
                    if start_time > 10:
                        pyautogui.keyDown('alt')
                        pyautogui.press('tab')
                        pyautogui.sleep(0.5)
                        pyautogui.press('tab')
                        pyautogui.keyUp('alt')
                        start_time = 0
                if count1 == 1:
                    if math.dist([x8, y8], [x0, y0]) > math.dist([x5, y5], [x0, y0]):
                        pyautogui.click()
                        pyautogui.sleep(0.2)
                    if math.dist([x12, y12], [x0, y0]) > math.dist([x9, y9], [x0, y0]):
                        pyautogui.doubleClick()

                elif count1 == 2:
                    if x4 < x8:
                        # get the updated distance between (x4, y4) and (x8, y8)
                        updated_distance = math.dist([x4, y4], [x8, y8])
                        print(start_time1, start_time2)
                        # check if the distance has increased or decreased
                        if updated_distance >= initial_distance:
                            pyautogui.keyDown('ctrl')
                            pyautogui.scroll(10)  # scroll up
                            pyautogui.keyUp('ctrl')
                            print("zooming in")

                        else:
                            pyautogui.keyDown('ctrl')
                            pyautogui.scroll(-10)  # scroll down
                            pyautogui.keyUp('ctrl')
                            print("zooming out")

                        print(initial_distance, " BBC")
                        print(updated_distance)
                        initial_distance = updated_distance

                    else:
                        pyautogui.moveTo(3.52 * (x5 - 20), 3.6 * (y5 - 90))

                elif count1 == 3:
                    if math.dist([x16, y16], [x0, y0]) > math.dist([x13, y13], [x0, y0]):
                        pyautogui.mouseDown()
                        pyautogui.sleep(0.1)

                elif count1 == 4:
                    if y16 < y0:
                        pyautogui.scroll(-250)  # scrolls down
                    else:
                        pyautogui.scroll(250)  # scrolls up

                cv2.putText(img, str(count1), (10, 50), cv2.FONT_HERSHEY_SIMPLEX, 1, (255, 0, 0), 2)
        cv2.imshow('MediaPipe Hands', img)
        if cv2.waitKey(1) == ord('q'):
            break

cap.release()
cv2.destroyAllWindows()
