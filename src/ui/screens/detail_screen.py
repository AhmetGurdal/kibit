from src.entity.item import Item
from src.ui.components.path_box import PathBox
from src.data_handler import DataHandler
from kivy.uix.boxlayout import BoxLayout
from kivy.uix.label import Label
from kivy.uix.button import Button
from kivy.uix.textinput import TextInput
from kivy.uix.scrollview import ScrollView


class DetailScreen(BoxLayout):
    def __init__(self, data_handler: DataHandler,
                 save_item,
                 to_list_view,
                 to_history_view,
                 convertAbsolute2Relative,
                 convertRelative2Absolute,
                 **kwargs):
        super().__init__(**kwargs)
        self.data_handler = data_handler
        self.convertAbsolute2Relative = convertAbsolute2Relative
        self.convertRelative2Absolute = convertRelative2Absolute
        self.item = None
        self.save_item = save_item
        self.to_history_view = to_history_view
        header = BoxLayout(orientation="horizontal",
                           size=(1, 50), size_hint_y=None)
        back_to_list_button = Button(
            text="Back", size=(1, 50), size_hint=(0.2, None))
        back_to_list_button.bind(on_press=to_list_view)
        self.to_list_view = to_list_view
        header.add_widget(back_to_list_button)
        self.title_label = Label(
            text="Add New Item", size=(1, 30), size_hint_y=None, padding=[0, 0, 150, 0])
        header.add_widget(self.title_label)
        form = BoxLayout(orientation="vertical",
                         size=(1, 50), size_hint_y=None, padding=[0, 50, 0, 0])
        self.name = TextInput(hint_text="Name", size=(1, 30), size_hint_y=None)
        path_label = Label(
            text="Paths", size=(1, 30), size_hint_y=None, padding=[0, 50, 0, 0])
        form.add_widget(self.name)
        form.add_widget(path_label)
        path_view = ScrollView()
        self.path_layout = BoxLayout(orientation='vertical', size_hint_y=None)
        self.path_layout.bind(minimum_height=self.path_layout.setter('height'))
        self.path_inputs = {}
        path_view.add_widget(self.path_layout)
        path_add_button = Button(text=f"Add Path", size_hint_y=None, height=50)
        path_add_button.bind(on_press=self.add_path)
        save_button = Button(text=f"Save", size_hint_y=None, height=50)
        save_button.bind(on_press=self.on_save)
        self.add_widget(header)
        self.add_widget(form)
        self.add_widget(path_view)
        self.add_widget(path_add_button)
        self.add_widget(save_button)

    def set_item(self, index: int, item: Item):
        self.index = index
        self.item = item
        self.title_label.text = f"{item.name}"
        self.name.text = item.name
        # TODO: Set Paths
        for path in item.paths:
            path_box = PathBox(
                index=index, on_delete=self.on_path_delete,
                to_history=self.to_history_view,
                parent_item=self.item, parent_index=self.index,
                is_detail=True, text=path)
            self.path_inputs[index] = path_box
            self.path_layout.add_widget(path_box)

    def add_path(self, _):
        index = len(self.path_inputs)
        if (self.item != None):
            path_box = PathBox(
                index=index, on_delete=self.on_path_delete,
                to_history=self.to_history_view,
                parent_item=self.item, parent_index=self.index,
                is_detail=True)
        else:
            path_box = PathBox(
                index=index, on_delete=self.on_path_delete,
                to_history=self.to_history_view,
                parent_item=None, parent_index=None,
                is_detail=False)
        self.path_inputs[index] = path_box
        self.path_layout.add_widget(path_box)

    def on_path_delete(self, index):
        try:
            self.path_layout.remove_widget(self.path_inputs[index])
            del self.path_inputs[index]
        except:
            pass

    def on_save(self, _):
        paths = []
        for i in self.path_inputs:
            value = self.path_inputs[i].get_value()

            paths.append(self.convertAbsolute2Relative(value))
        if (self.item):
            item = Item(self.name.text)
            item.setPaths(paths)
            self.data_handler.update_item(
                item=item, index=self.index)
        else:
            item = Item(self.name.text)
            item.setPaths(paths)
            self.data_handler.add_item(item=item)
        self.to_list_view(None)
