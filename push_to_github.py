import os
import subprocess
import sys

def run_git_commands_automated(project_path, repo_url):
    """
    Executes git remote add and git push commands automatically using a hardcoded URL.
    """
    print(f"\n--- Initiating Git Remote Setup and Initial Push ---")
    print(f"Project path: {project_path}")
    print(f"Repository URL: {repo_url}")
    print("-" * 70)

    try:
        # Change to the project directory
        os.chdir(project_path)
        print(f"Changed current directory to: {os.getcwd()}")

        # Check if 'origin' remote already exists
        result = subprocess.run(["git", "remote", "-v"], check=False, capture_output=True, text=True)
        if "origin" in result.stdout:
            print("Remote 'origin' already exists. Attempting to set URL if different.")
            # Optionally, you could try to update it: git remote set-url origin <new_url>
            # For simplicity, if it exists and might be wrong, we'll try to remove and re-add.
            # Or, for robustness, you might ask user or skip if URL matches.
            try:
                subprocess.run(["git", "remote", "remove", "origin"], check=True, capture_output=True, text=True)
                print("Existing remote 'origin' removed.")
            except subprocess.CalledProcessError as e:
                print(f"Warning: Could not remove existing remote 'origin'. It might be in use or protected.\n{e.stderr.strip()}")
                print("Skipping remote add/push for safety. Please resolve manually if needed.")
                return False

        # Add the remote origin
        print(f"Adding remote origin: {repo_url}")
        subprocess.run(["git", "remote", "add", "origin", repo_url], check=True, capture_output=True, text=True)
        print("Remote origin added successfully.")

        # Push the code to the remote repository
        print("\nPushing code to remote repository (you may be prompted for credentials)...")
        # Using sys.stdin for input=sys.stdin allows git to prompt for credentials in the console
        # If Git Credential Manager or SSH keys are configured, it might be fully automatic.
        subprocess.run(["git", "push", "-u", "origin", "main"], check=True, capture_output=False, text=True, stdin=sys.stdin)
        print("\nCode pushed successfully to 'main' branch.")

    except subprocess.CalledProcessError as e:
        print(f"Error during Git operation:")
        print(f"STDOUT:\n{e.stdout.strip()}")
        print(f"STDERR:\n{e.stderr.strip()}")
        print("\nPossible reasons for error:")
        print(" - Repository URL might be incorrect or unreachable.")
        print(" - You might need to provide valid GitHub credentials (username/Personal Access Token) when prompted.")
        print(" - Network issues.")
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

    # *** YOUR REPOSITORY URL - HARDCODED AS REQUESTED ***
    # This script is specific to this URL.
    my_github_repo_url = "https://github.com/Andrew43390/Python.git"

    print("\n" + "=" * 70)
    print("WARNING: This script contains a hardcoded GitHub repository URL.")
    print("It is intended for your specific use and is NOT a general-purpose solution.")
    print("=" * 70)

    if not os.path.exists(project_full_path):
        print(f"Error: Project directory '{project_full_path}' not found.")
        print("Please ensure the 'setup_automated_ci_cd.py' script was run successfully first.")
        sys.exit(1)

    confirm = input(f"Confirm linking and pushing project '{project_name}' to '{my_github_repo_url}'? (yes/no): ").lower()

    if confirm == 'yes':
        success = run_git_commands_automated(project_full_path, my_github_repo_url)
        if success:
            print("\n" + "=" * 70)
            print("GIT REPOSITORY PUSH AUTOMATION COMPLETE!")
            print("Your local project should now be on GitHub.")
            print("=" * 70)
            print("\n**FINAL MANUAL STEPS (CRUCIAL FOR CI/CD)**:")
            print("---------------------------------------")
            print("4. **Develop your application:** Write your actual Python code in `src/my_app/` and corresponding tests in `tests/`.")
            print("\n9. **Configure Secrets in GitHub (if needed for deployment):**")
            print("   - If your CI/CD pipeline (`.github/workflows/ci_cd.yml`) uses secrets (like `PYPI_API_TOKEN`, `AWS_ACCESS_KEY_ID`),")
            print("     you MUST configure them in your GitHub repository settings:")
            print("     Go to `https://github.com/Andrew43390/Python` -> `Settings` -> `Secrets and variables` -> `Actions` -> `New repository secret`.")
            print("     **Never hardcode secrets in your repository!**")
            print("\n10. **Update External Repo URL in CI/CD YAML on GitHub (if applicable):**")
            print(f"   - Open the `ci_cd.yml` file directly on GitHub.com (`https://github.com/Andrew43390/Python/blob/main/.github/workflows/ci_cd.yml`).")
            print("   - Find `EXTERNAL_REPO_URL` and `EXTERNAL_REPO_BRANCH` under the `env` section.")
            print("   - Replace `https://github.com/your-org/external_dependency_repo.git` and `main` with the *actual URL and branch/tag* of your external Git repository that your project depends on.")
            print("   - **Commit this change directly on GitHub** (or pull, edit locally, and push).")
            print("\nOnce these final manual steps are completed, your CI/CD pipeline will trigger automatically on future pushes to your main branch!")
        else:
            print("\nGit push failed. Please review the errors above and complete the process manually.")
            print(f"You can manually navigate to '{project_full_path}' and run 'git remote add origin {my_github_repo_url}' followed by 'git push -u origin main'.")
    else:
        print("Operation cancelled.")