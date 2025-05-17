from src.config import Config

from kivy.uix.boxlayout import BoxLayout
from kivy.uix.button import Button
from kivy.uix.textinput import TextInput
from kivy.uix.label import Label
from kivy.uix.popup import Popup
from kivy.uix.checkbox import CheckBox


class OptionScreen(BoxLayout):

    def __init__(self, config: Config, on_back_button, to_manual_path, to_relative_path, **kwargs):
        super().__init__(**kwargs)
        self.config = config
        header = BoxLayout(orientation="horizontal",
                           size_hint_y=None, size=(1, 50))

        # Title label
        title_label = Label(text="Options", font_size=20,
                            size=(1, 50), size_hint_y=None)
        back_button = Button(text="Back", size=(
            100, 50), size_hint=(None, None))
        back_button.bind(on_press=on_back_button)
        header.add_widget(back_button)
        header.add_widget(title_label)
        self.add_widget(header)

        github_box = BoxLayout(orientation='horizontal',
                               padding=10, spacing=10)
        self.repo_input = TextInput(
            hint_text="https://github.com/user/repo",
            multiline=False,
            size=(50, 50),
            size_hint_y=None)
        github_box.add_widget(self.repo_input)
        if (len(config.getGitLink()) > 0):
            self.repo_input.text = config.getGitLink()
        self.submit_button = Button(
            text="Save", size=(100, 50), size_hint=(None, None))
        self.submit_button.bind(on_press=self.save_repo_url)
        github_box.add_widget(self.submit_button)
        self.add_widget(github_box)
        self.on_start_checkbox = CheckBox()
        self.on_start_checkbox.bind(active=self.on_checkbox_active)
        self.add_widget(self.on_start_checkbox)
        relative_paths_button = Button(
            text="Relative Paths", size_hint_y=None, size=(1, 50))
        relative_paths_button.bind(on_press=to_relative_path)
        manual_commit_button = Button(text="Manual Save",
                                      size_hint_y=None, size=(1, 50))
        manual_commit_button.bind(on_press=to_manual_path)
        self.add_widget(relative_paths_button)
        self.add_widget(manual_commit_button)
        # self.pick_folder_button = Button(
        #     text="Choose Folder", size_hint=(1, 1))
        # self.pick_folder_button.bind(on_press=self.open_filechooser)
        # self.add_widget(self.pick_folder_button)

    def add_to_startup(self, file_path=""):
        import os
        if file_path == "":
            file_path = os.path.dirname(os.path.realpath(__file__))
        bat_path = f'{self.config.userPath}\AppData\Roaming\Microsoft\Windows\Start Menu\Programs\Startup'
        with open(bat_path + '\\' + "open.bat", "w+") as bat_file:
            bat_file.write(r'start "" "%s"' % file_path)

    def on_checkbox_active(self, checkbox, value):
        if value:
            print('The checkbox', checkbox, 'is active')

        else:
            print('The checkbox', checkbox, 'is inactive')

    # def open_filechooser(self, _):
    #     root = Tk()
    #     root.withdraw()
    #     root.folder = filedialog.askdirectory(
    #         initialdir="/", title="Select Save Folder")
    #     print(root.folder)

    def save_repo_url(self, _):
        repo_url = self.repo_input.text
        print(repo_url)
        try:
            self.config.setGitLink(repo_url)
            self.show_popup("Success", f"Repository URL saved: {repo_url}")
        except:
            self.show_popup(
                "Error", "Please enter a valid GitHub repository URL.")

    def show_popup(self, title, message):
        popup_content = BoxLayout(orientation='vertical', padding=10)
        popup_content.add_widget(Label(text=message))
        close_button = Button(text="Close", size_hint=(1, 0.3))
        close_button.bind(on_press=self.close_popup)
        popup_content.add_widget(close_button)

        self.popup = Popup(
            title=title, content=popup_content, size_hint=(0.5, 0.5))
        self.popup.open()

    def close_popup(self, _):
        self.popup.dismiss()
