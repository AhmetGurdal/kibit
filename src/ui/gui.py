from src.entity.item import Item
from src.ui.screens.option_screen import OptionScreen
from src.ui.screens.list_screen import ListScreen
from src.ui.screens.detail_screen import DetailScreen
from src.ui.screens.history_screen import HistoryScreen
from src.ui.screens.manual_save_screen import ManualSaveScreen
from src.ui.screens.relative_paths_screen import RelativePathsScreen
from src.data_handler import DataHandler
from src.process_handler import ProcessHandler
from src.config import Config
import kivy
from kivy.app import App
from kivy.uix.boxlayout import BoxLayout
from kivy.core.window import Window
import pystray
from PIL import Image
from threading import Event, Thread
from time import sleep

kivy.require('2.1.0')

class GUI(App):

    def start(self, config: Config, data_handler: DataHandler, process_handler : ProcessHandler):
        self.tray_icon_running = Event()
        self.tray_icon = None
        self.appConfig = config
        self.title = "Kibit"
        self.data_handler = data_handler
        self.process_handler = process_handler
        self.window = BoxLayout(orientation='vertical', padding=10, spacing=10)
        self.current_view = None
        self.run()

    def run_in_background(self):
        while True:
            self.process_handler.check_processes(self.data_handler)
            self.process_handler.update_ended_items(self.appConfig)
            sleep(10)
            
    def build(self):
        Window.bind(on_request_close=self.on_request_close)
        self.current_view = ListScreen(data_handler=self.data_handler,
                                       to_option_view=self.to_option_view,
                                       to_add_view=self.to_add_view,
                                       to_detail_view=self.to_detail_view,
                                       delete_item=self.delete_item,
                                       orientation='vertical',
                                       spacing=10,
                                       padding=10)
        self.window.add_widget(self.current_view)
        if self.tray_icon_running.is_set():
            self.tray_icon_running.wait(timeout=5)
        return self.window

    def on_start(self):
        Thread(target=self.run_tray_icon, daemon=True).start()

    def on_request_close(self, *args):
        thread = Thread(target=self.run_in_background, daemon=True)
        thread.start()
        self.hide_window()
        return True 

    def show_window(self, *args):
        Window.show()

    def hide_window(self, *args):
        Window.hide()

    def run_tray_icon(self):
        try:
            image = Image.open("./bat.png")
            self.tray_icon = pystray.Icon(
                'kibit',
                image,
                'Kibit',
                menu=pystray.Menu(
                    # pystray.MenuItem('Show App', self.show_window_from_tray),
                    # pystray.MenuItem('Hide App', self.hide_window_from_tray),
                    # pystray.Menu.SEPARATOR, 
                    pystray.MenuItem('Quit', self.quit_app_from_tray)
                )
            )
            print("Kibit: Starting tray icon.")
            self.tray_icon_running.set()
            self.tray_icon.run()
        except Exception as e:
            print(f"Kibit: Error running tray icon: {e}")
        finally:
            self.tray_icon_running.clear()

    # def show_window_from_tray(self, icon, item):
    #     App.get_running_app().show_window()
        
    # def hide_window_from_tray(self, icon, item):
    #     App.get_running_app().hide_window()
        
    def quit_app_from_tray(self, icon, item):
        if self.tray_icon:
            self.tray_icon.stop()
        App.get_running_app().stop()

    def to_detail_view(self, item: Item, index: int):
        self.window.remove_widget(self.current_view)
        self.current_view = DetailScreen(
            data_handler=self.data_handler,
            save_item=self.update_item,
            to_history_view=self.to_history_view,
            to_list_view=self.to_list_view,
            convertAbsolute2Relative=self.appConfig.convertAbsolute2Relative,
            convertRelative2Absolute=self.appConfig.convertRelative2Absolute,
            orientation='vertical',
            spacing=10,
            padding=10)
        self.current_view.set_item(index, item)
        self.window.add_widget(self.current_view)

    def to_list_view(self, _):
        self.window.remove_widget(self.current_view)
        self.current_view = ListScreen(data_handler=self.data_handler,
                                       to_option_view=self.to_option_view,
                                       to_add_view=self.to_add_view,
                                       to_detail_view=self.to_detail_view,
                                       delete_item=self.delete_item,
                                       orientation='vertical',
                                       spacing=10,
                                       padding=10)
        self.window.add_widget(self.current_view)

    def to_add_view(self, _):
        self.window.remove_widget(self.current_view)
        self.current_view = DetailScreen(
            data_handler=self.data_handler,
            save_item=self.add_new_item,
            to_list_view=self.to_list_view,
            to_history_view=self.to_history_view,
            convertAbsolute2Relative=self.appConfig.convertAbsolute2Relative,
            convertRelative2Absolute=self.appConfig.convertRelative2Absolute,
            orientation='vertical',
            spacing=10,
            padding=10)
        self.window.add_widget(self.current_view)

    def to_history_view(self, path, path_index, parent_item: Item, parent_index):
        self.window.remove_widget(self.current_view)
        absolute_path = self.appConfig.convertRelative2Absolute(path)
        self.current_view = HistoryScreen(
            path=absolute_path,
            path_index=path_index,
            branch_name=parent_item.getBranchName(path_index),
            parent_item=parent_item,
            parent_index=parent_index,
            to_detail_view=self.to_detail_view)
        self.window.add_widget(self.current_view)

    def to_option_view(self, _):
        self.window.remove_widget(self.current_view)
        self.current_view = OptionScreen(
            self.appConfig,
            self.to_list_view,
            to_manual_path=self.to_manual_commit_path,
            to_relative_path=self.to_relative_path_view,
            orientation='vertical',
            spacing=10,
            padding=10)
        self.window.add_widget(self.current_view)

    def to_relative_path_view(self, _):
        self.window.remove_widget(self.current_view)
        self.current_view = RelativePathsScreen(
            relative_paths=self.appConfig.getRelativePaths(),
            to_back=self.to_option_view, save_relative_paths=self.on_relative_paths_save)
        self.window.add_widget(self.current_view)

    def to_manual_commit_path(self, _):
        self.window.remove_widget(self.current_view)
        self.current_view = ManualSaveScreen(
            on_back=self.to_option_view,
            config=self.appConfig, dataHandler=self.data_handler)
        self.window.add_widget(self.current_view)

    def on_relative_paths_save(self, data):
        self.appConfig.setRelativePaths(data)
        self.appConfig.saveRelativePaths()

    def add_new_item(self, **kargv):
        item = kargv.get("item")
        self.data_handler.items.append(item)
        self.data_handler.save_items()

    def update_item(self, **kargv):
        index = kargv.get("index")
        item = kargv.get("item")
        self.data_handler.items[index] = item
        self.data_handler.save_items()

    def delete_item(self, **kargv):
        index = kargv.get("index")
        del self.data_handler.items[index]
        self.data_handler.save_items()
        self.to_list_view(None)
