

import os, re, subprocess
import datetime

def run_command(command, cwd=None):
    result = subprocess.run(command, shell=True, cwd=cwd, capture_output=True, text=True)
    if result.returncode != 0:
        print(f"Error: {result.stderr}")
    else:
        print(result.stdout)

def clone_and_commit():
    """Clone a Git repo, make a commit, and push changes."""
    t1 = "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"
    t2 = "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"
    repo_url = ""
    local_path = F"data/GA2"
    file_to_modify = "sample.txt"
    commit_message = "Updated sample.txt with new content"
    
    # Ensure Git is installed
    run_command("git --version")

    # Configure Git user
    run_command('git config --global user.name "Royiitian"')
    run_command('git config --global user.email "23f1001348@ds.study.iitm.ac.in"')

    # 1. Clone the repository
    print("Cloning repository...")

    cwd = os.getcwd()
    try:

        # Clone the repository
        if os.path.exists(local_path):
            print("Repository already exists. Pulling latest changes.")
            run_command("git pull", cwd=local_path)
        else:
            # Clone the repository
            print(f"Cloning repository... {repo_url}")
            run_command(f"git clone {repo_url}", cwd="data")
            
            # 2. Change to repo directory
            os.chdir(local_path)
        
        print("Making changes...")
        now = datetime.datetime.now()
        # Create a new file as an example change
        with open(file_to_modify, "a+") as f:
            f.write(f"{now.isoformat()}: This is an automated commit from Docker.")
        f.close()
        
        print("Committing changes...")
        # Stage, commit, and push the changes
        run_command("git add .")
        print("Committing changes...")
        run_command(f"git commit -m \"{commit_message}\"")
        print("Pushing changes...")
        run_command("git push")

    finally:
        os.chdir(cwd)
    
    return "Changes committed and pushed successfully!"

def get_repo_name(repo_url):
    match = re.search(r"([^/]+)\.git$", repo_url)
    return match.group(1) if match else None
