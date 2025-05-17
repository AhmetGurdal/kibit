from kivy.uix.boxlayout import BoxLayout
from kivy.uix.textinput import TextInput
from kivy.uix.button import Button
from kivy.uix.popup import Popup
from kivy.uix.label import Label

from tkinter import filedialog
from tkinter import Tk


class PathBox(BoxLayout):
    def __init__(self, index,
                 on_delete,
                 is_detail,
                 to_history,
                 parent_item,
                 parent_index,
                 text=None, ** kwargs):
        super().__init__(**kwargs)
        self.to_history = to_history
        self.parent_item = parent_item
        self.parent_index = parent_index
        self.index = index
        self.orientation = 'horizontal'
        self.size_hint_y = None
        self.height = 50
        self.spacing = 10
        self.padding = (10, 5)
        self.on_delete = on_delete
        if (text is not None):
            self.path_input = TextInput(
                hint_text="Path", text=text, size=(1, 30), size_hint_y=None)
        else:
            self.path_input = TextInput(
                hint_text="Path", size=(1, 30), size_hint_y=None)
        self.delete_button = Button(text='Delete', size=(
            1, 30), size_hint_y=None, size_hint_x=0.2, background_color=(1, 0, 0, 1))
        self.delete_button.bind(on_press=self.show_popup)
        # Button to open folder picker
        self.pick_folder_button = Button(
            text="Select", size=(1, 30),
            size_hint_y=None, size_hint_x=0.2)
        self.pick_folder_button.bind(on_press=self.open_filechooser)
        self.add_widget(self.path_input)
        self.add_widget(self.pick_folder_button)
        if (is_detail):
            history_button = Button(text="History", size=(1, 30),
                                    size_hint_y=None, size_hint_x=0.2)
            history_button.bind(on_press=self.on_history)
            self.add_widget(history_button)
        self.add_widget(self.delete_button)

    def get_value(self):
        return self.path_input.text

    def on_history(self, _):
        self.to_history(path=self.path_input.text,
                        path_index=self.index,
                        parent_item=self.parent_item,
                        parent_index=self.parent_index)

    def on_path_delete(self, _):
        self.on_delete(self.index)
        self.popup.dismiss()

    def open_filechooser(self, _):
        # Create a FileChooserPopup with a folder selection mode
        root = Tk()
        root.withdraw()
        root.folder = filedialog.askdirectory(
            initialdir="/", title="Select Folder Path")
        self.path_input.text = root.folder

    def show_popup(self, _):
        popup_content = BoxLayout(orientation='vertical', padding=10)
        popup_content.add_widget(
            Label(text="Do you want to delete this path?"))
        accept_button = Button(text="Accept", size_hint=(
            1, 0.3), background_color=(1, 0, 0, 0.6))
        accept_button.bind(on_press=self.on_path_delete)
        close_button = Button(text="Close", size_hint=(1, 0.3))
        close_button.bind(on_press=self.close_popup)
        popup_content.add_widget(accept_button)
        popup_content.add_widget(close_button)

        self.popup = Popup(
            title="Are you sure?", content=popup_content, size_hint=(0.5, 0.5))
        self.popup.open()

    def close_popup(self, _):
        self.popup.dismiss()
