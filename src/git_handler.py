from src.entity.history import History

import git
from datetime import datetime


class GitHandler:

    @staticmethod
    def git_push(repo_path: str, branch: str):
        repo = git.Repo(repo_path)
        repo.git.checkout(branch)
        repo.git.add(A=True)
        repo.git.commit(m='New Save')
        repo.git.push('--set-upstream', 'origin', branch)

    @staticmethod
    def git_pull(repo_path: str, branch: str):
        repo = git.Repo(repo_path)
        repo.git.checkout(branch)
        repo.git.pull('--set-upstream', 'origin', branch)

    @staticmethod
    def get_commits(repo_path: str, branch: str):
        history_list = list()
        repo = git.Repo(repo_path)
        repo.active_branch = branch
        for commit in repo.iter_commits():
            committed_datetime = datetime.fromtimestamp(commit.committed_date)
            history_list.append(History(commit.hexsha, committed_datetime))
