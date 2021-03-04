import os, sys
from kivy.resources import resource_add_path, resource_find
import kivy
import importlib
from kivy.app import App
from kivy.uix.label import Label
from kivy.uix.gridlayout import GridLayout
from kivy.uix.textinput import TextInput
from kivy.uix.button import Button
from kivy.uix.widget import Widget
from kivy.lang import Builder
from kivy.core.window import Window
from kivy.core.spelling import Spelling
from kivy.uix.screenmanager import Screen, ScreenManager
from kivy.animation import Animation


class MainScreen(Screen):

    def selected(self, files_list):
        if len(files_list) > 0:
            print(files_list[0])

    def animate_it(self, widget, *args):
        animate = Animation(
            size_hint = (0.33, 0.33),
            duration = 0.1
        )
        animate += Animation(
            size_hint = (0.32, 0.32),
            duration = 0.1
        )
        animate.start(widget)
        

class SecondScreen(Screen):
    pass


class MyManager(ScreenManager):

    def on_text(self, instance, value):
        if self.ids.original.text.strip() != "":
            self.ids.generated.text = self.ids.original.text
        # s = Spelling()
        # s.select_language("en_US")
        # if self.ids.original.text.strip() != "":
        #     word = self.ids.original.text
        #     options = s.suggest(word)
        #     res = ""
        #     for option in options:
        #         res = f"{res} {option}"
        #     self.ids.suggestions.text = res
    
    def onClear(self):
        self.generated.text = "Enter a sentence and click Generate Button to auto generate grammar"
        self.original.text = ""

    def selected(self, filename):
        self.ids.icon.source = filename[0]
    

interface = Builder.load_file("interface.kv")

class MyLayout(Widget):

    #original = ObjectProperty(None)
    #generated = ObjectProperty(None)
    #submit = ObjectProperty(None)

    def __init__(self, **kwargs):
        super(MyLayout, self).__init__(**kwargs)
        self.ids.original.bind(text=self.on_text)

    def on_text(self, instance, value):
        if self.ids.original.text.strip() != "":
            self.ids.generated.text = self.ids.original.text
        # s = Spelling()
        # s.select_language("en_US")
        # if self.ids.original.text.strip() != "":
        #     word = self.ids.original.text
        #     options = s.suggest(word)
        #     res = ""
        #     for option in options:
        #         res = f"{res} {option}"
        #     self.ids.suggestions.text = res
    
    def onClear(self):
        self.generated.text = "Enter a sentence and click Generate Button to auto generate grammar"
        self.original.text = ""

    def selected(self, filename):
        self.ids.icon.source = filename[0]


class AutoGen(App):

    def build(self):
        Window.clearcolor = (224/255, 226/255, 219/255,1)
        #Window.size = (800, 600)
        return interface

if __name__ == "__main__":
    AutoGen().run()
