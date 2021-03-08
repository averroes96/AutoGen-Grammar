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
from kivy.uix.recycleview import RecycleView
from kivy.uix.settings import SettingsWithSidebar
import autogenTagger
import func

interface = Builder.load_file("gui.kv")

class SentencesRV(RecycleView):

    def __init__(self, **kwargs):
        super().__init__(**kwargs)

    data = ObjectProperty()

class ImportText(Popup):
    load = ObjectProperty()

class ImportCorpus(Popup):
    load_corpus = ObjectProperty()

class MyLayout(Widget):

    def __init__(self, **kwargs):
        super(MyLayout, self).__init__(**kwargs)
        #self.ids.original.bind(text=self.on_text)

    file_path = StringProperty("No file chosen")
    corpus_path = StringProperty("No file chosen")
    text_popup = ObjectProperty(None)
    corpus_popup = ObjectProperty(None)

    sents_rv = ObjectProperty(None)

    def analysis(self):
        if self.original.text.strip() != "":
            sents = func.get_text_sents(self.original.text, "\n|./\.|./:")
            tagger = autogenTagger.load_tagger("tagger.pkl")
            tagged_sents = []
            
            for sent in sents:
                tokens = tagger.tag(sent.split())
                tags = "[color=ff0000]===>"
                for tag in tokens:
                    tags = f"{tags} {tag[1]}"
                tagged_sents.append(f"{tags}[/color]")

            self.ids.sents_rv.data = [{"title.text": f"Sentence {i+1}", "original_sent.text" : sents[i], "analysed_sent.text" : tagged_sents[i]} for i in range(0, len(sents))] 

    def open_popup(self):
        self.text_popup = ImportText(load=self.load)
        self.text_popup.open()

    def open_corpus_popup(self):
        self.corpus_popup = ImportCorpus(load_corpus = self.load_corpus)

    def load_corpus(self, selection):
        self.corpus_path = str(selection[0])
        self.corpus_popup.dismiss()
        # check for non-empty list i.e. file selected
        if self.corpus_path:
            list_file = open(self.file_path).read().strip()
            self.ids.original.text = list_file 

    def load(self, selection):
        self.file_path = str(selection[0])
        self.text_popup.dismiss()
        # check for non-empty list i.e. file selected
        if self.file_path:
            list_file = open(self.file_path).read().strip()
            self.ids.original.text = list_file

    def on_text(self, instance, value):
        if self.ids.original.text.strip() != "":
            # tagger = autogenTagger.load_tagger("tagger.pkl")
            # tagged_words = tagger.tag(self.ids.original.text.strip().split())
            # tags = ""
            # for tag_word in tagged_words:
            #     tags = f"{tags} {tag_word[1].upper()}"
            # self.tagger.text = tags
            text = self.ids.original.text.strip()
            sents = text.split("\n")
            
        else:
            # self.tagger.text = "Tagged text will be shown here"
            self.ids.sents_rv.data = [] 
        # s = Spelling()
        # s.select_language("en_US")
        # if self.ids.original.text.strip() != "":
        #     word = self.ids.original.text
        #     options = s.suggest(word)
        #     res = ""
        #     for option in options:
        #         res = f"{res} {option}"
        #     self.ids.suggestions.text = res
    
    def clear(self):
        #self.generated.text = "Enter a sentence and click Generate Button to auto generate grammar"
        self.original.text = ""
        self.sents_rv.data = []

    def selected(self, files_list):
        if len(files_list) > 0:
            print(files_list[0])

class AutoGen(App):

    def build(self):
        # self.settings_cls = SettingsWithSidebar
        Window.clearcolor = (224/255, 226/255, 219/255,1)
        #Window.size = (800, 600)
        return MyLayout()

    # def build_config(self, config):
    #     config.setdefaults("Options",
    #     {
    #         "corpus" : "brown_corpus"
    #     })

    # def build_settings(self, settings):
    #     settings.add_json_panel("Options", self.config, "settings.json")

if __name__ == "__main__":
    AutoGen().run()
