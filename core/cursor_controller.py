import pyautogui
import threading
import time
from collections import deque

class CursorController:
    """
    Controls the system cursor based on head orientation.
    Uses threading for smooth movement and deque for smoothing.
    Based on Kalash's implementation.
    """
    
    def __init__(self, sensitivity_x=20, sensitivity_y=10, filter_length=8):
        """
        Initialize cursor controller.
        
        Args:
            sensitivity_x: Yaw range (degrees) for full screen width
            sensitivity_y: Pitch range (degrees) for full screen height
            filter_length: Number of frames to average for smoothing
        """
        # Get screen dimensions
        self.MONITOR_WIDTH, self.MONITOR_HEIGHT = pyautogui.size()
        self.CENTER_X = self.MONITOR_WIDTH // 2
        self.CENTER_Y = self.MONITOR_HEIGHT // 2
        
        # Control parameters
        self.sensitivity_x = sensitivity_x  # yaw range
        self.sensitivity_y = sensitivity_y  # pitch range
        self.filter_length = filter_length
        
        # Smoothing filters
        self.ray_directions = deque(maxlen=filter_length)
        
        # Calibration offsets
        self.calibration_offset_yaw = 0
        self.calibration_offset_pitch = 0
        
        # Mouse control state
        self.mouse_control_enabled = False
        self.mouse_target = [self.CENTER_X, self.CENTER_Y]
        self.mouse_lock = threading.Lock()
        
        # Start mouse movement thread
        self.running = True
        self.mouse_thread = threading.Thread(target=self._mouse_mover, daemon=True)
        self.mouse_thread.start()
    
    def _mouse_mover(self):
        """Background thread that smoothly moves the mouse to target position."""
        while self.running:
            if self.mouse_control_enabled:
                with self.mouse_lock:
                    x, y = self.mouse_target
                try:
                    pyautogui.moveTo(x, y)
                except:
                    pass  # Handle pyautogui errors gracefully
            time.sleep(0.01)  # 100Hz update rate
    
    def update(self, pitch, yaw, forward_axis):
        """
        Update cursor position based on head orientation.
        
        Args:
            pitch: Pitch angle in degrees
            yaw: Yaw angle in degrees
            forward_axis: Forward direction vector (for smoothing)
        """
        if not self.mouse_control_enabled:
            return
        
        # Add to smoothing filter
        self.ray_directions.append(forward_axis)
        
        # Apply calibration
        calibrated_yaw = yaw + self.calibration_offset_yaw
        calibrated_pitch = pitch + self.calibration_offset_pitch
        
        # Normalize angles to 0-360 range
        calibrated_yaw = calibrated_yaw % 360
        calibrated_pitch = calibrated_pitch % 360
        
        # Dead zone for center position
        if abs(calibrated_yaw - 180) < 2:
            calibrated_yaw = 180
        if abs(calibrated_pitch - 180) < 3:
            calibrated_pitch = 180
        
        # Map angles to screen coordinates
        # Yaw: 180 is center, (180-range) is left, (180+range) is right
        screen_x = int(
            ((calibrated_yaw - (180 - self.sensitivity_x)) / (2 * self.sensitivity_x)) 
            * self.MONITOR_WIDTH
        )
        
        # Pitch: 180 is center, (180+range) is up, (180-range) is down
        screen_y = int(
            ((180 + self.sensitivity_y - calibrated_pitch) / (2 * self.sensitivity_y)) 
            * self.MONITOR_HEIGHT
        )
        
        # Clamp to screen boundaries (with small margin)
        screen_x = max(10, min(self.MONITOR_WIDTH - 10, screen_x))
        screen_y = max(10, min(self.MONITOR_HEIGHT - 10, screen_y))
        
        # Update target position
        with self.mouse_lock:
            self.mouse_target[:] = [screen_x, screen_y]
    
    def calibrate(self, raw_yaw, raw_pitch):
        """
        Calibrate the system to treat current head position as center.
        
        Args:
            raw_yaw: Current yaw angle
            raw_pitch: Current pitch angle
        """
        self.calibration_offset_yaw = 180 - raw_yaw
        self.calibration_offset_pitch = 180 - raw_pitch
        print("[Cursor Controller] Calibrated to current position")
    
    def toggle(self):
        """Toggle cursor control on/off."""
        self.mouse_control_enabled = not self.mouse_control_enabled
        status = "ENABLED" if self.mouse_control_enabled else "DISABLED"
        print(f"[Cursor Controller] Mouse control {status}")
        return self.mouse_control_enabled
    
    def enable(self):
        """Enable cursor control."""
        self.mouse_control_enabled = True
        print("[Cursor Controller] Mouse control ENABLED")
    
    def disable(self):
        """Disable cursor control."""
        self.mouse_control_enabled = False
        print("[Cursor Controller] Mouse control DISABLED")
    
    def get_position(self):
        """Get current target cursor position."""
        with self.mouse_lock:
            return self.mouse_target[0], self.mouse_target[1]
    
    def is_enabled(self):
        """Check if cursor control is enabled."""
        return self.mouse_control_enabled
    
    def cleanup(self):
        """Stop the mouse movement thread."""
        self.running = False
        if self.mouse_thread.is_alive():
            self.mouse_thread.join(timeout=1.0)
