import os

BASE_PATH = r"C:\Users\james\Desktop\Network"
WORKFLOW_PATH = os.path.join(BASE_PATH, ".github", "workflows")
TESTS_PATH = os.path.join(BASE_PATH, "tests")

CI_YML_CONTENT = """name: CI

on:
  push:
    branches:
      - main
  pull_request:

jobs:
  test:
    runs-on: windows-latest

    steps:
      - name: Checkout code
        uses: actions/checkout@v4

      - name: Set up Python
        uses: actions/setup-python@v5
        with:
          python-version: '3.11'

      - name: Install dependencies
        run: |
          python -m pip install --upgrade pip
          pip install pytest

      - name: Run tests
        run: |
          pytest --maxfail=1 --disable-warnings -q
"""

TEST_FILE_CONTENT = """def test_addition():
    assert 2 + 2 == 4
"""

def create_file(path, content):
    os.makedirs(os.path.dirname(path), exist_ok=True)
    with open(path, "w", encoding="utf-8") as f:
        f.write(content)
    print(f"✅ Created: {path}")

def main():
    print("🚀 Generating CI setup files...")
    workflow_file = os.path.join(WORKFLOW_PATH, "ci.yml")
    test_file = os.path.join(TESTS_PATH, "test_dummy.py")

    create_file(workflow_file, CI_YML_CONTENT)
    create_file(test_file, TEST_FILE_CONTENT)

    print("\n📦 Done! You can now commit and push to GitHub to trigger CI.")

if __name__ == "__main__":
    main()
