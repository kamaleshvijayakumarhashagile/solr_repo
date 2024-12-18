""" import os
import requests

def download_github_folder(repo_url, local_dir):
    parts = repo_url.strip("/").split("/")
    if len(parts) < 5 or parts[-2] != "tree":
        raise ValueError("Invalid GitHub URL. Use the format: https://github.com/owner/repo/tree/branch")

    owner, repo, branch = parts[3], parts[4], parts[-1]
    api_url = f"https://api.github.com/repos/{owner}/{repo}/contents"
    headers = {"Accept": "application/vnd.github.v3+json"}

    def download_recursive(path, save_path):
        response = requests.get(f"{api_url}/{path}?ref={branch}", headers=headers)
        if response.status_code != 200:
            print(f"Failed to fetch {path}: {response.status_code}")
            return

        items = response.json()
        os.makedirs(save_path, exist_ok=True)
        for item in items:
            item_path = os.path.join(save_path, item["name"])
            if item["type"] == "file":
                file_response = requests.get(item["download_url"])
                with open(item_path, "wb") as file:
                    file.write(file_response.content)
                print(f"Downloaded file: {item_path}")
            elif item["type"] == "dir":
                print(f"Creating folder: {item_path}")
                download_recursive(item["path"], item_path)

    
    download_recursive("", local_dir)

github_repo_url = "https://github.com/kamaleshvijayakumarhashagile/sample_git/tree/main"
local_directory = "./downloaded_repo"

download_github_folder(github_repo_url, local_directory)


 """


import subprocess
local_file_path = '/home/kamalesh_vijayakumar/vscode/manoj_tasks/git_and_solr/sample_folder/downloaded_repo/entity_conf_9_7_2'

container_id = 'c06b545bd3d5'  

solr_target_dir = '/solr-9.7.0/server/solr/configsets/entity_conf_9_7'

copy_command = f'docker cp {local_file_path} {container_id}:{solr_target_dir}'


result = subprocess.run(copy_command, shell=True, capture_output=True, text=True)


if result.returncode == 0:
    print('File copied successfully.')
else:
    print(f'Failed to copy file. Error: {result.stderr}')


