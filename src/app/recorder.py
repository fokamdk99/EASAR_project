import pyaudio as pa
import wave
from kivy.clock import Clock
import os


class Recorder:

    def __init__(self):
        self.audio = pa.PyAudio()
        self.frames = []
        self.stream = None
        self.frames_collect_event = None
        self.rec_number = None
        self.last_recording = None

    def start_recording(self):
        self.stream = self.audio.open(format=pa.paInt16, channels=1, rate=44100, input=True, frames_per_buffer=1024)
        self.frames_collect_event = Clock.schedule_interval(self.frames_collect_callback, 1 / 44100.)

    def frames_collect_callback(self, dt):
        #print(dt)
        data = self.stream.read(1024)
        self.frames.append(data)

    def return_number_of_files(self):

        self.onlyfiles = next(os.walk("Recordings"))[2]  # dir is your directory path as string

        return len(self.onlyfiles)

    def end_recording(self):
        Clock.unschedule(self.frames_collect_event)
        self.stream.stop_stream()
        self.stream.close()
        self.audio.terminate()

        self.rec_number = self.return_number_of_files() + 1
        print(self.rec_number)

        recording_saved = False
        standard_save = True
        last_recording_number = None

        for x in range(self.return_number_of_files()):
            print(x)
            if not os.path.isfile('Recordings/R' + str(x+1) + ".wav"):
                sound_file = wave.open('Recordings/R' + str(x+1) + '.wav', "wb")
                recording_saved = True
                standard_save = False
                #wav_name1 = 'Nagranie_' + str(x+1) + ".wav"
                break

        if not recording_saved:
            sound_file = wave.open('Recordings/R' + str(self.rec_number) + '.wav', "wb")  # do konkretnego folderu
            recording_saved = True
            standard_save = True
            #wav_name2 ='Nagranie_' + str(self.rec_number) + ".wav"


        #sound_file = wave.open("Recordings/Nagranie.wav", "wb") #do konkretnego folderu
        print("Sound file saved")
        sound_file.setnchannels(1)
        sound_file.setsampwidth(self.audio.get_sample_size(pa.paInt16))
        sound_file.setframerate(44100)
        sound_file.writeframes(b''.join(self.frames))
        sound_file.close()