import time

class FPSCounter:
    """
    Simple FPS counter for performance monitoring.
    Based on Om's implementation.
    """
    
    def __init__(self):
        self.last_time = time.time()
    
    def tick(self):
        """
        Calculate FPS since last tick.
        
        Returns:
            Current FPS as integer
        """
        now = time.time()
        fps = 1 / (now - self.last_time + 1e-6)  # Avoid division by zero
        self.last_time = now
        return int(fps)
