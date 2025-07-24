import os
import subprocess
import sys # For getting current Python info if needed, though not directly used in this script's core logic

def run_git_commands(project_path, repo_url):
    """
    Executes git remote add and git push commands.
    """
    print(f"\nAttempting to link local Git repository to remote and push...")
    print("-" * 70)

    try:
        # Change to the project directory
        os.chdir(project_path)
        print(f"Changed current directory to: {os.getcwd()}")

        # Add the remote origin
        print(f"Adding remote origin: {repo_url}")
        subprocess.run(["git", "remote", "add", "origin", repo_url], check=True, capture_output=True, text=True)
        print("Remote origin added successfully.")

        # Push the code to the remote repository
        print("Pushing code to remote repository (you may be prompted for credentials)...")
        # Using sys.stdin for input=sys.stdin to allow git to prompt for credentials
        subprocess.run(["git", "push", "-u", "origin", "main"], check=True, capture_output=False, text=True, stdin=sys.stdin)
        print("Code pushed successfully to 'main' branch.")

    except subprocess.CalledProcessError as e:
        print(f"Error during Git operation:\nSTDOUT:\n{e.stdout}\nSTDERR:\n{e.stderr}")
        print("\nPossible reasons for error:")
        print(" - Repository URL might be incorrect or unreachable.")
        print(" - You might need to provide valid GitHub credentials (username/PAT).")
        print(" - The remote 'origin' might already exist (run 'git remote -v' to check).")
        return False
    except FileNotFoundError:
        print("Error: Git command not found. Please ensure Git is installed and in your PATH.")
        return False
    except Exception as e:
        print(f"An unexpected error occurred: {e}")
        return False
    return True

# --- Main execution ---
if __name__ == "__main__":
    # Define the base directory where the previous script created the project
    base_directory = r"C:\Users\james\Desktop\Network"
    project_name = "my_ci_cd_app"
    project_full_path = os.path.join(base_directory, project_name)

    print("--- Git Remote Setup and Initial Push Script ---")
    print("This script helps you link your local project to a remote GitHub repository.")
    print("It assumes the project structure has already been created by the previous script.")
    print("-" * 70)

    if not os.path.exists(project_full_path):
        print(f"Error: Project directory '{project_full_path}' not found.")
        print("Please run the 'setup_automated_ci_cd.py' script first to create the project.")
        sys.exit(1)

    print(f"Ready to configure Git for project: {project_full_path}")

    # Prompt user for the remote repository URL
    repo_url = input("Please enter the FULL URL of your new, EMPTY GitHub repository (e.g., https://github.com/your-username/your-repo.git): ").strip()

    if not repo_url:
        print("Repository URL cannot be empty. Exiting.")
        sys.exit(1)

    confirm = input(f"About to link '{project_full_path}' to '{repo_url}' and push. Continue? (yes/no): ").lower()

    if confirm == 'yes':
        success = run_git_commands(project_full_path, repo_url)
        if success:
            print("\n" + "=" * 70)
            print("GIT SETUP AUTOMATION COMPLETE (Partial Success)!")
            print("=" * 70)
            print("\nRemaining MANUAL NEXT STEPS (CRUCIAL!):")
            print("---------------------------------------")
            print("4. **Develop your application:** Write your actual Python code in `src/my_app/` and corresponding tests in `tests/`.")
            print("\n9. **Configure Secrets in GitHub:**")
            print(f"   - If your CI/CD pipeline (in `{project_full_path}\.github\workflows\ci_cd.yml`) uses secrets (like `PYPI_API_TOKEN`, `AWS_ACCESS_KEY_ID`),")
            print("     you MUST configure them in your GitHub repository settings:")
            print("     Go to `Your_Repo` -> `Settings` -> `Secrets and variables` -> `Actions` -> `New repository secret`.")
            print("     **Never hardcode secrets in your repository!**")
            print("\n10. **Update External Repo URL in YAML (if applicable):**")
            print(f"   - Open `{project_full_path}\.github\workflows\ci_cd.yml` (e.g., in VS Code or Notepad).")
            print("   - Find `EXTERNAL_REPO_URL` and `EXTERNAL_REPO_BRANCH` under the `env` section.")
            print("   - Replace `https://github.com/your-org/external_dependency_repo.git` and `main` with the *actual URL and branch/tag* of your external Git repository.")
            print("   - **Commit and push this change** to trigger the pipeline after the initial setup. Example commands:")
            print(f"     cd \"{project_full_path}\"")
            print(f"     git add .github/workflows/ci_cd.yml")
            print(f"     git commit -m \"Update CI/CD YAML with external repo URL\"")
            print(f"     git push")
            print("\nOnce these manual steps are done, your CI/CD pipeline will trigger automatically on future pushes!")
        else:
            print("\nGit setup failed. Please review the errors above and try again manually.")
            print(f"You can manually perform the steps by navigating to '{project_full_path}' and running git commands.")
    else:
        print("Operation cancelled.")