import requests


class GitLabHelper:
    def __init__(self, data):
        self.access_token = data["AccessToken"]
        self.project_id = data["ProjectId"]
        self.is_self_managed = data["isSelfManaged"]
        self.self_managed_url = data["selfManagedUrl"] if self.is_self_managed else None

        # Base URL depends on whether it's a self-managed GitLab instance or GitLab.com
        if self.is_self_managed:
            self.base_url = f"{self.self_managed_url}/api/v4/projects/{self.project_id}"
        else:
            self.base_url = f"https://gitlab.com/api/v4/projects/{self.project_id}"

    def _get_headers(self):
        # GitLab uses Bearer token for API requests
        headers = {'Authorization': f'Bearer {self.access_token}'}
        return headers

    def get_all_commit_data(self):
        commits_url = f"{self.base_url}/repository/commits"
        all_commits = []
        page = 1
        per_page = 100  # GitLab allows up to 100 items per page

        while len(all_commits) < 250:
            params = {'per_page': per_page, 'page': page}
            response = requests.get(commits_url, headers=self._get_headers(), params=params)
            if response.status_code == 200:
                data = response.json()
                for commit in data:
                    all_commits.append(commit['id'])
                    if len(all_commits) >= 250:
                        break
                page += 1
            else:
                return {"error": f"Failed to retrieve commits. Status code: {response.status_code}"}

            # If the retrieved data is less than 'per_page', it means we've reached the last page
            if len(data) < per_page:
                break

        return all_commits[:250]  # Ensure to return only up to 250 commits
