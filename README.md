# Custom-Virtualenv

This Python utility helps manage Python virtual environments, list installed packages, and handle package installations based on a requirements file.

## Features

- Create and manage custom Python virtual environments.
- Install packages interactively or from a requirements file.

## Installation

1. Install the package using pip.

   ```bash
   pip install custom-virtualenv
   ```
## Usage

The tool provides two command-line flags:

1. **Interactive Mode (-i or --interactive)**
   - Use this flag to interactively install  packages.
   
   ```bash
   custom-virtualenv --interactive
   ```

2. **Install python packages from requirements.txt file (-l or --list)**
   - Use this flag to install all installed packages from requirements.txt.
   
   ```bash
   custom-virtualenv --list requirements.txt
   ```



## License

This project is licensed under the MIT License.

---


