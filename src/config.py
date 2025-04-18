from src.statics import Static
from configparser import ConfigParser
from os import makedirs
from json import dump, load


class Config:

    def __init__(self):
        self.config = ConfigParser()
        self.load_config()

    def load_config(self):
        # try:
        self.config.read(Static.defaultConfigFilepath)
        if ("item_list_filepath" not in self.config["DEFAULT"]):
            self.config["DEFAULT"]["item_list_filepath"] = Static.defaultItemListFilepath
            self.config["DEFAULT"]["relative_paths_filepath"] = Static.defaultRelativePathsFilepath
            self.config["DEFAULT"]["git_repo_link"] = Static.defaultGitLink
            self.saveConfig()
        self.loadRelativePaths()

    def getRelativePathsFilepath(self):
        return self.config["DEFAULT"]["relative_paths_filepath"]

    def getGitLink(self):
        return self.config["DEFAULT"]["git_repo_link"]

    def getItemListFilepath(self):
        return self.config["DEFAULT"]["item_list_filepath"]

    def setRelativePathsFilepath(self, path: str):
        self.config["DEFAULT"]["relative_paths_filepath"] = path
        self.saveConfig()

    def setGitLink(self, link: str):
        self.config["DEFAULT"]["git_repo_link"] = link
        self.saveConfig()

    def setItemListFilepath(self, path: str):
        self.config["DEFAULT"]["item_list_filepath"] = path
        self.saveConfig()

    def saveConfig(self, is_retry=False):
        try:
            with open(Static.defaultConfigFilepath, 'w') as configfile:
                self.config.write(configfile)
        except:
            if (not is_retry):
                makedirs(Static.defaultConfigFolder)
                self.saveConfig(is_retry=True)
            else:
                print("Error while creating config file!")
                quit()

    def setRelativePaths(self, data):
        self.relative_paths = data

    def getRelativePaths(self):
        return self.relative_paths

    def saveRelativePaths(self, is_retry=False):
        try:
            with open(self.getRelativePathsFilepath(), "w") as f:
                dump(self.relative_paths, f, indent=4)
        except:
            if (not is_retry):
                makedirs(Static.defaultConfigFolder)
                self.saveRelativePaths(is_retry=True)
            else:
                print("Error while creating config file!")
                quit()

    def loadRelativePaths(self):
        try:
            with open(self.getRelativePathsFilepath(), "r") as f:
                self.relative_paths = load(f)
        except:
            self.relative_paths = {}
            print("Error while importing relative paths!")
            pass
