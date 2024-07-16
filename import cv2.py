import cv2
import mediapipe as mp

mp_hands = mp.solutions.hands
hands = mp_hands.Hands()
mp_draw = mp.solutions.drawing_utils
cap = cv2.VideoCapture(0)

while cap.isOpened():
    ret, frame = cap.read()
    if not ret:
        break

    # Flip the frame horizontally for a later selfie-view display
    frame = cv2.flip(frame, 1)
    frame_rgb = cv2.cvtColor(frame, cv2.COLOR_BGR2RGB)
    results = hands.process(frame_rgb)
    
    if results.multi_hand_landmarks:
        for hand_landmarks in results.multi_hand_landmarks:
            mp_draw.draw_landmarks(frame, hand_landmarks, mp_hands.HAND_CONNECTIONS)

            # Initialize list to store landmark coordinates
            landmark_list = []
            for id, lm in enumerate(hand_landmarks.landmark):
                # Get the coordinates
                h, w, c = frame.shape
                cx, cy = int(lm.x * w), int(lm.y * h)
                landmark_list.append([cx, cy])

            # Gesture recognition logic
            gesture = None  # Initialize gesture to None
            if len(landmark_list) != 0:
                # Open Hand (Palm) Gesture
                if (landmark_list[4][1] < landmark_list[3][1] and 
                    landmark_list[8][1] < landmark_list[6][1] and
                    landmark_list[12][1] < landmark_list[10][1] and
                    landmark_list[16][1] < landmark_list[14][1] and
                    landmark_list[20][1] < landmark_list[18][1]):
                    gesture = "Sailesh Open Hand"
                # Pointing Up Gesture
                elif (landmark_list[8][1] < landmark_list[6][1] and 
                      landmark_list[4][1] > landmark_list[3][1] and
                      landmark_list[12][1] > landmark_list[10][1] and
                      landmark_list[16][1] > landmark_list[14][1] and
                      landmark_list[20][1] > landmark_list[18][1]):
                    gesture = "Sailesh Pointing Up"
                # Thumbs Up Gesture
                elif (landmark_list[4][1] < landmark_list[3][1] and 
                      landmark_list[4][0] > landmark_list[3][0] and
                      landmark_list[8][1] > landmark_list[6][1] and
                      landmark_list[12][1] > landmark_list[10][1] and
                      landmark_list[16][1] > landmark_list[14][1] and
                      landmark_list[20][1] > landmark_list[18][1]):
                    gesture = "Sailesh Thumbs Up"
                # Victory Sign Gesture
                elif (landmark_list[8][1] < landmark_list[6][1] and 
                      landmark_list[12][1] < landmark_list[10][1] and
                      landmark_list[4][1] > landmark_list[3][1] and
                      landmark_list[16][1] > landmark_list[14][1] and
                      landmark_list[20][1] > landmark_list[18][1]):
                    gesture = "Sailesh Victory"
                # Fist Gesture
                elif (landmark_list[4][1] > landmark_list[3][1] and
                      landmark_list[8][1] > landmark_list[6][1] and
                      landmark_list[12][1] > landmark_list[10][1] and
                      landmark_list[16][1] > landmark_list[14][1] and
                      landmark_list[20][1] > landmark_list[18][1]):
                    gesture = "Sailesh Fist"

            # Display the corresponding text
            if gesture:
                print(f"Gesture detected: {gesture}")  # Debug print
                cv2.putText(frame, gesture, (landmark_list[0][0] - 50, landmark_list[0][1] - 50),
                            cv2.FONT_HERSHEY_SIMPLEX, 1, (0, 255, 0), 2, cv2.LINE_AA)

    # Display the Frame
    cv2.imshow('Hand Gesture Recognition', frame)
    if cv2.waitKey(1) & 0xFF == ord('q'):
        break

cap.release()
cv2.destroyAllWindows()
