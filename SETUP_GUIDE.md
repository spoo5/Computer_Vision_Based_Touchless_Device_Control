# Setup and Integration Guide

This guide will help you set up the integrated repository and understand how everything works together.

## Part 1: First-Time Setup

### Step 1: Create Your GitHub Repository

1. Go to GitHub and create a new repository named `Computer_Vision_Based_Touchless_Device_Control`
2. **Do NOT** initialize with README (we already have one)
3. Copy the repository URL

### Step 2: Set Up Local Repository

Open your terminal/command prompt and run:

```bash
# Navigate to where you want the project
cd /path/to/your/projects/folder

# Copy the integrated folder (you'll have this from Claude)
# Then initialize git
cd Computer_Vision_Based_Touchless_Device_Control
git init
git add .
git commit -m "Initial integration: Om's framework + Kalash's cursor control"

# Link to your GitHub repo (replace with your URL)
git remote add origin https://github.com/YOUR_USERNAME/Computer_Vision_Based_Touchless_Device_Control.git
git branch -M main
git push -u origin main
```

### Step 3: Install Dependencies

```bash
# Create virtual environment
python -m venv venv

# Activate it
# Windows:
venv\Scripts\activate
# Mac/Linux:
source venv/bin/activate

# Install packages
pip install -r requirements.txt
```

### Step 4: Test the System

```bash
python main.py
```

If everything works:
- You should see a window with your webcam feed
- Press F7 to enable cursor control
- Move your head to move the cursor
- Press C to calibrate
- Press ESC to exit

## Part 2: Understanding the Integration

### What We Took From Each Person

**From Om's Code:**
- ✅ Clean folder structure (core/, utils/, tests/)
- ✅ Modular components (Camera, FaceDetector classes)
- ✅ State management system
- ✅ FPS counter

**From Kalash's Code:**
- ✅ Actual cursor movement logic (the math!)
- ✅ Smoothing using deques
- ✅ Threading for smooth movement
- ✅ Calibration system
- ✅ PyAutoGUI implementation

**Combined Result:**
- Clean code structure (easy to add new features)
- Working cursor control
- Professional organization
- Easy to understand and modify

### File Mapping

| Integrated File | Source | Changes Made |
|----------------|--------|--------------|
| `core/camera.py` | Om | None (used as-is) |
| `core/face_detector.py` | Om | None (used as-is) |
| `core/head_pose.py` | Kalash's math + Om's structure | Combined both approaches |
| `core/cursor_controller.py` | Kalash | Restructured into class |
| `core/state.py` | Om | None (used as-is) |
| `core/state_manager.py` | Om | Minor enhancements |
| `utils/fps.py` | Om | None (used as-is) |
| `main.py` | New | Integrated both systems |

## Part 3: Next Steps

### When Shreyas Sends Code

1. Create a new branch:
   ```bash
   git checkout -b integrate-virtual-keyboard
   ```

2. Review Shreyas's code structure

3. Integrate following this pattern:
   - If it's a single file: Add to `core/virtual_keyboard.py`
   - If it's multiple files: Create `core/keyboard/` folder
   - Import in `main.py`
   - Add keyboard controls

4. Test thoroughly

5. Commit and merge:
   ```bash
   git add .
   git commit -m "Integrated Shreyas's virtual keyboard"
   git push origin integrate-virtual-keyboard
   # Create pull request on GitHub
   ```

### Adding Your Hand Gesture Features

#### Plan for Hand Gestures:

1. **Create hand detector module**
   ```
   core/hand_detector.py
   ```
   - Use MediaPipe Hands
   - Detect hand landmarks
   - Recognize gesture patterns

2. **Create gesture recognizer**
   ```
   core/gesture_recognizer.py
   ```
   - Define gesture classes (scroll, zoom, volume)
   - Pattern matching logic
   - Threshold values

3. **Create action controllers**
   ```
   core/scroll_controller.py
   core/zoom_controller.py
   core/volume_controller.py
   ```
   - Each handles specific actions
   - Uses appropriate system libraries

4. **Integration steps:**
   - Initialize in main.py
   - Add to main loop
   - Add keyboard shortcuts
   - Update README

#### Suggested Libraries:

```python
# For scrolling
import pyautogui  # Already have this

# For volume control
# Windows:
from ctypes import cast, POINTER
from comtypes import CLSCTX_ALL
from pycaw.pycaw import AudioUtilities, IAudioEndpointVolume

# Mac:
import osascript

# Linux:
import alsaaudio
```

Add to requirements.txt:
```
# For volume control (Windows)
pycaw
comtypes

# For hand tracking
mediapipe  # Already have this
```

## Part 4: Testing Checklist

Before considering integration complete:

- [ ] Camera opens without errors
- [ ] Face detection works in various lighting
- [ ] Cursor moves smoothly when head moves
- [ ] F7 toggles control on/off
- [ ] C calibration works
- [ ] ESC exits cleanly
- [ ] FPS is acceptable (>20 FPS)
- [ ] No crashes during 5-minute run
- [ ] State management works (pause when face lost)
- [ ] Works on all team member's computers

## Part 5: Common Issues and Solutions

### Issue 1: "Could not open webcam"
**Solution:**
- Close other apps using camera
- Try different camera index in Camera(index=0) → Camera(index=1)

### Issue 2: Import errors
**Solution:**
```bash
# Make sure you're in the right directory
cd Computer_Vision_Based_Touchless_Device_Control

# Make sure virtual environment is activated
# You should see (venv) in your terminal

# Reinstall packages
pip install -r requirements.txt
```

### Issue 3: Cursor movement is inverted or weird
**Solution:**
- Press C to calibrate
- Adjust sensitivity in main.py:
  ```python
  cursor_controller = CursorController(
      sensitivity_x=20,  # Increase for more sensitive
      sensitivity_y=10,  # Decrease for less sensitive
      filter_length=8
  )
  ```

### Issue 4: F7 not working
**Solution:**
- Some keyboards need Fn + F7
- Or change to different key in main.py

## Part 6: Git Workflow for Team

### Daily workflow:

```bash
# Start of day: Get latest code
git pull origin main

# Create feature branch
git checkout -b my-feature-name

# Make changes, then:
git add .
git commit -m "Description of changes"
git push origin my-feature-name

# Create pull request on GitHub
# After review and approval, merge to main
```

### Keeping your fork updated:

```bash
# If you forked the main repo
git remote add upstream <main-repo-url>
git fetch upstream
git merge upstream/main
```

## Part 7: Code Quality Tips

### Before committing:

1. **Test your code**
   ```bash
   python main.py
   # Try all features
   ```

2. **Check for errors**
   - No print statement spam
   - No commented-out code blocks
   - Proper error handling

3. **Format your code**
   - Use consistent indentation (4 spaces)
   - Add docstrings to functions
   - Keep lines under 100 characters

4. **Update documentation**
   - Update README.md if you added features
   - Add comments for complex logic
   - Update requirements.txt if you added packages

## Need Help?

### Resources:
- MediaPipe Docs: https://google.github.io/mediapipe/
- OpenCV Docs: https://docs.opencv.org/
- PyAutoGUI Docs: https://pyautogui.readthedocs.io/

### Team Communication:
- Create GitHub Issues for bugs
- Use pull requests for code review
- Comment your code for others to understand

Good luck with the integration! 🚀
