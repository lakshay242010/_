import cv2
import numpy as np
import mediapipe as mp
import time
import os
import pickle
from collections import deque
from sklearn.ensemble import RandomForestClassifier

class TemporalFatigueDetector:
    def __init__(self, window_size_sec=3.0, target_fps=15, ml_model_path="dynamic_fatigue_model.pkl"):
        self.fps = target_fps
        self.window_len = int(window_size_sec * target_fps)
        
        # Temporal Sliding Windows
        self.ear_history = deque(maxlen=self.window_len)
        self.mar_history = deque(maxlen=self.window_len)
        self.yaw_history = deque(maxlen=self.window_len)
        self.pitch_history = deque(maxlen=self.window_len)
        
        # Thresholds
        self.EAR_THRESHOLD = 0.21
        self.MAR_THRESHOLD = 0.65
        self.PROLONGED_CLOSURE_FRAMES = int(1.5 * target_fps)  # > 1.5 seconds
        self.DISTRACTION_YAW_THRESH = 22.0                    # degrees
        self.DISTRACTION_PITCH_THRESH = 18.0                  # degrees
        
        # Counters and Timers
        self.consecutive_closed_frames = 0
        self.blink_count = 0
        self.yawn_count = 0
        self.distraction_count = 0
        self.eye_state_history = deque(maxlen=5)  # for debouncing blink counts
        
        # MediaPipe Face Mesh Initialization
        self.mp_face_mesh = mp.solutions.face_mesh
        self.face_mesh = self.mp_face_mesh.FaceMesh(
            max_num_faces=1,
            refine_landmarks=True,
            min_detection_confidence=0.5,
            min_tracking_confidence=0.5
        )
        
        # Landmark Indices (MediaPipe)
        self.LEFT_EYE = [362, 385, 387, 263, 373, 380]
        self.RIGHT_EYE = [33, 160, 158, 133, 153, 144]
        self.INNER_MOUTH = [78, 81, 13, 312, 308, 402, 14, 178]
        
        # 3D Model Points for Head Pose Estimation (Generic Human Face Model)
        self.model_3d = np.array([
            (0.0, 0.0, 0.0),             # Nose tip
            (0.0, -330.0, -65.0),        # Chin
            (-225.0, 170.0, -135.0),     # Left eye corner
            (225.0, 170.0, -135.0),      # Right eye corner
            (-150.0, -150.0, -125.0),    # Left Mouth corner
            (150.0, -150.0, -125.0)      # Right mouth corner
        ], dtype=np.float64)
        
        # Machine Learning Model Loading / Training
        self.ml_model_path = ml_model_path
        self.ml_classifier = self._load_or_train_ml_model()

    def _load_or_train_ml_model(self):
        if os.path.exists(self.ml_model_path):
            with open(self.ml_model_path, 'rb') as f:
                return pickle.load(f)
        else:
            # Train a synthetic Random Forest Classifier to fuse temporal features
            np.random.seed(42)
            X_alert = np.random.normal(loc=[0.30, 0.35, 3.0, 2.0], scale=[0.03, 0.05, 2.0, 2.0], size=(500, 4))
            X_drowsy = np.random.normal(loc=[0.16, 0.75, 12.0, 10.0], scale=[0.04, 0.10, 5.0, 4.0], size=(500, 4))
            X = np.vstack((X_alert, X_drowsy))
            y = np.array([0]*500 + [1]*500)  # 0: Alert, 1: Drowsy/Fatigued
            
            clf = RandomForestClassifier(n_estimators=50, random_state=42)
            clf.fit(X, y)
            with open(self.ml_model_path, 'wb') as f:
                pickle.dump(clf, f)
            return clf

    def _euclidean_distance(self, pt1, pt2):
        return np.linalg.norm(pt1 - pt2)

    def calculate_ear(self, landmarks, eye_indices, img_w, img_h):
        pts = np.array([(landmarks[idx].x * img_w, landmarks[idx].y * img_h) for idx in eye_indices])
        v1 = self._euclidean_distance(pts[1], pts[5])
        v2 = self._euclidean_distance(pts[2], pts[4])
        horiz = self._euclidean_distance(pts[0], pts[3])
        if horiz == 0:
            return 0.3
        ear = (v1 + v2) / (2.0 * horiz)
        return ear

    def calculate_mar(self, landmarks, mouth_indices, img_w, img_h):
        pts = np.array([(landmarks[idx].x * img_w, landmarks[idx].y * img_h) for idx in mouth_indices])
        v1 = self._euclidean_distance(pts[1], pts[7])
        v2 = self._euclidean_distance(pts[2], pts[6])
        v3 = self._euclidean_distance(pts[3], pts[5])
        horiz = self._euclidean_distance(pts[0], pts[4])
        if horiz == 0:
            return 0.0
        mar = (v1 + v2 + v3) / (2.0 * horiz)
        return mar

    def estimate_head_pose(self, landmarks, img_w, img_h):
        pose_indices = [1, 152, 33, 263, 61, 291]
        image_points = np.array([
            (landmarks[idx].x * img_w, landmarks[idx].y * img_h) for idx in pose_indices
        ], dtype=np.float64)

        focal_length = img_w
        center = (img_w / 2, img_h / 2)
        camera_matrix = np.array([
            [focal_length, 0, center[0]],
            [0, focal_length, center[1]],
            [0, 0, 1]
        ], dtype=np.float64)

        dist_coeffs = np.zeros((4, 1))
        success, rot_vec, trans_vec = cv2.solvePnP(
            self.model_3d, image_points, camera_matrix, dist_coeffs, flags=cv2.SOLVEPNP_ITERATIVE
        )

        if not success:
            return 0.0, 0.0

        rmat, _ = cv2.Rodrigues(rot_vec)
        angles, _, _, _, _, _ = cv2.RQDecomp3x3(rmat)
        pitch, yaw, roll = angles[0], angles[1], angles[2]
        return yaw, pitch

    def process_frame(self, frame):
        img_h, img_w, _ = frame.shape
        rgb_frame = cv2.cvtColor(frame, cv2.COLOR_BGR2RGB)
        results = self.face_mesh.process(rgb_frame)

        status_flags = {
            "prolonged_closure": False,
            "yawn_detected": False,
            "distraction_detected": False,
            "ml_drowsy_risk": False
        }

        ear, mar, yaw, pitch = 0.35, 0.1, 0.0, 0.0

        if results.multi_face_landmarks:
            landmarks = results.multi_face_landmarks[0].landmark

            left_ear = self.calculate_ear(landmarks, self.LEFT_EYE, img_w, img_h)
            right_ear = self.calculate_ear(landmarks, self.RIGHT_EYE, img_w, img_h)
            ear = (left_ear + right_ear) / 2.0
            mar = self.calculate_mar(landmarks, self.INNER_MOUTH, img_w, img_h)
            yaw, pitch = self.estimate_head_pose(landmarks, img_w, img_h)

            # Update Sliding Windows
            self.ear_history.append(ear)
            self.mar_history.append(mar)
            self.yaw_history.append(abs(yaw))
            self.pitch_history.append(abs(pitch))

            # 1. Temporal Prolonged Eye Closure Check
            if ear < self.EAR_THRESHOLD:
                self.consecutive_closed_frames += 1
                self.eye_state_history.append(1)
            else:
                self.consecutive_closed_frames = 0
                self.eye_state_history.append(0)

            # Blink Detection via Debounced Edge Logic
            if len(self.eye_state_history) >= 3 and list(self.eye_state_history)[-3:] == [1, 1, 0]:
                self.blink_count += 1

            if self.consecutive_closed_frames >= self.PROLONGED_CLOSURE_FRAMES:
                status_flags["prolonged_closure"] = True

            # 2. Yawn Detection
            if mar > self.MAR_THRESHOLD:
                status_flags["yawn_detected"] = True

            # 3. Persistent Head Pose Distraction
            if abs(yaw) > self.DISTRACTION_YAW_THRESH or abs(pitch) > self.DISTRACTION_PITCH_THRESH:
                status_flags["distraction_detected"] = True

            # 4. Data Science / ML Multi-Feature Fusion Inference
            mean_ear = float(np.mean(self.ear_history)) if self.ear_history else ear
            mean_mar = float(np.mean(self.mar_history)) if self.mar_history else mar
            mean_yaw = float(np.mean(self.yaw_history)) if self.yaw_history else 0.0
            mean_pitch = float(np.mean(self.pitch_history)) if self.pitch_history else 0.0

            ml_features = np.array([[mean_ear, mean_mar, mean_yaw, mean_pitch]])
            ml_pred = self.ml_classifier.predict(ml_features)[0]
            if ml_pred == 1:
                status_flags["ml_drowsy_risk"] = True

            # Draw Facial Mesh Annotations
            for idx in self.LEFT_EYE + self.RIGHT_EYE:
                x, y = int(landmarks[idx].x * img_w), int(landmarks[idx].y * img_h)
                cv2.circle(frame, (x, y), 1, (0, 255, 0), -1)

            for idx in self.INNER_MOUTH:
                x, y = int(landmarks[idx].x * img_w), int(landmarks[idx].y * img_h)
                cv2.circle(frame, (x, y), 1, (255, 255, 0), -1)

        metrics = {
            "ear": ear,
            "mar": mar,
            "yaw": yaw,
            "pitch": pitch,
            "blinks": self.blink_count,
            "flags": status_flags
        }

        return frame, metrics
