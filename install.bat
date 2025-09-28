@echo off
REM LocalUtilityBox Installation Script for Windows

echo 🚀 LocalUtilityBox Installation Script
echo ======================================

REM Check Python version
python --version >nul 2>&1
if errorlevel 1 (
    echo ❌ Python is not installed or not in PATH
    echo Please install Python 3.8+ from https://python.org
    pause
    exit /b 1
)

echo ✅ Python found

REM Check pip
pip --version >nul 2>&1
if errorlevel 1 (
    echo ❌ pip is not installed
    echo Please install pip first
    pause
    exit /b 1
)

echo ✅ pip found

echo.
echo Choose installation method:
echo 1) Install from PyPI (recommended)
echo 2) Install from GitHub (latest version)
echo 3) Install from local wheel file
echo 4) Install in development mode

set /p choice="Enter your choice (1-4): "

if "%choice%"=="1" (
    echo 📦 Installing from PyPI...
    pip install localutilitybox
) else if "%choice%"=="2" (
    echo 📦 Installing from GitHub...
    pip install git+https://github.com/elokwentnie/localutilitybox.git
) else if "%choice%"=="3" (
    echo 📦 Installing from local wheel...
    if not exist "dist\localutilitybox-0.2.0-py3-none-any.whl" (
        echo ❌ Wheel file not found. Please run 'python -m build' first.
        pause
        exit /b 1
    )
    pip install dist\localutilitybox-0.2.0-py3-none-any.whl
) else if "%choice%"=="4" (
    echo 📦 Installing in development mode...
    pip install -e .
) else (
    echo ❌ Invalid choice. Exiting.
    pause
    exit /b 1
)

REM Verify installation
echo.
echo 🔍 Verifying installation...

png_to_jpg --help >nul 2>&1
if errorlevel 1 (
    echo ❌ png_to_jpg command not found
    pause
    exit /b 1
) else (
    echo ✅ png_to_jpg command found
)

pdf_to_png --help >nul 2>&1
if errorlevel 1 (
    echo ❌ pdf_to_png command not found
    pause
    exit /b 1
) else (
    echo ✅ pdf_to_png command found
)

echo.
echo 🧪 Testing commands...
png_to_jpg --help >nul 2>&1 && echo ✅ png_to_jpg help works || echo ❌ png_to_jpg help failed
pdf_to_png --help >nul 2>&1 && echo ✅ pdf_to_png help works || echo ❌ pdf_to_png help failed

echo.
echo 🎉 Installation completed successfully!
echo.
echo Usage examples:
echo   png_to_jpg input.png output.jpg
echo   pdf_to_png input.pdf -v
echo   csv_to_excel data.csv output.xlsx
echo.
echo For more information, visit: https://github.com/elokwentnie/localutilitybox

pause
