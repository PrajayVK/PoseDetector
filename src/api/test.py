import cv2
import mediapipe as mp
import numpy as np
import pandas as pd
import joblib

# Load the trained RandomForest model
model = joblib.load("P:/PoseDetector/my-vue-app/src/api/new_model_withhip.h5")

# Define a dictionary to convert model output to human-readable labels
label_dict = {0: "Correct", 1: "Too High", 2: "Too Low"}

# Initialize mediapipe pose class
mp_pose = mp.solutions.pose
pose = mp_pose.Pose(static_image_mode=False, min_detection_confidence=0.5)

# Initialize the video capture object
cap = cv2.VideoCapture(0)  # 0 is typically the built-in webcam

frame_count = 0
frame_skip = 9  # this will process every 10th frame

try:
    while cap.isOpened():
        success, image = cap.read()
        if not success:
            print("Ignoring empty camera frame.")
            continue  # skip empty frames

        # Skip frames to process every 10th frame

        frame_count += 1
        if frame_count % (frame_skip + 1) != 0:
            continue

        # Convert the BGR image to RGB
        image = cv2.cvtColor(image, cv2.COLOR_BGR2RGB)

        # Perform pose detection
        results = pose.process(image)

        # Draw pose annotations on the image
        mp_drawing = mp.solutions.drawing_utils
        mp_drawing.draw_landmarks(image, results.pose_landmarks, mp_pose.POSE_CONNECTIONS)

        # Calculate the squat angles if pose landmarks are detected
        if results.pose_landmarks:
            # Extract landmarks
            landmarks = results.pose_landmarks.landmark
            try:
                # Calculate knee angle
                knee_hip = np.array([landmarks[mp_pose.PoseLandmark.LEFT_HIP.value].x,
                                     landmarks[mp_pose.PoseLandmark.LEFT_HIP.value].y])
                knee_knee = np.array([landmarks[mp_pose.PoseLandmark.LEFT_KNEE.value].x,
                                      landmarks[mp_pose.PoseLandmark.LEFT_KNEE.value].y])
                knee_ankle = np.array([landmarks[mp_pose.PoseLandmark.LEFT_ANKLE.value].x,
                                       landmarks[mp_pose.PoseLandmark.LEFT_ANKLE.value].y])
                knee_angle = np.arccos(np.dot((knee_hip - knee_knee), (knee_ankle - knee_knee)) /
                                       (np.linalg.norm(knee_hip - knee_knee) * np.linalg.norm(knee_ankle - knee_knee)))
                knee_angle = np.degrees(knee_angle)

                # Calculate hip angle
                hip_shoulder = np.array([landmarks[mp_pose.PoseLandmark.LEFT_SHOULDER.value].x,
                                         landmarks[mp_pose.PoseLandmark.LEFT_SHOULDER.value].y])
                hip_hip = np.array([landmarks[mp_pose.PoseLandmark.LEFT_HIP.value].x,
                                    landmarks[mp_pose.PoseLandmark.LEFT_HIP.value].y])
                hip_knee = np.array([landmarks[mp_pose.PoseLandmark.LEFT_KNEE.value].x,
                                     landmarks[mp_pose.PoseLandmark.LEFT_KNEE.value].y])
                hip_angle = np.arccos(np.dot((hip_shoulder - hip_hip), (hip_knee - hip_hip)) /
                                      (np.linalg.norm(hip_shoulder - hip_hip) * np.linalg.norm(hip_knee - hip_hip)))
                hip_angle = np.degrees(hip_angle)

                new_data = pd.DataFrame({'Knee Angle': [knee_angle], 'Hip Angle': [hip_angle]})

        # Predict the posture
                prediction = model.predict(new_data)

        # Interpret the model's output for knee and hip labels
                label = label_dict[prediction[0]]  # Interpretation for knee
                  

        # Display the predictions and angles on the frame
                cv2.rectangle(image, (5, 5), (300, 120), (0, 0, 0), -1)  # Smaller background rectangle

                font_scale = 0.7  # Smaller font size
                line_thickness = 2
                vertical_spacing = 25  # Adjust the vertical spacing between lines

                cv2.putText(image, f'Knee Angle: {int(knee_angle)}', (10, 25), cv2.FONT_HERSHEY_SIMPLEX, font_scale, (255, 255, 255), line_thickness, cv2.LINE_AA)
                cv2.putText(image, f'Hip Angle: {int(hip_angle)}', (10, 25 + vertical_spacing), cv2.FONT_HERSHEY_SIMPLEX, font_scale, (255, 255, 255), line_thickness, cv2.LINE_AA)
                cv2.putText(image, f'Label: {label}', (10, 25 + 2 * vertical_spacing), cv2.FONT_HERSHEY_SIMPLEX, font_scale, (255, 255, 255), line_thickness, cv2.LINE_AA)
                

            except Exception as e:
                # Print any exceptions to the terminal
                print(e)
                pass  # If there is any error in the landmark detection, ignore it

        # Convert the RGB image back to BGR
        image = cv2.cvtColor(image, cv2.COLOR_RGB2BGR)

        # Display the resulting frame
        cv2.namedWindow("Squat Posture Evaluation", cv2.WND_PROP_FULLSCREEN)
        cv2.setWindowProperty("Squat Posture Evaluation",cv2.WND_PROP_FULLSCREEN,
               cv2.WINDOW_FULLSCREEN)
        cv2.imshow('Squat Posture Evaluation', image)

        # Press 'q' to break out of the loop
        if cv2.waitKey(5) & 0xFF == ord('q'):
            break
finally:
    # When everything is done, release the capture
    cap.release()
    cv2.destroyAllWindows()
