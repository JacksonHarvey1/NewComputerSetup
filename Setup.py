import os
import subprocess
import winreg as reg

def run_exe_files_in_folder(folder_path):
    try:
        # Check if the folder exists
        if not os.path.exists(folder_path):
            print(f"The folder '{folder_path}' does not exist.")
            return

        # Get a list of all .exe files in the folder
        exe_files = [f for f in os.listdir(folder_path) if f.endswith('.exe')]

        if not exe_files:
            print("No .exe files found in the folder.")
            return

        # Execute each .exe file
        for exe_file in exe_files:
            exe_path = os.path.join(folder_path, exe_file)
            print(f"Running: {exe_path}")

            try:
                # Use subprocess to run the .exe file
                subprocess.run([exe_path], check=True)
            except subprocess.CalledProcessError as e:
                print(f"Error occurred while running {exe_file}: {e}")
            except Exception as e:
                print(f"Unexpected error occurred: {e}")

    except Exception as e:
        print(f"An error occurred: {e}")

def install_requirements_from_file(requirements_file):
    try:
        # Check if the file exists
        if not os.path.exists(requirements_file):
            print(f"The file '{requirements_file}' does not exist.")
            return

        # Read the file line by line to get the packages
        with open(requirements_file, 'r') as file:
            packages = file.readlines()

        # Remove whitespace and empty lines
        packages = [pkg.strip() for pkg in packages if pkg.strip()]

        if not packages:
            print("The requirements file is empty or invalid.")
            return

        # Install each package using pip
        for package in packages:
            print(f"Installing: {package}")
            try:
                subprocess.run(["pip", "install", package], check=True)
            except subprocess.CalledProcessError as e:
                print(f"Error occurred while installing {package}: {e}")
            except Exception as e:
                print(f"Unexpected error occurred: {e}")

    except Exception as e:
        print(f"An error occurred: {e}")
def add_to_path(path):
    """
    Add Tesseract installation directory to system PATH.
    
    Modifies Windows registry to include Tesseract in system-wide PATH,
    enabling OCR functionality across the system.
    """
    try:
        # Open system PATH environment variable in registry
        reg_key = reg.OpenKey(reg.HKEY_LOCAL_MACHINE, 
                            r"SYSTEM\CurrentControlSet\Control\Session Manager\Environment", 
                            0, 
                            reg.KEY_READ | reg.KEY_WRITE)

        # Retrieve current PATH value
        current_path, _ = reg.QueryValueEx(reg_key, "Path")

        # Add Tesseract path if not already present
        if path not in current_path:
            updated_path = f"{current_path};{path}"
            reg.SetValueEx(reg_key, "Path", 0, reg.REG_EXPAND_SZ, updated_path)
            print(f"Added {path} to PATH.")
        else:
            print(f"{path} is already in PATH.")

        reg.CloseKey(reg_key)
    
    except PermissionError:
        # Handle lack of administrative privileges
        print("Access denied: Run the script as an administrator.")
    
    except Exception as e:
        # Log any unexpected errors during PATH modification
        print(f"Error: {e}")

def process_lines_from_file(file_path, function):
    try:
        # Check if the file exists
        if not os.path.exists(file_path):
            print(f"The file '{file_path}' does not exist.")
            return

        # Read the file line by line and pass each line to the function
        with open(file_path, 'r') as file:
            for line in file:
                line = line.strip()
                if line:  # Skip empty lines
                    function(line)

    except Exception as e:
        print(f"An error occurred while processing the file: {e}")
# Example usage
if __name__ == "__main__":
    run_exe_files_in_folder("Apps Installed")
    install_requirements_from_file("requirements.txt")
    process_lines_from_file("enviromentVariables.txt", add_to_path)