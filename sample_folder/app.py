import os
import requests

def download_github_dir(repo_url, dir_path, save_dir):
    url = f"https://api.github.com/repos/{repo_url}/contents/{dir_path}"
    response = requests.get(url)

    if response.status_code == 200:
        contents = response.json()
        save_path = os.path.join(save_dir, dir_path)

        if not os.path.exists(save_path):
            os.makedirs(save_path)

        for item in contents:
            item_path = item['path']
            if item['type'] == 'file':
                file_url = item['download_url']
                save_file_path = os.path.join(save_path, item['name'])
                download_file(file_url, save_file_path)
            elif item['type'] == 'dir':
                new_save_dir = os.path.join(save_path, item['name'])
                download_github_dir(repo_url, item_path, new_save_dir)
    else:
        print(f"Failed to list contents of {dir_path}. HTTP status code {response.status_code}.")

def download_file(url, save_path):
    response = requests.get(url)
    if response.status_code == 200:
        with open(save_path, 'wb') as file:
            file.write(response.content)
        print(f"Downloaded {save_path}.")
    else:
        print(f"Failed to download file. HTTP status code {response.status_code}.")


repo_url = 'kamaleshvijayakumarhashagile/sample_git'
dir_path = 'sample_dir'  
save_dir = 'downloaded_files'

download_github_dir(repo_url, dir_path, save_dir)

