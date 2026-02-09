import cv2

class Camera:
    """
    Handles webcam initialization and frame capture.
    Based on Om's implementation.
    """
    def __init__(self, index=0, width=640, height=480):
        self.cap = cv2.VideoCapture(index, cv2.CAP_DSHOW)
        if not self.cap.isOpened():
            raise RuntimeError("Could not open webcam")
        
        self.cap.set(cv2.CAP_PROP_FRAME_WIDTH, width)
        self.cap.set(cv2.CAP_PROP_FRAME_HEIGHT, height)
    
    def read(self):
        """Read a frame from the camera."""
        ret, frame = self.cap.read()
        if not ret:
            return None
        return frame
    
    def release(self):
        """Release the camera resource."""
        self.cap.release()
