import cv2
import mediapipe as mp
import numpy as np
import pandas as pd
import pickle
import time

with open('body_language.pkl', 'rb') as f:
    model = pickle.load(f)

mp_drawing = mp.solutions.drawing_utils  # Drawing helpers
mp_holistic = mp.solutions.holistic  # Mediapipe Solutions

cap = cv2.VideoCapture(0)
# Initiate holistic model
with mp_holistic.Holistic(min_detection_confidence=0.5, min_tracking_confidence=0.5) as holistic:
    expected_body_language_order = ['Happy', 'Sad', 'Victory', 'Wakanda Forever']
    detected_body_languages = []
    current_stage = 0
    start_time = None
    timeout_duration = 30  # 30 seconds

    while cap.isOpened():
        ret, frame = cap.read()

        # Recolor Feed
        image = cv2.cvtColor(frame, cv2.COLOR_BGR2RGB)
        image.flags.writeable = False

        # Make Detections
        results = holistic.process(image)
        # print(results.face_landmarks)

        # face_landmarks, pose_landmarks, left_hand_landmarks, right_hand_landmarks

        # Recolor image back to BGR for rendering
        image.flags.writeable = True
        image = cv2.cvtColor(image, cv2.COLOR_RGB2BGR)

        # 1. Draw face landmarks
        mp_drawing.draw_landmarks(image, results.face_landmarks, mp_holistic.FACEMESH_CONTOURS,
                                  mp_drawing.DrawingSpec(color=(80, 110, 10), thickness=1, circle_radius=1),
                                  mp_drawing.DrawingSpec(color=(80, 256, 121), thickness=1, circle_radius=1)
                                  )

        # 2. Right hand
        mp_drawing.draw_landmarks(image, results.right_hand_landmarks, mp_holistic.HAND_CONNECTIONS,
                                  mp_drawing.DrawingSpec(color=(80, 22, 10), thickness=2, circle_radius=4),
                                  mp_drawing.DrawingSpec(color=(80, 44, 121), thickness=2, circle_radius=2)
                                  )

        # 3. Left Hand
        mp_drawing.draw_landmarks(image, results.left_hand_landmarks, mp_holistic.HAND_CONNECTIONS,
                                  mp_drawing.DrawingSpec(color=(121, 22, 76), thickness=2, circle_radius=4),
                                  mp_drawing.DrawingSpec(color=(121, 44, 250), thickness=2, circle_radius=2)
                                  )

        # 4. Pose Detections
        mp_drawing.draw_landmarks(image, results.pose_landmarks, mp_holistic.POSE_CONNECTIONS,
                                  mp_drawing.DrawingSpec(color=(245, 117, 66), thickness=2, circle_radius=4),
                                  mp_drawing.DrawingSpec(color=(245, 66, 230), thickness=2, circle_radius=2)
                                  )
        # Export coordinates
        try:
            # Extract Pose landmarks
            pose = results.pose_landmarks.landmark
            pose_row = list(
                np.array([[landmark.x, landmark.y, landmark.z, landmark.visibility] for landmark in pose]).flatten())

            # Extract Face landmarks
            face = results.face_landmarks.landmark
            face_row = list(
                np.array([[landmark.x, landmark.y, landmark.z, landmark.visibility] for landmark in face]).flatten())

            # Concat rows
            row = pose_row + face_row

            # Make Detections
            X = pd.DataFrame([row])
            body_language_class = model.predict(X)[0]
            body_language_prob = model.predict_proba(X)[0]
            print(body_language_class, body_language_prob)

            if body_language_class == expected_body_language_order[current_stage]:
                detected_body_languages.append(body_language_class)
                current_stage += 1

            # Grab ear coords
            coords = tuple(np.multiply(
                np.array(
                    (results.pose_landmarks.landmark[mp_holistic.PoseLandmark.LEFT_EAR].x,
                     results.pose_landmarks.landmark[mp_holistic.PoseLandmark.LEFT_EAR].y))
                , [640, 480]).astype(int))

            cv2.rectangle(image,
                          (coords[0], coords[1] + 5),
                          (coords[0] + len(body_language_class) * 20, coords[1] - 30),
                          (245, 117, 16), -1)
            cv2.putText(image, body_language_class, coords,
                        cv2.FONT_HERSHEY_SIMPLEX, 1, (255, 255, 255), 2, cv2.LINE_AA)

            # Get status box (left corner)
            cv2.rectangle(image, (0, 0), (250, 60), (245, 117, 16), -1)

            # Display Class
            cv2.putText(image, 'CLASS'
                        , (95, 12), cv2.FONT_HERSHEY_SIMPLEX, 0.5, (0, 0, 0), 1, cv2.LINE_AA)
            cv2.putText(image, body_language_class.split(' ')[0]
                        , (90, 40), cv2.FONT_HERSHEY_SIMPLEX, 1, (255, 255, 255), 2, cv2.LINE_AA)

            # Display Probability
            cv2.putText(image, 'PROB'
                        , (15, 12), cv2.FONT_HERSHEY_SIMPLEX, 0.5, (0, 0, 0), 1, cv2.LINE_AA)
            cv2.putText(image, str(round(body_language_prob[np.argmax(body_language_prob)], 2))
                        , (10, 40), cv2.FONT_HERSHEY_SIMPLEX, 1, (255, 255, 255), 2, cv2.LINE_AA)

            # Get status box (right corner)
            cv2.rectangle(image, (image.shape[1] - 400, 0), (image.shape[1], 60), (245, 117, 16), -1)

            # Display instructions and handle timeouts
            if current_stage < len(expected_body_language_order):
                instruction = f"Show {expected_body_language_order[current_stage]}"
                text_size = cv2.getTextSize(instruction, cv2.FONT_HERSHEY_SIMPLEX, 1, 2)[0]
                text_x = image.shape[1] - 400 + (400 - text_size[0]) // 2
                text_y = 20 + (60 - text_size[1]) // 2
                cv2.putText(image, instruction, (text_x, text_y), cv2.FONT_HERSHEY_SIMPLEX, 0.7, (255, 255, 255), 2,
                            cv2.LINE_AA)

                # Start the timer for the current stage
                if start_time is None:
                    start_time = time.time()

                # Check if the timeout duration has passed
                elapsed_time = time.time() - start_time
                if elapsed_time >= timeout_duration:
                    current_stage += 1
                    start_time = None

            else:
                success_message = "Good job!"
                text_size = cv2.getTextSize(success_message, cv2.FONT_HERSHEY_SIMPLEX, 1, 2)[0]
                text_x = image.shape[1] - 400 + (400 - text_size[0]) // 2
                text_y = 20 + (60 - text_size[1]) // 2
                cv2.putText(image, success_message, (text_x, text_y), cv2.FONT_HERSHEY_SIMPLEX, 0.7, (255, 255, 255), 2,
                            cv2.LINE_AA)

        except:
            # Print the detected body language classes
            print(detected_body_languages)
            detected_languages_text = ", ".join(detected_body_languages)

            # Get status box (left corner)
            cv2.rectangle(image, (0, 0), (1000, 60), (245, 117, 16), -1)

            # Display Class
            cv2.putText(image, 'Good Job!'
                        , (95, 12), cv2.FONT_HERSHEY_SIMPLEX, 0.5, (0, 0, 0), 1, cv2.LINE_AA)
            cv2.putText(image, 'Captured: '
                        , (15, 12), cv2.FONT_HERSHEY_SIMPLEX, 0.5, (0, 0, 0), 1, cv2.LINE_AA)
            cv2.putText(image, detected_languages_text
                        , (10, 40), cv2.FONT_HERSHEY_SIMPLEX, 0.7, (255, 255, 255), 2, cv2.LINE_AA)

        cv2.imshow('Raw Webcam Feed', image)

        if cv2.waitKey(10) & 0xFF == ord('q'):
            break

cap.release()
cv2.destroyAllWindows()