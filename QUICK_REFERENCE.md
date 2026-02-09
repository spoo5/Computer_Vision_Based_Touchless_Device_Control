# Quick Reference Guide

## For You (The Integrator)

### What You Have Now ✅

A fully integrated system combining:
- Om's clean architecture
- Kalash's working cursor control
- Proper documentation
- Test suite

### Your Immediate Next Steps

1. **Get the files to your computer**
   - Download the `Computer_Vision_Based_Touchless_Device_Control` folder
   - Or copy files Claude created

2. **Test it works**
   ```bash
   cd Computer_Vision_Based_Touchless_Device_Control
   python -m venv venv
   venv\Scripts\activate  # Windows
   pip install -r requirements.txt
   python tests/test_integration.py
   python main.py
   ```

3. **Push to GitHub**
   ```bash
   git init
   git add .
   git commit -m "Initial integration"
   git remote add origin <your-repo-url>
   git push -u origin main
   ```

4. **Share with team**
   - Send them the GitHub link
   - They can clone and test

### When Shreyas Sends Code

**Pattern to follow:**

1. **Understand their code**
   - What does it do?
   - What are the inputs/outputs?
   - What dependencies does it have?

2. **Plan integration**
   - Where does it fit? (new file in core/?)
   - What does main.py need to import?
   - Any new keyboard shortcuts?

3. **Integrate step by step**
   ```python
   # Example: Adding virtual keyboard
   
   # In core/virtual_keyboard.py
   class VirtualKeyboard:
       def __init__(self):
           # Their initialization code
           pass
       
       def process(self, frame):
           # Their processing code
           pass
   
   # In main.py
   from core.virtual_keyboard import VirtualKeyboard
   
   # In main():
   vkeyboard = VirtualKeyboard()
   
   # In main loop:
   if some_condition:
       vkeyboard.process(frame)
   ```

4. **Test thoroughly**
   - Does it work standalone?
   - Does it work with cursor control?
   - Any conflicts?

5. **Commit**
   ```bash
   git add .
   git commit -m "Integrated Shreyas's virtual keyboard"
   git push
   ```

### Adding Your Hand Gesture Features

**Recommended approach:**

1. **Start simple - one gesture at a time**
   - First: Just detect hand
   - Then: Recognize one gesture (e.g., scroll)
   - Then: Add action (actually scroll)
   - Then: Add next gesture

2. **Create files as you go**
   ```
   core/hand_detector.py      # First
   core/gesture_recognizer.py # Second  
   core/scroll_controller.py  # Third
   ```

3. **Use this pattern**
   ```python
   # hand_detector.py
   import mediapipe as mp
   
   class HandDetector:
       def __init__(self):
           self.mp_hands = mp.solutions.hands
           self.hands = self.mp_hands.Hands(
               max_num_hands=1,
               min_detection_confidence=0.7
           )
       
       def detect(self, frame):
           rgb = cv2.cvtColor(frame, cv2.COLOR_BGR2RGB)
           results = self.hands.process(rgb)
           return results
   ```

4. **Test each piece separately**
   - Create test_hand_detection.py
   - Make sure hand detection works
   - Then integrate into main.py

### Code Template for Adding Features

```python
# In main.py, add to imports:
from core.your_new_feature import YourNewClass

# In main(), add initialization:
your_feature = YourNewClass(parameters)

# In main loop, add processing:
if face_detected:
    # existing code...
    
    # your new code:
    gesture = your_feature.process(frame)
    if gesture == "SCROLL_UP":
        pyautogui.scroll(10)

# Add keyboard shortcut if needed:
elif key == ord('s'):  # Toggle scroll mode
    your_feature.toggle()
```

### Common Patterns You'll Use

**Pattern 1: Adding a new detector**
```python
class NewDetector:
    def __init__(self):
        # Initialize MediaPipe or other tools
        pass
    
    def process(self, frame):
        # Detect something
        # Return results
        pass
```

**Pattern 2: Adding a new controller**
```python
class NewController:
    def __init__(self):
        self.enabled = False
    
    def enable(self):
        self.enabled = True
    
    def disable(self):
        self.enabled = False
    
    def execute(self, params):
        if not self.enabled:
            return
        # Do the action
        pass
```

**Pattern 3: Adding to main loop**
```python
# In main loop:
if condition:
    result = detector.process(frame)
    if result:
        controller.execute(result)
```

## Hand Gesture Features - Implementation Plan

### Feature 1: Scroll

**What you need:**
- Detect hand moving up/down
- Trigger scroll action

**Code location:**
- `core/hand_detector.py` - detect hand
- `core/scroll_controller.py` - perform scroll
- `main.py` - integrate both

**Pseudocode:**
```python
hand_y_position = detect_hand_y()
if hand_y_position > previous_y:
    scroll_down()
else:
    scroll_up()
```

### Feature 2: Zoom

**What you need:**
- Detect pinch gesture (thumb + index finger)
- Measure distance
- Trigger zoom

**Code location:**
- `core/gesture_recognizer.py` - recognize pinch
- `core/zoom_controller.py` - perform zoom

**Pseudocode:**
```python
distance = get_thumb_index_distance()
if distance < threshold:
    # Pinching - zoom in
    pyautogui.hotkey('ctrl', '+')
```

### Feature 3: Volume

**What you need:**
- Detect hand open/close
- Map to volume level
- Change system volume

**Libraries needed:**
```python
# Windows
from pycaw.pycaw import AudioUtilities, IAudioEndpointVolume
```

**Code location:**
- `core/volume_controller.py`

## Useful Code Snippets

### Check if hand is detected
```python
if results.multi_hand_landmarks:
    hand_landmarks = results.multi_hand_landmarks[0]
    # Process landmarks
```

### Get landmark position
```python
landmark = hand_landmarks.landmark[INDEX]
x = int(landmark.x * frame_width)
y = int(landmark.y * frame_height)
```

### Scroll
```python
import pyautogui
pyautogui.scroll(10)  # Scroll up
pyautogui.scroll(-10) # Scroll down
```

### Zoom
```python
pyautogui.hotkey('ctrl', '+')  # Zoom in
pyautogui.hotkey('ctrl', '-')  # Zoom out
```

### Volume (Windows)
```python
from ctypes import cast, POINTER
from comtypes import CLSCTX_ALL
from pycaw.pycaw import AudioUtilities, IAudioEndpointVolume

devices = AudioUtilities.GetSpeakers()
interface = devices.Activate(IAudioEndpointVolume._iid_, CLSCTX_ALL, None)
volume = cast(interface, POINTER(IAudioEndpointVolume))

volume.SetMasterVolumeLevelScalar(0.5, None)  # 50%
```

## Debugging Tips

### Print statements
```python
# Use these to understand what's happening
print(f"Hand detected: {hand_detected}")
print(f"Gesture: {gesture_type}")
print(f"Position: ({x}, {y})")
```

### Visual feedback
```python
# Draw on frame to see what's detected
cv2.circle(frame, (x, y), 10, (0, 255, 0), -1)
cv2.putText(frame, f"Gesture: {gesture}", (10, 150), ...)
```

### Error handling
```python
try:
    result = risky_operation()
except Exception as e:
    print(f"Error: {e}")
    # Continue or fallback
```

## Resources

### Documentation
- MediaPipe Hands: https://google.github.io/mediapipe/solutions/hands
- PyAutoGUI: https://pyautogui.readthedocs.io/
- OpenCV: https://docs.opencv.org/

### Example Code
Look at:
- `core/cursor_controller.py` - for threading pattern
- `core/face_detector.py` - for MediaPipe pattern
- `main.py` - for integration pattern

### Ask for Help
- Create GitHub issues
- Check with team members
- Google error messages
- Read the docs

## Success Checklist

Before considering a feature "done":

- [ ] Code works in isolation
- [ ] Code works with other features
- [ ] No crashes or errors
- [ ] Added to README.md
- [ ] Added to requirements.txt (if new packages)
- [ ] Tested by someone else
- [ ] Committed to GitHub
- [ ] Documented how to use

Good luck! You got this! 🚀

---

**Remember:**
- Start small, test often
- One feature at a time
- Ask for help when stuck
- Document as you go
- Have fun building!
