from src.git_handler import GitHandler
from src.data_handler import DataHandler
from src.config import Config
from kivy.uix.boxlayout import BoxLayout
from kivy.uix.textinput import TextInput
from kivy.uix.button import Button
from kivy.clock import mainthread
import threading
from time import sleep


class ManualSaveScreen(BoxLayout):

    def __init__(self, config: Config, dataHandler: DataHandler, on_back, **kwargs):
        super().__init__(**kwargs)
        self.config = config
        self.dataHandler = dataHandler
        self.orientation = "vertical"
        header = ()
        back_button = Button(
            text="Back", size_hint=(None, None), size=(100, 50))
        back_button.bind(on_press=on_back)
        self.commit_button = Button(
            text="Save", size_hint_y=None, size=(1, 50))
        header = BoxLayout(orientation="horizontal",
                           size_hint_y=None, size=(1, 50))
        header.add_widget(back_button)
        header.add_widget(self.commit_button)
        self.commit_button.bind(on_press=self.on_commit)
        self.text_area = TextInput(readonly=True, background_color=(0.1, 0.1, 0.1, 1),
                                   foreground_color=(1, 1, 1, 1), cursor_width=0)
        self.add_widget(header)
        self.add_widget(self.text_area)

    @mainthread
    def append_text(self, text):
        self.text_area.text += text

    @mainthread
    def on_commit(self, _):
        self.change_button_availability()
        self.text_area.text = ""
        threading.Thread(target=self.simulate_process, daemon=True, args=(
            self.change_button_availability,)).start()

    @mainthread
    def change_button_availability(self):
        if (self.commit_button.disabled):
            self.commit_button.disabled = False
        else:
            self.commit_button.disabled = True

    def simulate_process(self, callback):
        for item in self.dataHandler.items:
            sleep(3)
            self.append_text(f"-> {item.name}\n")
            for index, path in enumerate(item.paths):
                branch_name = f"{item.name.replace("-", "_").replace(" ", "")}_{index}"
                self.append_text(f"   ->Path :  {path}\n")
                absolute_path = self.config.convertRelative2Absolute(path=path)
                self.append_text(("    " * 2) + "->Repo Initialization:\n")
                result = GitHandler.setup_git_repo(
                    path=absolute_path, remote_url=self.config.getGitLink(), branch_name=branch_name)
                self.append_text(("    " * 4) + result)
                self.append_text(("    " * 2) + "->Saving Operation:\n")
                result = GitHandler.git_push(
                    repo_path=absolute_path, branch=branch_name)
                self.append_text(("    " * 4) + result)
            self.append_text(
                "---------------------------------------------------------------------------------------------------------------------\n")
        if (callback):
            callback()
