#!/usr/bin/env python3
"""
Development installation script for LocalUtilityBox.

This script sets up the development environment with all necessary dependencies.
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
    """Main installation function."""
    print("🚀 Setting up LocalUtilityBox development environment...")
    
    # Check Python version
    if sys.version_info < (3, 8):
        print("❌ Python 3.8 or higher is required")
        sys.exit(1)
    
    print(f"✅ Python {sys.version_info.major}.{sys.version_info.minor} detected")
    
    # Install the package in development mode
    if not run_command("pip install -e .", "Installing LocalUtilityBox in development mode"):
        sys.exit(1)
    
    # Install development dependencies
    if not run_command("pip install -r requirements-dev.txt", "Installing development dependencies"):
        sys.exit(1)
    
    # Run tests to verify installation
    if not run_command("pytest --version", "Checking pytest installation"):
        sys.exit(1)
    
    print("\n🎉 Development environment setup complete!")
    print("\nNext steps:")
    print("1. Run tests: pytest")
    print("2. Run with coverage: pytest --cov=localutilitybox")
    print("3. Format code: black src tests")
    print("4. Lint code: flake8 src tests")
    print("5. Type check: mypy src")


if __name__ == "__main__":
    main()
