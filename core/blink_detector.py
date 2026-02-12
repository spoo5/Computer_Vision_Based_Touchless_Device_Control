import time
import numpy as np
import pyautogui


class BlinkDetector:
    def __init__(self,
                 eye_closed_threshold=0.20,
                 blink_duration_threshold=1.0):

        # MediaPipe FaceMesh left eye landmarks
        self.LEFT_EYE = [33, 160, 158, 133, 153, 144]

        self.EYE_CLOSED_THRESHOLD = eye_closed_threshold
        self.BLINK_DURATION_THRESHOLD = blink_duration_threshold

        self.left_eye_closed_start = None
        self.left_eye_clicked = False

    # -----------------------------------------------------
    # Calculate Eye Aspect Ratio (EAR)
    # -----------------------------------------------------
    def _calculate_EAR(self, landmarks, w, h):
        points = []

        for idx in self.LEFT_EYE:
            x = int(landmarks[idx].x * w)
            y = int(landmarks[idx].y * h)
            points.append((x, y))

        # Vertical distances
        A = np.linalg.norm(np.array(points[1]) - np.array(points[5]))
        B = np.linalg.norm(np.array(points[2]) - np.array(points[4]))

        # Horizontal distance
        C = np.linalg.norm(np.array(points[0]) - np.array(points[3]))

        ear = (A + B) / (2.0 * C)
        return ear

    # -----------------------------------------------------
    # Process blink detection
    # -----------------------------------------------------
    def process(self, landmarks, w, h):
        ear = self._calculate_EAR(landmarks, w, h)

        current_time = time.time()

        # Eye is closed
        if ear < self.EYE_CLOSED_THRESHOLD:

            if self.left_eye_closed_start is None:
                self.left_eye_closed_start = current_time

            else:
                duration = current_time - self.left_eye_closed_start

                if (duration >= self.BLINK_DURATION_THRESHOLD
                        and not self.left_eye_clicked):

                    pyautogui.click()
                    print("Left eye long blink detected → CLICK")

                    self.left_eye_clicked = True

        # Eye is open again → reset
        else:
            self.left_eye_closed_start = None
            self.left_eye_clicked = False
