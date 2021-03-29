# -*- coding: utf-8 -*-

try:
    from setuptools import setup
except ImportError:
    from distutils.core import setup

readme = ""

setup(
    long_description=readme,
    name="geoLife",
    version="0.0.0",
    python_requires=">=3.7",
    packages=["geoLife"],
    package_dir={"geoLife": "src"},
    package_data={},
    install_requires=[
        "click",
        "geopy",
        "matplotlib",
        "numpy",
        "opencv-python",
        "pandas",
        "pillow",
        "python-dotenv",
        "scikit-image",
        "seaborn",
    ],
    extras_require={"dev": ["black", "ipykernel", "pylint"]},
    entry_points={
        "console_scripts": ["geoheatmap=src.cli:cli"],
    },
)
