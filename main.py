from Helpers.GitLabHelper import GitLabHelper
from Helpers.GithubHelper import GithubHelper
from Helpers.JsonHelper import JsonHelper


def main():
    js_helper = JsonHelper()
    apps_data = js_helper.GetData()
    try:
        # Initialize helpers
        for data in apps_data:
            gitlab_helper = GitLabHelper(data)
            github_helper = GithubHelper()

            # Get all commit data from gitLab
            gitlab_commits = gitlab_helper.get_all_commit_data()
            if isinstance(gitlab_commits, dict) and 'error' in gitlab_commits:
                print(f"Error fetching GitLab commits: {gitlab_commits['error']}")
                continue

            # List files in the 'commits' directory on GitHub
            github_commits = github_helper.list_files_in_dir("commits")
            if not github_commits:  # Checks if github_commits is empty or an error occurred
                print("Error or no files found in GitHub 'commits' directory.")
                continue

            # Convert lists to sets for comparison
            gitlab_commits_set = set(gitlab_commits)
            github_commits_set = set(github_commits)

            # Find commits new to gitLab
            new_to_gitlab = gitlab_commits_set - github_commits_set
            if not new_to_gitlab:
                print("No new commits in GitLab to update to GitHub.")
                continue

            print(f"{len(new_to_gitlab)} commits to push.")

            for commit in new_to_gitlab:
                # Try to commit each new commit to GitHub
                try:
                    # Assuming the commit message or content is being fetched in a manner suitable for GitHub
                    commit_message = f"Commit {commit} from GitLab"
                    github_helper.commit(commit_message, "commits", f"{commit}.txt", file_content=commit)
                except Exception as e:
                    print(f"Failed to commit {commit} to GitHub: {e}")

            print("Process completed successfully.")

    except Exception as e:
        print(f"An unexpected error occurred: {e}")


if __name__ == "__main__":
    main()
