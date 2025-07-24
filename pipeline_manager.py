import os
import shutil
import datetime
import subprocess
import logging
import argparse
import sys
import json

# === CONFIGURATION ===
BASE_PATH = r"C:\Users\james\Desktop\Network"
CONFIG_FILE = "unwanted_files.txt"
GIT_REPO_URL = "https://github.com/Andrew43390/Python.git"
GIT_BRANCH = "master"
COMMIT_MSG = "Add CI workflow and tests"
ARCHIVE_PREFIX = "archive_unwanted_"

# === SETUP LOGGING ===
def setup_logging():
    logging.basicConfig(
        level=logging.INFO,
        format="[%(asctime)s] %(levelname)s: %(message)s",
        handlers=[logging.StreamHandler(sys.stdout)]
    )

# === CLEANUP FUNCTION ===
def cleanup_unwanted_files(base_path, config_file):
    config_path = os.path.join(base_path, config_file)
    logging.info(f"Looking for config file '{config_path}'...")
    if not os.path.isfile(config_path):
        raise FileNotFoundError(f"Config file '{config_path}' not found.")

    with open(config_path, 'r') as f:
        files_to_archive = [line.strip() for line in f if line.strip()]

    if not files_to_archive:
        logging.info("No files listed in config for cleanup.")
        return

    timestamp = datetime.datetime.now().strftime("%Y%m%d_%H%M%S")
    archive_dir = os.path.join(base_path, ARCHIVE_PREFIX + timestamp)
    logging.info(f"Creating archive directory at '{archive_dir}'")
    os.makedirs(archive_dir, exist_ok=True)

    moved_files = []

    for file_rel_path in files_to_archive:
        src_path = os.path.join(base_path, file_rel_path)
        if not os.path.exists(src_path):
            logging.warning(f"File/folder '{file_rel_path}' not found, skipping.")
            continue

        dest_path = os.path.join(archive_dir, file_rel_path)
        os.makedirs(os.path.dirname(dest_path), exist_ok=True)

        logging.info(f"Moving '{src_path}' -> '{dest_path}'")
        shutil.move(src_path, dest_path)
        moved_files.append((src_path, dest_path))

    # Save undo info for potential restoration
    undo_file = os.path.join(base_path, "last_cleanup_undo.json")
    with open(undo_file, "w") as uf:
        json.dump(moved_files, uf, indent=2)

    logging.info(f"Cleanup complete. Moved {len(moved_files)} files/folders.")
    logging.info(f"Undo info saved to '{undo_file}'.")

# === GENERATE CI FILES FUNCTION ===
def generate_ci_files(base_path):
    workflows_dir = os.path.join(base_path, ".github", "workflows")
    tests_dir = os.path.join(base_path, "tests")

    os.makedirs(workflows_dir, exist_ok=True)
    os.makedirs(tests_dir, exist_ok=True)

    ci_yaml = """name: CI

on:
  push:
    branches: [ master ]
  pull_request:
    branches: [ master ]

jobs:
  build:
    runs-on: ubuntu-latest
    steps:
    - uses: actions/checkout@v3
    - name: Set up Python
      uses: actions/setup-python@v4
      with:
        python-version: 3.11
    - name: Install dependencies
      run: pip install -r requirements.txt
    - name: Run tests
      run: pytest
"""

    test_dummy_py = '''def test_dummy():
    assert True
'''

    ci_file_path = os.path.join(workflows_dir, "ci.yml")
    test_file_path = os.path.join(tests_dir, "test_dummy.py")

    with open(ci_file_path, "w") as f:
        f.write(ci_yaml)
    logging.info(f"Created GitHub Actions workflow at '{ci_file_path}'")

    with open(test_file_path, "w") as f:
        f.write(test_dummy_py)
    logging.info(f"Created dummy test file at '{test_file_path}'")

# === RUN SHELL COMMAND ===
def run_cmd(cmd, cwd=None):
    logging.info(f"> {' '.join(cmd)}")
    result = subprocess.run(cmd, cwd=cwd, capture_output=True, text=True)
    if result.returncode != 0:
        logging.error(f"Error: {result.stderr.strip()}")
        raise RuntimeError(f"Command {' '.join(cmd)} failed with code {result.returncode}")
    return result.stdout.strip()

# === PREPARE LOCAL GIT REPO FUNCTION ===
def prepare_local_repo(repo_url, local_path, branch):
    if not os.path.exists(local_path):
        os.makedirs(local_path)

    if not os.path.isdir(os.path.join(local_path, ".git")):
        run_cmd(["git", "init"], cwd=local_path)
    else:
        logging.info("Git repository already initialized.")

    remotes = run_cmd(["git", "remote"], cwd=local_path).splitlines()
    if "origin" not in remotes:
        run_cmd(["git", "remote", "add", "origin", repo_url], cwd=local_path)
    else:
        logging.info("Remote 'origin' already exists.")

    run_cmd(["git", "fetch"], cwd=local_path)
    branches = run_cmd(["git", "branch", "--list", branch], cwd=local_path)
    if not branches:
        run_cmd(["git", "checkout", "-b", branch], cwd=local_path)
    else:
        run_cmd(["git", "checkout", branch], cwd=local_path)
    logging.info(f"Checked out branch '{branch}'")

# === PUSH CHANGES FUNCTION ===
def push_changes(local_path, commit_msg):
    # Configure user if not set
    try:
        run_cmd(["git", "config", "user.name"], cwd=local_path)
        run_cmd(["git", "config", "user.email"], cwd=local_path)
    except RuntimeError:
        run_cmd(["git", "config", "user.name", "James Green"], cwd=local_path)
        run_cmd(["git", "config", "user.email", "james@example.com"], cwd=local_path)

    run_cmd(["git", "add", "."], cwd=local_path)

    status = run_cmd(["git", "status", "--porcelain"], cwd=local_path)
    if not status:
        logging.info("No changes to commit.")
        return

    run_cmd(["git", "commit", "-m", commit_msg], cwd=local_path)
    run_cmd(["git", "push", "-u", "origin", GIT_BRANCH], cwd=local_path)
    logging.info(f"Pushed changes to remote branch '{GIT_BRANCH}'.")

# === MAIN FUNCTION ===
def main():
    setup_logging()

    parser = argparse.ArgumentParser(description="Manage CI/CD pipeline tasks.")
    parser.add_argument("--cleanup", action="store_true", help="Run cleanup of unwanted files")
    parser.add_argument("--generate-ci", action="store_true", help="Generate GitHub Actions CI workflow and tests")
    parser.add_argument("--prepare-repo", action="store_true", help="Prepare local git repo by cloning/checking out branch")
    parser.add_argument("--push", action="store_true", help="Commit and push changes to remote repository")

    args = parser.parse_args()

    # If no flags given, run all steps
    if not any(vars(args).values()):
        args.cleanup = True
        args.generate_ci = True
        args.prepare_repo = True
        args.push = True

    try:
        if args.cleanup:
            logging.info("=== Starting Cleanup Step ===")
            cleanup_unwanted_files(BASE_PATH, CONFIG_FILE)

        if args.generate_ci:
            logging.info("=== Generating CI files ===")
            generate_ci_files(BASE_PATH)

        if args.prepare_repo:
            logging.info("=== Preparing local Git repository ===")
            prepare_local_repo(GIT_REPO_URL, BASE_PATH, GIT_BRANCH)

        if args.push:
            logging.info("=== Pushing changes to GitHub ===")
            push_changes(BASE_PATH, COMMIT_MSG)

        logging.info("All selected steps completed successfully.")

    except Exception as e:
        logging.error(f"Fatal error: {e}")
        sys.exit(1)

if __name__ == "__main__":
    main()
