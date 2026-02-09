# Computer Vision Based Touchless Device Control

A computer vision system that allows touchless control of your computer using head movements and hand gestures.

## Team Members
- **Shreyas**: Virtual keyboard typing (integration pending)
- **Om**: System architecture and framework design
- **Kalash**: Cursor movement using head orientation
- **[Your Name]**: Hand gesture features + System integration

## Features

### Currently Implemented ✅
- **Head-based Cursor Control**: Move your computer cursor by moving your head
- **Real-time Face Detection**: Uses MediaPipe for accurate face landmark detection
- **Smooth Movement**: Threading-based smooth cursor movement with filtering
- **Calibration System**: Press 'C' to calibrate center position
- **State Management**: Clean state system (ON/OFF/PAUSED/FROZEN)
- **Visual Feedback**: On-screen display of system status and FPS

### Coming Soon 🚧
- Virtual keyboard typing (Shreyas)
- Hand gestures for scrolling
- Hand gestures for zooming
- Hand gestures for volume control
- Additional gesture controls

## System Architecture

```
Computer_Vision_Based_Touchless_Device_Control/
│
├── core/                      # Core system components
│   ├── camera.py             # Webcam handling
│   ├── face_detector.py      # MediaPipe face detection
│   ├── head_pose.py          # Head orientation estimation
│   ├── cursor_controller.py  # Cursor control logic
│   ├── state.py              # System state enum
│   └── state_manager.py      # State management
│
├── utils/                     # Utility functions
│   └── fps.py                # FPS counter
│
├── tests/                     # Test modules
│   └── __init__.py
│
├── main.py                   # Main application
├── requirements.txt          # Python dependencies
├── .gitignore               # Git ignore file
└── README.md                # This file
```

## Installation

### Prerequisites
- Python 3.8 or higher
- Webcam
- Windows/Linux/Mac OS

### Setup Steps

1. **Clone the repository**
   ```bash
   git clone <your-repo-url>
   cd Computer_Vision_Based_Touchless_Device_Control
   ```

2. **Create a virtual environment** (recommended)
   ```bash
   python -m venv venv
   
   # On Windows:
   venv\Scripts\activate
   
   # On Mac/Linux:
   source venv/bin/activate
   ```

3. **Install dependencies**
   ```bash
   pip install -r requirements.txt
   ```

## Usage

### Running the Application

```bash
python main.py
```

### Controls

| Key | Action |
|-----|--------|
| **F7** | Toggle cursor control ON/OFF |
| **C** | Calibrate (set current head position as center) |
| **ESC** | Exit application |

### How to Use

1. **Start the program**: Run `python main.py`
2. **Position yourself**: Sit comfortably in front of your webcam
3. **Calibrate**: Press 'C' to set your current head position as center
4. **Enable control**: Press F7 to enable cursor control
5. **Move cursor**: Move your head left/right and up/down to control the cursor
6. **Disable when needed**: Press F7 again to disable cursor control

## Technical Details

### Head Pose Estimation
- Uses 3D facial landmarks from MediaPipe Face Mesh
- Calculates yaw (left/right) and pitch (up/down) angles
- Creates coordinate system based on facial geometry

### Cursor Control
- Maps head angles to screen coordinates
- Configurable sensitivity (default: ±20° yaw, ±10° pitch)
- Smoothing filter using rolling average (8 frames)
- Threading for smooth movement (100Hz update rate)

### State Management
- **OFF**: Cursor control disabled
- **ON**: Cursor control active
- **FROZEN**: Cursor position locked
- **PAUSED**: Face not detected, waiting

## Troubleshooting

### Camera not opening
- Check if camera is being used by another application
- Try changing camera index in `main.py` (0, 1, 2, etc.)

### Cursor movement is jittery
- Increase `filter_length` in CursorController initialization
- Reduce sensitivity values

### Face not detected
- Ensure good lighting
- Position face clearly in front of camera
- Check if face is too close or too far

### Permission errors (keyboard/pyautogui)
- On macOS: Grant accessibility permissions in System Preferences
- On Linux: You may need to run with appropriate permissions

## Development

### Adding New Features

To add new gesture features:

1. Create a new module in `core/` (e.g., `hand_gesture.py`)
2. Follow the existing class structure
3. Import and initialize in `main.py`
4. Add appropriate keyboard shortcuts
5. Update this README

### Testing

```bash
# Run individual tests
python -m pytest tests/

# Or create your own test
python tests/test_integration.py
```

## Integration Progress

- [x] Integrated Om's framework
- [x] Integrated Kalash's cursor control
- [ ] Integrate Shreyas's virtual keyboard (waiting for code)
- [ ] Add hand gesture scrolling
- [ ] Add hand gesture zooming
- [ ] Add hand gesture volume control

## Contributing

This is a team project. If you're a team member:
1. Create a new branch for your feature
2. Test thoroughly
3. Create a pull request
4. Get review from team
5. Merge to main

## License

[Add your license here]

## Acknowledgments

- **MediaPipe**: For the excellent face mesh model
- **OpenCV**: For computer vision capabilities
- **PyAutoGUI**: For system cursor control
- Team members for their individual contributions

## Contact

[Add contact information or links]

---

**Last Updated**: February 2026
**Version**: 1.0 (Integrated - Cursor Control)
