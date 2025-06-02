
from git import Repo

class GitManager:
    def __init__(self, repo_path: str):
        self.repo = Repo(repo_path)

    def commit_changes(self, message: str) -> None:
        self.repo.git.add(A=True)
        self.repo.index.commit(message)

    def create_branch(self, branch_name: str) -> None:
        self.repo.git.checkout(b=branch_name)

    def push_changes(self, remote_name: str = 'origin', branch_name: str = 'main') -> None:
        self.repo.git.push(remote_name, branch_name)
