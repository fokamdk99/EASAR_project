from kivy.app import App

from kivy.properties import StringProperty
from kivy.uix.screenmanager import ScreenManager, Screen
from kivy.lang import Builder

from app.AnalyzeScreen import AnalyzeScreen

from app.analyzer import Analyzer
from app.recorder import Recorder
import os

print(os.listdir())
Builder.load_file('./app/MenuScreen.kv')
Builder.load_file('./app/RecordingScreen.kv')
Builder.load_file('./app/AnalyzeScreen.kv')

class RecordingScreen(Screen):
    record_button_text = StringProperty()
    recording = False
    frames_collect_event = None

    def __init__(self, **kwargs):
        """konstruktor"""

        super(RecordingScreen, self).__init__(**kwargs)
        self.record_button_text = 'Start'
        self.dyktafon = None
    pass

    def record_button_pressed(self):

        self.recording = not self.recording  # przycisk zmienia flagę nagrywam/nie nagrywam

        # jeśli nagrywa
        if self.recording:
            print("Recording started")
            self.dyktafon = Recorder()
            self.dyktafon.start_recording()
            self.record_button_text = 'Stop'

        else:
            self.record_button_text = 'Start'
            self.dyktafon.end_recording()
            print("Recording finished")


class MenuScreen(Screen):

    def record_go_button_pressed(self):
        print('Opening Recording Screen')

    def analyze_go_button_pressed(self):
        print('Opening Analyze Screen')

    def exit_button_pressed(self):
        print('Leaving the program')
        exit()

class EASARApp(App):

    def build(self):
        an = Analyzer()
        sm = ScreenManager()
        sm.add_widget(MenuScreen(name='menu'))
        sm.add_widget(RecordingScreen(name='record'))
        sm.add_widget(AnalyzeScreen(analyzer=an, name='analyze'))
        return sm
if __name__ == '__main__':
    EASARApp(). run()
