from src.git_handler import GitHandler
from src.config import Config
from src.data_handler import DataHandler
import psutil

class ProcessHandler:
    
    def __init__(self):
        self.running_items = {}
        self.ended_items = []


    def check_processes(self, dataHandler : DataHandler):
        # for proc in psutil.process_iter(['pid', 'name', 'exe']):
        procs = {}
        for proc in psutil.process_iter(['pid', 'name']):
            try:
                procs[proc.info["name"]] = proc.info["pid"]
                # print(f"PID : {proc.info["pid"]}, Name: {proc.info['name']}, Path: {proc.info['exe']}")
                # print(f"PID : {proc.info["pid"]}, Name: {proc.info['name']}")
            except (psutil.NoSuchProcess, psutil.AccessDenied, psutil.ZombieProcess):
                pass
        for item in dataHandler.items:
            if(item.process):
                if(item.process in procs):
                    self.running_items[item.process] = item
                    item.setLoading(True)
                
        for process in self.running_items:
            if(process not in procs):
                self.ended_items.append(self.running_items[process])
    
        for ended_item in self.ended_items:
            del self.running_items[ended_item.process]
    
        # print("Running Items:")
        # for i in self.running_items:
        #     print(i +" -> " + self.running_items[i].toStr())
        # print("--------------------")

        # print("Ended Items:")
        # for i in self.ended_items:
        #     print(i.toStr())
        # print("--------------------")


    def update_ended_items(self, config : Config):
        for item in self.ended_items:
            print(item.toStr())
            result = GitHandler.update_item(item, config)
            if(result.success):
                item.setUpToDate(True)
            else:
                item.setUpToDate(False)
        self.ended_items = []
            
