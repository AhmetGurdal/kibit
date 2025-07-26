from src.ui.components.item_box import ItemBox
from src.data_handler import DataHandler

from kivy.uix.scrollview import ScrollView
from kivy.uix.boxlayout import BoxLayout
from kivy.uix.button import Button
from kivy.clock import Clock


class ListScreen(BoxLayout):

    def __init__(self, data_handler: DataHandler, to_option_view, to_add_view, to_detail_view, delete_item, **kwargs):
        super().__init__(**kwargs)
        # ScrollView container
        self.scroll_view = ScrollView(size_hint=(1, 1))
        self.data_handler = data_handler
        self.to_detail_view = to_detail_view
        self.delete_item = delete_item
        self.to_option_view = to_option_view
        self.to_add_view = to_add_view
        # Inner layout (to be scrolled)
        self.layout = BoxLayout(orientation='vertical', size_hint_y=None,)
        self.layout.bind(minimum_height=self.layout.setter('height'))

        for i, item in enumerate(self.data_handler.items):
            btn = ItemBox(item=item,
                          index=i, 
                          is_even=i % 2 == 0, 
                          to_detail_view=self.to_detail_view, 
                          delete_item=self.delete_item)
            self.layout.add_widget(btn)

        self.scroll_view.add_widget(self.layout)
        self.add_btn = Button(text=f"Add", size_hint_y=None, height=50)
        self.add_btn.bind(on_press=self.to_add_view)
        self.option_btn = Button(text=f"Options", size_hint_y=None, height=50)
        self.option_btn.bind(on_press=self.to_option_view)

        self.add_widget(self.option_btn)
        self.add_widget(self.scroll_view)
        self.add_widget(self.add_btn)
        Clock.schedule_interval(self.updateView, 0.5)
            
    def updateView(self,_):
        self.remove_widget(self.scroll_view)
        self.remove_widget(self.option_btn)
        self.remove_widget(self.add_btn)
        self.layout = BoxLayout(orientation='vertical', size_hint_y=None)
        self.layout.bind(minimum_height=self.layout.setter('height'))
        for i, item in enumerate(self.data_handler.items):
            btn = ItemBox(item=item, 
                          index=i, 
                          is_even=i % 2 == 0, 
                          to_detail_view=self.to_detail_view, 
                          delete_item=self.delete_item)
            self.layout.add_widget(btn)
        self.scroll_view = ScrollView(size_hint=(1, 1))
        self.scroll_view.add_widget(self.layout)
        self.add_widget(self.option_btn)
        self.add_widget(self.scroll_view)
        self.add_widget(self.add_btn)