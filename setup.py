from setuptools import setup, find_packages
import sys


# Check if the platform is Windows
if sys.platform == "win32":
    sys.exit("This utility is not supported on Windows.")

setup(
    name="custom-virtualenv",
    version="2.0.0",
    description="Custom Virtual Environment Manager is a utility that allows you to create virtual environments with packages of your choice, based on the Python packages installed globally on your system.",
    long_description=open("README.md").read(),
    long_description_content_type="text/markdown",
    author="afrhan-repo",
    author_email="afrhanhossain11@gmail.com",
    url="https://github.com/afrhan-repo/custom-virtualenv",
    packages=find_packages(),
    py_modules=["custom_virtualenv"],
    entry_points={"console_scripts": ["custom-virtualenv=custom_virtualenv:main"]},
    classifiers=[
        "Programming Language :: Python :: 3",
        "License :: OSI Approved :: MIT License",
        "Operating System :: POSIX :: Linux",
        "Operating System :: MacOS",
    ],
    python_requires=">=3.7",
    install_requires=["InquirerPy", "pipdeptree", "virtualenv"],
)
