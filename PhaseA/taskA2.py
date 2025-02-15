
import subprocess, sys, os, time
from pathlib import Path
from AIProxy import get_completions

def execute_task(filename: str, targetfile: str) -> str:
    #format_markdown_with_openai(filename)
    formatted_text = format_markdown(filename)
    #print(formatted_text)
    if formatted_text:
        os.remove(filename) # Remove the original file
        with open(filename, "w", encoding="utf-8") as file:
            file.write(formatted_text)
        return filename

def format_markdown(input_file: str):
    """Format a Markdown file using Prettier 3.4.2 and return formatted content."""
    
    input_path = Path(input_file)
    
    # Check if file exists
    if not input_path.exists():
        return {"error": f"File '{input_file}' not found"}

    # Run Prettier via subprocess
    try:
        result = subprocess.run(
            ["npx", "prettier@3.4.2", "--parser", "markdown", "--stdin-filepath", "format.md"],
            input=input_path.read_text(),  # Pass file content as stdin
            capture_output=True,
            text=True,
            check=True
        )
        return result.stdout  # Return formatted content

    except subprocess.CalledProcessError as e:
        return {"error": "Prettier formatting failed", "details": e.stderr}

def one_more_try():
    # Run Prettier and save the formatted output to a new file
    # Define file paths
    input_file = "./data/format.md"
    output_file = "./data/format-formatted.md"
    try:
        result = subprocess.run(
            ["npx", "prettier@3.4.2", "--parser", "markdown", input_file],
            capture_output=True,
            text=True,
            check=True
        )

        # Write the formatted output to the new file
        with open(output_file, "w", encoding="utf-8") as file:
            file.write(result.stdout)

        print(f"Formatted Markdown saved to {output_file}")

    except subprocess.CalledProcessError as e:
        print(f"Error running Prettier: {e.stderr}")

def format_markdown_with_openai(filename):
    """
    Reads a Markdown file, formats it using OpenAI, and writes the formatted content back.
    """
    # Read the original file
    with open(filename, "r", encoding="utf-8") as file:
        markdown_text = file.read()
    
    response = get_completions([
            {"role": "system", "content": "You are a Markdown formatter. Improve readability, fix spacing, and ensure proper Markdown syntax. return only the formatted content"},
            {"role": "user", "content": f"Format this Markdown document:{markdown_text}"}
        ])

    # Extract the formatted content
    formatted_text = response
    #print(f"Formatted content: {formatted_text}")

    # Write the formatted content back to the file
    with open("./data/formatted_text.md", "w", encoding="utf-8") as file:
        file.write(formatted_text)
    
    return f"Formatted Markdown file: {filename}"

def format_run_task(filename: str) -> str:
    # Run Prettier to format the file in-place
    try:
        result = subprocess.run(
            ["npx", "prettier@3.4.2", "--write --prose-wrap always --trailing-comma all --print-width 80 --tab-width 2 --use-tabs false ", filename],
            capture_output=True,
            text=True,
            check=True
        )
        print(f"Formatted {filename} successfully. Output: {result.stdout}")
    except subprocess.CalledProcessError as e:
        print(f"Error running Prettier: {e}")
    except FileNotFoundError:
        print("Prettier (npx) not found. Make sure Node.js and Prettier are installed.")

def prettify_markdown(file_path):
    # Run Prettier using npx
    get_prettier_version()
    print(f"🚀 Formatting {file_path} using Prettier...")
    last_modified = os.path.getmtime(file_path)
    try:
        # Read the file content
        with open(file_path, "r", encoding="utf-8") as file:
            content = file.read()

        # Run Prettier with absolute path (avoids relative path issues in Docker)
        formatted = subprocess.run(
            ["npx", "prettier@3.4.2", "--stdin-filepath", f".{os.path.abspath(file_path)}"],
            input=content,
            capture_output=True,
            text=True,
            check=True,
            shell=True,  # ✅ Ensure npx is executed correctly
        ).stdout

        # Write formatted content back to the same file
        with open(file_path, "w", encoding="utf-8") as file:
            file.write(formatted)

        print(f"✅ Successfully formatted {file_path}")
    except subprocess.CalledProcessError as e:
        print(f"Error formatting {file_path}: {e}")
    except FileNotFoundError:
        print("npx or Prettier is not installed. Install Node.js and try again.")
        
    # Wait briefly and check if the file was actually modified
    time.sleep(1)  # Give filesystem time to register changes
    new_modified = os.path.getmtime(file_path)

    if new_modified > last_modified:
        print(f"✅ Changes persisted successfully.")
    else:
        print(f"⚠️ Warning: No changes detected{new_modified}. Check Prettier output.")


def format_with_prettier(file_path):
    """Formats a markdown file using Prettier inside a Docker container."""
    abs_path = os.path.abspath(file_path)
    print(f"🚀 Formatting {abs_path} using Prettier...")

    try:
        with open(abs_path, "r", encoding="utf-8") as file:
            content = file.read()

        formatted = subprocess.run(
            ["npx", "prettier@3.4.2", "--stdin-filepath", abs_path],
            input=content,
            capture_output=True,
            text=True,
            check=True,
            shell=True  # ✅ Required in Docker
        ).stdout

        if formatted:
            with open(abs_path, "w", encoding="utf-8") as file:
                file.write(formatted)
            print(f"✅ Formatted {abs_path} successfully.")
        else:
            print(f"⚠️ Prettier returned an empty output for {abs_path}.")

    except subprocess.CalledProcessError as e:
        print(f"❌ Error formatting {file_path}: {e}")
        print(f"🚨 Prettier Output: {e.stderr}")

        
def get_prettier_version():
    try:
        result = subprocess.run(
            ["npx", "prettier", "--version"],
            capture_output=True,
            text=True,
            check=True,
            shell=True  # Required for npx execution on some systems
        )
        version = result.stdout.strip()
        print(f"✅ Prettier version: {version}")
        return version
    except subprocess.CalledProcessError as e:
        print(f"❌ Error checking Prettier version: {e}")
        print(f"🚨 Prettier Output: {e.stderr}")
        return None

def install_prettier(version="3.4.2"):
    """Check if a specific version of `prettier` is installed, and install it if necessary."""
    print(f"🚀 Checking if prettier v{version} is installed...")

    try:
        # Get installed version of Prettier
        result = subprocess.run(["npx", "prettier", "--version"], check=True, stdout=subprocess.PIPE, stderr=subprocess.PIPE, text=True)
        installed_version = result.stdout.strip()

        if installed_version == version:
            print(f"✅ Prettier v{version} is already installed.")
            return
        else:
            print(f"⚠️ Found Prettier v{installed_version}, but v{version} is required. Installing correct version...")

    except (subprocess.CalledProcessError, FileNotFoundError):
        print("⚠️ Prettier is not installed or not found. Installing...")

    # Install the specified version using npm
    try:
        #subprocess.run(["pip", "install", "-g", f"prettier@{version}"], check=True)
        subprocess.run(["npm", "install", "-g", f"prettier@{version}"], check=True)
        #subprocess.run([sys.executable, "-m", "pip", "install", f"prettier@{version}"], check=True)
        print(f"✅ Successfully installed Prettier v{version}.")
    except subprocess.CalledProcessError as e:
        print(f"❌ Failed to install Prettier v{version}: {e}")