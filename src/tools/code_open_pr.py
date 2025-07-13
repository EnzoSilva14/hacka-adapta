from crewai.tools import tool
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
    Creates a new branch, commits a single file (create or update), and opens a GitHub Pull Request.
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
        if "Reference already exists" not in create_resp.text:
            return f"❌ Failed to create new branch: {create_resp.text}"

    # Step 3: Check if file exists to get its SHA
    file_url = f"{base_url}/contents/{file_path}?ref={new_branch}"
    file_resp_get = requests.get(file_url, headers=headers)
    file_sha = None
    if file_resp_get.status_code == 200:
        file_sha = file_resp_get.json().get("sha")

    # Step 4: Commit file (create or update)
    content_encoded = base64.b64encode(file_content.encode()).decode()
    file_payload = {
        "message": file_message,
        "content": content_encoded,
        "branch": new_branch
    }
    if file_sha:
        file_payload["sha"] = file_sha

    file_commit_resp = requests.put(file_url.split("?")[0], json=file_payload, headers=headers)
    if file_commit_resp.status_code >= 300:
        return f"❌ Failed to commit file {file_path}: {file_commit_resp.text}"

    # Step 5: Create Pull Request
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
