from src.ui.gui import GUI
from src.config import Config
from src.data_handler import DataHandler
from src.process_handler import ProcessHandler

config = Config()
data_handler = DataHandler(config=config)
process_handler = ProcessHandler()
GUI().start(config=config, data_handler=data_handler, process_handler=process_handler)
