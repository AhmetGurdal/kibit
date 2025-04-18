from kivy.uix.boxlayout import BoxLayout
from kivy.uix.textinput import TextInput
from kivy.uix.button import Button


class RelativePathBox(BoxLayout):
    def __init__(self, index, remove_path, key="", value="", **kwargs):
        super().__init__(**kwargs)
        self.index = index
        self.remove_path = remove_path
        self.orientation = 'horizontal'
        self.size_hint_y = None
        self.height = 40
        self.spacing = 10
        self.padding = (10, 5)
        self.key_input = TextInput(text=key,
                                   hint_text="Key", size_hint_y=None, size=(1, 30))
        self.value_input = TextInput(text=value,
                                     hint_text="Value", size_hint_y=None, size=(1, 30))
        self.delete_button = Button(
            text="Delete", background_color=(1, 0, 0, 1), size_hint=(None, None), size=(100, 30))
        self.delete_button.bind(on_press=self.on_delete)
        self.add_widget(self.key_input)
        self.add_widget(self.value_input)
        self.add_widget(self.delete_button)

    def on_delete(self, _):
        self.remove_path(self.index)
