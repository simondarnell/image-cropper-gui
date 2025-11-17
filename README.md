# Batch Image Cropper & Mirrorer

A Windows GUI application for batch processing images by cropping pixels from specified sides and mirroring them to the opposite side while maintaining image resolution.

## Features

- **Batch Processing**: Process multiple images at once
- **Directional Cropping**: Specify pixel values for top, bottom, left, and right sides
- **Smart Mirroring**: Cropped pixels are automatically mirrored to opposite sides
- **Real-time Progress**: Visual progress bar and live logging
- **Error Handling**: Detailed error reporting for failed images
- **Standalone Executable**: Can be packaged as a single `.exe` file

## How It Works

1. **Input**: Select a folder containing images
2. **Configure**: Set pixel values to crop from each side (0-500 pixels)
3. **Output**: Specify where to save processed images
4. **Process**: Click "Process Images" to batch process all images

Example:
- If you specify `Top: 50`, the top 50 pixels will be removed and the same content will be pasted to the bottom
- Image resolution stays the same (50 pixels removed + 50 pixels added)

## Supported Formats

- JPG / JPEG
- PNG
- BMP
- GIF
- TIFF

## Installation

### Prerequisites
- Python 3.8 or later
- Windows OS (for standalone executable)

### Setup

1. Install dependencies:
```powershell
pip install -r requirements.txt
```

2. Run the application:
```powershell
python main.py
```

## Creating a Standalone Executable

Build a Windows `.exe` file that doesn't require Python:

```powershell
python build_exe.py
```

The executable will be created at: `dist/ImageCropper.exe`

You can then distribute this single file to other Windows computers without requiring Python installation.

## Usage Example

1. Launch the application (either `python main.py` or `ImageCropper.exe`)
2. Click "Browse" next to "Input Folder" and select a folder with images
3. Click "Browse" next to "Output Folder" and select where to save results
4. Set crop values:
   - **Top**: Pixels to crop from top and mirror to bottom (e.g., 30)
   - **Bottom**: Pixels to crop from bottom and mirror to top (e.g., 30)
   - **Left**: Pixels to crop from left and mirror to right (e.g., 20)
   - **Right**: Pixels to crop from right and mirror to left (e.g., 20)
5. Click "Process Images"
6. Monitor progress in the log window
7. Check the output folder for processed images

## Technical Details

- **GUI Framework**: tkinter (built-in with Python)
- **Image Processing**: Pillow
- **Executable Builder**: PyInstaller
- **Threading**: Background processing to keep UI responsive

## File Structure

```
image-cropper-gui/
├── main.py                 # GUI application
├── image_processor.py      # Image processing logic
├── build_exe.py           # Build script for executable
├── requirements.txt       # Python dependencies
└── README.md             # This file
```

## Troubleshooting

### "No images found"
- Make sure your input folder contains supported image files (.jpg, .png, etc.)
- Check that file extensions are correct

### "Permission denied" errors
- Ensure output folder is writable
- Close any other programs that might have images locked

### Build fails
- Make sure PyInstaller is installed: `pip install PyInstaller`
- Run from the application directory
- Check that `main.py` exists in the same directory

## License

Free to use and modify.
