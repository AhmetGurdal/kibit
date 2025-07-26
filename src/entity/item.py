from kivy.properties import BooleanProperty

class Item:

    def __init__(self, name: str, process : str | None = None, upToDate : bool = False):
        self.setPaths([])
        self.setName(name)
        self.setProcess(process)
        self.setUpToDate(upToDate)
        self.loading = False

    def setPaths(self, paths: list):
        self.paths = paths

    def setName(self, name: str):
        self.name = name

    def setProcess(self, name : str):
        self.process = name

    def setUpToDate(self, value : bool):
        self.upToDate = value

    def setLoading(self, value : bool):
        self.loading = value

    def getBranchName(self, path_index : int):
        return f"{self.name.replace("-", "_").replace(" ", "")}_{path_index}"

    def toStr(self):
        return f"Item: {self.name} \n\
Paths: {len(self.paths)}\n\
Process: {self.process}\n\
Loading: {self.loading}\n\
UpToDate : {self.upToDate}"
