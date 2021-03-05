import os, sys
from kivy import config
from kivy.resources import resource_add_path, resource_find
import kivy
import importlib
from kivy.app import App
from kivy.uix.label import Label
from kivy.uix.gridlayout import GridLayout
from kivy.uix.textinput import TextInput
from kivy.uix.button import Button
from kivy.uix.widget import Widget
from kivy.uix.popup import Popup
from kivy.lang import Builder
from kivy.properties import ObjectProperty, StringProperty
from kivy.core.window import Window
from kivy.core.spelling import Spelling
from kivy.uix.screenmanager import Screen, ScreenManager
from kivy.animation import Animation
from kivy.config import ConfigParser
import autogenTagger

interface = Builder.load_file("gui.kv")

class ImportText(Popup):
    load = ObjectProperty()

class MyLayout(Widget):

    #original = ObjectProperty(None)
    #generated = ObjectProperty(None)
    #submit = ObjectProperty(None)

    file_path = StringProperty("No file chosen")
    the_popup = ObjectProperty(None)
    settings = ObjectProperty(None) 

    def open_popup(self):
        self.the_popup = ImportText(load=self.load)
        self.the_popup.open()

    def load(self, selection):
        self.file_path = str(selection[0])
        self.the_popup.dismiss()
        # check for non-empty list i.e. file selected
        if self.file_path:
            list_file = open(self.file_path).read().strip()
            self.ids.original.text = list_file

    def __init__(self, **kwargs):
        super(MyLayout, self).__init__(**kwargs)
        self.ids.original.bind(text=self.on_text)

    def on_text(self, instance, value):
        if self.ids.original.text.strip() != "":
            tagger = autogenTagger.load_tagger("tagger.pkl")
            tagged_words = tagger.tag(self.ids.original.text.strip().split())
            tags = ""
            for tag_word in tagged_words:
                tags = f"{tags} {tag_word[1].upper()}"
            self.tagger.text = tags
        else:
            self.tagger.text = "Tagged text will be shown here"
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

    def selected(self, files_list):
        if len(files_list) > 0:
            print(files_list[0])

class AutoGen(App):

    def build(self):
        Window.clearcolor = (224/255, 226/255, 219/255,1)
        #Window.size = (800, 600)
        return MyLayout()

if __name__ == "__main__":
    AutoGen().run()
