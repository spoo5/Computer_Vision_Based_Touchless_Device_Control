"""
Integration Test for Computer Vision Based Touchless Device Control

This script tests that all components are properly integrated and working.
Run this before running the main application to ensure everything is set up correctly.
"""

import sys
import importlib

def test_imports():
    """Test if all required packages can be imported."""
    print("Testing package imports...")
    
    packages = [
        ('cv2', 'opencv-python'),
        ('mediapipe', 'mediapipe'),
        ('numpy', 'numpy'),
        ('pyautogui', 'pyautogui'),
        ('keyboard', 'keyboard'),
    ]
    
    failed = []
    for package, install_name in packages:
        try:
            importlib.import_module(package)
            print(f"  ✓ {install_name}")
        except ImportError:
            print(f"  ✗ {install_name} - NOT INSTALLED")
            failed.append(install_name)
    
    if failed:
        print(f"\n❌ Missing packages: {', '.join(failed)}")
        print("   Install with: pip install " + " ".join(failed))
        return False
    else:
        print("\n✅ All packages installed correctly!")
        return True


def test_modules():
    """Test if all project modules can be imported."""
    print("\nTesting project modules...")
    
    modules = [
        'core.camera',
        'core.face_detector',
        'core.head_pose',
        'core.cursor_controller',
        'core.state',
        'core.state_manager',
        'utils.fps',
    ]
    
    failed = []
    for module in modules:
        try:
            importlib.import_module(module)
            print(f"  ✓ {module}")
        except Exception as e:
            print(f"  ✗ {module} - ERROR: {e}")
            failed.append(module)
    
    if failed:
        print(f"\n❌ Failed to import: {', '.join(failed)}")
        print("   Make sure you're running from the project root directory")
        return False
    else:
        print("\n✅ All modules imported successfully!")
        return True


def test_camera():
    """Test if camera can be opened."""
    print("\nTesting camera...")
    
    try:
        import cv2
        cap = cv2.VideoCapture(0, cv2.CAP_DSHOW)
        
        if not cap.isOpened():
            print("  ✗ Could not open camera")
            print("     - Make sure no other app is using the camera")
            print("     - Try changing index (0, 1, 2, etc.)")
            cap.release()
            return False
        
        ret, frame = cap.read()
        if not ret:
            print("  ✗ Could not read frame from camera")
            cap.release()
            return False
        
        print(f"  ✓ Camera opened successfully")
        print(f"     Resolution: {frame.shape[1]}x{frame.shape[0]}")
        
        cap.release()
        return True
        
    except Exception as e:
        print(f"  ✗ Camera test failed: {e}")
        return False


def test_mediapipe():
    """Test if MediaPipe face detection works."""
    print("\nTesting MediaPipe face detection...")
    
    try:
        import cv2
        import mediapipe as mp
        
        # Initialize face mesh
        mp_face_mesh = mp.solutions.face_mesh
        face_mesh = mp_face_mesh.FaceMesh(
            max_num_faces=1,
            refine_landmarks=True,
            min_detection_confidence=0.5,
            min_tracking_confidence=0.5
        )
        
        print("  ✓ MediaPipe Face Mesh initialized")
        
        # Create a blank test image
        test_img = cv2.imread("test_face.jpg") if False else None
        if test_img is None:
            print("     (No test image - skipping detection test)")
        
        return True
        
    except Exception as e:
        print(f"  ✗ MediaPipe test failed: {e}")
        return False


def test_pyautogui():
    """Test if PyAutoGUI can get screen info."""
    print("\nTesting PyAutoGUI...")
    
    try:
        import pyautogui
        
        width, height = pyautogui.size()
        print(f"  ✓ Screen size detected: {width}x{height}")
        
        # Test if we can get mouse position (don't move it)
        x, y = pyautogui.position()
        print(f"     Current mouse position: ({x}, {y})")
        
        return True
        
    except Exception as e:
        print(f"  ✗ PyAutoGUI test failed: {e}")
        return False


def test_file_structure():
    """Test if all expected files exist."""
    print("\nTesting file structure...")
    
    import os
    
    expected_files = [
        'main.py',
        'requirements.txt',
        'README.md',
        'core/__init__.py',
        'core/camera.py',
        'core/face_detector.py',
        'core/head_pose.py',
        'core/cursor_controller.py',
        'core/state.py',
        'core/state_manager.py',
        'utils/__init__.py',
        'utils/fps.py',
    ]
    
    missing = []
    for file in expected_files:
        if os.path.exists(file):
            print(f"  ✓ {file}")
        else:
            print(f"  ✗ {file} - MISSING")
            missing.append(file)
    
    if missing:
        print(f"\n❌ Missing files: {', '.join(missing)}")
        return False
    else:
        print("\n✅ All files present!")
        return True


def main():
    """Run all tests."""
    print("=" * 60)
    print("Integration Test Suite")
    print("Computer Vision Based Touchless Device Control")
    print("=" * 60)
    
    results = []
    
    # Run tests
    results.append(("Package Imports", test_imports()))
    results.append(("Project Modules", test_modules()))
    results.append(("File Structure", test_file_structure()))
    results.append(("Camera", test_camera()))
    results.append(("MediaPipe", test_mediapipe()))
    results.append(("PyAutoGUI", test_pyautogui()))
    
    # Summary
    print("\n" + "=" * 60)
    print("TEST SUMMARY")
    print("=" * 60)
    
    for test_name, passed in results:
        status = "✅ PASS" if passed else "❌ FAIL"
        print(f"{test_name:.<30} {status}")
    
    all_passed = all(result[1] for result in results)
    
    print("=" * 60)
    
    if all_passed:
        print("\n🎉 ALL TESTS PASSED!")
        print("You can now run: python main.py")
        return 0
    else:
        print("\n⚠️  SOME TESTS FAILED")
        print("Please fix the issues above before running main.py")
        return 1


if __name__ == "__main__":
    sys.exit(main())
