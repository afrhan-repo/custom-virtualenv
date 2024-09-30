import os
import inquirer
import json
import subprocess


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
        ),
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
            for pkg in all_installed_packages:  #type: ignore
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


def create_virtualenv(virtualenv_name):
    cwd = os.getcwd()

    #Path to the virtual environment
    path_to_venv = os.path.join(cwd,virtualenv_name)

    #Check if the virtual environment already exists
    if os.path.exists(path_to_venv):
        print("Virtual environment already exists")
        choice = input("Do you want to delete the existing virtual environment and create a new one? (y/N): ")
        if choice.lower() == "y":
            print("Deleting existing virtual environment")
            command = ["rm", "-rf", path_to_venv]
            subprocess.run(command, check=True)
            print("Creating a new virtual environment")
            command = ["virtualenv" ,virtualenv_name , "-p","python3"]
        else:
            print("Exiting")
            exit(0)

    else:
        print("Creating virtual environment named ",virtualenv_name)
        command = ["virtualenv" ,virtualenv_name , "-p","python3","--system-site-packages"]
        subprocess.run(command,check=True,stdout=subprocess.DEVNULL)


def main():
    virtualenv_name = input("Enter the name of the virtual environment: ")
    create_virtualenv(virtualenv_name)
    selected_packages = user_package_choice()
    all_dependencies = get_nested_dependencies(selected_packages)
    

if __name__ == "__main__":
    main()
