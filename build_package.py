#!/usr/bin/env python3
"""
Build script for LocalUtilityBox package distribution.

This script builds the package for distribution to PyPI.
"""

import subprocess
import sys
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


def main():
    """Main build function."""
    print("🚀 Building LocalUtilityBox for distribution...")
    
    # Clean previous builds
    print("🧹 Cleaning previous builds...")
    for pattern in ["build/", "dist/", "*.egg-info/"]:
        subprocess.run(f"rm -rf {pattern}", shell=True)
    
    # Build the package
    if not run_command("python3 -m build", "Building package"):
        print("❌ Build failed. Make sure you have 'build' installed:")
        print("pip install build")
        sys.exit(1)
    
    # Check the built package
    if not run_command("python3 -m twine check dist/*", "Checking package"):
        print("❌ Package check failed. Make sure you have 'twine' installed:")
        print("pip install twine")
        sys.exit(1)
    
    print("\n🎉 Package built successfully!")
    print("\nNext steps:")
    print("1. Test the package: pip install dist/*.whl")
    print("2. Upload to PyPI: python3 -m twine upload dist/*")
    print("3. Or upload to Test PyPI first: python3 -m twine upload --repository testpypi dist/*")


if __name__ == "__main__":
    main()
