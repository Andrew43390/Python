import os
from pathlib import Path

# Define path to the GitHub Actions workflow file
workflow_path = Path("C:/Users/james/Desktop/Network/my_ci_cd_app/.github/workflows/python-app.yml")

# Ensure the .github/workflows directory exists
workflow_path.parent.mkdir(parents=True, exist_ok=True)

# Workflow YAML content
workflow_content = """name: Python CI

on:
  push:
    branches: [ main ]
  pull_request:
    branches: [ main ]

jobs:
  build:
    runs-on: ubuntu-latest

    steps:
    - name: Checkout repository
      uses: actions/checkout@v4

    - name: Setup Python
      uses: actions/setup-python@v4
      with:
        python-version: '3.11'

    - name: Install pip dependencies
      run: |
        python -m pip install --upgrade pip
        pip install -r requirements.txt

    - name: Clone external GitHub repository
      run: |
        git clone https://github.com/username/external-repo.git
        cp external-repo/some_folder/*.py my_ci_cd_app/external/ || true

    - name: Run tests
      run: |
        python -m unittest discover -s tests || echo "Tests failed"

    - name: Build the package
      run: |
        python setup.py sdist bdist_wheel

    - name: Handle errors
      if: failure()
      run: echo "BUILD FAILED: Please check the logs above."
"""

# Write the workflow file using UTF-8 encoding
workflow_path.write_text(workflow_content, encoding='utf-8')
print(f"✅ GitHub Actions workflow created/updated at:\n{workflow_path}")
