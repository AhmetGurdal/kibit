from kivy.uix.boxlayout import BoxLayout
from kivy.uix.button import Button
from kivy.uix.label import Label

from src.entity.history import History


class HistoryBox(BoxLayout):
    def __init__(self, history: History, index: int, **kwargs):
        super().__init__(**kwargs)
        self.history = history
        self.index = index
        self.orientation = 'horizontal'
        self.size_hint_y = None
        self.height = 50
        self.spacing = 10
        self.padding = (10, 5)
        self.time_label = Label(text=f"{self.history.get_time()}", size=(
            1, 30), size_hint_y=None)
        self.commit_id_label = Label(text=f"{self.history.get_commit_id()}", size=(
            1, 30), size_hint_y=None)
        self.load_button = Button(text='Load', size=(
            1, 30), size_hint_y=None, size_hint_x=0.2)
        self.load_button.bind(on_press=self.on_load)
        self.add_widget(self.time_label)
        self.add_widget(self.commit_id_label)
        self.add_widget(self.load_button)

    def on_load(self, _):
        pass
