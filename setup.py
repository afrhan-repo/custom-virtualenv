from setuptools import setup, find_packages
import os

# Checking PulseAudio is installed or not

setup(
    name="custom-virtualenv",
    version="0.1.0",
    description="A Python program to create your virtual environment with your desired packages installed in global or system interpreter.",
    long_description=open("README.md").read(),
    long_description_content_type="text/markdown",
    author="afrhan-repo",
    author_email="afrhanhossain11@gmail.com",
    url="https://github.com/afrhan-repo/custom-virtualenv",  # Add your GitHub URL here
    packages=find_packages(),  # Automatically find and include packages
    classifiers=[
        "Programming Language :: Python :: 3",
        "License :: OSI Approved :: MIT License",
        "Operating System :: OS Independent",
    ],
    python_requires=">=3.7",
    install_requires=["virtualenv", "pip-autoremove", "wheel", "inquirer"],
)
