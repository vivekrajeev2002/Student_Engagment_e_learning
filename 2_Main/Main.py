import sys
import cv2
from PyQt5.QtWidgets import QApplication, QWidget, QVBoxLayout, QLabel, QHBoxLayout
from PyQt5.QtCore import QTimer, Qt
from PyQt5.QtGui import QImage, QPixmap
from fer import FER
from headpose import poseDetector
import dlib
from scipy.spatial import distance
import face_recognition
import cv2
import pickle

with open("registered_face_encoding.pkl", "rb") as f:
    registered_face_encoding = pickle.load(f)

def face(out):
    frame=out.copy()
    rgb_frame = cv2.cvtColor(frame, cv2.COLOR_BGR2RGB)

    # Find all face locations and encodings in the current frame
    face_locations = face_recognition.face_locations(rgb_frame)
    face_encodings = face_recognition.face_encodings(rgb_frame, face_locations)

    # Loop through all detected faces
    for (top, right, bottom, left), face_encoding in zip(face_locations, face_encodings):
        # Compare the current face encoding with the registered face encoding
        matches = face_recognition.compare_faces([registered_face_encoding], face_encoding)

        if True in matches:
            # If the face matches, label it as recognized
            cv2.rectangle(frame, (left, top), (right, bottom), (0, 255, 0), 2)
            cv2.putText(frame, "Vivek Rajeev V", (left, top - 10), cv2.FONT_HERSHEY_SIMPLEX, 0.9, (0, 255, 0), 2)
        else:
            # If the face doesn't match, label it as unknown
            cv2.rectangle(frame, (left, top), (right, bottom), (0, 0, 255), 2)
            cv2.putText(frame, "Unknown", (left, top - 10), cv2.FONT_HERSHEY_SIMPLEX, 0.9, (0, 0, 255), 2)
    return frame

def face(out):
    frame=out.copy()
    rgb_frame = cv2.cvtColor(frame, cv2.COLOR_BGR2RGB)

    # Find all face locations and encodings in the current frame
    face_locations = face_recognition.face_locations(rgb_frame)
    face_encodings = face_recognition.face_encodings(rgb_frame, face_locations)

    # Loop through all detected faces
    for (top, right, bottom, left), face_encoding in zip(face_locations, face_encodings):
        # Compare the current face encoding with the registered face encoding
        matches = face_recognition.compare_faces([registered_face_encoding], face_encoding)

        if True in matches:
            # If the face matches, label it as recognized
            cv2.rectangle(frame, (left, top), (right, bottom), (0, 255, 0), 2)
            cv2.putText(frame, "Vivek Rajeev V", (left, top - 10), cv2.FONT_HERSHEY_SIMPLEX, 0.9, (0, 255, 0), 2)
        else:
            # If the face doesn't match, label it as unknown
            cv2.rectangle(frame, (left, top), (right, bottom), (0, 0, 255), 2)
            cv2.putText(frame, "Unknown", (left, top - 10), cv2.FONT_HERSHEY_SIMPLEX, 0.9, (0, 0, 255), 2)
    return frame

EAR_THRESHOLD = 0.25
CONSECUTIVE_FRAMES = 3
detector = dlib.get_frontal_face_detector()
predictor = dlib.shape_predictor("shape_predictor_68_face_landmarks.dat")
LEFT_EYE_LANDMARKS = range(36, 42)
RIGHT_EYE_LANDMARKS = range(42, 48)
def calculate_EAR(eye):
    A = distance.euclidean(eye[1], eye[5])
    B = distance.euclidean(eye[2], eye[4])
    C = distance.euclidean(eye[0], eye[3])
    ear = (A + B) / (2.0 * C)
    return ear
frame_counter=0
def eyestatus(out,frame_counter):   
    frame=out.copy()
    gray = cv2.cvtColor(frame, cv2.COLOR_BGR2GRAY)
    faces = detector(gray)
    for face in faces:
        landmarks = predictor(gray, face)
        left_eye = [(landmarks.part(i).x, landmarks.part(i).y) for i in LEFT_EYE_LANDMARKS]
        right_eye = [(landmarks.part(i).x, landmarks.part(i).y) for i in RIGHT_EYE_LANDMARKS]
        left_ear = calculate_EAR(left_eye)
        right_ear = calculate_EAR(right_eye)
        ear = (left_ear + right_ear) / 2.0
        if ear < EAR_THRESHOLD:
            frame_counter += 1
            if frame_counter >= CONSECUTIVE_FRAMES:
                cv2.putText(frame, "EYES CLOSED", (50, 50), cv2.FONT_HERSHEY_SIMPLEX, 1, (0, 0, 255), 2)
        else:
            frame_counter = 0
            cv2.putText(frame, "EYES OPEN", (50, 50), cv2.FONT_HERSHEY_SIMPLEX, 1, (0, 0, 0), 2)
        for (x, y) in left_eye + right_eye:
            cv2.circle(frame, (x, y), 2, (255, 0, 0), -1)
    return frame


emotion_detector = FER()
def emotioninvoke(fr):
    frame=fr.copy()
    emotions = emotion_detector.detect_emotions(frame)
    if(len(emotions)==0):
        return frame
    # Loop through detected faces and their emotions
    for emotion_data in emotions:
        box = emotion_data["box"]  # Bounding box for the face
        emotions = emotion_data["emotions"]  # Dictionary of emotions

        # Get the most likely emotion
        top_emotion = max(emotions, key=emotions.get)

        # Draw the bounding box
        x, y, w, h = box
        cv2.rectangle(frame, (x, y), (x + w, y + h), (0, 255, 255), 2)
        
        # Display the top emotion
        label = f"{top_emotion}: {emotions[top_emotion]:.2f}"
        cv2.putText(frame, label, (x, y - 10), cv2.FONT_HERSHEY_SIMPLEX, 0.6, (0, 255, 0), 2)
        return frame


class VideoWindow(QWidget):
    def __init__(self):
        super().__init__()

        self.setWindowTitle("OpenCV Output with Filters")
        self.setGeometry(100, 100, 1000, 600)

        # Layout to hold four labels in a row
        self.layout = QHBoxLayout()
        
        self.labels = [QLabel() for _ in range(4)]
        for label in self.labels:
            self.layout.addWidget(label)

        self.setLayout(self.layout)

        # OpenCV capture (video feed)
        self.capture = cv2.VideoCapture(0)
        
        # Timer to periodically update the feed
        self.timer = QTimer(self)
        self.timer.timeout.connect(self.update_video_stream)
        self.timer.start(100)

    
    def update_video_stream(self):
        ret, frame = self.capture.read()
        if ret:
            # Apply the filters
            original=emotioninvoke(frame)
            pose = poseDetector(frame)
            eyestat=eyestatus(frame,frame_counter)
            fac=face(frame)
            # Convert each filtered frame to RGB and display in corresponding label
            filtered_frames = [original,pose,eyestat,fac]
            for i, label in enumerate(self.labels):
                rgb_frame = cv2.cvtColor(filtered_frames[i], cv2.COLOR_BGR2RGB)      
                h, w, _ = rgb_frame.shape
                bytes_per_line = 3 * w
                qt_img = QImage(rgb_frame.data, w, h, bytes_per_line, QImage.Format_RGB888)
                pixmap = QPixmap.fromImage(qt_img)
                label.setPixmap(pixmap.scaled(340, 180, Qt.KeepAspectRatio))

    def closeEvent(self, event):
        self.capture.release()

if __name__ == '__main__':
    app = QApplication(sys.argv)
    
    window = VideoWindow()
    window.show()
    
    sys.exit(app.exec_())
