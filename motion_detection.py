"""
Efficient Real-Time Emotion Detection using MediaPipe + Scikit-learn

Author: zuhair
Purpose: Educational / Assignment
-----------------------------------------------------------
Features:
- Uses MediaPipe Face Mesh for fast, accurate facial landmark detection.
- Extracts real numeric features (eye aspect ratio, mouth ratio, smile width).
- Trains a lightweight supervised model (RandomForestClassifier).
- Runs in real-time using OpenCV with high FPS and optimized frame handling.
-----------------------------------------------------------
"""

import cv2
import numpy as np
import mediapipe as mp
from sklearn.ensemble import RandomForestClassifier
from sklearn.model_selection import train_test_split
from sklearn.metrics import accuracy_score
import joblib
import time

# -------------------------------------------------------------
# 1️⃣ MediaPipe initialization
# -------------------------------------------------------------
mp_face_mesh = mp.solutions.face_mesh
face_mesh = mp_face_mesh.FaceMesh(static_image_mode=False, max_num_faces=1, min_detection_confidence=0.6)

# -------------------------------------------------------------
# 2️⃣ Feature Extraction Helpers
# -------------------------------------------------------------
def euclidean_distance(p1, p2):
    return np.linalg.norm(np.array(p1) - np.array(p2))

def extract_face_features(landmarks, img_w, img_h):
    """Extract numeric features from facial landmarks."""
    # Eye landmarks (left/right)
    left_eye_top = landmarks[159]
    left_eye_bottom = landmarks[145]
    right_eye_top = landmarks[386]
    right_eye_bottom = landmarks[374]
    
    # Mouth landmarks
    mouth_left = landmarks[61]
    mouth_right = landmarks[291]
    mouth_top = landmarks[13]
    mouth_bottom = landmarks[14]
    
    # Convert to pixel coordinates
    def to_pixel(landmark):
        return (int(landmark.x * img_w), int(landmark.y * img_h))

    lt, lb = to_pixel(left_eye_top), to_pixel(left_eye_bottom)
    rt, rb = to_pixel(right_eye_top), to_pixel(right_eye_bottom)
    ml, mr = to_pixel(mouth_left), to_pixel(mouth_right)
    mt, mb = to_pixel(mouth_top), to_pixel(mouth_bottom)

    # Eye aspect ratio (proxy for openness)
    left_eye_h = euclidean_distance(lt, lb)
    right_eye_h = euclidean_distance(rt, rb)
    eye_openness = (left_eye_h + right_eye_h) / 2.0

    # Mouth aspect ratio (proxy for smile)
    mouth_width = euclidean_distance(ml, mr)
    mouth_height = euclidean_distance(mt, mb)
    smile_ratio = mouth_height / (mouth_width + 1e-6)

    # Normalized features
    return [eye_openness / img_h, smile_ratio * 10]  # scale smile ratio

# -------------------------------------------------------------
# 3️⃣ Simulated training (happy, sad, neutral)
# -------------------------------------------------------------
def simulate_training_data(n=300):
    X, y = [], []
    for _ in range(n):
        label = np.random.choice(['happy', 'sad', 'neutral'], p=[0.4, 0.3, 0.3])
        if label == 'happy':
            eye = np.random.uniform(0.25, 0.4)
            smile = np.random.uniform(0.25, 0.45)
        elif label == 'sad':
            eye = np.random.uniform(0.15, 0.25)
            smile = np.random.uniform(0.02, 0.12)
        else:
            eye = np.random.uniform(0.18, 0.32)
            smile = np.random.uniform(0.10, 0.20)
        X.append([eye, smile])
        y.append(label)
    return np.array(X), np.array(y)

X, y = simulate_training_data(500)
X_train, X_test, y_train, y_test = train_test_split(X, y, test_size=0.2, random_state=42)
model = RandomForestClassifier(n_estimators=100, random_state=42)
model.fit(X_train, y_train)
acc = accuracy_score(y_test, model.predict(X_test))
print(f"✅ Model trained — Accuracy: {acc*100:.2f}%")

joblib.dump(model, "emotion_rf_model.pkl")

# -------------------------------------------------------------
# 4️⃣ Real-time Emotion Detection
# -------------------------------------------------------------
cap = cv2.VideoCapture(0)
if not cap.isOpened():
    raise Exception("Webcam not detected!")

print("🎥 Starting real-time emotion detection... Press 'q' to quit.")
p_time = 0

while True:
    success, frame = cap.read()
    if not success:
        break

    img_h, img_w = frame.shape[:2]
    rgb_frame = cv2.cvtColor(frame, cv2.COLOR_BGR2RGB)
    results = face_mesh.process(rgb_frame)

    if results.multi_face_landmarks:
        for face_landmarks in results.multi_face_landmarks:
            landmarks = face_landmarks.landmark
            features = extract_face_features(landmarks, img_w, img_h)
            pred = model.predict([features])[0]

            # Display label
            cv2.putText(frame, f"Emotion: {pred}", (30, 50),
                        cv2.FONT_HERSHEY_SIMPLEX, 1.0, (0, 255, 0), 2)

    # FPS display
    c_time = time.time()
    fps = 1 / (c_time - p_time)
    p_time = c_time
    cv2.putText(frame, f"FPS: {int(fps)}", (30, 90), cv2.FONT_HERSHEY_SIMPLEX, 0.8, (255, 255, 255), 2)

    cv2.imshow("Real-Time Emotion Detection (Efficient)", frame)

    if cv2.waitKey(1) & 0xFF == ord('q'):
        break

cap.release()
cv2.destroyAllWindows()
