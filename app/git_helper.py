# pip install gitpython
import git
import os


def clone_or_fetch_from_repo(repo_url):
    repo_path = repo_url.split("/")[-1].split(".")[0]
    repo_path = os.path.join('repos', repo_path)
    brita_branch_name = "brita_update"
    # If the repo hasn't been cloned yet
    if not os.path.isdir(repo_path):
        repo = git.Repo.clone_from(repo_url, repo_path)
    # The repo is already cloned
    else:
        repo = git.Repo(repo_path)
    origin = repo.remote('origin')
    # Fetch by default
    origin.fetch()
    # Get current branch
    current_branch = repo.active_branch
    current_branch_name = current_branch.name
    # Create a brita branch if it does not exist
    if not (current_branch_name == brita_branch_name):
        brita_branch = repo.create_head(brita_branch_name, current_branch)
        brita_branch.checkout()

    return repo, repo_path


def read_src_files(repo_path, action):
    # Files targeted for readin
    if action == "readme":
        target_files = ['README.md']
    elif action == "docstrings":
        target_files = ['howdoi.py']
    results_dict = {}
    # Directory walk to find files
    for root, dir, files in os.walk(repo_path, topdown=True):
        for file in files:
            if file in target_files:
                fpath = os.path.join(root, file)
                # Read the file content and add to the results dictionary
                with open(fpath, 'r') as f:
                    res = f.read()
                    results_dict[fpath] = res
    return results_dict
