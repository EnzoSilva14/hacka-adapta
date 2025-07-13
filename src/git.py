import requests
import base64

token = "ghp_your_personal_access_token_here"  # Replace with your actual PAT
owner = "your-github-username"
repo = "your-private-repo"
branch = "main"  # Or any specific branch or commit SHA
file_path = "path/to/your/file.txt"  # Path inside the repo

def get_git_file_contents():
    url = f"https://api.github.com/repos/{owner}/{repo}/contents/{file_path}?ref={branch}"

    headers = {
        "Authorization": f"token {token}",
        "Accept": "application/vnd.github.v3.raw"
    }

    response = requests.get(url, headers=headers)
    if response.status_code == 200:
        content = response.text
        print("File Content:\n", content)
    else:
        print(f"Failed to fetch file. Status code: {response.status_code}")
        print("Response:", response.json())
