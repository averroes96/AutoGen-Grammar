import os, sys
from kivy.resources import resource_add_path, resource_find
from kivy.app import App
from kivy.uix.widget import Widget
from kivy.uix.popup import Popup
from kivy.lang import Builder
from kivy.properties import ObjectProperty, StringProperty
from kivy.core.window import Window
from kivy.core.spelling import Spelling
from kivy.uix.recycleview import RecycleView
import autogenTagger
import autogenPruner
import autogen
import func
import time
import nltk
import threading

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

    def slide_it(self, *args):
        self.slideVal.text = str(int(args[1]))
        self.slideVal.font_size = str(int(args[1]/2))
        print(self.slider.value)

    def analysis(self):
        try:
            if self.original.text.strip() != "":
                sents = func.get_text_sents(self.original.text, "\n|./\.|./:")
                tagged_sents = self.tag_sents(sents)
                result = self.get_grammar(tagged_sents)

                self.ids.sents_rv.data = [{"title.text": f"Sentence {i+1}", "original_sent.text" : sents[i], "analysed_sent.text" : f"[color=ff0000]{result[i]}[/color]"} for i in range(0, len(sents))] 
        except ValueError:
            self.ids.sents_rv.data = [{"title.text": f"Value Error", "original_sent.text" : "Grammar does not cover some of the input words: "'bez*'"", "analysed_sent.text": ""}]

    def tag_sents(self, sents)->list:

        tagger = autogenTagger.load_tagger("tagger.pkl")
        tagged_sents = []
        
        for sent in sents:
            tokens = tagger.tag(sent.split())
            tags = ""
            for tag in tokens:
                tags = f"{tags} {tag[1]}"
                tags = func.prune(tags)
            print(tags)
            tagged_sents.append(f"{tags}")

        return tagged_sents

    def get_grammar(self, tagged_sents):

        res = []

        grammarfile = nltk.data.load('file:grammar.cfg')
        rd = nltk.ChartParser(grammarfile)
        for tagged_sent in tagged_sents:
            b = False
            for tree in rd.parse(tagged_sent.split()):
                if tree != "":
                    res.append(f"[color=00ff00]{tree}[/color]")
                    b = True
            if b == False:
                res.append("[color=ff0000]Sentence is grammatically wrong according to your grammar[/color]")

        return res

    def open_popup(self):
        self.text_popup = ImportText(load=self.load)
        self.text_popup.open()

    def open_corpus_popup(self):
        self.corpus_popup = ImportCorpus(load_corpus = self.load_corpus)
        self.corpus_popup.open()

    def load_corpus(self, selection):
        self.corpus_path = str(selection[0])
        self.corpus_popup.dismiss()
        # check for non-empty list i.e. file selected
        if self.corpus_path:
            result = ""
            print(self.corpus_path)
            sents = func.get_sents(self.corpus_path, sep = "\n|./\.|./:")
            print(len(sents))
            self.train_corpus(result, sents)
            self.test_corpus(result, sents)

    def train_corpus(self, result, sents):
        sents_len = len(sents)
        max_train = int((int(self.slider.value) * sents_len)/100)
        func.corpus_light(sents, max = int(max_train))
        autogenPruner.regularize_corpus("corpus_light")
        start = time.time()
        rules = autogen.run("corpus_light")
        end = time.time()
        result += "Total extracted " + str(len(rules)) + " rule\n"
        result += "Getting the rules took " + str((end-start)/60) + " min\n"
        autogen.save_grammar(rules)

    def test_corpus(self, result, sents):
        sents_len = len(sents)
        max_train = int((int(self.slider.value) * sents_len)/100)
        max_test = sents_len - max_train
        func.corpus_light(sents, start = int(max_train), max = int(max_test))
        autogenPruner.regularize_corpus("corpus_light")
        cpt = autogen.test_corpus("corpus_light")
        result += f"{cpt[1]} testing sentences out of {cpt[0]} sentences, are wrong gramatically according to our grammar"
        self.results.text = result
    
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


if __name__ == "__main__":
    if hasattr(sys, '_MEIPASS'):
        resource_add_path(os.path.join(sys._MEIPASS))
    AutoGen().run()
