"""
Improved build script for creating a standalone executable with better compatibility.
This script creates an exe that works better on other computers by including
all necessary dependencies and using optimized PyInstaller settings.
"""

import PyInstaller.__main__
import sys
import os
from pathlib import Path

# Get the project directory
PROJECT_DIR = Path(__file__).parent
DIST_DIR = PROJECT_DIR / "dist"
BUILD_DIR = PROJECT_DIR / "build"

def build_exe():
    """Build the executable with optimal settings for distribution."""
    
    print("=" * 60)
    print("Building Image Cropper GUI Executable")
    print("=" * 60)
    
    # PyInstaller arguments
    pyinstaller_args = [
        # Main entry point
        str(PROJECT_DIR / "main.py"),
        
        # Output settings
        f"--distpath={DIST_DIR}",
        f"--workpath={BUILD_DIR}",
        f"--specpath={PROJECT_DIR}",
        
        # Executable name
        "--name=ImageCropper",
        
        # One-file distribution (single exe)
        "--onefile",
        
        # Windowed mode (no console window)
        "--windowed",
        
        # Hidden imports that PyInstaller might miss
        "--hidden-import=PIL",
        "--hidden-import=PIL.Image",
        "--hidden-import=PIL.ImageFilter",
        "--hidden-import=tkinter",
        
        # Collect all data files
        "--collect-all=PIL",
        
        # Console output during build
        "--log-level=INFO",
    ]
    
    # Build the executable
    print("\nStarting PyInstaller build...")
    PyInstaller.__main__.run(pyinstaller_args)
    
    print("\n" + "=" * 60)
    print("Build Complete!")
    print("=" * 60)
    print(f"\nExecutable location: {DIST_DIR / 'ImageCropper.exe'}")
    print(f"File size: {get_size_mb(DIST_DIR / 'ImageCropper.exe'):.1f} MB")
    print("\nNotes:")
    print("- The exe is self-contained and portable")
    print("- No Python installation needed on target computer")
    print("- First launch may take a few seconds as files are extracted")
    print("- If exe doesn't work on another computer:")
    print("  1. Install Visual C++ Redistributable (x64)")
    print("  2. See DISTRIBUTION.md for troubleshooting")

def get_size_mb(file_path):
    """Get file size in MB."""
    return os.path.getsize(file_path) / (1024 * 1024)

if __name__ == "__main__":
    build_exe()
