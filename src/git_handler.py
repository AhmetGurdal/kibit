from src.entity.history import History

from git import Repo, InvalidGitRepositoryError, GitCommandError
from datetime import datetime


class GitHandler:

    @staticmethod
    def git_push(repo_path: str, branch: str):
        try:
            repo = Repo(repo_path)
        except:
            print("Repo not found!")
            return "Repo not found!\n"
        try:
            repo.git.checkout(branch)
        except:
            repo.git.checkout("-b", branch)
        try:
            repo.git.add(A=True)
            repo.git.commit(m='New Save')
            repo.git.push('--set-upstream', 'origin', branch)
            return "SUCCESS : Data on path is saved!\n"
        except GitCommandError as e:
            print(f"Push Error: {e}")
            if ("Your branch is up to date" in e.stdout):
                return f"SUCCESS : Up to date!\n"
            else:
                print(e)
                return f"ERROR : Push Error: Unknown Error!\n"

    @staticmethod
    def git_pull(repo_path: str, branch: str):
        try:
            repo = Repo(repo_path)
            repo.git.checkout(branch)
            repo.git.pull('--set-upstream', 'origin', branch)
            return True
        except GitCommandError as e:
            print(f"Pull Error: {e}")
            return False

    @staticmethod
    def get_commits(repo_path: str, branch: str):
        history_list = list()
        try:
            repo = Repo(repo_path)
            try:
                repo.git.checkout(branch)
                for commit in repo.iter_commits():
                    committed_datetime = datetime.fromtimestamp(
                        commit.committed_date)
                    history_list.append(
                        History(commit.hexsha, committed_datetime))
            except e:
                print("Repo active branch branch issue", e)
        except GitCommandError as e:
            print(f"Commit History Error: {e}")
        return history_list

    @staticmethod
    def setup_git_repo(path: str,
                       remote_url: str,
                       branch_name: str,
                       remote_name: str = "origin"):
        try:
            repo = Repo(path)
            print("Repository already initialized.")
        except InvalidGitRepositoryError:
            repo = Repo.init(path)
            print("Initialized new Git repository.")

        # Check if the remote already exists
        if remote_name not in [remote.name for remote in repo.remotes]:
            repo.create_remote(remote_name, remote_url)
        #     print(f"Remote '{remote_name}' added with URL: {remote_url}")
        # else:
        #     print(f"Remote '{remote_name}' already exists.")

         # Checkout or create the branch
        if branch_name not in repo.heads:
            try:
                repo.git.checkout('-b', branch_name)
                print(f"Created and checked out new branch '{branch_name}'.")
                return f"Repo and new branch '{branch_name}' are created.\n"
            except GitCommandError as e:
                print(f"ERROR : Branch creation failed: {e}")
                return f"ERROR : Branch creation failed: {e}\n"
        else:
            return "SUCCESS : Repo is created and branch is found!\n"
        # else:
        #     repo.git.checkout(branch_name)
        #     print(f"Checked out existing branch '{branch_name}'.")
