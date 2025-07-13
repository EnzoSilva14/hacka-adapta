from crewai_tools import tool
import os
import base64
import requests
from dotenv import load_dotenv

load_dotenv()

@tool("Create a GitHub PR with a file on a new branch")
def create_pr_with_files(
    new_branch: str,
    file_path: str,
    file_content: str,
    file_message: str,
    pr_title: str,
    pr_body: str,
    repo_full_name: str = "hillarykb/lazy-invest-web",
    base_branch: str = "main"
) -> str:
    """
    Creates a new branch, commits a single file, and opens a GitHub Pull Request.

    Args:
        new_branch (str): The name of the branch to create.
        file_path (str): The path (in the repo) of the file to create or update.
        file_content (str): The raw string content to place in the file.
        file_message (str): Commit message for the file.
        pr_title (str): Title of the pull request.
        pr_body (str): Body/description of the pull request.
        repo_full_name (str): GitHub repo in 'owner/repo' format.
        base_branch (str): Branch from which to create the new branch.

    Returns:
        str: Success message with PR link or an error message.
    """
    token = os.getenv("GITHUB_TOKEN")
    if not token:
        return "❌ GITHUB_TOKEN not found in environment."

    headers = {
        "Authorization": f"Bearer {token}",
        "Accept": "application/vnd.github+json"
    }

    base_url = f"https://api.github.com/repos/{repo_full_name}"

    # Step 1: Get base branch SHA
    ref_url = f"{base_url}/git/ref/heads/{base_branch}"
    ref_resp = requests.get(ref_url, headers=headers)
    if ref_resp.status_code != 200:
        return f"❌ Failed to get base branch: {ref_resp.text}"
    sha = ref_resp.json()["object"]["sha"]

    # Step 2: Create new branch
    create_ref_url = f"{base_url}/git/refs"
    ref_payload = {
        "ref": f"refs/heads/{new_branch}",
        "sha": sha
    }
    create_resp = requests.post(create_ref_url, json=ref_payload, headers=headers)
    if create_resp.status_code >= 300:
        return f"❌ Failed to create new branch: {create_resp.text}"

    # Step 3: Add or update file on new branch
    content_encoded = base64.b64encode(file_content.encode()).decode()
    file_payload = {
        "message": file_message,
        "content": content_encoded,
        "branch": new_branch
    }
    file_url = f"{base_url}/contents/{file_path}"
    file_resp = requests.put(file_url, json=file_payload, headers=headers)
    if file_resp.status_code >= 300:
        return f"❌ Failed to commit file {file_path}: {file_resp.text}"

    # Step 4: Create Pull Request
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
