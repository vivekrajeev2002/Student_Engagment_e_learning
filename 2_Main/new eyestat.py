import cv2
import dlib
from scipy.spatial import distance as dist

def eye_aspect_ratio(eye):
    # Compute the Euclidean distances between the two sets of vertical eye landmarks
    A = dist.euclidean(eye[1], eye[5])
    B = dist.euclidean(eye[2], eye[4])

    # Compute the Euclidean distance between the horizontal eye landmarks
    C = dist.euclidean(eye[0], eye[3])

    # Calculate the eye aspect ratio
    ear = (A + B) / (2.0 * C)
    return ear

# Load pre-trained facial landmarks predictor and detector
detector = dlib.get_frontal_face_detector()
predictor = dlib.shape_predictor("shape_predictor_68_face_landmarks.dat")  # Download from dlib website

# Indices for eyes landmarks in the 68-point model
LEFT_EYE = slice(36, 42)
RIGHT_EYE = slice(42, 48)

# Threshold for EAR to detect closure
EAR_THRESHOLD = 0.25

# Start video capture
cap = cv2.VideoCapture(0)  # Use 0 for the default webcam or provide a video file path

while True:
    ret, frame = cap.read()
    if not ret:
        break

    # Convert the frame to grayscale
    gray = cv2.cvtColor(frame, cv2.COLOR_BGR2GRAY)

    # Detect faces
    faces = detector(gray)

    for face in faces:
        # Detect landmarks
        landmarks = predictor(gray, face)

        # Convert landmarks to a numpy array
        landmarks_points = [(landmarks.part(n).x, landmarks.part(n).y) for n in range(68)]

        # Extract left and right eye points
        left_eye = landmarks_points[LEFT_EYE]
        right_eye = landmarks_points[RIGHT_EYE]

        # Calculate EAR for both eyes
        left_ear = eye_aspect_ratio(left_eye)
        right_ear = eye_aspect_ratio(right_eye)

        # Average the EAR
        avg_ear = (left_ear + right_ear) / 2.0

        # Detect eye closure
        if avg_ear < EAR_THRESHOLD:
            cv2.putText(frame, "Eyes Closed", (30, 30), cv2.FONT_HERSHEY_SIMPLEX, 1, (0, 0, 255), 2)
        else:
            cv2.putText(frame, "Eyes Open", (30, 30), cv2.FONT_HERSHEY_SIMPLEX, 1, (0, 255, 0), 2)

        # Draw eyes on the frame for visualization
        for point in left_eye + right_eye:
            cv2.circle(frame, point, 2, (0, 255, 0), -1)

    # Display the frame
    cv2.imshow("Eye Closure Detection", frame)

    # Break loop with 'q'
    if cv2.waitKey(1) & 0xFF == ord('q'):
        break

# Release the video capture and close windows
cap.release()
cv2.destroyAllWindows()
