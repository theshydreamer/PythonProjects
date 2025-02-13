import cv2
import mediapipe as mp
import pyautogui

# Initialize Mediapipe
mp_hands = mp.solutions.hands
hands = mp_hands.Hands(min_detection_confidence=0.7, min_tracking_confidence=0.7)
mp_draw = mp.solutions.drawing_utils

# Screen resolution
screen_w, screen_h = pyautogui.size()

# Webcam
cap = cv2.VideoCapture(0)

while cap.isOpened():
    ret, frame = cap.read()
    if not ret:
        break

    frame = cv2.flip(frame, 1)
    rgb_frame = cv2.cvtColor(frame, cv2.COLOR_BGR2RGB)
    result = hands.process(rgb_frame)

    if result.multi_hand_landmarks:
        for hand_landmarks in result.multi_hand_landmarks:
            mp_draw.draw_landmarks(frame, hand_landmarks, mp_hands.HAND_CONNECTIONS)

            # Get index finger tip position
            index_finger = hand_landmarks.landmark[8]
            thumb = hand_landmarks.landmark[4]

            x, y = int(index_finger.x * screen_w), int(index_finger.y * screen_h)
            pyautogui.moveTo(x, y)

            # Check if thumb and index finger are close (pinch)
            if abs(index_finger.x - thumb.x) < 0.02 and abs(index_finger.y - thumb.y) < 0.02:
                pyautogui.click()

    cv2.imshow("Mouse Control", frame)
    if cv2.waitKey(1) & 0xFF == ord('q'):
        break

cap.release()
cv2.destroyAllWindows()
