import os

workflow_dir = os.path.join('.github', 'workflows')
os.makedirs(workflow_dir, exist_ok=True)

workflow_path = os.path.join(workflow_dir, 'python-app.yml')

workflow_content = '''\
name: Python CI

on:
  push:
    branches: [ "main" ]
  pull_request:
    branches: [ "main" ]

jobs:
  build:

    runs-on: ubuntu-latest

    steps:
    - uses: actions/checkout@v3

    - name: Set up Python
      uses: actions/setup-python@v4
      with:
        python-version: '3.10'

    - name: Install dependencies
      run: |
        python -m pip install --upgrade pip
        pip install -r requirements.txt

    - name: Run tests
      run: |
        pytest
'''

with open(workflow_path, 'w') as f:
    f.write(workflow_content)

print(f"Workflow file created at {workflow_path}")
