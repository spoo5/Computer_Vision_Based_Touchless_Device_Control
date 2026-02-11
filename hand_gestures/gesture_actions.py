import pyautogui
import math
import time


class GestureActions:
    def __init__(self):
        """
        Controls system actions using hand gestures
        """
        self.last_action_time = 0
        self.action_delay = 0.4  # seconds (prevents repeated triggers)

    def _can_perform_action(self):
        """
        Prevents gesture spamming
        """
        current_time = time.time()
        if current_time - self.last_action_time > self.action_delay:
            self.last_action_time = current_time
            return True
        return False

    def _distance(self, p1, p2):
        """
        Euclidean distance between two landmarks
        """
        return math.hypot(p1.x - p2.x, p1.y - p2.y)

    def perform_actions(self, hand_landmarks):
        """
        Main gesture-action mapping logic
        """
        landmarks = hand_landmarks.landmark

        # Important landmarks
        thumb_tip = landmarks[4]
        index_tip = landmarks[8]
        middle_tip = landmarks[12]

        # ---------------- ZOOM (PINCH) ----------------
        pinch_distance = self._distance(thumb_tip, index_tip)

        if pinch_distance < 0.03 and self._can_perform_action():
            pyautogui.hotkey("ctrl", "+")   # Zoom in

        elif pinch_distance > 0.08 and self._can_perform_action():
            pyautogui.hotkey("ctrl", "-")   # Zoom out

        # ---------------- SCROLL ----------------
        if index_tip.y < middle_tip.y and self._can_perform_action():
            pyautogui.scroll(50)            # Scroll up

        elif index_tip.y > middle_tip.y and self._can_perform_action():
            pyautogui.scroll(-50)           # Scroll down

        # ---------------- VOLUME ----------------
        if thumb_tip.y < index_tip.y and self._can_perform_action():
            pyautogui.press("volumeup")

        elif thumb_tip.y > index_tip.y and self._can_perform_action():
            pyautogui.press("volumedown")
