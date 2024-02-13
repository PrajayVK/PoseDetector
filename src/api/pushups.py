# import cv2
# import mediapipe as mp
# import numpy as np
# import os
# import pickle



# def real_time_predict(model, pose):
#     cap = cv2.VideoCapture(0)  # 0 for the default webcam
#     print("Press 'q' to quit")

#     while True:
#         ret, frame = cap.read()
#         if not ret:
#             break

#         image = cv2.cvtColor(frame, cv2.COLOR_BGR2RGB)
#         results = pose.process(image)

#         if results.pose_landmarks:
#             keypoints = np.array([[lmk.x, lmk.y] for lmk in results.pose_landmarks.landmark]).flatten()
#             avg_keypoints = keypoints.reshape(1, -1)
#             prediction = model.predict(avg_keypoints)
#             text = "Correct" if prediction[0] == 1 else "Incorrect"
#             cv2.putText(frame, text, (10, 30), cv2.FONT_HERSHEY_SIMPLEX, 1, (0, 255, 0), 2)

#         cv2.imshow('Pushup Analysis', frame)

#         if cv2.waitKey(1) & 0xFF == ord('q'):
#             break

#     cap.release()
#     cv2.destroyAllWindows()

# # Load the trained model
# with open('src/api/combined_model.pkl', 'rb') as f:
#     loaded_model = pickle.load(f)

# # Initialize MediaPipe Pose
# mp_pose = mp.solutions.pose
# pose = mp_pose.Pose(static_image_mode=False, model_complexity=1, min_detection_confidence=0.5)

# # Example usage for real-time prediction
# real_time_predict(loaded_model, pose)


import cv2
import numpy as np
import mediapipe as mp
import pickle
from tensorflow.keras.applications.mobilenet_v2 import MobileNetV2, preprocess_input
from tensorflow.keras.preprocessing.image import img_to_array

# Initialize MediaPipe Pose and CNN model
mp_pose = mp.solutions.pose
pose = mp_pose.Pose(static_image_mode=False, model_complexity=1, min_detection_confidence=0.5)
cnn_model = MobileNetV2(weights='imagenet', include_top=False)

# Load the trained model
with open('src/api/combined_model.pkl', 'rb') as f:
    combined_model = pickle.load(f)

def process_and_predict(frame, cnn_model, pose_model, combined_model):
    # Extract CNN features
    frame_resized = cv2.resize(frame, (224, 224))
    frame_rgb = cv2.cvtColor(frame_resized, cv2.COLOR_BGR2RGB)
    img_array = img_to_array(frame_rgb)
    img_batch = np.expand_dims(img_array, axis=0)
    img_preprocessed = preprocess_input(img_batch)
    cnn_features = cnn_model.predict(img_preprocessed).flatten()

    # Extract keypoints
    frame_rgb = cv2.cvtColor(frame, cv2.COLOR_BGR2RGB)
    results = pose_model.process(frame_rgb)
    if results.pose_landmarks:
        keypoints = np.array([[lmk.x, lmk.y, lmk.z] for lmk in results.pose_landmarks.landmark]).flatten()
    else:
        keypoints = np.zeros(33 * 3)

    # Combine features and predict
    combined_features = np.concatenate([cnn_features, keypoints])
    prediction = combined_model.predict(combined_features.reshape(1, -1))
    
    return "Correct" if prediction[0] == 1 else "Incorrect"

def real_time_analysis():
    cap = cv2.VideoCapture(0)  # Use 0 for default webcam

    while cap.isOpened():
        ret, frame = cap.read()
        if not ret:
            break

        prediction = process_and_predict(frame, cnn_model, pose, combined_model)
        cv2.putText(frame, prediction, (10, 30), cv2.FONT_HERSHEY_SIMPLEX, 1, (0, 255, 0), 2)
        cv2.imshow('Real-Time Pushup Analysis', frame)

        if cv2.waitKey(10) & 0xFF == ord('q'):
            break

    cap.release()
    cv2.destroyAllWindows()

# Start real-time analysis
real_time_analysis()