"""
Computer Vision Based Touchless Device Control
Integrated System - Main Application

Team Members:
- Shreyas: Virtual keyboard typing
- Om: System architecture and framework
- Kalash: Cursor movement implementation
- Your name: Hand gestures + Integration

"""

import cv2
import keyboard
import time
from core.camera import Camera
from core.face_detector import FaceDetector
from core.head_pose import HeadPoseEstimator
from core.cursor_controller import CursorController
from core.state_manager import StateManager
from utils.fps import FPSCounter


def main():
    print("=" * 60)
    print("Computer Vision Based Touchless Device Control")
    print("=" * 60)
    print("\nInitializing system...")
    
    # Initialize components
    try:
        camera = Camera(index=0, width=640, height=480)
        print("✓ Camera initialized")
    except RuntimeError as e:
        print(f"✗ Camera error: {e}")
        return
    
    face_detector = FaceDetector()
    print("✓ Face detector initialized")
    
    head_pose = HeadPoseEstimator()
    print("✓ Head pose estimator initialized")
    
    cursor_controller = CursorController(
        sensitivity_x=20,  # Yaw range (degrees)
        sensitivity_y=10,  # Pitch range (degrees)
        filter_length=8    # Smoothing filter size
    )
    print("✓ Cursor controller initialized")
    
    state_manager = StateManager(pause_timeout=0.5)
    print("✓ State manager initialized")
    
    fps_counter = FPSCounter()
    print("✓ FPS counter initialized")
    
    print("\n" + "=" * 60)
    print("CONTROLS:")
    print("  t        - Toggle cursor control ON/OFF")
    print("  C         - Calibrate (set current position as center)")
    print("  ESC       - Exit application")
    print("=" * 60)
    print("\nStarting main loop...\n")
    
    # For storing raw angles (used for calibration)
    raw_yaw = 0
    raw_pitch = 0
    
    # Main loop
    try:
        while True:
            # Read frame from camera
            frame = camera.read()
            if frame is None:
                print("Failed to read frame")
                break
            
            # Flip frame horizontally for mirror effect
            frame = cv2.flip(frame, 1)
            h, w = frame.shape[:2]
            
            # Detect face landmarks
            result = face_detector.process(frame)
            
            # Check if face is detected
            face_detected = result.multi_face_landmarks is not None
            state_manager.update_face_presence(face_detected)
            
            # Process head pose if face is detected
            if face_detected:
                landmarks = result.multi_face_landmarks[0].landmark
                
                # Estimate head orientation
                pitch, yaw, forward_axis = head_pose.estimate(landmarks, w, h)
                raw_pitch = pitch
                raw_yaw = yaw
                
                # Update cursor if state is active
                if state_manager.is_active():
                    cursor_controller.update(pitch, yaw, forward_axis)
                
                # Optional: Draw face mesh for debugging
                # face_detector.draw(frame, result)
            
            # Get current FPS
            current_fps = fps_counter.tick()
            
            # Draw UI overlays
            _draw_ui(frame, state_manager, cursor_controller, current_fps, face_detected)
            
            # Display frame
            cv2.imshow("Touchless Device Control", frame)
            
            # Handle keyboard input
            key = cv2.waitKey(1) & 0xFF
            
            # ESC to exit
            if key == 27:
                print("\nExiting...")
                break
            
            # 'C' to calibrate
            elif key == ord('c') or key == ord('C'):
                cursor_controller.calibrate(raw_yaw, raw_pitch)
            
            # t to toggle (using keyboard library for F7)
            if keyboard.is_pressed('t'):
                was_enabled = cursor_controller.toggle()
                # Sync state manager with cursor controller
                if was_enabled:
                    state_manager.state = state_manager.state.ON
                else:
                    state_manager.state = state_manager.state.OFF
                time.sleep(0.3)  # Debounce
    
    except KeyboardInterrupt:
        print("\nInterrupted by user")
    
    finally:
        # Cleanup
        print("\nCleaning up...")
        cursor_controller.cleanup()
        camera.release()
        cv2.destroyAllWindows()
        print("Done!")


def _draw_ui(frame, state_manager, cursor_controller, fps, face_detected):
    """Draw UI overlays on the frame."""
    h, w = frame.shape[:2]
    
    # Draw FPS
    cv2.putText(
        frame,
        f"FPS: {fps}",
        (10, 30),
        cv2.FONT_HERSHEY_SIMPLEX,
        0.7,
        (0, 255, 0),
        2
    )
    
    # Draw face detection status
    face_color = (0, 255, 0) if face_detected else (0, 0, 255)
    face_text = "Face: DETECTED" if face_detected else "Face: NOT FOUND"
    cv2.putText(
        frame,
        face_text,
        (10, 60),
        cv2.FONT_HERSHEY_SIMPLEX,
        0.7,
        face_color,
        2
    )
    
    # Draw system state
    state = state_manager.get_state()
    state_colors = {
        state.OFF: (128, 128, 128),      # Gray
        state.ON: (0, 255, 0),           # Green
        state.FROZEN: (255, 165, 0),     # Orange
        state.PAUSED: (0, 0, 255)        # Red
    }
    
    state_text = f"State: {state.name}"
    state_color = state_colors.get(state, (255, 255, 255))
    cv2.putText(
        frame,
        state_text,
        (10, 90),
        cv2.FONT_HERSHEY_SIMPLEX,
        0.7,
        state_color,
        2
    )
    
    # Draw cursor status
    if cursor_controller.is_enabled():
        cursor_x, cursor_y = cursor_controller.get_position()
        cursor_text = f"Cursor: ({cursor_x}, {cursor_y})"
        cv2.putText(
            frame,
            cursor_text,
            (10, 120),
            cv2.FONT_HERSHEY_SIMPLEX,
            0.7,
            (0, 255, 0),
            2
        )
    
    # Draw help text at bottom
    help_text = "t: Toggle | C: Calibrate | ESC: Exit"
    text_size = cv2.getTextSize(help_text, cv2.FONT_HERSHEY_SIMPLEX, 0.5, 1)[0]
    text_x = (w - text_size[0]) // 2
    cv2.putText(
        frame,
        help_text,
        (text_x, h - 20),
        cv2.FONT_HERSHEY_SIMPLEX,
        0.5,
        (255, 255, 255),
        1
    )


if __name__ == "__main__":
    main()
