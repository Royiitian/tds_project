
import subprocess
import sys
import os
import urllib.request
import faker

'''
A1. Install uv (if required) and run https://raw.githubusercontent.com/sanand0/tools-in-data-science-public/tds-2025-01/project-1/datagen.py with ${user.email} as the only argument. 
(NOTE: This will generate data files required for the next tasks.)
'''

# Define the user's email (Replace this with an actual email or get it dynamically)
user_email = os.getenv("USER_EMAIL", "23f1001348@ds.study.iitm.ac.in")
output_path = os.getenv("OUTPUT_PATH", "./data")  # Default path is "./data"
url = "https://raw.githubusercontent.com/sanand0/tools-in-data-science-public/tds-2025-01/project-1/datagen.py"
script_path = "datagen.py"

def execute_task(filename: str, targetfile: str, email: str) -> str:
    install_uv()
    url = filename
    script_path = targetfile
    user_email = email
    download_script(url, script_path)
    clean_output_directory(output_path)
    run_script(script_path, user_email, output_path)
    return f"Data generation at {output_path} from { targetfile } complete."

  
def install_uv():
    """Check if `uv` is installed, and install it if necessary."""
    print("🚀 Checking if uv is installed...")
    try:
        subprocess.run(["uv", "--version"], check=True, stdout=subprocess.PIPE, stderr=subprocess.PIPE)
        print("✅ uv is already installed.")
    except subprocess.CalledProcessError:
        print("🚀 Installing uv...")
        subprocess.run([sys.executable, "-m", "pip", "install", "uv"], check=True)
        print("✅ uv installed successfully.")
    except FileNotFoundError:
        print("🚀 Installing uv...")
        subprocess.run([sys.executable, "-m", "pip", "install", "uv"], check=True)
        print("✅ uv installed successfully.")

def download_script(url, script_path):
    """Download a script from a given URL."""
    if os.path.exists(script_path):
        os.remove(script_path)
    print(f"⬇️ Downloading {script_path}...")
    try:
        urllib.request.urlretrieve(url, script_path)
        print("✅ Download complete.")
    except Exception as e:
        print(f"❌ Error downloading script: {e}")

def clean_output_directory(output_path):
    """Remove the specified output directory."""
    print(f"🚀 Cleaning the output directory: {output_path}")
    subprocess.run(["rm", "-rf", output_path], check=True)

def run_script(script_path, user_email, output_path):
    """Run the downloaded script with the given email and output path."""
    print(f"🚀 Running {script_path} with arguments: Email='{user_email}', Path='{output_path}'")
    subprocess.run([sys.executable, script_path, user_email, "--root", output_path], check=True)
    print("✅ Data generation complete.")
