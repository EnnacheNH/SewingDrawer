import sqlite3

import kivy
from kivy.app import App
from kivy.lang import Builder
from kivy.uix.screenmanager import ScreenManager, Screen
from kivy.core.text import LabelBase
from kivy.core.window import Window
from kivy.uix.button import Button
from kivy.uix.label import Label
from kivy.uix.gridlayout import GridLayout
from kivy.uix.floatlayout import FloatLayout
from kivy.uix.popup import Popup
from kivy.properties import ObjectProperty
import functions_sqlite as fct_sql

LabelBase.register(name="Pacifico",
                   fn_regular="Pacifico.ttf"
                   )

Window.keyboard_anim_args = {'d': .2, 't': 'in_out_expo'}
Window.softinput_mode = "below_target"  # '', 'pan', 'scale', 'resize' or 'below_target'.


class WindowManager(ScreenManager):
    pass


# ---------------------------------------------------------------------------------------------------------------------- Home Window
class HomeWindow(Screen):
    pass


# ---------------------------------------------------------------------------------------------------------------------- Fabric Window
class FabricMainWindow(Screen):
    def __init__(self, **kwargs):
        super(FabricMainWindow, self).__init__(**kwargs)

        self.fabric_buttons = []
        self.fabric_buttons_order = "newest"
        self.order_to_index = {"newest": 0, "name": 1, "color": 2, "material": 3, "length": 4, "width": 5, "other": 6}
        self.load_buttons()

    def on_pre_enter(self, *args):
        self.reload_buttons()

    def load_buttons(self):
        self.fabric_buttons = []
        fabric_list = fct_sql.fabric_show_all(self.fabric_buttons_order)
        if self.fabric_buttons_order in ["color", "material", "length", "width", "other"]:
            for fabric in fabric_list:
                order_txt = str(fabric[self.order_to_index[self.fabric_buttons_order]])
                if order_txt == "":
                    order_txt = "None"

                btn = ItemButton(fabric[0], fabric[1] + " - " + order_txt)
                self.fabric_buttons.append(btn)
                self.ids.fabric_list_id.add_widget(btn)
        else:
            for fabric in fabric_list:
                btn = ItemButton(fabric[0], fabric[1])
                self.fabric_buttons.append(btn)
                self.ids.fabric_list_id.add_widget(btn)

    def reload_buttons(self):
        for button in self.fabric_buttons:
            self.ids.fabric_list_id.remove_widget(button)

        self.load_buttons()

    def add(self):
        wm.current = 'fabric_edit'
        wm.transition.direction = 'left'
        fabric_edit_window.initialize(0)

    def remove_from_list(self, button):
        self.fabric_buttons.remove(button)
        # print(len(self.fabric_buttons))

    def sort_popup(self):
        popup_window = Popup(title="Sort By", content=FabricSortPopUp(), size_hint=(0.7, 0.9))
        popup_window.open()


class FabricEditWindow(Screen):
    title_var = ObjectProperty(None)
    name_var = ObjectProperty(None)
    color_var = ObjectProperty(None)
    material_var = ObjectProperty(None)
    length_var = ObjectProperty(None)
    width_var = ObjectProperty(None)
    other_var = ObjectProperty(None)

    rowid = 0

    def initialize(self, fabric_id):
        self.rowid = fabric_id
        if self.rowid == 0:
            self.title_var.text = "New"

            self.name_var.text = ""
            self.color_var.text = ""
            self.material_var.text = ""
            self.length_var.text = ""
            self.width_var.text = ""
            self.other_var.text = ""
        else:
            self.title_var.text = "Edit"

            fabric_info = fct_sql.fabric_lookup(fabric_id)
            self.name_var.text = str(fabric_info[0])
            self.color_var.text = str(fabric_info[1])
            self.material_var.text = str(fabric_info[2])
            self.length_var.text = str(fabric_info[3])
            self.width_var.text = str(fabric_info[4])
            self.other_var.text = str(fabric_info[5])

    def submit_fabric(self):
        if self.rowid == 0:
            fct_sql.fabric_add_one(self.name_var.text, self.color_var.text, self.material_var.text, self.length_var.text, self.width_var.text, self.other_var.text)
        else:
            fct_sql.fabric_update(self.rowid, self.name_var.text, self.color_var.text, self.material_var.text, self.length_var.text, self.width_var.text, self.other_var.text)

        wm.current = 'fabric_main'
        wm.transition.direction = 'right'


# ---------------------------------------------------------------------------------------------------------------------- Project Window
class ProjectMainWindow(Screen):
    def __init__(self, **kwargs):
        super(ProjectMainWindow, self).__init__(**kwargs)

        self.item_buttons = []
        self.item_buttons_order = "newest"
        self.load_buttons()

    def on_pre_enter(self, *args):
        self.reload_buttons()

    def load_buttons(self):
        self.item_buttons = []
        item_list = fct_sql.project_show_all(self.item_buttons_order)
        if self.item_buttons_order == "completed":
            for item in item_list:
                if item[8]:
                    order_txt = "Completed"
                else:
                    order_txt = "To Do"

                btn = ItemButton(item[0], item[1] + " - " + order_txt)
                self.item_buttons.append(btn)
                self.ids.project_list_id.add_widget(btn)
        else:
            for item in item_list:
                btn = ItemButton(item[0], item[1])
                self.item_buttons.append(btn)
                self.ids.project_list_id.add_widget(btn)

    def reload_buttons(self):
        for button in self.item_buttons:
            self.ids.project_list_id.remove_widget(button)

        self.load_buttons()

    def add(self):
        wm.current = 'project_edit'
        wm.transition.direction = 'left'
        project_edit_window.initialize(0)

    def remove_from_list(self, button):
        self.item_buttons.remove(button)

    def sort_popup(self):
        popup_window = Popup(title="Sort By", content=ProjectSortPopUp(), size_hint=(0.7, 0.9))
        popup_window.open()


class ProjectEditWindow(Screen):
    title_var = ObjectProperty(None)
    name_var = ObjectProperty(None)
    notes_var = ObjectProperty(None)
    supplies_var = ObjectProperty(None)
    measurements_var = ObjectProperty(None)
    ref_var = ObjectProperty(None)
    cost_var = ObjectProperty(None)
    due_var = ObjectProperty(None)
    completed_var = ObjectProperty(None)

    rowid = 0
    completed_state = False

    def initialize(self, project_id):
        self.rowid = project_id
        if self.rowid == 0:
            self.title_var.text = "New"
            self.name_var.text = ""
            self.notes_var.text = ""
            self.supplies_var.text = ""
            self.measurements_var.text = ""
            self.ref_var.text = "https://www.example.com"
            self.cost_var.text = ""
            self.due_var.text = ""
            self.set_completed_no()
        else:
            self.title_var.text = "Edit"

            project_info = fct_sql.project_lookup(project_id)

            self.name_var.text = str(project_info[0])
            self.notes_var.text = str(project_info[1])
            self.supplies_var.text = str(project_info[2])
            self.measurements_var.text = str(project_info[3])
            self.ref_var.text = str(project_info[4])
            self.cost_var.text = str(project_info[5])
            self.due_var.text = str(project_info[6])
            if project_info[7]:
                self.set_completed_yes()
            else:
                self.set_completed_no()

    def submit_project(self):
        if self.rowid == 0:
            fct_sql.project_add_one(self.name_var.text, self.notes_var.text, self.supplies_var.text, self.measurements_var.text, self.ref_var.text, self.cost_var.text, self.due_var.text, self.completed_state)
        else:
            fct_sql.project_update(self.rowid, self.name_var.text, self.notes_var.text, self.supplies_var.text, self.measurements_var.text, self.ref_var.text, self.cost_var.text, self.due_var.text, self.completed_state)

        wm.current = 'project_main'
        wm.transition.direction = 'right'

    def completed_button(self):
        if self.completed_var.text == "No":
            self.set_completed_yes()
        else:
            self.set_completed_no()

    def set_completed_no(self):
        self.completed_var.text = "No"
        self.completed_var.background_color = [1, 1, 1, 1]
        self.completed_state = False

    def set_completed_yes(self):
        self.completed_var.text = "Yes"
        self.completed_var.background_color = [0, 1, 0, 1]
        self.completed_state = True


# ---------------------------------------------------------------------------------------------------------------------- Shopping Window
class ShoppingWindow(Screen):
    name_var = ObjectProperty(None)

    def __init__(self, **kwargs):
        super(ShoppingWindow, self).__init__(**kwargs)

        self.item_buttons = []
        self.item_buttons_order = "newest"
        self.load_buttons()

    def on_pre_enter(self, *args):
        self.reload_buttons()

    def load_buttons(self):
        self.item_buttons = []
        item_list = fct_sql.shopping_show_all(self.item_buttons_order)
        for item in item_list:
            btn = ShoppingItem(item[0], item[1])
            self.item_buttons.append(btn)
            self.ids.shopping_list_id.add_widget(btn)

    def reload_buttons(self):
        for button in self.item_buttons:
            self.ids.shopping_list_id.remove_widget(button)

        self.load_buttons()

    def add(self):
        fct_sql.shopping_add_one(self.name_var.text)
        self.name_var.text = ""
        self.reload_buttons()

    def remove_from_list(self, button):
        self.item_buttons.remove(button)

    def sort_popup(self):
        popup_window = Popup(title="Sort By", content=ShoppingSortPopUp(), size_hint=(0.7, 0.9))
        popup_window.open()


class ShoppingItem(GridLayout):
    def __init__(self, item_id, item_name, **kwargs):
        super(ShoppingItem, self).__init__(**kwargs)
        self.cols = 2
        self.item_id = item_id
        self.item_name = item_name

        self.label_edit = Label(text=item_name)
        self.add_widget(self.label_edit)

        self.btn_delete = Button(text="delete")
        self.btn_delete.size_hint_x = 0.2
        self.btn_delete.bind(on_press=self.remove)
        self.add_widget(self.btn_delete)

    def remove(self, instance):
        fct_sql.shopping_delete_one(self.item_id)
        shopping_window.remove_from_list(self)
        self.parent.remove_widget(self)


# ---------------------------------------------------------------------------------------------------------------------- Measurements Window
class MeasureMainWindow(Screen):
    def __init__(self, **kwargs):
        super(MeasureMainWindow, self).__init__(**kwargs)

        self.item_buttons = []
        self.item_buttons_order = "newest"
        self.load_buttons()

    def on_pre_enter(self, *args):
        self.reload_buttons()

    def load_buttons(self):
        self.item_buttons = []
        item_list = fct_sql.measure_show_all(self.item_buttons_order)
        for item in item_list:
            btn = ItemButton(item[0], item[1])
            self.item_buttons.append(btn)
            self.ids.measure_list_id.add_widget(btn)

    def reload_buttons(self):
        for button in self.item_buttons:
            self.ids.measure_list_id.remove_widget(button)

        self.load_buttons()

    def add(self):
        wm.current = 'measure_edit'
        wm.transition.direction = 'left'
        measure_edit_window.initialize(0)

    def remove_from_list(self, button):
        self.item_buttons.remove(button)

    def sort_popup(self):
        popup_window = Popup(title="Sort By", content=MeasureSortPopUp(), size_hint=(0.7, 0.9))
        popup_window.open()


class MeasureEditWindow(Screen):
    title_var = ObjectProperty(None)
    name_var = ObjectProperty(None)
    height_var = ObjectProperty(None)
    bust_var = ObjectProperty(None)
    waist_var = ObjectProperty(None)
    hips_var = ObjectProperty(None)
    in_seam_var = ObjectProperty(None)
    other_var = ObjectProperty(None)
    last_date_var = ObjectProperty(None)

    rowid = 0

    def initialize(self, measure_id):
        self.rowid = measure_id
        if self.rowid == 0:
            self.title_var.text = "New"
            self.name_var.text = ""
            self.height_var.text = ""
            self.bust_var.text = ""
            self.waist_var.text = ""
            self.hips_var.text = ""
            self.in_seam_var.text = ""
            self.other_var.text = ""
            self.last_date_var.text = ""
        else:
            self.title_var.text = "Edit"

            measure_info = fct_sql.measure_lookup(measure_id)

            self.name_var.text = str(measure_info[0])
            self.height_var.text = str(measure_info[1])
            self.bust_var.text = str(measure_info[2])
            self.waist_var.text = str(measure_info[3])
            self.hips_var.text = str(measure_info[4])
            self.in_seam_var.text = str(measure_info[5])
            self.other_var.text = str(measure_info[6])
            self.last_date_var.text = str(measure_info[7])

    def submit_project(self):
        if self.rowid == 0:
            fct_sql.measure_add_one(self.name_var.text, self.height_var.text, self.bust_var.text, self.waist_var.text, self.hips_var.text, self.in_seam_var.text, self.other_var.text, self.last_date_var.text)
        else:
            fct_sql.measure_update(self.rowid, self.name_var.text, self.height_var.text, self.bust_var.text, self.waist_var.text, self.hips_var.text, self.in_seam_var.text, self.other_var.text, self.last_date_var.text)

        wm.current = 'measure_main'
        wm.transition.direction = 'right'


# ---------------------------------------------------------------------------------------------------------------------- ItemButton
class ItemButton(GridLayout):
    def __init__(self, item_id, item_name, **kwargs):
        super(ItemButton, self).__init__(**kwargs)
        self.cols = 2
        self.item_id = item_id
        self.item_name = item_name

        self.btn_edit = Button(text=item_name)
        self.btn_edit.bind(on_press=self.edit)
        self.add_widget(self.btn_edit)

        self.btn_delete = Button(text="delete")
        self.btn_delete.size_hint_x = 0.2
        self.btn_delete.bind(on_press=self.remove_popup)
        self.add_widget(self.btn_delete)

    def remove_popup(self, instance):
        message = "Do you want to delete \n" + self.item_name + "\n?"
        popup_window = Popup(title="Delete this?", content=DeletePopUp(self, message), size_hint=(0.7, 0.9))
        popup_window.open()

    def remove(self):
        if wm.current == "fabric_main":
            fct_sql.fabric_delete_one(self.item_id)
            fabric_main_window.remove_from_list(self)
        elif wm.current == "project_main":
            fct_sql.project_delete_one(self.item_id)
            project_main_window.remove_from_list(self)
        elif wm.current == "measure_main":
            fct_sql.measure_delete_one(self.item_id)
            measure_main_window.remove_from_list(self)

        self.parent.remove_widget(self)

    def edit(self, instance):
        if wm.current == "fabric_main":
            wm.current = 'fabric_edit'
            wm.transition.direction = 'left'
            fabric_edit_window.initialize(self.item_id)
        elif wm.current == "project_main":
            wm.current = 'project_edit'
            wm.transition.direction = 'left'
            project_edit_window.initialize(self.item_id)
        elif wm.current == "measure_main":
            wm.current = 'measure_edit'
            wm.transition.direction = 'left'
            measure_edit_window.initialize(self.item_id)


# ---------------------------------------------------------------------------------------------------------------------- Settings Window
class SettingsWindow(Screen):
    erase_target = ""

    def remove_popup(self, target):
        self.erase_target = target
        message = "Do you want to erase all \n" + target + "\n?"
        popup_window = Popup(title="Delete this?", content=DeletePopUp(self, message), size_hint=(0.7, 0.9))
        popup_window.open()

    def remove(self):
        fct_sql.reset_table(self.erase_target)


# ---------------------------------------------------------------------------------------------------------------------- PopUp
class SortPopUp(FloatLayout):
    def sort(self, order):
        if wm.current == "fabric_main":
            fabric_main_window.fabric_buttons_order = order
            fabric_main_window.reload_buttons()
        elif wm.current == "project_main":
            project_main_window.item_buttons_order = order
            project_main_window.reload_buttons()
        elif wm.current == "shopping":
            shopping_window.item_buttons_order = order
            shopping_window.reload_buttons()
        elif wm.current == "measure_main":
            measure_main_window.item_buttons_order = order
            measure_main_window.reload_buttons()


class FabricSortPopUp(SortPopUp):
    pass


class ProjectSortPopUp(SortPopUp):
    pass


class ShoppingSortPopUp(SortPopUp):
    pass


class MeasureSortPopUp(SortPopUp):
    pass


class DeletePopUp(FloatLayout):
    message_var = ObjectProperty(None)

    def __init__(self, item_button, message, **kwargs):
        super(DeletePopUp, self).__init__(**kwargs)
        self.item_button = item_button
        self.message_var.text = message

    def confirm_delete(self):
        self.item_button.remove()


# ---------------------------------------------------------------------------------------------------------------------- Rest of the fucking owl
kv = Builder.load_file("home.kv")
wm = WindowManager()
fabric_main_window = FabricMainWindow()
fabric_edit_window = FabricEditWindow()
project_main_window = ProjectMainWindow()
project_edit_window = ProjectEditWindow()
shopping_window = ShoppingWindow()
measure_main_window = MeasureMainWindow()
measure_edit_window = MeasureEditWindow()



class MyApp(App):
    def build(self):
        wm.add_widget(HomeWindow())
        wm.add_widget(fabric_main_window)
        wm.add_widget(fabric_edit_window)
        wm.add_widget(project_main_window)
        wm.add_widget(project_edit_window)
        wm.add_widget(shopping_window)
        wm.add_widget(measure_main_window)
        wm.add_widget(measure_edit_window)
        wm.add_widget(SettingsWindow())
        wm.current = 'home'
        return wm

'''
fct_sql.fabric_add_one("Coton noir", "Noir", "Coton", 1.2, 1, "Meh")
fct_sql.fabric_add_one("Satin de maman", "Blanc", "Satin", 1.2, 1, "A rendre")
fct_sql.fabric_add_one("Soie", "Blanc", "Soie", 1.2, 1, "Doux mais chiant")

fct_sql.project_add_one("Test1", "note1", "supplies1", "measurements1", "ref1", None, None, None)
fct_sql.project_add_one("Test2", "note2", "supplies2", "measurements2", "ref2", None, None, None)
fct_sql.project_add_one("Test3", "note3", "supplies3", "measurements3", "ref3", None, None, None)
'''

'''
connection = sqlite3.connect("inventory.db")
cursor = connection.cursor()

cursor.execute("""
CREATE TABLE fabrics (
    name text,
    color text,
    material text,
    length float,
    width float,
    other float
    )
""")

cursor.execute("""
CREATE TABLE projects (
    name text,
    notes text,
    supplies text,
    measurements text,
    ref text,
    cost text,
    due text,
    completed bool
    )
""")

cursor.execute("""
CREATE TABLE shopping (
    item text
    )
""")

cursor.execute("""
CREATE TABLE measurements (
    name text,
    height float,
    bust float,
    waist float,
    hips float,
    in_seam float,
    other text,
    last_date text
    )
""")

connection.commit()
connection.close()
'''

"""
print(fct_sql.fabric_show_all())
print(fct_sql.fabric_show_all()[0])
print(fct_sql.fabric_show_all()[0][0])
print(len(fct_sql.fabric_show_all()))
"""

if __name__ == "__main__":
    MyApp().run()
