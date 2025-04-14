from time import sleep
from src.save_handler import Save_Handler
from src.git_handler import GitHandler
class Controller:

    commands = ["store", "list", "return"]

    @staticmethod
    def printCommands():
        print(":store -> Start storing the game save files")
        print(":list -> List commits")
        print(":return -> Return to a prev commit")
    
    @staticmethod
    def start():
        Controller.printCommands()
        while True:
            command = input(":")
            if(command not in Controller.commands):
                print("Error - Unknown Command!")
            else:
                if(command == "store"):
                    Save_Handler.deleteSaves()
                    Save_Handler.collectSaves()
                    pass
                elif(command == "list"):
                    GitHandler.get_commits()
                    pass
                elif(command == "return"):
                    commit_id = input("Commit id:")
                    print("Commit id:", commit_id)
                    pass