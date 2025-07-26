
from src.config import Config
from src.entity.item import Item
from src.git_handler import GitHandler
from json import load, dump


class DataHandler:
    def __init__(self, config: Config):
        self.config = config
        self.items = []
        self.load_items()

    def load_items(self):
        try:
            self.items = []
            with open(self.config.getItemListFilepath(), "r") as f:
                data = load(f)
                for i in data:
                    item = Item(i["name"]) 
                    if("process" in i):
                        item.process = i["process"]
                    item.setPaths(i["paths"])
                    self.items.append(item)
                    isUpToDate = True
                    for index, path in enumerate(item.paths):
                        branch_name = item.getBranchName(index)
                        absolute_path = self.config.convertRelative2Absolute(path)
                        isUpToDate = GitHandler.check_changes(absolute_path, branch_name)
                        if(not isUpToDate):
                            break
                    item.setUpToDate(isUpToDate)

        except:
            pass              

    def add_item(self, item: Item):
        self.items.append(item)
        self.save_items()

    def update_item(self, index: int, item: Item):
        self.items[index] = item
        self.save_items()

    def save_items(self):
        with open(self.config.getItemListFilepath(), "w") as f:
            dump(list(map(DataHandler.item2JSON, self.items)), f, indent=4)

    def item2JSON(item: Item):
        if(item.process != None and len(item.process) > 0):
            return {"name" : item.name, "process": item.process, "paths": item.paths}
        return {"name": item.name, "paths": item.paths}
