import subprocess
import datetime
import os
import sys

PROJECT_PATH = r"C:\Users\james\Desktop\Network"
FILE_TO_TOUCH = os.path.join(PROJECT_PATH, "tests", "test_dummy.py")

def run_cmd(cmd, cwd=None):
    print(f"> {' '.join(cmd)}")
    result = subprocess.run(cmd, cwd=cwd, capture_output=True, text=True)
    if result.returncode != 0:
        print(f"Error: {result.stderr.strip()}")
        raise RuntimeError(f"Command {' '.join(cmd)} failed with exit code {result.returncode}")
    print(result.stdout.strip())
    return result.stdout.strip()

def touch_file(path):
    """Update file modification time or append a newline if empty."""
    if not os.path.exists(path):
        # Create file if missing
        with open(path, "w") as f:
            f.write("# Dummy test file\n")
        print(f"Created missing file {path}")
    else:
        # Append a timestamp comment to ensure file changes
        with open(path, "a") as f:
            f.write(f"# Updated {datetime.datetime.now().isoformat()}\n")
        print(f"Touched file {path}")

def main():
    print(f"Starting routine CI trigger at {datetime.datetime.now().isoformat()}")

    try:
        touch_file(FILE_TO_TOUCH)

        run_cmd(["git", "add", "."], cwd=PROJECT_PATH)

        commit_msg = f"Routine CI trigger commit at {datetime.datetime.now().isoformat()}"
        run_cmd(["git", "commit", "-m", commit_msg], cwd=PROJECT_PATH)

        run_cmd(["git", "push", "origin", "master"], cwd=PROJECT_PATH)

        print("Push complete. CI workflow should start shortly on GitHub.")

    except RuntimeError as e:
        print(f"Failed: {e}")
        sys.exit(1)

if __name__ == "__main__":
    main()
