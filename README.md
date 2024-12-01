# LocalUtilityBox
## Don't waste your time searching for web solutions, do it in your terminal.

**LocalUtilityBox** is a versatile command-line utility designed to simplify your image and document processing tasks. With LocalUtilityBox, you can:
* Work locally, keeping your data private and secure.
* Avoid online tools that share your files on external servers.
* Enjoy efficient processing directly from your terminal.

## Features
**LocalUtilityBox** comes packed with tools to make your life easier:
* Image Processing
   * Convert images between formats (e.g., WebP, JPG, PNG).
   * Resize and compress images.
   * Batch-process entire folders.
* PDF Management
   * Split, merge, and extract text or images from PDFs.
   * Convert PDFs to image files for easy use.
* Convenient CLI Tools
   * User-friendly command-line commands for all operations.


## Installation
Get started with **LocalUtilityBox** in just a few steps:

1. Clone the Repository
```bash
git clone https://github.com/elokwentnie/LocalUtilityBox.git
```
2. Navigate to the Project Directory
```bash
cd LocalUtilityBox
```
3. Set Up a Local Python Environment
```bash
python3 -m venv env
source env/bin/activate
```
4. Install Dependencies and Package
Ensure you have pip installed. Then, run:
```bash
pip3 install .
```
This command will install LocalUtilityBox and its dependencies as specified in `requirements.txt`.

## Set Up the `PYTHONPATH`
```bash
export PYTHONPATH=$PYTHONPATH:/path/to/LocalUtilityBox/src
```

## Usage
Once installed, **LocalUtilityBox** provides a set of simple commands for various tasks. Here are a few examples to get you started:
* Image Conversion
  * Convert WebP to JPG:
    ```bash
    webp_to_jpg [-h] [-o OUTPUT_FILE] [-b {white,black}] input_file
    ```
  * Remove background from image
    ```bash
    remove_background [-h] (-f INPUT_FILES [INPUT_FILES ...] | -d INPUT_DIRECTORY)
    ```
* PDF Management
  * Merge PDFs:
    ```bash
    merge_pdf [-h] (-f INPUT_FILES [INPUT_FILES ...] | -d INPUT_DIRECTORY) [-o OUTPUT]
    ```
  * Convert DOC to PDF:
    ```bash
    doc_to_pdf [-h] [-o OUTPUT_FILE] input_file
    ```
  * Extract text from images:
  ```bash
  extract_text_from_img [-h] [-s] input_file
  ```

## Contribute
Have ideas or improvements? Contributions are welcome! Feel free to fork the repository, make your changes, and submit a pull request.

Let me know if there’s anything more you’d like to include or refine!
