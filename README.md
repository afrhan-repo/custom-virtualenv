# Custom Virtual Environment Manager

This Python utility helps manage Python virtual environments, list installed packages, and handle package installations based on a requirements file.

## Features

- Create and manage custom Python virtual environments.
- List all installed packages.
- Install packages interactively or from a requirements file.

## Usage

The tool provides two command-line flags:

1. **Interactive Mode (-i or --interactive)**
   - Use this flag to interactively install or manage packages.
   
   ```bash
   python main.py --interactive
   ```

2. **List Installed Packages (-l or --list)**
   - Use this flag to list all installed packages.
   
   ```bash
   python main.py --list
   ```

## Installation

Ensure you have Python 3.x installed. Clone this repository and run:

```bash
git clone https://github.com/afrhan-repo/custom-virtualenv.git
cd custom-virtualenv
```

## Requirements

If you wish to install packages from a requirements file:

```bash
python main.py --list requirements.txt
```

## License

This project is licensed under the MIT License.

---

This should help users understand how to interact with your tool. Let me know if you need further customization!
