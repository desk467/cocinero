import os
import uuid
import subprocess
import shutil


def clone(repo_url):
    repo_destination_name = f'repo-{uuid.uuid4()}'
    repo_destination_path = f'/tmp/{repo_destination_name}'
    command = f'git clone {repo_url} {repo_destination_path}'

    process = subprocess.Popen(command.split(), stdout=subprocess.PIPE)
    output, error = process.communicate()

    return repo_destination_path


def clear_repo(repo_destination_path):
    os.remove(repo_destination_path)


def move_repo(repo_src_path, repo_destination_path):
    shutil.move(repo_src_path, repo_destination_path)


def commit_changes(repo_src_path, project_name):
    command = f'git commit -am'

    process = subprocess.Popen(command.split(
    ) + [f"chore: Cooking boilerplate to become {project_name}"], stdout=subprocess.PIPE)
    output, error = process.communicate()

    print(output, error)
