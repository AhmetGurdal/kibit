from src.ui.components.item_box import ItemBox
from src.data_handler import DataHandler

from kivy.uix.scrollview import ScrollView
from kivy.uix.boxlayout import BoxLayout
from kivy.uix.button import Button


class ListScreen(BoxLayout):

    def __init__(self, data_handler: DataHandler, to_option_view, to_add_view, to_detail_view, delete_item, **kwargs):
        super().__init__(**kwargs)
        # ScrollView container
        scroll_view = ScrollView(size_hint=(1, 1))

        # Inner layout (to be scrolled)
        layout = BoxLayout(orientation='vertical', size_hint_y=None,)
        layout.bind(minimum_height=layout.setter('height'))

        for i, item in enumerate(data_handler.items):
            btn = ItemBox(item=item, index=i, is_even=i %
                          2 == 0, to_detail_view=to_detail_view, delete_item=delete_item)
            layout.add_widget(btn)

        scroll_view.add_widget(layout)
        add_btn = Button(text=f"Add", size_hint_y=None, height=50)
        add_btn.bind(on_press=to_add_view)
        option_btn = Button(text=f"Options", size_hint_y=None, height=50)
        option_btn.bind(on_press=to_option_view)

        self.add_widget(option_btn)
        self.add_widget(scroll_view)
        self.add_widget(add_btn)
