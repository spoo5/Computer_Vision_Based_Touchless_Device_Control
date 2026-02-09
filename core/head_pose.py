import numpy as np
import math

class HeadPoseEstimator:
    """
    Estimates head orientation (pitch and yaw) using facial landmarks.
    Enhanced version combining Om's structure with Kalash's calculation method.
    """
    
    # Key landmark indices from MediaPipe Face Mesh
    LANDMARKS = {
        "left": 234,      # Left side of face
        "right": 454,     # Right side of face
        "top": 10,        # Top of head
        "bottom": 152,    # Bottom of chin
        "front": 1        # Nose tip
    }
    
    def __init__(self):
        pass
    
    def landmark_to_np(self, landmark, w, h):
        """Convert MediaPipe landmark to numpy array with pixel coordinates."""
        return np.array([landmark.x * w, landmark.y * h, landmark.z * w])
    
    def estimate(self, landmarks, frame_width, frame_height):
        """
        Estimate head pose using Kalash's method with 3D coordinate system.
        
        Args:
            landmarks: MediaPipe face landmarks
            frame_width: Width of the video frame
            frame_height: Height of the video frame
            
        Returns:
            (pitch, yaw): Head orientation angles in degrees
        """
        w, h = frame_width, frame_height
        
        # Extract key facial points in 3D space
        pts = {
            k: self.landmark_to_np(landmarks[i], w, h) 
            for k, i in self.LANDMARKS.items()
        }
        
        left = pts["left"]
        right = pts["right"]
        top = pts["top"]
        bottom = pts["bottom"]
        front = pts["front"]
        
        # Construct head coordinate system
        # Right axis: from left to right side of face
        right_axis = right - left
        right_axis = right_axis / np.linalg.norm(right_axis)
        
        # Up axis: from bottom to top of face
        up_axis = top - bottom
        up_axis = up_axis / np.linalg.norm(up_axis)
        
        # Forward axis: perpendicular to both (cross product)
        forward_axis = np.cross(right_axis, up_axis)
        forward_axis = forward_axis / np.linalg.norm(forward_axis)
        forward_axis = -forward_axis  # Face outward from head
        
        # Calculate center point
        center = (left + right + top + bottom + front) / 5
        
        # Reference forward direction (looking straight ahead)
        reference_forward = np.array([0, 0, -1])
        
        # Calculate YAW (left/right rotation)
        # Project forward vector onto horizontal plane (XZ)
        xz = np.array([forward_axis[0], 0, forward_axis[2]])
        xz_norm = np.linalg.norm(xz)
        if xz_norm > 0:
            xz = xz / xz_norm
        
        yaw = math.degrees(math.acos(np.clip(np.dot(reference_forward, xz), -1, 1)))
        if forward_axis[0] < 0:
            yaw = -yaw
        
        # Calculate PITCH (up/down rotation)
        # Project forward vector onto vertical plane (YZ)
        yz = np.array([0, forward_axis[1], forward_axis[2]])
        yz_norm = np.linalg.norm(yz)
        if yz_norm > 0:
            yz = yz / yz_norm
        
        pitch = math.degrees(math.acos(np.clip(np.dot(reference_forward, yz), -1, 1)))
        if forward_axis[1] > 0:
            pitch = -pitch
        
        return pitch, yaw, forward_axis
