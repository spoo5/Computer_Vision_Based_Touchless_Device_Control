import cv2
import mediapipe as mp


class HandDetector:
    def __init__(
        self,
        max_hands=1,
        detection_confidence=0.7,
        tracking_confidence=0.7
    ):
        """
        Initializes MediaPipe Hand Detector
        """
        self.mp_hands = mp.solutions.hands
        self.hands = self.mp_hands.Hands(
            static_image_mode=False,
            max_num_hands=max_hands,
            min_detection_confidence=detection_confidence,
            min_tracking_confidence=tracking_confidence
        )
        self.drawer = mp.solutions.drawing_utils

    def detect_hands(self, frame):
        """
        Detect hands in a frame and return result
        """
        rgb_frame = cv2.cvtColor(frame, cv2.COLOR_BGR2RGB)
        result = self.hands.process(rgb_frame)
        return result

    def draw_landmarks(self, frame, hand_landmarks):
        """
        Draw hand landmarks on frame
        """
        self.drawer.draw_landmarks(
            frame,
            hand_landmarks,
            self.mp_hands.HAND_CONNECTIONS
        )
