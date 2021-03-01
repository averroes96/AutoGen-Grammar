import kivy
from kivy.app import App
from kivy.uix.label import Label
from kivy.uix.gridlayout import GridLayout
from kivy.uix.textinput import TextInput
from kivy.uix.button import Button
from kivy.uix.widget import Widget
from kivy.properties import ObjectProperty
from kivy.lang import Builder
from kivy.core.window import Window

Builder.load_file("gui.kv")

class MyLayout(Widget):

    #original = ObjectProperty(None)
    #generated = ObjectProperty(None)
    #submit = ObjectProperty(None)

    def __init__(self, **kwargs):
        super(MyLayout, self).__init__(**kwargs)
        self.generated.bind(text = self.onTextChanged)

    def onAction(self):
        if self.original.text.strip() != "":
            self.generated.text = self.original.text * 3
    
    def onClear(self):
        self.generated.text = "Enter a sentence and click Generate Button to auto generate grammar"
        self.original.text = ""
 
    def onTextChanged(self, instance, text):
        print("Something")
        return self.ids.original.text
'''        self.cols = 1

        self.gl = GridLayout()
        self.gl.cols = 2
        self.add_widget(self.gl)

        self.gl.add_widget(Label(text="Enter a sentence"))
        self.original = TextInput(multiline=False)
        self.gl.add_widget(self.original)

        self.gl.add_widget(Label(text="Generated grammar"))
        self.grammar = TextInput(multiline=False)
        self.gl.add_widget(self.grammar)

        self.submit = Button(
            text="Generate", 
            font_size=32,
            size_hint_y = None,
            height = 128
            )
        self.submit.bind(on_press = self.onAction)
        self
        self.add_widget(self.submit)

    def onAction(self, intances):
            self.grammar.text = self.original.text * 3'''


class AutoGen(App):

    def build(self):
        Window.clearcolor = (224/255, 226/255, 219/255,1)
        return MyLayout()

if __name__ == "__main__":
    AutoGen().run()
