"""
PyInstaller build script to create a standalone Windows executable.
Run: python build_exe.py build
"""
import PyInstaller.__main__
import sys
import os

def build_exe():
    # Get the current working directory
    script_dir = os.getcwd()
    
    # PyInstaller arguments
    args = [
        'main.py',
        '--onefile',  # Single executable file
        '--windowed',  # No console window
        '--name=ImageCropper',  # Output executable name
        f'--icon=./icon.ico' if os.path.exists(os.path.join(script_dir, 'icon.ico')) else '',  # Icon if exists
        '--add-data=image_processor.py:.',  # Include image processor module
        '-y',  # Overwrite without asking
        '--distpath=./dist',
        '--buildpath=./build',
        '--specpath=./spec',
    ]
    
    # Remove empty strings
    args = [arg for arg in args if arg]
    
    print("Building Windows executable...")
    print(f"Command: pyinstaller {' '.join(args)}")
    
    PyInstaller.__main__.run(args)
    
    print("\nBuild complete!")
    print(f"Executable location: {os.path.join(script_dir, 'dist', 'ImageCropper.exe')}")


if __name__ == '__main__':
    build_exe()
