# backend/setup.py
from setuptools import setup, find_packages

setup(
    name="snapqr-backend",
    version="0.1.0",
    package_dir={"": "app"},
    packages=find_packages(where="app"),
)

