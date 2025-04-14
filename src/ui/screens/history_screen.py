from kivy.uix.boxlayout import BoxLayout
from kivy.uix.scrollview import ScrollView
from kivy.uix.button import Button
from kivy.uix.label import Label

from src.entity.item import Item
from src.entity.history import History
from src.ui.components.history_box import HistoryBox


class HistoryScreen(BoxLayout):

    def __init__(self, path, parent_item: Item, parent_index: int, to_detail_view, **kwargs):
        super().__init__(**kwargs)
        history = self.get_history()
        self.orientation = "vertical"
        self.parent_item = parent_item
        self.parent_index = parent_index
        self.to_detail_view = to_detail_view
        header = BoxLayout(orientation="horizontal",
                           size=(1, 50), size_hint_y=None)
        back_button = Button(text="Back", size=(
            100, 50), size_hint=(None, None))
        back_button.bind(on_press=self.on_back_press)
        label = Label(text="History")
        header.add_widget(back_button)
        header.add_widget(label)
        self.path = path
        scroll_view = ScrollView()
        self.history_layout = BoxLayout(
            orientation='vertical', size_hint_y=None)
        self.history_layout.bind(
            minimum_height=self.history_layout.setter('height'))
        for index, item in enumerate(history):
            self.history_layout.add_widget(
                HistoryBox(index=index, history=item))
        scroll_view.add_widget(self.history_layout)
        self.add_widget(header)
        self.add_widget(scroll_view)

    def get_history(self):
        return [History("ABC1234DSADA", "10-10-20")]

    def on_back_press(self, _):
        self.to_detail_view(self.parent_item, self.parent_index)
