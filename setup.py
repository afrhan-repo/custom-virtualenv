from setuptools import setup, find_packages

setup(
    name="custom-virtualenv",
    version="1.0.2",
    description="Custom Virtual Environment Manager is a utility that allows you to create virtual environments with packages of your choice, based on the Python packages installed globally on your system.",
    long_description=open("README.md").read(),
    long_description_content_type="text/markdown",
    author="afrhan-repo",
    author_email="afrhanhossain11@gmail.com",
    url="https://github.com/afrhan-repo/custom-virtualenv",
    packages=find_packages(),
    py_modules=["main"],
    entry_points={"console_scripts": ["custom-virtualenv=main:main"]},
    classifiers=[
        "Programming Language :: Python :: 3",
        "License :: OSI Approved :: MIT License",
        "Operating System :: OS Independent",
    ],
    python_requires=">=3.7",
    install_requires=["InquirerPy","pipdeptree"],
)
