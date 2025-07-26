from src.entity.history import History
from src.entity.item import Item
from src.config import Config

from git import Repo, InvalidGitRepositoryError, GitCommandError
from datetime import datetime


class GitHandler:

    @staticmethod
    def init_and_update_item(item: Item, config : Config) -> bool:
        result = True
        for index, path in enumerate(item.paths):
                branch_name = item.getBranchName(index)
                absolute_path = config.convertRelative2Absolute(path=path)
                result = GitHandler.setup_git_repo(
                    path=absolute_path, remote_url=config.getGitLink(), branch_name=branch_name)
                result = GitHandler.git_push(
                    repo_path=absolute_path, branch=branch_name)
        print("Update is Completed!")
        item.setLoading(False)
        item.setUpToDate(True)
        return result
                
    @staticmethod
    def update_item(item : Item, config : Config) -> dict:
        try:
            for index, path in enumerate(item.paths):
                branch_name = item.getBranchName(index)
                absolute_path = config.convertRelative2Absolute(path=path)
                return GitHandler.git_push(
                    repo_path=absolute_path, branch=branch_name)
            print("Update is Completed!")
            item.setLoading(False)
            item.setUpToDate(True)
        except Exception as e:
            print("ERR: ", e)

    @staticmethod
    def git_push(repo_path: str, branch: str) -> dict:
        try:
            repo = Repo(repo_path)
        except:
            print("Repo not found!")
            return {"success" : False, "message" : "Repo not found!\n"}
        try:
            repo.git.checkout(branch)
        except:
            repo.git.checkout("-b", branch)
        try:
            repo.git.add(A=True)
            repo.git.commit(m='New Save')
            repo.git.push('--set-upstream', 'origin', branch)
            return {"success" : True, "message" : "SUCCESS : Data on path is saved!\n"}
        except GitCommandError as e:
            print(f"Push Error: {e}")
            if ("Your branch is up to date" in e.stdout):
                return {"success" : True, "message" : f"SUCCESS : Up to date!\n"}
            else:
                print(e)
                return {"success" : False, "message" : f"ERROR : Push Error: Unknown Error!\n"}

    @staticmethod
    def git_pull(repo_path: str, branch: str):
        try:
            repo = Repo(repo_path)
            repo.git.checkout(branch)
            repo.remotes.origin.pull(branch)
            # repo.git.pull('--set-upstream', 'origin', branch)
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
            except Exception as e:
                print("Repo active branch issue", e)
        except GitCommandError as e:
            print(f"Commit History Error: {e}")
        return history_list
    
    @staticmethod
    def check_changes(repo_path:str, branch : str):
        try:
            repo = Repo(repo_path)
            try:
                # repo.git.checkout(branch)
                local_branch = repo.heads[branch]
                remote_branch = repo.remotes.origin.refs[branch]

                # Compare commits
                behind = list(repo.iter_commits(f'{local_branch}..{remote_branch}'))
                ahead = list(repo.iter_commits(f'{remote_branch}..{local_branch}'))
                print(repo_path)
                print("behind :",behind)
                print("ahead : ", ahead)
                return not behind and not ahead and not repo.is_dirty(untracked_files=True)
            except Exception as e:
                print("Repo active branch issue", e)
        except GitCommandError as e:
            print(f"Status Check Error: {e}")


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
