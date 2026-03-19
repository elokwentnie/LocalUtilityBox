#!/usr/bin/env python

from setuptools import setup, find_packages
from pathlib import Path


def _base_path():
    return Path(__file__).parent


def read_requirements():
    return (_base_path() / 'requirements.txt').read_text(encoding='utf-8').strip().splitlines()


setup(
    name='localutilitybox',
    version='1.1.0',
    packages=find_packages(where='src'),
    py_modules=['cli'],
    package_dir={'': 'src'},
    python_requires='>=3.9',
    install_requires=read_requirements(),
    extras_require={
        'rembg': ['rembg[cpu]'],
        'dnd': ['tkinterdnd2'],
        'qr': ['qrcode[pil]'],
    },
    description='A versatile utility for local image and document processing',
    long_description=(_base_path() / 'README.md').read_text(encoding='utf-8'),
    long_description_content_type='text/markdown',
    author='localutilitybox Contributors',
    url='https://github.com/elokwentnie/localutilitybox',
    classifiers=[
        'Programming Language :: Python :: 3',
        'License :: OSI Approved :: MIT License',
        'Operating System :: OS Independent',
        'Operating System :: Microsoft :: Windows',
        'Operating System :: POSIX :: Linux',
        'Operating System :: MacOS',
    ],
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
            'long_png_to_pdf=image_processing.long_png_to_pdf:main',
            'photos_to_gif=image_processing.photos_to_gif:main',

            'merge_pdf=file_management.merge_pdf:main',
            'compress_pdf=file_management.compress_pdf:main',
            'rotate_pdf=file_management.rotate_pdf:main',
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
            'video_to_gif=video_audio_manipulation.video_to_gif:main',
            'generate_qr=image_processing.generate_qr:main',

            'localutilitybox=cli:main',
            'lub=cli:main',
            'localutilitybox-gui=gui.main_gui:main',
            'lub-gui=gui.main_gui:main',
        ]
    },
)