# LocalUtilityBox GUI Guide

## 🖥️ **Graphical User Interface**

LocalUtilityBox now includes a comprehensive graphical user interface that makes all file processing tools accessible without using the command line!

## 🚀 **Quick Start**

### **Installation with GUI Support**
```bash
# Install LocalUtilityBox with GUI
pip install localutilitybox

# Or install from source
git clone https://github.com/elokwentnie/localutilitybox.git
cd localutilitybox
pip install -e .

# Install GUI dependencies
python install_gui.py
```

### **Launch GUI**
```bash
# Method 1: Using the GUI command
localutilitybox-gui

# Method 2: Using Python launcher
python src/gui/launcher.py

# Method 3: Using the launcher script
python launch_gui.py
```

## 🎯 **GUI Features**

### **🖼️ Image Processing Tab**
- **Format Conversion**: WebP ↔ PNG, JPG ↔ PNG, TIFF → JPG, HEIC → JPG
- **Image Processing**: Convert to greyscale, reduce size, remove background
- **Metadata Extraction**: Extract EXIF data and image information
- **OCR**: Extract text from images using optical character recognition
- **Batch Processing**: Process multiple images at once
- **Quality Control**: Adjust image quality and compression settings

### **📄 PDF Management Tab**
- **Merge PDFs**: Combine multiple PDF files into one
- **Split PDFs**: Split into individual pages or custom parts
- **Convert to Images**: Convert PDF pages to PNG or JPG images
- **Convert to DOCX**: Convert PDF to editable Word documents
- **Add Watermarks**: Add text watermarks to PDF files
- **Batch Processing**: Process multiple PDFs simultaneously

### **📊 Document Conversion Tab**
- **CSV ↔ Excel**: Convert between CSV and Excel formats
- **CSV ↔ JSON**: Convert between CSV and JSON formats
- **Format Options**: Customize separators, JSON formatting, and indexing
- **Batch Processing**: Convert multiple documents at once

### **🎵 Audio/Video Tab**
- **Extract Audio**: Extract audio from video files
- **Format Support**: MP4, AVI, MOV, MKV, and more
- **Audio Formats**: MP3, WAV, AAC, FLAC, OGG
- **Quality Settings**: Adjust audio and video quality
- **Batch Processing**: Process multiple media files

## 🎨 **GUI Interface Features**

### **Modern Design**
- **Tabbed Interface**: Organized by tool categories
- **Drag & Drop**: Easy file selection (coming soon)
- **Progress Tracking**: Real-time progress bars and status updates
- **Error Handling**: Clear error messages and validation
- **Responsive Layout**: Adapts to different screen sizes

### **User-Friendly Controls**
- **File Selection**: Browse files or entire folders
- **Output Directory**: Choose where to save processed files
- **Options Panel**: Customize processing parameters
- **Preview Mode**: Preview operations before execution
- **Reset Function**: Clear all settings and start over

### **Advanced Features**
- **Multi-threading**: Non-blocking operations
- **Batch Processing**: Handle multiple files simultaneously
- **Progress Monitoring**: Real-time status updates
- **Error Recovery**: Graceful error handling and reporting
- **Logging**: Detailed operation logs for debugging

## 📋 **Usage Examples**

### **Image Processing**
1. **Open GUI**: Launch `localutilitybox-gui`
2. **Select Images**: Go to Image Processing tab, click "Add Files"
3. **Choose Operation**: Select conversion type (e.g., WebP to PNG)
4. **Set Options**: Adjust quality, size reduction, etc.
5. **Process**: Click "Process Images" and watch the progress

### **PDF Management**
1. **Select PDFs**: Add multiple PDF files
2. **Choose Operation**: Select merge, split, or convert
3. **Configure Settings**: Set output directory, quality, etc.
4. **Process**: Click "Process PDFs" to start

### **Document Conversion**
1. **Add Documents**: Select CSV, Excel, or JSON files
2. **Choose Format**: Select target format
3. **Set Options**: Configure separators, formatting
4. **Convert**: Process all documents at once

## 🛠️ **System Requirements**

### **Minimum Requirements**
- **Python**: 3.8 or higher
- **RAM**: 512 MB available
- **Disk Space**: 100 MB for installation
- **OS**: Windows 10+, macOS 10.14+, or Linux

### **GUI Dependencies**
- **tkinter**: Usually included with Python
- **Pillow**: For image processing
- **opencv-python**: For advanced image operations
- **tkcolorpicker**: For color selection (optional)

### **Installation Check**
```bash
# Check if GUI requirements are met
python src/gui/launcher.py

# If tkinter is missing (Linux):
sudo apt-get install python3-tk

# If Pillow is missing:
pip install Pillow
```

## 🚨 **Troubleshooting**

### **GUI Won't Start**
```bash
# Check Python version
python --version  # Should be 3.8+

# Check tkinter
python -c "import tkinter"

# Check dependencies
pip install -r requirements.txt
```

### **Import Errors**
```bash
# Reinstall package
pip uninstall localutilitybox
pip install -e .

# Check path
python -c "import sys; print(sys.path)"
```

### **Performance Issues**
- **Close other applications** to free up memory
- **Process files in smaller batches** for large operations
- **Use SSD storage** for better performance
- **Increase virtual memory** if needed

## 🎯 **Keyboard Shortcuts**

- **Ctrl+O**: Open files
- **Ctrl+D**: Add folder
- **Ctrl+R**: Reset form
- **Ctrl+P**: Preview operation
- **F5**: Refresh file list
- **Escape**: Cancel operation

## 🔧 **Advanced Configuration**

### **Custom Settings**
- **Quality Settings**: Adjust image/video quality
- **Output Formats**: Choose preferred output formats
- **Batch Size**: Set number of files to process simultaneously
- **Log Level**: Configure logging verbosity

### **Integration with CLI**
- **Hybrid Usage**: Use GUI for complex operations, CLI for quick tasks
- **Script Integration**: Call GUI functions from Python scripts
- **Automation**: Use GUI for one-time setup, CLI for automation

## 📚 **Development**

### **Adding New GUI Tools**
1. Create new module in `src/gui/`
2. Import in `main_app.py`
3. Add tab in `create_widgets()`
4. Update entry points in `setup.py`

### **Customizing Interface**
- **Themes**: Modify `setup_main_window()` for different themes
- **Layout**: Adjust grid weights and padding
- **Colors**: Update style configurations
- **Fonts**: Change font families and sizes

## 🎉 **Benefits of GUI**

### **For End Users**
- **No Command Line**: Point-and-click interface
- **Visual Feedback**: See progress and results
- **Error Prevention**: Validation and warnings
- **Batch Operations**: Process multiple files easily

### **For Developers**
- **Easy Testing**: Visual interface for testing tools
- **User Feedback**: See how tools work in practice
- **Debugging**: Visual error messages and logs
- **Integration**: Combine GUI and CLI workflows

## 🚀 **Future Enhancements**

- **Drag & Drop**: Direct file dropping support
- **Preview Window**: Preview files before processing
- **Theme Support**: Dark/light mode themes
- **Plugin System**: Add custom tools
- **Cloud Integration**: Direct cloud storage support
- **Mobile App**: Companion mobile application

The LocalUtilityBox GUI makes file processing accessible to everyone, regardless of technical expertise! 🎯
