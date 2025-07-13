import requests
import base64
import os
from dotenv import load_dotenv
from crewai.tools import tool
load_dotenv()

git_token = os.getenv("GITHUB_TOKEN")

owner = "hillarykb"
repo = "lazy-invest-web"
file_path = "src/features/analysis/pages/stock-detail.page.tsx"  # Path inside the repo

@tool("Get File Content from repository")
def get_code_from_repository():
    """
    Recupera o conteúdo de um arquivo específico de um repositório Git remoto.
    
    Retorna:
    Conteúdo do arquivo como string.
    """
    url = f"https://api.github.com/repos/{owner}/{repo}/contents/{file_path}"

    headers = {
        "Authorization": f"Bearer {git_token}",
        "Accept": "application/vnd.github.v3.raw"
    }

    response = requests.get(url, headers=headers)
    if response.status_code == 200:
        content = response.text
        print("File Content:\n", content)
        return content
    else:
        print(f"Failed to fetch file. Status code: {response.status_code}")
        print("Response:", response.json())
