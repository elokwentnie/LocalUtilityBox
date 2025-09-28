#!/usr/bin/env python3
"""
GUI Installation Script for LocalUtilityBox.

This script installs LocalUtilityBox with GUI support and creates desktop shortcuts.
"""

import os
import sys
import subprocess
import platform
from pathlib import Path

def run_command(command, description):
    """Run a command and handle errors."""
    print(f"🔄 {description}...")
    try:
        result = subprocess.run(command, shell=True, check=True, capture_output=True, text=True)
        print(f"✅ {description} completed successfully")
        return True
    except subprocess.CalledProcessError as e:
        print(f"❌ {description} failed:")
        print(f"Error: {e.stderr}")
        return False

def check_python_version():
    """Check Python version."""
    if sys.version_info < (3, 8):
        print("❌ Python 3.8 or higher is required for GUI.")
        return False
    print(f"✅ Python {sys.version_info.major}.{sys.version_info.minor} detected")
    return True

def check_tkinter():
    """Check if tkinter is available."""
    try:
        import tkinter
        print("✅ tkinter is available")
        return True
    except ImportError:
        print("❌ tkinter is not available")
        print("Please install python3-tk:")
        if platform.system() == "Linux":
            print("  sudo apt-get install python3-tk")
        elif platform.system() == "Darwin":  # macOS
            print("  brew install python-tk")
        elif platform.system() == "Windows":
            print("  tkinter should be included with Python")
        return False

def install_dependencies():
    """Install required dependencies."""
    print("📦 Installing dependencies...")
    
    # Install core dependencies
    if not run_command("pip install -r requirements.txt", "Installing core dependencies"):
        return False
        
    # Install GUI-specific dependencies
    gui_deps = [
        "Pillow>=10.0.0",
        "opencv-python>=4.8.0",
        "tkcolorpicker>=1.2.0"
    ]
    
    for dep in gui_deps:
        if not run_command(f"pip install {dep}", f"Installing {dep}"):
            print(f"Warning: Failed to install {dep}")
            
    return True

def create_desktop_shortcut():
    """Create desktop shortcut for GUI."""
    system = platform.system()
    
    if system == "Windows":
        create_windows_shortcut()
    elif system == "Darwin":  # macOS
        create_macos_shortcut()
    elif system == "Linux":
        create_linux_shortcut()

def create_windows_shortcut():
    """Create Windows desktop shortcut."""
    try:
        import winshell
        from win32com.client import Dispatch
        
        desktop = winshell.desktop()
        path = os.path.join(desktop, "LocalUtilityBox.lnk")
        target = sys.executable
        wDir = os.path.dirname(os.path.abspath(__file__))
        icon = target
        
        shell = Dispatch('WScript.Shell')
        shortcut = shell.CreateShortCut(path)
        shortcut.Targetpath = target
        shortcut.Arguments = os.path.join(wDir, "src", "gui", "launcher.py")
        shortcut.WorkingDirectory = wDir
        shortcut.IconLocation = icon
        shortcut.save()
        
        print("✅ Windows desktop shortcut created")
    except ImportError:
        print("⚠️  Could not create Windows shortcut (winshell not available)")

def create_macos_shortcut():
    """Create macOS application bundle."""
    try:
        app_name = "LocalUtilityBox.app"
        app_path = Path.home() / "Applications" / app_name
        contents_path = app_path / "Contents"
        macos_path = contents_path / "MacOS"
        resources_path = contents_path / "Resources"
        
        # Create directory structure
        macos_path.mkdir(parents=True, exist_ok=True)
        resources_path.mkdir(parents=True, exist_ok=True)
        
        # Create Info.plist
        info_plist = f"""<?xml version="1.0" encoding="UTF-8"?>
<!DOCTYPE plist PUBLIC "-//Apple//DTD PLIST 1.0//EN" "http://www.apple.com/DTDs/PropertyList-1.0.dtd">
<plist version="1.0">
<dict>
    <key>CFBundleExecutable</key>
    <string>localutilitybox</string>
    <key>CFBundleIdentifier</key>
    <string>com.localutilitybox.app</string>
    <key>CFBundleName</key>
    <string>LocalUtilityBox</string>
    <key>CFBundleVersion</key>
    <string>0.2.0</string>
    <key>CFBundleShortVersionString</key>
    <string>0.2.0</string>
</dict>
</plist>"""
        
        with open(contents_path / "Info.plist", "w") as f:
            f.write(info_plist)
            
        # Create launcher script
        launcher_script = f"""#!/bin/bash
cd "{os.path.dirname(os.path.abspath(__file__))}"
python3 src/gui/launcher.py
"""
        
        with open(macos_path / "localutilitybox", "w") as f:
            f.write(launcher_script)
            
        os.chmod(macos_path / "localutilitybox", 0o755)
        
        print("✅ macOS application bundle created")
    except Exception as e:
        print(f"⚠️  Could not create macOS shortcut: {e}")

def create_linux_shortcut():
    """Create Linux desktop shortcut."""
    try:
        desktop_file = Path.home() / "Desktop" / "LocalUtilityBox.desktop"
        
        desktop_entry = f"""[Desktop Entry]
Version=1.0
Type=Application
Name=LocalUtilityBox
Comment=File Processing Suite
Exec=python3 {os.path.join(os.path.dirname(os.path.abspath(__file__)), "src", "gui", "launcher.py")}
Icon=applications-graphics
Terminal=false
Categories=Graphics;Office;
"""
        
        with open(desktop_file, "w") as f:
            f.write(desktop_entry)
            
        os.chmod(desktop_file, 0o755)
        
        print("✅ Linux desktop shortcut created")
    except Exception as e:
        print(f"⚠️  Could not create Linux shortcut: {e}")

def create_gui_launcher():
    """Create a GUI launcher script."""
    launcher_content = f"""#!/usr/bin/env python3
import sys
import os
from pathlib import Path

# Add src to path
src_path = Path(__file__).parent / "src"
sys.path.insert(0, str(src_path))

# Launch GUI
from gui.launcher import main
main()
"""
    
    launcher_path = Path("launch_gui.py")
    with open(launcher_path, "w") as f:
        f.write(launcher_content)
        
    os.chmod(launcher_path, 0o755)
    print("✅ GUI launcher script created: launch_gui.py")

def main():
    """Main installation function."""
    print("🚀 LocalUtilityBox GUI Installation")
    print("=" * 40)
    
    # Check Python version
    if not check_python_version():
        sys.exit(1)
        
    # Check tkinter
    if not check_tkinter():
        sys.exit(1)
        
    # Install dependencies
    if not install_dependencies():
        print("❌ Failed to install dependencies")
        sys.exit(1)
        
    # Create GUI launcher
    create_gui_launcher()
    
    # Create desktop shortcut
    create_desktop_shortcut()
    
    print("\n🎉 GUI installation completed successfully!")
    print("\nYou can now launch LocalUtilityBox GUI using:")
    print("  python3 launch_gui.py")
    print("  or")
    print("  python3 src/gui/launcher.py")
    print("\nOr use the desktop shortcut if created.")

if __name__ == "__main__":
    main()
