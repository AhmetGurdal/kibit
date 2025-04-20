from src.entity.item import Item
from src.entity.history import History
from src.ui.components.history_box import HistoryBox
from src.git_handler import GitHandler

from kivy.uix.boxlayout import BoxLayout
from kivy.uix.scrollview import ScrollView
from kivy.uix.button import Button
from kivy.uix.label import Label


class HistoryScreen(BoxLayout):

    def __init__(self, path, path_index, branch_name, parent_item: Item, parent_index: int, to_detail_view, **kwargs):
        super().__init__(**kwargs)

        self.orientation = "vertical"
        self.path_index = path_index
        self.brach_name = branch_name
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
        history = self.get_history()
        for index, item in enumerate(history):
            self.history_layout.add_widget(
                HistoryBox(index=index, history=item))
        scroll_view.add_widget(self.history_layout)
        self.add_widget(header)
        self.add_widget(scroll_view)

    def get_history(self):
        branch_name = self.brach_name
        histories = GitHandler.get_commits(self.path, branch_name)
        return histories

    def on_back_press(self, _):
        self.to_detail_view(self.parent_item, self.parent_index)
