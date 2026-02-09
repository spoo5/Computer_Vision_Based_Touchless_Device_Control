import cv2
import mediapipe as mp

class FaceDetector:
    """
    Handles face detection and landmark extraction using MediaPipe.
    Based on Om's implementation.
    """
    def __init__(self):
        self.mp_face_mesh = mp.solutions.face_mesh
        self.face_mesh = self.mp_face_mesh.FaceMesh(
            static_image_mode=False,
            max_num_faces=1,
            refine_landmarks=True,
            min_detection_confidence=0.5,
            min_tracking_confidence=0.5
        )
        self.drawer = mp.solutions.drawing_utils
        self.draw_style = mp.solutions.drawing_styles
    
    def process(self, frame):
        """
        Process a frame and detect face landmarks.
        Returns MediaPipe results object.
        """
        rgb = cv2.cvtColor(frame, cv2.COLOR_BGR2RGB)
        return self.face_mesh.process(rgb)
    
    def draw(self, frame, result):
        """Draw face mesh on the frame (optional visualization)."""
        if not result.multi_face_landmarks:
            return
        
        for face_landmarks in result.multi_face_landmarks:
            self.drawer.draw_landmarks(
                image=frame,
                landmark_list=face_landmarks,
                connections=self.mp_face_mesh.FACEMESH_TESSELATION,
                landmark_drawing_spec=None,
                connection_drawing_spec=self.draw_style.get_default_face_mesh_tesselation_style()
            )
