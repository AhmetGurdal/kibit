
from src.config import Config
from src.entity.item import Item

from json import load, dump


class DataHandler:
    def __init__(self, config: Config):
        self.config = config
        self.items = []
        self.load_items()

    def load_items(self):
        try:
            with open(self.config.getItemListFilepath(), "r") as f:
                data = load(f)
                for i in data:
                    item = Item(i["name"])
                    item.setPaths(i["paths"])
                    self.items.append(item)
        except:
            pass

    def save_items(self):
        with open(self.config.getItemListFilepath(), "w") as f:
            dump(self.items, f)
