from crewai_tools import tool
import os
import base64
import requests

@tool("Create a new branch, commit files, and open a GitHub Pull Request")
def create_pr_with_files(
    repo_full_name: str,
    base_branch: str,
    new_branch: str,
    files: list,
    pr_title: str,
    pr_body: str
) -> str:
    """
    Automates GitHub workflow: creates a branch, commits files, and opens a PR.

    Arguments:
    - repo_full_name: e.g. "username/repo"
    - base_branch: e.g. "main"
    - new_branch: e.g. "feature/my-feature"
    - files: list of dicts with 'path', 'content', 'message'
    - pr_title: title of the pull request
    - pr_body: body of the pull request
    """
    token = os.getenv("GITHUB_TOKEN")
    if not token:
        return "❌ GITHUB_TOKEN not found in environment."

    headers = {
        "Authorization": f"Bearer {token}",
        "Accept": "application/vnd.github+json"
    }

    base_url = f"https://api.github.com/repos/{repo_full_name}"

    # 1. Get base branch SHA
    ref_url = f"{base_url}/git/ref/heads/{base_branch}"
    ref_resp = requests.get(ref_url, headers=headers)
    if ref_resp.status_code != 200:
        return f"❌ Failed to get base branch: {ref_resp.text}"
    sha = ref_resp.json()["object"]["sha"]

    # 2. Create new branch from SHA
    create_ref_url = f"{base_url}/git/refs"
    ref_payload = {
        "ref": f"refs/heads/{new_branch}",
        "sha": sha
    }
    create_resp = requests.post(create_ref_url, json=ref_payload, headers=headers)
    if create_resp.status_code >= 300:
        return f"❌ Failed to create new branch: {create_resp.text}"

    # 3. Add or update files on new branch
    for f in files:
        file_url = f"{base_url}/contents/{f['path']}"
        content_encoded = base64.b64encode(f['content'].encode()).decode()

        file_payload = {
            "message": f.get("message", f"Add {f['path']}"),
            "content": content_encoded,
            "branch": new_branch
        }

        file_resp = requests.put(file_url, json=file_payload, headers=headers)
        if file_resp.status_code >= 300:
            return f"❌ Failed to commit file {f['path']}: {file_resp.text}"

    # 4. Create Pull Request
    pr_payload = {
        "title": pr_title,
        "head": new_branch,
        "base": base_branch,
        "body": pr_body
    }
    pr_url = f"{base_url}/pulls"
    pr_resp = requests.post(pr_url, json=pr_payload, headers=headers)
    if pr_resp.status_code >= 300:
        return f"❌ Failed to open PR: {pr_resp.text}"

    pr_html_url = pr_resp.json().get("html_url")
    return f"✅ Pull Request created: {pr_html_url}"
