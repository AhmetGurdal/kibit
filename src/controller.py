from src.git_handler import GitHandler
from src.data_handler import DataHandler
from src.config import Config


class Controller:

    commands = ["store", "list", "return"]

    # @staticmethod
    # def printCommands():
    #     print(":store -> Start storing the game save files")
    #     print(":list -> List commits")
    #     print(":return -> Return to a prev commit")

    @staticmethod
    def start(config: Config, dataHandler: DataHandler):
        dataHandler.load_items()
        for item in dataHandler.items:
            for index, path in enumerate(item.paths):
                branch_name = f"{item.name.replace(" ", "_")}_{index}"
                absolute_path = config.convertRelative2Absolute(path)
                print("Abs path :", absolute_path)
                GitHandler.setup_git_repo(
                    absolute_path, config.getGitLink(), branch_name)
                GitHandler.git_push(absolute_path, branch_name)
