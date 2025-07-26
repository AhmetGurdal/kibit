from kivy.app import App
from kivy.uix.boxlayout import BoxLayout
from kivy.uix.button import Button
from kivy.properties import BooleanProperty, ObjectProperty
from kivy.clock import Clock


# --- Item class with BooleanProperty ---
class Item(BoxLayout):
    is_disabled = BooleanProperty(True)


# --- Main widget ---
class MyWidget(BoxLayout):
    item = ObjectProperty()

    def __init__(self, **kwargs):
        super().__init__(**kwargs)
        self.orientation = "vertical"

        # Create the item (data model)
        self.item = Item()

        # Create the button that depends on item.is_disabled
        self.dependent_button = Button(text="I'm bound to item.is_disabled")
        self.add_widget(self.dependent_button)

        # Bind the button's disabled property to the item's is_disabled
        self.item.bind(is_disabled=self.update_button_state)
        self.update_button_state()  # Set initial state

        # Add a toggle button
        toggle_button = Button(text="Toggle item.is_disabled")
        toggle_button.bind(on_press=self.toggle_item_state)
        self.add_widget(toggle_button)

    def update_button_state(self, *args):
        self.dependent_button.disabled = self.item.is_disabled

    def toggle_item_state(self, instance):
        self.item.is_disabled = not self.item.is_disabled


# --- App class ---
class MyApp(App):
    def build(self):
        return MyWidget()


if __name__ == '__main__':
    MyApp().run()