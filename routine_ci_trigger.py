import os
import subprocess
from datetime import datetime

REPO_PATH = r"C:\Users\james\Desktop\Network"
FILE_TO_MODIFY = os.path.join(REPO_PATH, "tests", "test_dummy.py")
BRANCH = "master"

def run_cmd(cmd, cwd=None):
    result = subprocess.run(cmd, cwd=cwd, capture_output=True, text=True)
    print(f"> {' '.join(cmd)}")
    if result.stdout:
        print(result.stdout.strip())
    if result.stderr:
        print(result.stderr.strip())
    if result.returncode != 0:
        raise RuntimeError(f"Command failed with exit code {result.returncode}")
    return result.stdout.strip()

def touch_file():
    # Create or append a comment line with timestamp to trigger git change
    with open(FILE_TO_MODIFY, "a") as f:
        f.write(f"# Dummy update {datetime.now().isoformat()}\n")
    print(f"Modified {FILE_TO_MODIFY}")

def main():
    print(f"Starting routine push to trigger CI at {datetime.now().isoformat()}")
    touch_file()
    run_cmd(["git", "add", "."], cwd=REPO_PATH)
    commit_msg = f"Routine CI trigger commit at {datetime.now().isoformat()}"
    try:
        run_cmd(["git", "commit", "-m", commit_msg], cwd=REPO_PATH)
    except RuntimeError as e:
        if "nothing to commit" in str(e):
            print("No changes to commit, skipping commit.")
        else:
            raise
    run_cmd(["git", "push", "origin", BRANCH], cwd=REPO_PATH)
    print("Push complete. CI workflow should start shortly on GitHub.")

if __name__ == "__main__":
    main()
