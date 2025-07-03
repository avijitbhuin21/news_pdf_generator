import os
import shutil

def install_wkhtmltopdf():
    # Check if wkhtmltopdf is available in PATH
    if shutil.which('wkhtmltopdf'):
        print("wkhtmltopdf is already installed and available in PATH!")
        return True
    else:
        print("wkhtmltopdf not found. Installing...")
        
        # Run the installation command
        exit_code = os.system('sudo apt-get update && sudo apt-get install -y wkhtmltopdf')
        
        if exit_code == 0:
            print("Installation successful!")
            return True
        else:
            print(f"Installation failed with exit code: {exit_code}")
            return False