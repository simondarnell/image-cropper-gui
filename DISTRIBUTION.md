# Distribution Guide

## Running the Executable on Another Computer

If `ImageCropper.exe` doesn't work on another computer, follow these steps to resolve the issue.

### System Requirements

**Windows 10 or later (64-bit)**

The exe requires:
1. **Visual C++ Runtime Libraries** - Required by PyInstaller
2. **Windows 7 or later** - Operating system requirement
3. **500MB+ free disk space** - For the executable

### Solution 1: Install Visual C++ Runtime (RECOMMENDED)

This is the most common cause of exe failures on other computers.

**Download and install the Visual C++ Redistributable:**
- [Visual C++ Redistributable (x64)](https://support.microsoft.com/en-us/help/2977003/the-latest-supported-visual-c-downloads)
- Install the "Visual Studio 2022 x64" version (or the latest available)

After installation, try running `ImageCropper.exe` again.

### Solution 2: Run in Compatibility Mode

1. Right-click `ImageCropper.exe`
2. Select "Properties"
3. Go to "Compatibility" tab
4. Check "Run this program in compatibility mode for:"
5. Try "Windows 10" or "Windows 11"
6. Click "Apply" and "OK"

### Solution 3: Disable Full-Screen Optimizations

1. Right-click `ImageCropper.exe`
2. Select "Properties"
3. Go to "Compatibility" tab
4. Check "Disable fullscreen optimizations"
5. Click "Apply" and "OK"

### Solution 4: Run from Command Prompt for Error Details

Open Command Prompt and navigate to the folder with `ImageCropper.exe`, then run:
```cmd
ImageCropper.exe
```

This will show any error messages that appear, helping identify the exact issue.

### Solution 5: Run as Administrator

1. Right-click `ImageCropper.exe`
2. Select "Run as administrator"

## If None of These Work

**Alternative: Use Python Directly**

If the exe still doesn't work, you can run the Python version instead:

1. Install Python 3.8 or later from https://www.python.org
2. Download all files from the GitHub repository
3. In the folder with the files, open Command Prompt
4. Run:
   ```cmd
   pip install -r requirements.txt
   python main.py
   ```

## Building the Executable Yourself

If you want to rebuild the exe with better compatibility:

1. Install Python 3.8 or later
2. Clone the repository
3. Install dependencies:
   ```cmd
   pip install -r requirements.txt
   ```
4. Build the exe:
   ```cmd
   python build_exe.py
   ```
5. Find `ImageCropper.exe` in the `dist` folder

## Known Issues

### Issue: "The application failed to start because its side-by-side configuration is incorrect"
**Solution:** Install Visual C++ Runtime (Solution 1 above)

### Issue: "Tkinter not found" or GUI doesn't appear
**Solution:** This shouldn't happen with the packaged exe. Try Solution 4 to see the error.

### Issue: "Access Denied" when processing images
**Solution:** 
- Run as administrator
- Make sure output folder is not read-only
- Close any other programs that might be accessing the images

### Issue: Slow performance or freezing
**Solution:**
- Reduce the number of images being processed at once
- Close other programs to free up memory
- Try processing smaller images first

## System Architecture

The exe is built for **64-bit Windows only**. If you're on a 32-bit system, you'll need to:
1. Edit `build_exe.py` and change the build configuration
2. Rebuild the exe from source

## Antivirus Warnings

Some antivirus software may flag the exe as suspicious because it's a packaged Python application. This is normal and safe. You can:
1. Add it to your antivirus whitelist
2. Or build it yourself to verify the source code

## Support

If you continue to experience issues:
1. Check the [GitHub Issues](https://github.com/simondarnell/image-cropper-gui/issues) page
2. Note the exact error message and your Windows version
3. Try the "Run from Command Prompt" solution to capture full error details
