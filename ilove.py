import cv2
import mediapipe as mp


def count_fingers(hand_landmarks):
    fingers = [0, 0, 0, 0, 0]  # Thumb, Index, Middle, Ring, Pinky
    tips = [4, 8, 12, 16, 20]

    # Thumb: Special case (compare with palm landmark)
    if hand_landmarks.landmark[tips[0]].x > hand_landmarks.landmark[tips[0] - 2].x:
        fingers[0] = 1  # Thumb is up

    # Other fingers (compare fingertip y-coordinates with lower joint)
    for i in range(1, 5):
        if hand_landmarks.landmark[tips[i]].y < hand_landmarks.landmark[tips[i] - 2].y - 0.02:  # Small margin
            fingers[i] = 1

    print("Detected Fingers:", fingers)  # Debugging output
    return fingers


mp_hands = mp.solutions.hands
hands = mp_hands.Hands(min_detection_confidence=0.7, min_tracking_confidence=0.7)
mp_draw = mp.solutions.drawing_utils
cap = cv2.VideoCapture(0)

while cap.isOpened():
    ret, frame = cap.read()
    if not ret:
        break

    frame = cv2.flip(frame, 1)
    rgb_frame = cv2.cvtColor(frame, cv2.COLOR_BGR2RGB)
    result = hands.process(rgb_frame)

    text = "No Match"  # Default text if no match is found
    fingers_count = 0

    if result.multi_hand_landmarks:
        for hand_landmarks in result.multi_hand_landmarks:
            fingers_up = count_fingers(hand_landmarks)
            fingers_count = sum(fingers_up)

            # Define words based on finger positions
            words_map = {
                (0, 1, 0, 0, 0): "I",
                (0, 1, 1, 0, 0): "I LOVE",
                (0, 1, 1, 1, 0): "I LOVE YOU",
                (0, 0, 0, 0, 1): "I",
                (0, 0, 0, 1, 1): "I LOVE",
                (0, 0, 1, 1, 1): "I LOVE YOU",
                (0, 1, 1, 1, 1): "I LOVE YOU SO",
                (1, 1, 1, 1, 1): "I LOVE YOU SO MUCH",
                (0, 0, 1, 0, 0): "FUCK YOU"
            }

            text = words_map.get(tuple(fingers_up), "No Match")  # Fallback text

            # Display number of fingers and text
            cv2.putText(frame, f"Fingers: {fingers_count}", (50, 80), cv2.FONT_HERSHEY_SIMPLEX, 1, (0, 0, 0), 3)
            cv2.putText(frame, f"Word: {text}", (50, 130), cv2.FONT_HERSHEY_SIMPLEX, 1, (0, 0, 0), 3)

            # Draw hand landmarks
            mp_draw.draw_landmarks(frame, hand_landmarks, mp_hands.HAND_CONNECTIONS)

    cv2.imshow("Hand Cam", frame)

    if cv2.waitKey(1) & 0xFF == ord('q'):
        break

cap.release()
cv2.destroyAllWindows()
