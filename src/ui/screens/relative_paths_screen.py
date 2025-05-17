from src.ui.components.item_box import ItemBox
from src.ui.components.relative_path_box import RelativePathBox

from kivy.uix.button import Button
from kivy.uix.scrollview import ScrollView
from kivy.uix.label import Label
from kivy.uix.boxlayout import BoxLayout


class RelativePathsScreen(BoxLayout):

    def __init__(self, relative_paths, to_back, save_relative_paths=None, **kwargs):
        super().__init__(**kwargs)
        self.height = 150
        self.relative_path_boxes = {}
        self.orientation = "vertical"
        self.save_relative_paths = save_relative_paths
        header = BoxLayout(orientation="horizontal",
                           size_hint_y=None, size=(1, 50))
        relative_path_label = Label(
            text="Relative Paths", size_hint_y=None, size=(1, 30))
        back_button = Button(text="Back", size_hint=(
            None, None), size=(100, 50))
        back_button.bind(on_press=to_back)
        header.add_widget(back_button)
        header.add_widget(relative_path_label)
        relative_path_scrollview = ScrollView()
        self.relative_path_box = BoxLayout(
            orientation="vertical", size_hint_y=None, padding=(0, 10, 0, 10))
        self.relative_path_box.bind(
            minimum_height=self.relative_path_box.setter('height'))
        relative_path_add_button = Button(
            text="Add path", size_hint_y=None, size=(1, 50))
        relative_path_add_button.bind(on_press=self.add_empty_relative_path)
        relative_path_scrollview.add_widget(self.relative_path_box)
        save_button = Button(text="Save", size_hint_y=None, size=(1, 50))
        save_button.bind(on_press=self.on_save)
        self.add_widget(header)
        self.add_widget(relative_path_scrollview)
        self.add_widget(relative_path_add_button)
        self.add_widget(save_button)
        for key in relative_paths:
            self.add_relative_path(key=key, value=relative_paths[key])

    def add_empty_relative_path(self, _):
        self.add_relative_path(key="", value="")

    def add_relative_path(self, key: str, value: str):
        index = len(self.relative_path_boxes)
        self.relative_path_boxes[index] = RelativePathBox(key=key, value=value,
                                                          index=index, remove_path=self.remove_relative_path)
        self.relative_path_box.add_widget(self.relative_path_boxes[index])

    def remove_relative_path(self, index):
        self.relative_path_box.remove_widget(self.relative_path_boxes[index])
        del self.relative_path_boxes[index]

    def on_save(self, _):
        relatives = dict()
        for path_box in list(self.relative_path_boxes.values()):
            key = path_box.key_input.text
            value = path_box.value_input.text
            if (key != "" and value != ""):
                relatives[key] = value
        self.save_relative_paths(relatives)
