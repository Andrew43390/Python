import os
import sys # Import sys to get Python version for pyproject.toml

def create_project_structure_in_current_dir(base_path):
    """
    Creates the necessary directory structure and placeholder files
    for a new Python project intended for CI/CD,
    starting within the given base_path (where this script resides).
    """
    # Define the project folder name
    project_name = "my_ci_cd_app"
    project_path = os.path.join(base_path, project_name)

    # Create main project directory
    if not os.path.exists(project_path):
        os.makedirs(project_path)
        print(f"Created project directory: {project_path}")
    else:
        print(f"Project directory already exists: {project_path}")


    # Define subdirectories relative to project_path
    subdirectories = [
        os.path.join(project_path, "src", "my_app"),
        os.path.join(project_path, "tests"),
        os.path.join(project_path, ".github", "workflows"), # For GitHub Actions
    ]

    for subdir in subdirectories:
        os.makedirs(subdir, exist_ok=True)
        print(f"Ensured directory exists: {subdir}")

    # Create placeholder files
    print("\nCreating placeholder files...")

    # pyproject.toml
    pyproject_content = """
[tool.poetry]
name = "my-ci-cd-app"
version = "0.1.0"
description = "A Python application with CI/CD pipeline integration."
authors = ["James <james@example.com>"]
readme = "README.md"

[tool.poetry.dependencies]
python = "^{}.{}" # Adjust this to your desired Python version, e.g., "3.10"
# Add your external dependency here if it's a PyPI package
# external-lib = "^1.0.0"

[tool.poetry.group.dev.dependencies]
pytest = "^7.0"
flake8 = "^6.0"
# If your external_dependency_repo is a python package, you could reference it like this:
# external-lib = {{ git = "https://github.com/your-org/external_dependency_repo.git", branch = "main" }}
# or for local development, you might install it editable directly with pip or poetry.

[tool.poetry.group.build.dependencies]
pyinstaller = "^5.0"

[build-system]
requires = ["poetry-core"]
build-backend = "poetry.core.masonry.api"
""".format(sys.version_info.major, sys.version_info.minor) # Auto-detect current Python version

    with open(os.path.join(project_path, "pyproject.toml"), "w") as f:
        f.write(pyproject_content.strip())
    print(f"Created {project_name}/pyproject.toml")

    # README.md
    readme_content = f"""
# {project_name}

This is a Python application designed with a CI/CD pipeline in mind.

## CI/CD Pipeline

The CI/CD pipeline is defined in `.github/workflows/ci_cd.yml` (if using GitHub Actions) and handles:
- Dependency management (using Poetry)
- Cloning and integrating code from an external Git repository
- Running linters (flake8)
- Running tests (pytest)
- Building a Python package (.whl)
- Building a standalone executable (PyInstaller)
- Deployment (example stages for PyPI and S3)

## External Repository Integration

This project is set up to integrate code from an external Git repository, as configured in the CI/CD pipeline.
"""
    with open(os.path.join(project_path, "README.md"), "w") as f:
        f.write(readme_content.strip())
    print(f"Created {project_name}/README.md")

    # main.py
    main_py_content = """
import os
# Assuming external_lib is integrated either via file copy or package installation
try:
    # This import path assumes the external_lib was copied into
    # src/my_app/external_lib_integration/
    from my_app.external_lib_integration.utils import greet_external_user
except ImportError:
    # Fallback for local run without full external_lib integration setup
    # or if external_lib is intended to be installed as a separate package
    # (in which case the import would be 'from external_lib.utils import ...')
    def greet_external_user(name):
        return f"Hello, {{name}} from a placeholder external library!"

def main():
    print("Welcome to my CI/CD enabled Python app!")
    user_name = os.getenv("USERNAME", "there") # Get username from env var, default to 'there'
    print(greet_external_user(user_name))
    print("This app will be built and deployed via CI/CD!")

if __name__ == "__main__":
    main()
"""
    with open(os.path.join(project_path, "src", "my_app", "main.py"), "w") as f:
        f.write(main_py_content.strip())
    print(f"Created {project_name}/src/my_app/main.py")

    # __init__.py for src/my_app
    with open(os.path.join(project_path, "src", "my_app", "__init__.py"), "w") as f:
        f.write("") # Empty __init__.py to make it a package
    print(f"Created {project_name}/src/my_app/__init__.py")

    # test_app.py
    test_app_content = """
import pytest
# Adjust import based on your src structure and project_name
from my_ci_cd_app.src.my_app.main import main
from my_ci_cd_app.src.my_app.external_lib_integration.utils import greet_external_user # Example for testing external integration

# Simple test for main function (can be improved by mocking print)
def test_main_function_runs():
    # This is a basic test that just checks if main executes without errors
    # For more robust testing, you'd mock stdout or return values
    try:
        main()
        assert True
    except Exception as e:
        pytest.fail(f"main() raised an exception: {{e}}")

def test_greet_external_user():
    # This test assumes the 'greet_external_user' function is available
    # either through direct file copy or as an installed package.
    # Adjust this test if your external integration method changes.
    assert greet_external_user("World") == "Hello, World from the external library!"
    assert "Gemini" in greet_external_user("Gemini")
"""
    with open(os.path.join(project_path, "tests", "test_app.py"), "w") as f:
        f.write(test_app_content.strip())
    print(f"Created {project_name}/tests/test_app.py")

    # Placeholder for CI/CD YAML
    cicd_yaml_path = os.path.join(project_path, ".github", "workflows", "ci_cd.yml")
    cicd_yaml_content = """
# This file defines your GitHub Actions CI/CD pipeline.
#
# To enable this pipeline:
# 1. Push this entire 'my_ci_cd_app' folder to a new GitHub repository.
# 2. Go to your GitHub repository settings and ensure GitHub Actions are enabled.
# 3. Copy the full YAML pipeline content from the previous Gemini response
#    and paste it into this file, replacing these comments.
# 4. Make sure to update 'EXTERNAL_REPO_URL' and 'EXTERNAL_REPO_BRANCH'
#    in the 'env' section of the YAML to point to your actual external repository.
# 5. Commit and push these changes.
#
# Your first pipeline run should automatically trigger!

# Name of your workflow (appears in GitHub Actions tab)
name: Placeholder CI/CD Pipeline

on:
  push:
    branches:
      - main
      - develop
  pull_request:
    branches:
      - main
      - develop

jobs:
  placeholder_job:
    runs-on: ubuntu-latest
    steps:
      - name: Display Message
        run: |
          echo "This is a placeholder CI/CD job."
          echo "Please replace the content of this file with the full pipeline YAML provided by Gemini."
          echo "Don't forget to configure your external repository URL and branch!"
    """
    with open(cicd_yaml_path, "w") as f:
        f.write(cicd_yaml_content.strip())
    print(f"Created {project_name}/.github/workflows/ci_cd.yml (placeholder)")

    print(f"\nProject structure for '{project_name}' created successfully in '{base_path}'!")
    print("\nNext Steps:")
    print(f"1. Navigate into the new project directory: cd \"{project_path}\"")
    print("2. (If using Poetry) Initialize Poetry: poetry init (follow prompts) or poetry install if pyproject.toml is sufficient.")
    print("3. (If using Poetry) Add dev/build dependencies: poetry add pytest flake8 pyinstaller --group dev")
    print("4. Create your actual Python code in src/my_app/ and tests in tests/.")
    print(f"5. IMPORTANT: Go to '{cicd_yaml_path}' and paste the full CI/CD YAML from the previous detailed response into it, replacing the placeholder comments.")
    print("6. Initialize a Git repository in your project folder: git init && git add . && git commit -m \"Initial project setup\"")
    print("7. Create a new repository on GitHub (or GitLab, etc.).")
    print("8. Link your local repository to the remote one and push: git remote add origin <your_repo_url> && git push -u origin main")
    print("9. Ensure you configure any necessary secrets in your GitHub repository settings (e.g., PYPI_API_TOKEN, AWS_ACCESS_KEY_ID).")
    print("10. Your CI/CD pipeline should now trigger on push!")

# --- Main execution ---
if __name__ == "__main__":
    # This script assumes it is placed directly in the target base directory.
    # Get the directory where this script is located.
    script_directory = os.path.dirname(os.path.abspath(__file__))

    print("This script will set up a Python project structure ready for CI/CD.")
    print(f"The project will be created within the current directory: {script_directory}")

    confirm = input(f"Confirm creation of project structure in '{script_directory}'? (yes/no): ").lower()

    if confirm == 'yes':
        create_project_structure_in_current_dir(script_directory)
    else:
        print("Operation cancelled.")
