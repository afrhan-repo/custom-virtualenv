"""
This program will create a virtual environment with the user selected packages and their dependencies.I have used command line tools such as "rm" or "xcp" to make it faster
"""

import sys
import re
import os
import inquirer
import json
import subprocess
import importlib.util


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

    questions = [
        inquirer.Checkbox(
            "selected_packages",
            message="What packages do you want in your virtual environment?",
            choices=package_name_list,
        )
    ]
    selected_packages = inquirer.prompt(questions)["selected_packages"]  # type: ignore
    return selected_packages


# Function to get dependencies recursively (single argument: list of package names)
def get_nested_dependencies(packages):
    already_seen_packages = set()  # Track visited packages to avoid loops
    all_installed_packages = getAllInstalledPackage()

    def fetch_deps(package_list):
        all_dependencies = []

        for package_name in package_list:
            for pkg in all_installed_packages:  # type: ignore
                if pkg["package"]["package_name"] == package_name:
                    if package_name in already_seen_packages:
                        continue  # Avoid infinite recursion
                    already_seen_packages.add(package_name)

                    # Get direct dependencies
                    dependencies = pkg.get("dependencies", [])
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
            command = ["virtualenv", virtualenv_name, "-p", "python3"]
            subprocess.run(command, check=True, stdout=subprocess.DEVNULL)
            return path_to_venv
        else:
            print("Exiting")
            exit(0)

    else:
        print("Creating virtual environment named ", virtualenv_name)
        command = [
            "virtualenv",
            virtualenv_name,
            "-p",
            "python3",
            "--system-site-packages",
        ]
        subprocess.run(command, check=True, stdout=subprocess.DEVNULL)
        return path_to_venv


def all_selected_Packages_dir(pacakges_list: list) -> list:
    dir_list = []
    missing_dir_packages = []

    def add_to_dir(package_dir):
        if package_dir.endswith("__init__.py"):
            package_dir = package_dir.rsplit("/", 1)[0]
            dir_list.append(package_dir)
        else:
            dir_list.append(package_dir)

    for package in pacakges_list:
        package_spec = importlib.util.find_spec(package)

        # Tring for chainging the package name

        if package_spec is not None:
            add_to_dir(package_spec.origin)        
        else:
            new_package_name = package.replace("-", "_")
            pattern = re.sub(r"^py", "", new_package_name, flags=re.IGNORECASE)
            package_spec = importlib.util.find_spec(pattern.lower())
            if package_spec is not None:
                add_to_dir(package_spec.origin)
            else:
                new_package_name = new_package_name.split("_")[0]
                package_spec = importlib.util.find_spec(new_package_name)
                if package_spec is not None:
                    try:
                        package_dir = list(package_spec.submodule_search_locations)[0]  # type: ignore
                        dir_list.append(package_dir)
                    except:
                        #If submodule_search_locations return None ,then add to missing_dir_packages
                        missing_dir_packages.append(package)
                else:
                    print(
                        f"Could not find the package {package}. Installing them manually."
                    )
                    missing_dir_packages.append(package)
    #Converting the list to set to remove duplicates
    return list(set(dir_list)), missing_dir_packages  # type: ignore


def split_dir_list(folder_list, chunk_size):
    # Splitting the list into dir chunks of 'chunk_size'
    #I did this because copying all the packages at once was taking too long and make code slow
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

#Main function to run the program
def main():
    virtualenv_name = input("Enter the name of the virtual environment: ")
    if virtualenv_name == "":
        print("Please enter a valid name")
        exit(0)

    virtualenv_path = create_virtualenv(virtualenv_name)
    selected_packages = user_package_choice()
    all_dependencies = get_nested_dependencies(selected_packages)
    
    #Determining the python version 
    version_info = sys.version_info
    version = f"{version_info.major}.{version_info.minor}"
    print(version)

    # Get the directory of all the package
    all_packages_directory, missing_dir_packages = all_selected_Packages_dir(
        all_dependencies
    )
    # cooy the packsges to the virtual environment
    spilitted_dir_lists = split_dir_list(all_packages_directory, chunk_size=15)
    for i, package_dir_chunks in enumerate(spilitted_dir_lists):
        defaultCommand = f"xcp --recursive {'* '.join(package_dir_chunks)} {virtualenv_path}/lib/python{version}/site-packages/"

        try:
            #At first checking if xcp is installed
            subprocess.run(["whereis", "xcp"], check=True, stdout=subprocess.DEVNULL)
            subprocess.run(defaultCommand, check=True, shell=True)
        except:
            #Putting * in the command to copy all the .dist-info dirs
            command = f"cp -r {'* '.join(package_dir_chunks)} {virtualenv_path}/lib/python{version}/site-packages/"

                
            subprocess.run(command, check=True, shell=True)

        print(f"{i+1} out of {len(spilitted_dir_lists)} packages dir chunks copied")

    # Install the missing packages in the virtual environment
    install_missing_packages(virtualenv_path, missing_dir_packages)


if __name__ == "__main__":
    main()
