import librosa
import numpy as np
from dtaidistance import dtw
from dtaidistance import dtw_visualisation as dtwvis
import os

def analyze_stuff():
        
        template_path = './src/Patterns/'
        query_path = './src/Recordings/'
        #print(self.current_recording +" and "+self.current_pattern)
        query, fs_query = librosa.load(query_path + 'R1.wav')
        template, fs_template = librosa.load(template_path + 'C6.wav')

        query = np.array(query, dtype = np.double)
        template = np.array(template, dtype = np.double)

        number_of_samples_in_10ms = int(0.01 * fs_template)
        distance_list = []
        step = int(number_of_samples_in_10ms/2)
        counter = 0
        while (counter*step + number_of_samples_in_10ms < len(template)):
            piss = template[counter*step:(counter*step + number_of_samples_in_10ms)]
            distance_list.append(dtw.distance_fast(query, piss, use_pruning=True))
            counter += 1
        
        # oblicz dystans, tyle ze dla malych kawalkow
        print("wyniki\n")
        [print(x) for x in distance_list]
        print("koniec wynikow\n")

analyze_stuff()