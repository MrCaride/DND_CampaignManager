import subprocess
import sys

def uninstall_all_packages():
    # Get the list of installed packages
    installed_packages = subprocess.check_output([sys.executable, "-m", "pip", "freeze"]).decode().splitlines()
    for package in installed_packages:
        package_name = package.split('==')[0]
        subprocess.call([sys.executable, "-m", "pip", "uninstall", package_name, "-y"])

if __name__ == "__main__":
    uninstall_all_packages()
