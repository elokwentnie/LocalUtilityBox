#!/usr/bin/env python

from setuptools import setup, find_packages

# Function to read the requirements.txt file
def read_requirements():
    with open('requirements.txt') as req_file:
        return req_file.readlines()

setup(
    name='LocalUtilityBox',
    version='0.2.0',
    packages=find_packages(where='src'),
    package_dir={'': 'src'},
    install_requires=read_requirements(),
    entry_points={
        'console_scripts': [
            'webp_to_jpg=image_processing.webp_to_jpg:main',
            'webp_to_png=image_processing.webp_to_png:main',
            'jpg_to_png=image_processing.jpg_to_png:main',
            'png_to_jpg=image_processing.png_to_jpg:main',
            'tiff_to_jpg=image_processing.tiff_to_jpg:main',
            'img_to_pdf=image_processing.img_to_pdf:main',
            'img_to_greyscale=image_processing.img_to_greyscale:main',
            'heic_to_jpg=image_processing.heic_to_jpg:main',
            'reduce_img_size=image_processing.reduce_img_size:main',
            'remove_background=image_processing.remove_background:main',
            'extract_img_metadata=image_processing.extract_img_metadata:main',
            'extract_text_from_img=image_processing.extract_text_from_img:main',

            'merge_pdf=file_management.merge_pdf:main',
            'add_watermark=file_management.add_watermark:main',
            'doc_to_pdf=file_management.doc_to_pdf:main',
            'pdf_to_doc=file_management.pdf_to_doc:main',
            'split_pdf=file_management.split_pdf:main',
            'pdf_to_png=file_management.pdf_to_png:main',
            'pdf_to_jpg=file_management.pdf_to_jpg:main',
            'csv_to_excel=file_management.csv_to_excel:main',
            'excel_to_csv=file_management.excel_to_csv:main',
            'csv_to_json=file_management.csv_to_json:main',
            'json_to_csv=file_management.json_to_csv:main',

            'extract_audio_from_video=video_audio_manipulation.extract_audio_from_video:main',
            
            # GUI applications
            'localutilitybox-gui=src.gui.launcher:main',
        ]
    }
)