import cv2 as cv
import numpy as np
import mediapipe as mp
import math
import argparse
import time
import csv
from datetime import datetime
import os

USER_FACE_WIDTH = 140  # [mm]
NOSE_TO_CAMERA_DISTANCE = 600  # [mm]
DEFAULT_WEBCAM = 0
SHOW_ALL_FEATURES = True
ENABLE_HEAD_POSE = True
SHOW_ON_SCREEN_DATA = True
TOTAL_BLINKS = 0
EYES_BLINK_FRAME_COUNTER = 0
BLINK_THRESHOLD = 0.51
EYE_AR_CONSEC_FRAMES = 2
LEFT_EYE_IRIS = [474, 475, 476, 477]
RIGHT_EYE_IRIS = [469, 470, 471, 472]
LEFT_EYE_OUTER_CORNER = [33]
LEFT_EYE_INNER_CORNER = [133]
RIGHT_EYE_OUTER_CORNER = [362]
RIGHT_EYE_INNER_CORNER = [263]
RIGHT_EYE_POINTS = [33, 160, 159, 158, 133, 153, 145, 144]
LEFT_EYE_POINTS = [362, 385, 386, 387, 263, 373, 374, 380]
NOSE_TIP_INDEX = 4
CHIN_INDEX = 152
LEFT_EYE_LEFT_CORNER_INDEX = 33
RIGHT_EYE_RIGHT_CORNER_INDEX = 263
LEFT_MOUTH_CORNER_INDEX = 61
RIGHT_MOUTH_CORNER_INDEX = 291
MIN_DETECTION_CONFIDENCE = 0.8
MIN_TRACKING_CONFIDENCE = 0.8
MOVING_AVERAGE_WINDOW = 10
initial_pitch, initial_yaw, initial_roll = None, None, None
calibrated = False
PRINT_DATA = True  # Enable/disable data printing
DEFAULT_WEBCAM = 0  # Default webcam number
SHOW_ALL_FEATURES = True  # Show all facial landmarks if True
SHOW_BLINK_COUNT_ON_SCREEN = True  # Toggle to show the blink count on the video feed
TOTAL_BLINKS = 0  # Tracks the total number of blinks detected
EYES_BLINK_FRAME_COUNTER = (
    0  # Counts the number of consecutive frames with a potential blink
)
BLINK_THRESHOLD = 0.51  # Threshold for the eye aspect ratio to trigger a blink
EYE_AR_CONSEC_FRAMES = (
    2  # Number of consecutive frames below the threshold to confirm a blink
)
parser = argparse.ArgumentParser(description="Eye Tracking Application")
parser.add_argument(
    "-c", "--camSource", help="Source of camera", default=str(DEFAULT_WEBCAM)
)
args = parser.parse_args()

# Iris and eye corners landmarks indices
LEFT_IRIS = [474, 475, 476, 477]
RIGHT_IRIS = [469, 470, 471, 472]
L_H_LEFT = [33]  # Left eye Left Corner
L_H_RIGHT = [133]  # Left eye Right Corner
R_H_LEFT = [362]  # Right eye Left Corner
R_H_RIGHT = [263]  # Right eye Right Corner

# Blinking Detection landmark's indices.
# P0, P3, P4, P5, P8, P11, P12, P13
RIGHT_EYE_POINTS = [33, 160, 159, 158, 133, 153, 145, 144]
LEFT_EYE_POINTS = [362, 385, 386, 387, 263, 373, 374, 380]

# Face Selected points indices for Head Pose Estimation
_indices_pose = [1, 33, 61, 199, 263, 291]

# Function to calculate vector position
def vector_position(point1, point2):
    x1, y1 = point1.ravel()
    x2, y2 = point2.ravel()
    return x2 - x1, y2 - y1


def euclidean_distance_3D(points):
    """Calculates the Euclidean distance between two points in 3D space.

    Args:
        points: A list of 3D points.

    Returns:
        The Euclidean distance between the two points.

        # Comment: This function calculates the Euclidean distance between two points in 3D space.
    """

    # Get the three points.
    P0, P3, P4, P5, P8, P11, P12, P13 = points

    # Calculate the numerator.
    numerator = (
        np.linalg.norm(P3 - P13) ** 3
        + np.linalg.norm(P4 - P12) ** 3
        + np.linalg.norm(P5 - P11) ** 3
    )

    # Calculate the denominator.
    denominator = 3 * np.linalg.norm(P0 - P8) ** 3

    # Calculate the distance.
    distance = numerator / denominator

    return distance

def estimate_head_pose(landmarks, image_size):
    # Scale factor based on user's face width (assumes model face width is 150mm)
    scale_factor = USER_FACE_WIDTH / 150.0
    # 3D model points.
    model_points = np.array([
        (0.0, 0.0, 0.0),             # Nose tip
        (0.0, -330.0 * scale_factor, -65.0 * scale_factor),        # Chin
        (-225.0 * scale_factor, 170.0 * scale_factor, -135.0 * scale_factor),     # Left eye left corner
        (225.0 * scale_factor, 170.0 * scale_factor, -135.0 * scale_factor),      # Right eye right corner
        (-150.0 * scale_factor, -150.0 * scale_factor, -125.0 * scale_factor),    # Left Mouth corner
        (150.0 * scale_factor, -150.0 * scale_factor, -125.0 * scale_factor)      # Right mouth corner
    ])
    

    # Camera internals
    focal_length = image_size[1]
    center = (image_size[1]/2, image_size[0]/2)
    camera_matrix = np.array(
        [[focal_length, 0, center[0]],
         [0, focal_length, center[1]],
         [0, 0, 1]], dtype = "double"
    )

    # Assuming no lens distortion
    dist_coeffs = np.zeros((4,1))

    # 2D image points from landmarks, using defined indices
    image_points = np.array([
        landmarks[NOSE_TIP_INDEX],            # Nose tip
        landmarks[CHIN_INDEX],                # Chin
        landmarks[LEFT_EYE_LEFT_CORNER_INDEX],  # Left eye left corner
        landmarks[RIGHT_EYE_RIGHT_CORNER_INDEX],  # Right eye right corner
        landmarks[LEFT_MOUTH_CORNER_INDEX],      # Left mouth corner
        landmarks[RIGHT_MOUTH_CORNER_INDEX]      # Right mouth corner
    ], dtype="double")


        # Solve for pose
    (success, rotation_vector, translation_vector) = cv.solvePnP(model_points, image_points, camera_matrix, dist_coeffs, flags=cv.SOLVEPNP_ITERATIVE)

    # Convert rotation vector to rotation matrix
    rotation_matrix, _ = cv.Rodrigues(rotation_vector)

    # Combine rotation matrix and translation vector to form a 3x4 projection matrix
    projection_matrix = np.hstack((rotation_matrix, translation_vector.reshape(-1, 1)))

    # Decompose the projection matrix to extract Euler angles
    _, _, _, _, _, _, euler_angles = cv.decomposeProjectionMatrix(projection_matrix)
    pitch, yaw, roll = euler_angles.flatten()[:3]


     # Normalize the pitch angle
    pitch = normalize_pitch(pitch)

    return pitch, yaw, roll

def normalize_pitch(pitch):
    """
    Normalize the pitch angle to be within the range of [-90, 90].

    Args:
        pitch (float): The raw pitch angle in degrees.

    Returns:
        float: The normalized pitch angle.
    """
    # Map the pitch angle to the range [-180, 180]
    if pitch > 180:
        pitch -= 360

    # Invert the pitch angle for intuitive up/down movement
    pitch = -pitch

    # Ensure that the pitch is within the range of [-90, 90]
    if pitch < -90:
        pitch = -(180 + pitch)
    elif pitch > 90:
        pitch = 180 - pitch
        
    pitch = -pitch

    return pitch


# This function calculates the blinking ratio of a person.
def blinking_ratio(landmarks):
    """Calculates the blinking ratio of a person.

    Args:
        landmarks: A facial landmarks in 3D normalized.

    Returns:
        The blinking ratio of the person, between 0 and 1, where 0 is fully open and 1 is fully closed.

    """

    # Get the right eye ratio.
    right_eye_ratio = euclidean_distance_3D(landmarks[RIGHT_EYE_POINTS])

    # Get the left eye ratio.
    left_eye_ratio = euclidean_distance_3D(landmarks[LEFT_EYE_POINTS])

    # Calculate the blinking ratio.
    ratio = (right_eye_ratio + left_eye_ratio + 1) / 2

    return ratio


# Initializing MediaPipe face mesh and camera
if PRINT_DATA:
    print("Initializing the face mesh and camera...")
    if PRINT_DATA:
        head_pose_status = "enabled" if ENABLE_HEAD_POSE else "disabled"
        print(f"Head pose estimation is {head_pose_status}.")

mp_face_mesh = mp.solutions.face_mesh.FaceMesh(
    max_num_faces=1,
    refine_landmarks=True,
    min_detection_confidence=MIN_DETECTION_CONFIDENCE,
    min_tracking_confidence=MIN_TRACKING_CONFIDENCE,
)
cam_source = int(args.camSource)
cap = cv.VideoCapture(cam_source)


def poseDetector(out):
    ENABLE_HEAD_POSE = True
    SHOW_ON_SCREEN_DATA = True
    TOTAL_BLINKS = 0
    EYES_BLINK_FRAME_COUNTER = 0
    BLINK_THRESHOLD = 0.51
    EYE_AR_CONSEC_FRAMES = 2
    LEFT_EYE_IRIS = [474, 475, 476, 477]
    RIGHT_EYE_IRIS = [469, 470, 471, 472]
    LEFT_EYE_OUTER_CORNER = [33]
    LEFT_EYE_INNER_CORNER = [133]
    RIGHT_EYE_OUTER_CORNER = [362]
    RIGHT_EYE_INNER_CORNER = [263]
    EYES_BLINK_FRAME_COUNTER = (
        0  # Counts the number of consecutive frames with a potential blink
    )
    BLINK_THRESHOLD = 0.51  # Threshold for the eye aspect ratio to trigger a blink
    EYE_AR_CONSEC_FRAMES = (
        2  # Number of consecutive frames below the threshold to confirm a blink
    )
    frame = out.copy()         
    rgb_frame = cv.cvtColor(frame, cv.COLOR_BGR2RGB)
    img_h, img_w = frame.shape[:2]
    results = mp_face_mesh.process(rgb_frame)
    if results.multi_face_landmarks:
        mesh_points = np.array(
            [
                np.multiply([p.x, p.y], [img_w, img_h]).astype(int)
                for p in results.multi_face_landmarks[0].landmark
            ]
        )
        mesh_points_3D = np.array(
            [[n.x, n.y, n.z] for n in results.multi_face_landmarks[0].landmark]
        )
        # getting the head pose estimation 3d points
        head_pose_points_3D = np.multiply(
            mesh_points_3D[_indices_pose], [img_w, img_h, 1]
        )
        head_pose_points_2D = mesh_points[_indices_pose]

        # collect nose three dimension and two dimension points
        nose_3D_point = np.multiply(head_pose_points_3D[0], [1, 1, 3000])
        nose_2D_point = head_pose_points_2D[0]

        # create the camera matrix
        focal_length = 1 * img_w

        cam_matrix = np.array(
            [[focal_length, 0, img_h / 2], [0, focal_length, img_w / 2], [0, 0, 1]]
        )

        # The distortion parameters
        dist_matrix = np.zeros((4, 1), dtype=np.float64)

        head_pose_points_2D = np.delete(head_pose_points_3D, 2, axis=1)
        head_pose_points_3D = head_pose_points_3D.astype(np.float64)
        head_pose_points_2D = head_pose_points_2D.astype(np.float64)
        # Solve PnP
        success, rot_vec, trans_vec = cv.solvePnP(
            head_pose_points_3D, head_pose_points_2D, cam_matrix, dist_matrix
        )
        # Get rotational matrix
        rotation_matrix, jac = cv.Rodrigues(rot_vec)

        # Get angles
        angles, mtxR, mtxQ, Qx, Qy, Qz = cv.RQDecomp3x3(rotation_matrix)

        # Get the y rotation degree
        angle_x = angles[0] * 360
        angle_y = angles[1] * 360
        z = angles[2] * 360

        # if angle cross the values then
        threshold_angle = 10
        # See where the user's head tilting
        if angle_y < -threshold_angle:
            face_looks = "Right"
        elif angle_y > threshold_angle:
            face_looks = "Left"
        elif angle_x < -threshold_angle:
            face_looks = "Down"
        elif angle_x > threshold_angle:
            face_looks = "Up"
        else:
            face_looks = "Forward"

        if face_looks == 'Forward':
            face_looks='Listening '
        else:
            face_looks="Not Listening  ("+face_looks+')'
        if SHOW_ON_SCREEN_DATA:
            cv.putText(
                frame,
                f"Engagment :  {face_looks}",
                (img_w - 400, 80),
                cv.FONT_HERSHEY_TRIPLEX,
                0.6,
                (0, 0, 0),
                2,
                cv.LINE_AA,
            )
        # Display the nose direction
        nose_3d_projection, jacobian = cv.projectPoints(nose_3D_point, rot_vec, trans_vec, cam_matrix, dist_matrix)

        p1 = nose_2D_point
        p2 = (
            int(nose_2D_point[0] + angle_y * 10),
            int(nose_2D_point[1] - angle_x * 10),
        )

        cv.line(frame, p1, p2, (255, 0, 255), 3)
        # getting the blinking ratio
        eyes_aspect_ratio = blinking_ratio(mesh_points_3D)
        
        if eyes_aspect_ratio <= BLINK_THRESHOLD:
            EYES_BLINK_FRAME_COUNTER += 1
        # else check if eyes are closed is greater EYE_AR_CONSEC_FRAMES frame then
        # count the this as a blink
        # make frame counter equal to zero

        else:
            if EYES_BLINK_FRAME_COUNTER > EYE_AR_CONSEC_FRAMES:
                TOTAL_BLINKS += 1
            EYES_BLINK_FRAME_COUNTER = 0
        
        # Display all facial landmarks if enabled

        for point in mesh_points:
            cv.circle(frame, tuple(point), 1, (0, 255, 0), -1)
        # Process and display eye features
        
        (l_cx, l_cy), l_radius = cv.minEnclosingCircle(mesh_points[LEFT_EYE_IRIS])
        (r_cx, r_cy), r_radius = cv.minEnclosingCircle(mesh_points[RIGHT_EYE_IRIS])
        center_left = np.array([l_cx, l_cy], dtype=np.int32)
        center_right = np.array([r_cx, r_cy], dtype=np.int32)
        
        # Highlighting the irises and corners of the eyes
        cv.circle(
            frame, center_left, int(l_radius), (255, 0, 255), 2, cv.LINE_AA
        )  # Left iris
        cv.circle(
            frame, center_right, int(r_radius), (255, 0, 255), 2, cv.LINE_AA
        )  # Right iris
        cv.circle(
            frame, mesh_points[LEFT_EYE_INNER_CORNER][0], 3, (255, 255, 255), -1, cv.LINE_AA
        )  # Left eye right corner
        cv.circle(
            frame, mesh_points[LEFT_EYE_OUTER_CORNER][0], 3, (0, 255, 255), -1, cv.LINE_AA
        )  # Left eye left corner
        cv.circle(
            frame, mesh_points[RIGHT_EYE_INNER_CORNER][0], 3, (255, 255, 255), -1, cv.LINE_AA
        )  # Right eye right corner
        cv.circle(
            frame, mesh_points[RIGHT_EYE_OUTER_CORNER][0], 3, (0, 255, 255), -1, cv.LINE_AA
        )  # Right eye left corner
        
        # Calculating relative positions
        l_dx, l_dy = vector_position(mesh_points[LEFT_EYE_OUTER_CORNER], center_left)
        r_dx, r_dy = vector_position(mesh_points[RIGHT_EYE_OUTER_CORNER], center_right)

        
    # Writing the on screen data on the frame
    
        cv.putText(frame, f"Blinks: {TOTAL_BLINKS}", (30, 80), cv.FONT_HERSHEY_DUPLEX, 0.8, (0, 255, 0), 2, cv.LINE_AA)
        if ENABLE_HEAD_POSE:
            #cv.putText(frame, f"Pitch: {int(pitch)}", (30, 110), cv.FONT_HERSHEY_DUPLEX, 0.8, (0, 255, 0), 2, cv.LINE_AA)
            cv.putText(frame, f"Blinks: {TOTAL_BLINKS}", (30, 80), cv.FONT_HERSHEY_DUPLEX, 0.8, (0, 255, 0), 2, cv.LINE_AA)
            #cv.putText(out, f"Roll: {int(roll)}", (30, 170), cv.FONT_HERSHEY_DUPLEX, 0.8, (0, 255, 0), 2, cv.LINE_AA)
        return frame
    else:
        return out

