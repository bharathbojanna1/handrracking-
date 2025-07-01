# Hand Gesture Control System

A computer vision-based hand gesture control system that allows you to control your mouse cursor and perform clicks using hand movements captured through your webcam. The system also includes text-to-speech functionality for accessibility.

## Features

- **Hand Tracking**: Real-time hand landmark detection using MediaPipe
- **Cursor Control**: Move your mouse cursor by pointing with your index finger
- **Click Gestures**: Perform mouse clicks using specific finger combinations
- **Text-to-Speech**: Audio feedback for application names under the cursor
- **Smooth Movement**: Interpolated cursor movement for better user experience
- **OCR Integration**: Text extraction capabilities using Tesseract OCR
- **Configurable Settings**: Adjustable sensitivity and confidence thresholds

## Requirements

### Software Dependencies

```
pip install opencv-python
pip install mediapipe
pip install pyautogui
pip install pytesseract
pip install pyttsx3
pip install numpy
```

### External Dependencies

- **Tesseract OCR**: Download and install from [GitHub Tesseract](https://github.com/tesseract-ocr/tesseract)
  - Default installation path: `C:\Program Files\Tesseract-OCR\tesseract.exe`
  - Update the `tesseract_path` in the configuration if installed elsewhere

### Hardware Requirements

- Webcam (built-in or external)
- Sufficient lighting for hand detection
- Windows/macOS/Linux operating system

## Installation

1. **Clone or download** the project files
2. **Install Python dependencies**:
   ```bash
   pip install -r requirements.txt
   ```
3. **Install Tesseract OCR**:
   - Windows: Download installer from [UB Mannheim](https://github.com/UB-Mannheim/tesseract/wiki)
   - macOS: `brew install tesseract`
   - Ubuntu: `sudo apt install tesseract-ocr`

4. **Update configuration** if needed (see Configuration section)

## Usage

### Running the Application

```bash
python FINAL.py
```

### Hand Gestures

1. **Cursor Movement**:
   - Raise only your **index finger**
   - Point at the screen to move the cursor
   - Keep other fingers folded

2. **Mouse Click**:
   - Raise both **index finger** and **middle finger**
   - The system will perform a left-click

3. **Exit**:
   - Press `q` while the camera window is active

### Tips for Best Performance

- Ensure good lighting conditions
- Keep your hand within the camera frame
- Maintain a reasonable distance from the camera (arm's length)
- Make clear, distinct gestures
- Allow the system to stabilize before rapid movements

## Configuration

The application can be customized through the `CONFIG` dictionary:

```python
CONFIG = {
    'min_detection_confidence': 0.7,    # Hand detection sensitivity (0.0-1.0)
    'min_tracking_confidence': 0.7,     # Hand tracking sensitivity (0.0-1.0)
    'cursor_sensitivity': 1.0,          # Cursor movement sensitivity
    'tesseract_path': r"C:\Program Files\Tesseract-OCR\tesseract.exe",
    'debug_mode': False                 # Enable detailed logging
}
```

### Adjusting Settings

- **Higher detection confidence**: More accurate but may miss quick movements
- **Lower detection confidence**: More responsive but may have false positives
- **Cursor sensitivity**: Adjust how much cursor moves relative to hand movement
- **Debug mode**: Enable for troubleshooting and detailed logs

## Troubleshooting

### Common Issues

1. **"Tesseract not found" error**:
   - Verify Tesseract installation path
   - Update `tesseract_path` in configuration

2. **Poor hand detection**:
   - Improve lighting conditions
   - Adjust `min_detection_confidence` value
   - Check camera quality and positioning

3. **Cursor movement too sensitive/slow**:
   - Modify `cursor_sensitivity` value
   - Adjust `smooth_factor` for movement interpolation

4. **Audio feedback not working**:
   - Check system audio settings
   - Verify pyttsx3 installation
   - Test with different TTS voices

### Performance Optimization

- Close unnecessary applications to free up CPU
- Use a higher resolution webcam for better detection
- Ensure stable lighting conditions
- Position camera at eye level for optimal hand tracking

## File Structure

```
├── FINAL.py              # Main application file
├── README.md             # This documentation
└── requirements.txt      # Python dependencies (create this)
```

## Technical Details

### Key Components

- **MediaPipe Hands**: Google's hand landmark detection solution
- **OpenCV**: Computer vision and camera handling
- **PyAutoGUI**: Mouse control and screen capture
- **Tesseract OCR**: Optical character recognition
- **Pyttsx3**: Text-to-speech synthesis

### Hand Landmarks

The system uses MediaPipe's 21-point hand landmark model:
- Landmark 8: Index finger tip
- Landmark 6: Index finger DIP joint
- Landmark 12: Middle finger tip
- Landmark 10: Middle finger DIP joint

## Security Considerations

- The application controls your mouse and can perform clicks
- Only run in trusted environments
- Be cautious when using near sensitive applications
- The system captures video but does not store or transmit data

## License

This project is for educational and personal use. Please respect the licenses of all dependencies:
- MediaPipe: Apache 2.0
- OpenCV: Apache 2.0
- PyAutoGUI: BSD 3-Clause
- Tesseract: Apache 2.0

## Contributing

To contribute to this project:
1. Test thoroughly before submitting changes
2. Follow Python PEP 8 style guidelines
3. Update documentation for any new features
4. Consider accessibility improvements

## Support

For issues and questions:
1. Check the troubleshooting section above
2. Verify all dependencies are correctly installed
3. Test with different lighting and camera conditions
4. Enable debug mode for detailed error logs

---

**Note**: This system requires careful calibration and may need adjustments based on your specific hardware and environment setup.
