import os
import sys

BASE_PATH = r"C:\Users\james\Desktop\Network"
CONFIG_FILE = "unwanted_files.txt"

def load_unwanted_files():
    print(f"Looking for config file '{CONFIG_FILE}'...")
    if not os.path.exists(CONFIG_FILE):
        print(f"Config file '{CONFIG_FILE}' NOT found. Cannot continue.")
        return []
    with open(CONFIG_FILE, "r") as f:
        files = [line.strip() for line in f if line.strip()]
    print(f"Config file loaded. Files: {files}")
    return files

def main():
    print("Cleanup.py started")

    unwanted_files = load_unwanted_files()
    if not unwanted_files:
        print("No unwanted files loaded. Exiting gracefully.")
        return

    print("Would continue with scanning and cleanup here...")
    # For now, stop here to check output flow.

if __name__ == "__main__":
    main()
