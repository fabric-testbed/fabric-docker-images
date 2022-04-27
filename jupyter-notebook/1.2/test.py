from git import Repo
from git import Git

repo_url="https://github.com/fabric-testbed/jupyter-examples.git"
repo_path="./jupyter-examples"
tag_name="rel1.1.1"

repo = git.Repo.clone_from(repo_url, repo_path, no_checkout=True)
g = Git(repo_path)

g.checkout(tag_name)


