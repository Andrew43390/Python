import subprocess
import shutil
from pathlib import Path

# Configuration
repo_url = "https://github.com/Andrew43390/Python.git"
target_dir = Path("C:/Users/james/Desktop/Network/my_ci_cd_app")

# Delete the folder if it already exists
if target_dir.exists():
    print("🧹 Removing existing folder:", target_dir)
    shutil.rmtree(target_dir)

# Clone the repo
print("🌱 Cloning repo into:", target_dir)
result = subprocess.run(["git", "clone", repo_url, str(target_dir)], capture_output=True, text=True)

if result.returncode != 0:
    print("❌ Git clone failed:\n", result.stderr)
    exit(result.returncode)

print("✅ Clone successful!")

# Optional: switch to 'main' branch if needed
print("🔁 Checking out 'main' branch...")
subprocess.run(["git", "checkout", "main"], cwd=target_dir)

print("📂 Ready to work inside:", target_dir)
