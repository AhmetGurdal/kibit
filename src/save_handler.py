from os import listdir,makedirs
from json import load
from shutil import copytree, rmtree
from src.statics import Static

class Save_Handler:
    games = None
    game_paths = None
    
    with open(Static.GAME_LIST_PATH) as f:
        games = load(f)
    try:
        with open(Static.GAME_PATH) as f:
            game_paths = load(f)
    except:
        pass

    @staticmethod
    def deleteSaves():
        for i in listdir(f"./{Save_Handler.SAVES}"):
            rmtree(f"./{Save_Handler.SAVES}/{i}")

    @staticmethod
    def collectSaves():
        if(Static.SAVES not in listdir("./")):
            makedirs(f"./{Static.SAVES}")
        for game_index in range(len(Save_Handler.games)):
            game = Save_Handler.games[game_index]
            try:
                for index, path in enumerate(game["paths"]):
                    if("{GAME_PATH}" in path):
                        try:  
                            path = str(path).format(GAME_PATH=Save_Handler.game_paths[game["name"]])
                            print(path)                         
                        except:
                            print(f"'GAME PATH' for {game["name"]} is not defined!")
                    path = str(path).format(USER_PATH = Static.defaultUserPath)
                    copytree(path, f"./{Save_Handler.SAVES}/{game["name"]}/{index}")
                    print(f"{game["name"]} is collected!" )
            except:
                print(f"Error - {game["name"]} is not collected!")
                pass
    
    @staticmethod
    def loadSaves():
        for index in range(len(Save_Handler.games)):
            Save_Handler._loadSave(index)
    
    @staticmethod
    def listGames():
        for i,v in enumerate(Save_Handler.games):
            print(f"{i+1} - {v["name"]}")

    @staticmethod
    def _loadSave(index):
        game = Save_Handler.games[index-1]
        game_save = f"./{Save_Handler.SAVES}/{game["name"]}/"
        for index,path in enumerate(game["paths"]):
            path = str(path).format(USER_PATH = Static.defaultUserPath)
            rmtree(path)
            game_save += f"{index}/"
            try:
                copytree(game_save, path)
                print(f"{game["name"]} - save is Loaded!")
            except:
                print(f"Error - {game["name"]} save load error!")
                pass

    @staticmethod
    def loadSave():
        Save_Handler.listGames()
        index = int(input(":"))
        Save_Handler._loadSave(index)
        
        