# LocalUtilityBox Distribution Guide

This guide explains how to make LocalUtilityBox installable as a proper package that users can install and use directly from the command line.

## 🚀 **Method 1: PyPI Distribution (Recommended)**

### For Package Maintainers

1. **Prepare for PyPI Upload**:
   ```bash
   # Build the package
   python3 -m build
   
   # Check the package
   python3 -m twine check dist/*
   
   # Upload to Test PyPI first (recommended)
   python3 -m twine upload --repository testpypi dist/*
   
   # Upload to PyPI (production)
   python3 -m twine upload dist/*
   ```

2. **Set up PyPI credentials**:
   - Create account at https://pypi.org
   - Create API token
   - Configure `~/.pypirc`:
   ```ini
   [pypi]
   username = __token__
   password = pypi-your-api-token-here
   ```

### For End Users

Once published to PyPI, users can install with:
```bash
pip install localutilitybox
```

## 📦 **Method 2: GitHub Distribution**

### For Package Maintainers

1. **Push to GitHub**:
   ```bash
   git add .
   git commit -m "Release v0.2.0"
   git tag v0.2.0
   git push origin main --tags
   ```

### For End Users

Users can install directly from GitHub:
```bash
# Install latest version
pip install git+https://github.com/elokwentnie/localutilitybox.git

# Install specific version
pip install git+https://github.com/elokwentnie/localutilitybox.git@v0.2.0

# Install in development mode
git clone https://github.com/elokwentnie/localutilitybox.git
cd localutilitybox
pip install -e .
```

## 🎯 **Method 3: Local Wheel Distribution**

### For Package Maintainers

1. **Build wheel**:
   ```bash
   python3 -m build
   ```

2. **Distribute wheel file**:
   - Share `dist/localutilitybox-0.2.0-py3-none-any.whl`
   - Upload to file sharing service
   - Email to users

### For End Users

Users can install from wheel file:
```bash
# Download wheel file first
pip install localutilitybox-0.2.0-py3-none-any.whl

# Or install directly from URL
pip install https://example.com/path/to/localutilitybox-0.2.0-py3-none-any.whl
```

## 🔧 **Method 4: pipx (Isolated Installation)**

### For End Users

```bash
# Install pipx if not available
brew install pipx  # macOS
# or
python -m pip install pipx  # Other systems

# Install LocalUtilityBox
pipx install localutilitybox

# Or install from GitHub
pipx install git+https://github.com/elokwentnie/localutilitybox.git
```

## 🐍 **Method 5: conda Distribution**

### For Package Maintainers

1. **Create conda recipe**:
   ```yaml
   # meta.yaml
   package:
     name: localutilitybox
     version: "0.2.0"
   
   source:
     git_url: https://github.com/elokwentnie/localutilitybox.git
     git_tag: v0.2.0
   
   build:
     script: python -m pip install . --no-deps
   
   requirements:
     host:
       - python >=3.8
       - pip
     run:
       - python >=3.8
       - pillow >=10.0.0
       - pypdf2 >=3.0.0
       # ... other dependencies
   ```

2. **Build conda package**:
   ```bash
   conda-build .
   ```

### For End Users

```bash
# Install from conda-forge (when available)
conda install -c conda-forge localutilitybox

# Install from local build
conda install --use-local localutilitybox
```

## ✅ **Verification After Installation**

After any installation method, verify it works:

```bash
# Test CLI tools
png_to_jpg --help
pdf_to_png --help
csv_to_excel --help

# Test actual conversion
png_to_jpg input.png output.jpg
```

## 🛠️ **System Dependencies**

Some tools require additional system libraries:

### macOS
```bash
brew install poppler imagemagick
```

### Ubuntu/Debian
```bash
sudo apt-get install poppler-utils imagemagick
```

### Windows
- Download poppler for Windows
- Download ImageMagick for Windows

## 🚨 **Troubleshooting**

### Command not found
```bash
# Check if installed
pip list | grep localutilitybox

# Check PATH
echo $PATH

# Try with python -m
python -m image_processing.png_to_jpg --help
```

### Permission errors
```bash
# Install for user only
pip install --user localutilitybox

# Or use virtual environment
python -m venv venv
source venv/bin/activate  # Linux/Mac
# or
venv\Scripts\activate  # Windows
pip install localutilitybox
```

### Import errors
```bash
# Check dependencies
pip install -r requirements.txt

# Check Python version
python --version  # Should be 3.8+
```

## 📋 **Best Practices**

1. **Always test before distribution**:
   ```bash
   # Test in clean environment
   python -m venv test_env
   source test_env/bin/activate
   pip install dist/localutilitybox-0.2.0-py3-none-any.whl
   png_to_jpg --help
   ```

2. **Version management**:
   - Use semantic versioning (MAJOR.MINOR.PATCH)
   - Update version in both `setup.py` and `pyproject.toml`
   - Tag releases in git

3. **Documentation**:
   - Keep README.md updated
   - Document all installation methods
   - Provide troubleshooting guide

4. **Testing**:
   - Run full test suite before release
   - Test on multiple Python versions
   - Test on different operating systems

## 🎯 **Recommended Distribution Strategy**

1. **Start with GitHub**: Easy to set up, good for development
2. **Add PyPI**: Professional distribution, easy for users
3. **Consider conda**: For scientific computing users
4. **Provide wheels**: For easy installation without compilation

This approach ensures maximum accessibility for different user types and environments.
