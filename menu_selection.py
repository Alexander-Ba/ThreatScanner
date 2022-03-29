from tempfile import template
from templates import PrintTemplates
import time
from tkinter import filedialog
from tkinter import *

templates = PrintTemplates()


class MenuSelection:
    def __init__(
        self,
    ):
        pass

    def get_selections(
        self,
        options_dict,
        module,
        options_type='numbers'
    ):
        if not options_dict:
            return []
        time.sleep(1)
        self.show_selection_options(
            options_dict,
            module,
        )
        choices = input('---> ')
        options = options_dict.keys()
        return [
            options_dict.get(choice) for choice in choices
            if choice in options
        ]

    def show_selection_options(
        self,
        options_dict,
        higher_module,
    ):
        menu = templates.build_options_menu(
            options_dict,
            higher_module,
        )
        print(menu)

    def get_assets_by_module(
        self,
        module,
    ):
        time.sleep(1)
        menu = templates.build_assets_menu(module)
        print(menu)
        return input('---> ')

    def get_logs_path(self):
        print(templates.FILE_EXPORT_REQUEST)
        root = Tk()
        root.withdraw()
        selected_path = filedialog.askdirectory()
        print(f'Files Path has been set to: {selected_path}')
        return selected_path+'/'

    def main(
        self,
    ):
        main_modules = self.get_selections(
            templates.MAIN_MENU,
            'MAIN',
        )
        modules_dict = {}

        for module in main_modules:
            if not modules_dict.get(module):
                modules_dict[module] = {}
            modules_dict[module]['modules'] = self.get_selections(
                templates.SUB_MENU.get(module),
                module,
            )
        return modules_dict