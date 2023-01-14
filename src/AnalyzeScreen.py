from recorder import Recorder
from analyzer import Analyzer
from kivy.properties import StringProperty
from kivy.uix.screenmanager import ScreenManager, Screen
from kivy.uix.dropdown import DropDown
from kivy.uix.button import Button
import pygame
import os


class AnalyzeScreen(Screen):

    record_button_text = StringProperty()
    recording = False

    checking_pattern = False

    recording_chosen = False
    pattern_chosen = False

    def __init__(self, analyzer, **kwargs):
        """konstruktor"""
        super(AnalyzeScreen, self).__init__(**kwargs)


        self.an = analyzer

        self.record_button_text = 'Start'
        self.dyktafon = None
        self.sound = None
        pass

    def back_button_pressed(self):
        if not self.recording:
            print("Back to Menu")
        else:
            print("Stop recording to leave the screen.")




    def select_recording(self, recordings_dropdown, recording_selected):
        self.an.current_recording = recording_selected
        self.recording_chosen = True
        print("Selected recording: " + self.an.current_recording)

    def select_pattern(self, patterns_dropdown, pattern_selected):
        self.an.current_pattern = pattern_selected
        self.pattern_chosen = True
        print("Selected pattern: " + self.an.current_pattern)

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
                    self.recording_chosen = True



    def analyze_button_pressed(self):

        if self.an.current_recording is None:
            print("First choose a recordng to analyze")

        else:
            print(f'Chosen recording: {self.an.current_recording}')

            if self.an.current_pattern is None: #jeszcze próbowałem z recording_chosen is False, ale też się szczególnie nie przejął,
                                                            #a jest False dopóki któryś z guzików wyboru wzorca tej flagi nie zmieni.
                print("Pattern not chosen")

            else:
                print("Chosen pattern " + str(self.an.current_pattern))
                self.an.analyze_stuff()


    def analyzer_open_rec_list_screen_button_pressed(self):
        print("Opening recording list")



    def analyzer_open_rec_dir(self):
        if not self.recording:

            path = "Recordings"
            path = os.path.realpath(path)
            os.startfile(path)


    def analyzer_open_pat_dir(self):
        if not self.recording:
            path = "Patterns"
            path = os.path.realpath(path)
            os.startfile(path)

    def show_pat_list(self, button):

        patterns_dropdown = DropDown()
        listdir = os.listdir()
        [print(x) for x in listdir]
        patterns = os.listdir("./src/Patterns")
        
        for pat in patterns:
            new_pattern_button = Button(text=pat, size_hint_y=None, height=44)
            new_pattern_button.bind(on_release=lambda btn:  patterns_dropdown.select(btn.text))
            patterns_dropdown.add_widget(new_pattern_button)

        patterns_dropdown.bind(on_select=self.select_pattern)
        patterns_dropdown.open(button)

    def show_rec_list(self, button):

        recordings_dropdown = DropDown()

        recordings = os.listdir("./src/Recordings")
        for rec in recordings:
            new_recording_button = Button(text=rec, size_hint_y=None, height=44)
            new_recording_button.bind(on_release=lambda btn: recordings_dropdown.select(btn.text))
            recordings_dropdown.add_widget(new_recording_button)

        recordings_dropdown.bind(on_select=self.select_recording)
        recordings_dropdown.open(button)

    def spectrogram_pattern_button_pressed(self):
        self.an.compute_spectrogram(self.an.current_pattern)
        pass

    def spectrogram_recording_button_pressed(self):
        self.an.compute_spectrogram(self.an.current_recording)
        pass
