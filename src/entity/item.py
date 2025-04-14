class Item:

    def __init__(self, name: str):
        self.setPaths([])
        self.setName(name)

    def setPaths(self, paths: list):
        self.paths = paths

    def setName(self, name: str):
        self.name = name

    def toStr(self):
        return f"Item: {self.name} has {len(self.paths)} paths"
