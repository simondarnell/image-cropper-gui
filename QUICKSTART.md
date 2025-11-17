# Quick Start Guide

## Installation & Running

### Step 1: Install Python
Download Python 3.8+ from: https://www.python.org/downloads/
**Important**: Check "Add Python to PATH" during installation

### Step 2: Install Dependencies
Open PowerShell in the application folder and run:
```powershell
pip install -r requirements.txt
```

### Step 3: Run the Application
```powershell
python main.py
```

## Creating a Standalone Executable

To create an `.exe` file that can be shared or run without Python:

### Step 1: Build the executable
```powershell
python build_exe.py
```

### Step 2: Find the executable
Look in the `dist` folder:
```
image-cropper-gui/
└── dist/
    └── ImageCropper.exe
```

### Step 3: Run the executable
Double-click `ImageCropper.exe` to launch the application.

## Using the Application

### Basic Workflow:
1. **Select Input Folder**: Click "Browse" and choose a folder with images
2. **Select Output Folder**: Click "Browse" and choose where to save results
3. **Set Crop Values**: 
   - Top: pixels to crop from top (mirrored to bottom)
   - Bottom: pixels to crop from bottom (mirrored to top)
   - Left: pixels to crop from left (mirrored to right)
   - Right: pixels to crop from right (mirrored to left)
4. **Process**: Click "Process Images" button
5. **Review Results**: Check the output folder for processed images

### Example Use Cases:

**Remove letterbox and extend sides:**
```
Top: 50
Bottom: 50
Left: 0
Right: 0
```
This removes 50 pixels from top/bottom and extends those pixels to opposite sides.

**Crop pillar box and extend:**
```
Top: 0
Bottom: 0
Left: 40
Right: 40
```
This removes 40 pixels from left/right and extends to opposite sides.

**All-around crop:**
```
Top: 30
Bottom: 30
Left: 25
Right: 25
```
This crops equally from all sides and mirrors each section.

## Testing the Application

### Run unit tests (requires Pillow):
```powershell
python test_processor.py
```

This will:
- Create sample test images
- Process them with different settings
- Save results to `test_output_batch/` folder

### Testing the GUI:
1. Run `python main.py`
2. Create a test folder with some images
3. Select it as input
4. Choose an output folder
5. Set some crop values (e.g., Top: 20, Bottom: 20)
6. Click "Process Images"
7. Check the results in your output folder

## Troubleshooting

### Issue: "pip install" doesn't work
**Solution**: 
- Make sure Python is in your PATH
- Try: `python -m pip install -r requirements.txt`

### Issue: Executable won't run
**Solution**:
- Run from Command Prompt (not PowerShell)
- Or run from the `dist/` folder directly
- Antivirus software might block it - add exception

### Issue: "No images found"
**Solution**:
- Make sure input folder has supported formats (.jpg, .png, .bmp, .gif, .tiff)
- Check folder permissions

### Issue: "Permission denied" on output
**Solution**:
- Make sure output folder exists and is writable
- Close any programs that have output images open
- Try a different output folder

## Building for Distribution

To distribute the application to others:

1. Build the executable: `python build_exe.py`
2. The file `dist/ImageCropper.exe` is completely standalone
3. No Python installation required on target computers
4. You can distribute just the `.exe` file

Note: On Windows, some antivirus might flag newly built executables as suspicious. This is normal and should be whitelisted.

## System Requirements

**To Run Application:**
- Windows 7 or later
- No additional software needed (if using .exe)

**To Build Application:**
- Python 3.8+
- 500 MB disk space (for build tools)

## Advanced: Custom Icon

To add a custom icon to the executable:

1. Place a 256x256 pixel `.ico` file in the application folder named `icon.ico`
2. Run `python build_exe.py`
3. The executable will have your custom icon

## Support

For issues or suggestions, check:
1. Ensure all images are in supported formats
2. Verify folder paths are correct
3. Check the processing log for detailed error messages

