from src.entity.item import Item

from kivy.uix.boxlayout import BoxLayout
from kivy.uix.label import Label
from kivy.uix.button import Button
from kivy.graphics import Color, Rectangle
from kivy.uix.popup import Popup


class ItemBox(BoxLayout):

    def __init__(self, item: Item, index, is_even, to_detail_view=None, delete_item=None, **kwargs):
        super().__init__(**kwargs)
        self.to_detail_view = to_detail_view
        self.delete_item = delete_item
        self.index = index
        self.item = item
        self.orientation = 'horizontal'
        self.size_hint_y = None
        self.height = 50
        self.spacing = 10
        self.padding = (10, 5)
        with self.canvas.before:
            if (is_even):
                Color(0.2, 0.2, 0.2, 1)  # RGBA, values from 0 to 1
            else:
                Color(0.25, 0.25, 0.25, 1)
            self.rect = Rectangle(size=self.size, pos=self.pos)
        self.bind(size=self._update_rect, pos=self._update_rect)

        self.label = Label(text=f"{index+1}- {item.name}", size_hint_x=0.6,
                           halign='left', valign='middle')
        self.label.bind(size=self._update_label_text_align)

        self.detail_button = Button(text='detail', size_hint_x=0.2)
        self.detail_button.bind(on_press=self.detail)
        self.delete_button = Button(
            text='Delete', size_hint_x=0.2, background_color=(1, 0, 0, 1))
        self.delete_button.bind(on_press=self.show_popup)
        self.add_widget(self.label)
        self.add_widget(self.detail_button)
        self.add_widget(self.delete_button)

    def _update_rect(self, *args):
        self.rect.size = self.size
        self.rect.pos = self.pos

    def detail(self, _):
        self.to_detail_view(self.item, self.index)

    def _update_label_text_align(self, _, value):
        self.label.text_size = value

    def on_delete_item(self, _):
        self.delete_item(index=self.index)
        self.popup.dismiss()

    def show_popup(self, _):
        popup_content = BoxLayout(orientation='vertical', padding=10)
        popup_content.add_widget(
            Label(text="Do you want to delete this item?"))
        accept_button = Button(text="Accept", size_hint=(
            1, 0.3), background_color=(1, 0, 0, 0.6))
        accept_button.bind(on_press=self.on_delete_item)
        close_button = Button(text="Close", size_hint=(1, 0.3))
        close_button.bind(on_press=self.close_popup)
        popup_content.add_widget(accept_button)
        popup_content.add_widget(close_button)

        self.popup = Popup(
            title="Are you sure?", content=popup_content, size_hint=(0.5, 0.5))
        self.popup.open()

    def close_popup(self, _):
        self.popup.dismiss()
