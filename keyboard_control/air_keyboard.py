import cv2
import math
import time
import pyautogui


class AirKeyboard:
    def __init__(self):
        self.enabled = False
        self.last_action_time = 0
        self.action_delay = 0.4
        self.smooth_angle = 0
        self.selected_char = ""

        self.LETTERS = " ABCDEFGHIJKLMNOPQRSTUVWXYZ"
        self.SYMBOLS = "1234567890.,!?;:@#&+-/*="
        self.DIAL_SMOOTHING = 0.2
        self.PINCH_T = 0.06

    def toggle(self):
        self.enabled = not self.enabled
        print(f"[Keyboard] {'Enabled' if self.enabled else 'Disabled'}")

    def _can_act(self):
        return time.time() - self.last_action_time > self.action_delay

    def _dist(self, p1, p2):
        return math.hypot(p1.x - p2.x, p1.y - p2.y)

    def is_fist(self, lms):
        tips = [8, 12, 16, 20]
        return all(self._dist(lms[t], lms[0]) < 0.18 for t in tips)

    def process(self, right_hand, left_hand, frame):
        """
        right_hand, left_hand: hand_landmarks or None
        frame: OpenCV frame (for UI drawing)
        """
        if not self.enabled:
            return

        h, w = frame.shape[:2]

        # -------- RIGHT HAND: DIAL SELECTION --------
        if right_hand:
            current_set = self.SYMBOLS if self.is_fist(right_hand) else self.LETTERS

            raw_rad = math.atan2(
                right_hand[0].y - right_hand[9].y,
                right_hand[0].x - right_hand[9].x
            )
            deg = math.degrees(raw_rad) - 90
            deg = max(-90, min(0, deg))

            self.smooth_angle = (
                self.DIAL_SMOOTHING * deg +
                (1 - self.DIAL_SMOOTHING) * self.smooth_angle
            )

            idx = int((abs(self.smooth_angle) / 90) * (len(current_set) - 1))
            self.selected_char = current_set[idx]

            # ---- UI DRAW ----
            center = (w - 60, h - 60)
            cv2.ellipse(frame, center, (320, 320), 0, 180, 270, (40, 40, 40), 30)

            for i, ch in enumerate(current_set):
                angle = 180 + (i / (len(current_set)-1) * 90)
                x = int(center[0] + 360 * math.cos(math.radians(angle)))
                y = int(center[1] + 360 * math.sin(math.radians(angle)))

                if ch == self.selected_char:
                    cv2.circle(frame, (x, y), 24, (0, 255, 0), -1)
                    cv2.putText(frame, ch, (x-10, y+10), 1, 2, (255,255,255), 3)
                else:
                    cv2.putText(frame, ch, (x-5, y+5), 1, 0.7, (200,200,200), 1)

        # -------- LEFT HAND: ACTIONS --------
        if left_hand and self._can_act():
            if self._dist(left_hand[4], left_hand[8]) < self.PINCH_T:
                pyautogui.write(self.selected_char)
                self.last_action_time = time.time()

            elif self._dist(left_hand[4], left_hand[12]) < self.PINCH_T:
                pyautogui.press("space")
                self.last_action_time = time.time()

            elif self._dist(left_hand[4], left_hand[20]) < self.PINCH_T:
                pyautogui.press("backspace")
                self.last_action_time = time.time()
