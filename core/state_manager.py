from core.state import SystemState
import time

class StateManager:
    """
    Manages system state transitions and face detection tracking.
    Enhanced version of Om's implementation.
    """
    
    def __init__(self, pause_timeout=0.5):
        """
        Initialize state manager.
        
        Args:
            pause_timeout: Seconds without face before pausing (default 0.5s)
        """
        self.state = SystemState.OFF
        self.last_face_time = time.time()
        self.pause_timeout = pause_timeout
    
    def update_face_presence(self, face_detected: bool):
        """
        Update state based on face detection.
        
        Args:
            face_detected: True if face is currently detected
        """
        if face_detected:
            self.last_face_time = time.time()
            # If we were paused, go back to OFF state
            if self.state == SystemState.PAUSED:
                self.state = SystemState.OFF
        else:
            # Check if we should pause due to no face
            if time.time() - self.last_face_time > self.pause_timeout:
                if self.state != SystemState.PAUSED:
                    print("[State Manager] Face lost - PAUSED")
                self.state = SystemState.PAUSED
    
    def toggle_mouse(self):
        """Toggle between ON and OFF states."""
        if self.state == SystemState.ON:
            self.state = SystemState.OFF
            print("[State Manager] Mouse control OFF")
        elif self.state == SystemState.OFF:
            self.state = SystemState.ON
            print("[State Manager] Mouse control ON")
    
    def freeze_cursor(self):
        """Freeze the cursor in place."""
        if self.state == SystemState.ON:
            self.state = SystemState.FROZEN
            print("[State Manager] Cursor FROZEN")
    
    def unfreeze_cursor(self):
        """Unfreeze the cursor."""
        if self.state == SystemState.FROZEN:
            self.state = SystemState.ON
            print("[State Manager] Cursor UNFROZEN")
    
    def get_state(self):
        """Get current system state."""
        return self.state
    
    def is_active(self):
        """Check if mouse control should be active."""
        return self.state == SystemState.ON
    
    def is_paused(self):
        """Check if system is paused."""
        return self.state == SystemState.PAUSED
