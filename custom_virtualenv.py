# Write a descriptiong for this project
# This is a utility that allows you to create virtual environments with packages of your choice, based on the Python packages installed globally on your system.
# This utility will create a virtual environment with the name provided by the user and then copy the packages to the virtual environment.
# The user can choose the packages they want in the virtual environment, and the utility will copy the packages to the virtual environment.
# The utility will also install any missing packages in the virtual environment.
# The user can run the utility in interactive mode or provide a requirements file with the packages they want in the virtual environment.
# In this project I have used commands like "rm" and "cp" which are unix commands, so this script will only work on unix based systems like linux and macos.The reason behind using this is that it is more faster than shutil module functions.

import argparse
from virtualenv import cli_run as create_venv
import sys
import re
import os
from InquirerPy import inquirer
import json
import subprocess
import importlib.util ,importlib.metadata


# Get all installed packages in user global environment
def getAllInstalledPackage():
    command = ["pipdeptree", "--warn", "silence", "--json"]
    try:
        result = subprocess.run(command, check=True, stdout=subprocess.PIPE)
        parsed_json = json.loads(result.stdout.decode("utf-8"))
        return parsed_json
    except json.JSONDecodeError as e:
        print("Could not parse JSON")
        print(e)
        return None
    except Exception as e:
        print(e)
        return None


# Taking the user input
def user_package_choice():
    all_packages = getAllInstalledPackage()  # Get all all_packages

    package_name_list = [package["package"]["package_name"] for package in all_packages]  # type: ignore

    selected_packages = inquirer.fuzzy(message="What packages do you want in your venv:", choices=package_name_list, multiselect=True, max_height="79%", keybindings={"toggle": [{"key": "space"}]}).execute()  # type: ignore
    return selected_packages


# Function to get dependencies recursively (single argument: list of package names)


def get_nested_dependencies(packages: list):
    already_seen_packages = set()  # Track visited packages to avoid loops
    all_installed_packages = getAllInstalledPackage()

    # Create a dictionary for quick lookup of packages
    package_dict = {pkg["package"]["package_name"]: pkg for pkg in all_installed_packages}  # type: ignore

    def fetch_deps(package_list):
        all_dependencies = []

        for package_name in package_list:
            if package_name in already_seen_packages:
                continue  # Skip if already seen to avoid infinite recursion

            already_seen_packages.add(package_name)

            # Check if the package exists in the installed packages
            package = package_dict.get(package_name)
            all_dependencies.append(package_name)  # Always include the package itself
            if package:
                # Get direct dependencies
                dependencies = package.get("dependencies", [])
                direct_deps = [dep["package_name"] for dep in dependencies]
                all_dependencies.extend(direct_deps)

                # Recursively get dependencies of each dependency
                nested_deps = fetch_deps(direct_deps)
                all_dependencies.extend(nested_deps)

        return all_dependencies

    return fetch_deps(packages)


def create_virtualenv(virtualenv_name) -> str:
    """
    Creates a virtual environment with the given name.

        Args:
            virtualenv_name (str): The name for the virtual environment.

        Returns:
            str: The path to the created virtual environment.

    """
    cwd = os.getcwd()

    # Path to the virtual environment
    path_to_venv = os.path.join(cwd, virtualenv_name)

    # command_to_create_venv = ["virtualenv", virtualenv_name, "-p", "python3"]
    # Check if the virtual environment already exists
    if os.path.exists(path_to_venv):
        print("Virtual environment already exists")
        choice = input(
            "Do you want to delete the existing virtual environment and create a new one? (y/N): "
        )
        if choice.lower() == "y":
            print("Deleting existing virtual environment")
            command = ["rm", "-rf", path_to_venv]
            subprocess.run(command, check=True)
            print("Creating a new virtual environment")
            # Create a new virtual environment
            create_venv(([path_to_venv]))
            return path_to_venv
        else:
            print("Exiting")
            exit(0)

    else:
        print("Creating virtual environment named ", virtualenv_name)
        create_venv(([path_to_venv]))
        return path_to_venv

#Get the directory of all the packages and their metadata
def all_selected_Packages_dir(pacakges_list: list) -> list:
    dir_list = []
    missing_dir_packages = []

    # Function to get the metadata directory of a package
    def add_metadata_dir(package_name : str):
        try:
            metadata_dir = importlib.metadata.distribution(package_name).locate_file(f"{package_name}.dist-info")
            dir_list.append(metadata_dir)
        except:
            missing_dir_packages.append(package_name)

    def add_to_dir(package_name,package_dir):
        try :
            dir_list.append(package_dir[0])
            #If thr package directory is found then add the metadata directory
            add_metadata_dir(package_name)
        except:
            missing_dir_packages.append(package)
    for package in pacakges_list:
        package_spec = importlib.util.find_spec(package)

        # Tring for chainging the package name

        if package_spec is not None:
            add_to_dir(package,package_spec.submodule_search_locations)
        else:
            new_package_name = package.replace("-", "_")
            pattern = re.sub(r"^py", "", new_package_name, flags=re.IGNORECASE)
            package_spec = importlib.util.find_spec(pattern.lower())
            if package_spec is not None:
                add_to_dir(package,package_spec.submodule_search_locations)
            else:
                new_package_name = new_package_name.split("_")[0]
                package_spec = importlib.util.find_spec(new_package_name)

                if package_spec is not None:
                    add_to_dir(package,package_spec.submodule_search_locations)
                else:
                    # If package_spec is None, then add to missing_dir_packages
                    missing_dir_packages.append(package)

    if len(missing_dir_packages) != 0:
        print("The following packages could not be found: ", missing_dir_packages, " Installing them through pip\n")

    # Converting the list to set to remove duplicates
    return list(set(dir_list)), missing_dir_packages  # type: ignore


def split_dir_list(folder_list, chunk_size):
    # Splitting the list into dir chunks of 'chunk_size'
    # I did this because copying all the packages at once was taking too long and make code slow
    return [
        folder_list[i : i + chunk_size] for i in range(0, len(folder_list), chunk_size)
    ]


def install_missing_packages(venv_path, missing_dir_packagesissingPackages):
    if len(missing_dir_packagesissingPackages) == 0:
        return  # No missing packages to install
    else:
        pip_path = os.path.join(venv_path, "bin", "pip")

        # Installing those packages whose directory could not be copied to vorutal environment
        subprocess.run(
            [f"{pip_path}", "install"] + missing_dir_packagesissingPackages, check=True
        )


def parse_arguments():
    parser = argparse.ArgumentParser(
        description="Custom Virtual Environment Manager is a utility that allows you to create virtual environments with packages of your choice, based on the Python packages installed globally on your system."
    )

    group = parser.add_mutually_exclusive_group(required=True)
    group.add_argument(
        "-i", "--interactive", action="store_true", help="Run in interactive mode"
    )
    group.add_argument("-l", "--list", metavar="file", help="Provide requirements file")

    return parser.parse_args()


# Main function to run the program
def main():

    args = parse_arguments()

    if len(sys.argv) == 1:  # No arguments provided
        print("Error: No arguments provided. Use -i or -l flags.")
        sys.exit(1)
    virtualenv_name = input("Enter the name of the virtual environment: ")
    if virtualenv_name == "":
        print("Please enter a valid name")
        sys.exit(1)

    virtualenv_path = create_virtualenv(virtualenv_name)

    # Parsing the arguments

    if args.interactive:
        print("\nRunning in interactive mode")
        selected_packages = user_package_choice()
    elif args.list:
        with open(args.list) as f:
            # Removing version number from the package names
            selected_packages = [line.split("==")[0] for line in f.read().splitlines()]

    all_dependencies = get_nested_dependencies(selected_packages)  # type: ignore

    # Determining the python version
    version_info = sys.version_info
    version = f"{version_info.major}.{version_info.minor}"

    # Get the directory of all the package
    all_packages_directory, missing_dir_packages = all_selected_Packages_dir(
        all_dependencies
    )

    # Path to site-packages directory
    site_packages_path = f"{virtualenv_path}/lib/python{version}/site-packages/"

    # cooy the packsges to the virtual environment
    spilitted_dir_lists = split_dir_list(all_packages_directory, chunk_size=5)
    for i, package_dir_chunks in enumerate(spilitted_dir_lists):

        # Putting * in the command to copy all the .dist-info dirs
        command = f"cp -r {' '.join(package_dir_chunks)} {site_packages_path}"

        subprocess.run(command, check=True, shell=True)
        print(f"{i+1} out of {len(spilitted_dir_lists)} packages dir chunks copied")

    # Install the missing packages in the virtual environment
    install_missing_packages(virtualenv_path, missing_dir_packages)


if __name__ == "__main__":
    main()
