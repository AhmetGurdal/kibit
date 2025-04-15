
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

    def add_item(self, item: Item):
        self.items.append(item)
        self.save_items()

    def update_item(self, index: int, item: Item):
        self.items[index] = item
        self.save_items()

    def save_items(self):
        print(self.config.getItemListFilepath())

        with open(self.config.getItemListFilepath(), "w") as f:
            dump(list(map(DataHandler.item2JSON, self.items)), f, indent=4)

    def item2JSON(item: Item):
        return {"name": item.name, "paths": item.paths}
