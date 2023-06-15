from kivymd.app import MDApp
from kivy.uix.popup import Popup
from kivy.lang import Builder
from kivy.clock import mainthread
from kivymd.uix.dialog import MDDialog
from kivymd.uix.card import MDCard
from kivy.core.window import Window
from kivy.properties import ObjectProperty, StringProperty
from kivy.metrics import dp
import pathlib
import os
import time
import concurrent.futures
import subprocess

Window.maximize()
app_path = os.getcwd()
Builder.load_file('main.kv')

class DMEInputPopup(Popup):
    drop_id = ObjectProperty(None)
    filePath = StringProperty('')
    folderpath = []

    def __init__(self, **kwargs):
        super(DMEInputPopup, self).__init__(**kwargs)
        del self.folderpath[:]
        Window.bind(on_dropfile=self._on_file_drop)

    def _on_file_drop(self, window, file_path):
        path = file_path.decode("utf-8")
        dirpath = pathlib.PureWindowsPath(str(path)).as_posix()
        self.ids.input_textbox.text = dirpath
        del self.folderpath[:]
        self.folderpath.append(self.ids.input_textbox.text)

    def clear_input(self):
        del self.folderpath[:]
        self.ids.input_textbox.text = 'Please drop your folder here'

    def add_extension(self):
        self.pop_up1()
        executor = concurrent.futures.ThreadPoolExecutor()
        executor.submit(self.addition_process, True)

    def remove_extension(self):
        self.pop_up1()
        executor = concurrent.futures.ThreadPoolExecutor()
        executor.submit(self.addition_process, False)

    def pop_up1(self):
        self.dialog = MDDialog(
            size_hint=(None, None),
            width=dp(200),
            auto_dismiss=True,
            type="custom",
            content_cls = Matter(),
        )
        self.dialog.open()

    @mainthread
    def addition_process(self, choice):
        if self.folderpath != []:
            try:
                os.chdir(pathlib.PureWindowsPath(os.path.join(app_path, r'source/add_dme')).as_posix())
                extension_addition = pathlib.PureWindowsPath(os.path.join(app_path, r'source/add_dme/launch_dme.bat')).as_posix()
                if choice == True:
                    subprocess.call([extension_addition, self.ids.input_textbox.text, "1"])
                else:
                    subprocess.call([extension_addition, self.ids.input_textbox.text, "0"])
                time.sleep(2)
                self.dialog.dismiss()
            except NotADirectoryError:
                self.dialog.dismiss()
                incorrect_ip = MDDialog(title='Not A Directory',
                                        text='Please provide the path for folder, not a file')
                incorrect_ip.open()
        else:
            alert = MDDialog(title='No Input Found',
                             text='Please provide the path for data modules')
            self.dialog.dismiss()
            alert.open()


class Matter(MDCard):
    pass


class DMEEditor(MDApp):

    def build(self):
        self.theme_cls.theme_style = 'Light'
        return DMEInputPopup().open()

def reset():
    import kivy.core.window as window
    from kivy.base import EventLoop
    if not EventLoop.event_listeners:
        from kivy.cache import Cache
        window.Window = window.core_select_lib('window', window.window_impl, True)
        Cache.print_usage()
        for cat in Cache._categories:
            Cache._objects[cat] = {}

if __name__ == '__main__':
    reset()
    DMEEditor().run()
    