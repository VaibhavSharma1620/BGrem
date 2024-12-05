# 🖼️ BGrem: Background Replacement Tool

BGrem is a versatile Python application that allows you to replace backgrounds in images, videos, and live webcam feeds using machine learning-based segmentation.

## 🌟 Features

### Background Replacement Modes
- **Image Mode**: Replace background of a single image
- **Video Mode**: Replace background of entire video files
- **Webcam Mode**: Real-time background replacement using your webcam

### Key Functionalities
- Cycle through multiple background images in real-time
- Save processed images and videos
- User-friendly GUI interface
- Uses MediaPipe for advanced image segmentation

## 🛠️ Prerequisites

### Required Libraries
- OpenCV (cv2)
- MediaPipe
- NumPy
- Pillow (PIL)
- tkinter

### Installation

1. Clone the repository:
```bash
git clone https://github.com/VaibhavSharma1620/BGrem.git
cd BGrem
```

2. Create a virtual environment (recommended):
```bash
python -m venv venv
source venv/bin/activate  # On Windows, use `venv\Scripts\activate`
```

3. Install required packages:
```bash
pip install opencv-python mediapipe numpy pillow
```

## 🚀 How to Use

### Prepare Background Images
- Create a folder with background images (PNG, JPG, JPEG supported)
- These will be used to replace the original background

### Running the Application

```bash
python BGrem.py
```

### Using the Tool

#### Mode Selection
1. Choose your mode:
   - **Image Mode**: Select a single image to process
   - **Video Mode**: Select a video file to process
   - **Webcam Mode**: Use your live webcam feed

2. Optional: Check "Save Video Output" for recording processed videos

#### During Playback
- Press `n`: Next background image
- Press `p`: Previous background image
- Press `s`: Save current frame/image
- Press `q`: Quit the application

## 🎨 Example Workflow

1. Launch the application
2. Select "Video" mode
3. Choose your input video
4. Select a folder with background images
5. Press keys to cycle through backgrounds
6. Save desired outputs

## 💡 Tips
- Use high-contrast background images for best results
- Ensure good lighting in your original image/video
- Background images will be automatically resized

## 🔬 Technical Details
- Uses MediaPipe's SelfieSegmentation model
- Foreground detection threshold: 0.8 (adjustable in code)
- Supports multiple image formats
- Real-time performance optimized

## 🤝 Contributing
1. Fork the repository
2. Create your feature branch (`git checkout -b feature/AmazingFeature`)
3. Commit your changes (`git commit -m 'Add some AmazingFeature'`)
4. Push to the branch (`git push origin feature/AmazingFeature`)
5. Open a Pull Request

## 📝 License
Distributed under the MIT License. See `LICENSE` for more information.

## 🐛 Issues
Report bugs or feature requests in the [Issues](https://github.com/VaibhavSharma1620/BGrem/issues) section.
