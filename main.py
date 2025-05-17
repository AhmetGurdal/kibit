from src.ui.gui import GUI
from src.config import Config
from src.data_handler import DataHandler

config = Config()
data_handler = DataHandler(config=config)
GUI().start(config=config, data_handler=data_handler)
