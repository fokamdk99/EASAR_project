import detect_notes_commented as dnc
import librosa
import matplotlib.pyplot as plt
import numpy as np
from dtaidistance import dtw
from dtaidistance import dtw_visualisation as dtwvis
from scipy import signal
from scipy.io import wavfile

class Analyzer():

    def __init__(self):
        self.current_pattern = None
        self.current_tempo = 100
        self.current_recording = None
        self.result_plot = None

    def compute_local_average(self, x, m):

        N = len(x)
        local_average = np.zeros(N)
        for n in range(N):
            a = max(n - m, 0)
            b = min(n + m + 1, n)
            local_average[n] = (1 / (2 * m + 1)) * np.sum(x[a:b])
        return local_average

    def compute_spectral_novelty(self, audio_data, fs=22050, stft_hop=256, stft_win=1024, gamma=1, averaging_window=0.1, normalise=True):

        stft = librosa.stft(audio_data, n_fft=stft_win, hop_length=stft_hop, win_length=stft_win,
                            window='hanning')
        fs_nov = fs / stft_hop

        if gamma > 0:
            stft = np.log(1 + gamma * np.abs(stft))
        stft_diff = np.diff(stft)
        stft_diff[
            stft_diff < 0] = 0
        nov = np.sum(stft_diff, axis=0)
        nov = np.concatenate((nov, np.array([0.0])))

        if averaging_window > 0:
            local_average = dnc.compute_local_average(nov, int(np.ceil(averaging_window * fs_nov)))
            nov = nov - local_average
            nov[nov < 0] = 0

        if normalise:
            nov = nov / max(nov)

        return nov, fs_nov

    def analyze_stuff(self):
        
        template_path = './src/Patterns/'
        query_path = './src/Recordings/'
        #print(self.current_recording +" and "+self.current_pattern)
        query, fs_query = librosa.load(query_path + self.current_recording)
        template, fs_template = librosa.load(template_path + self.current_pattern)

        query = np.array(query, dtype = np.double)
        template = np.array(template, dtype = np.double)

        number_of_samples_in_10ms = 0.01 * fs_template
        distance_list = []
        step = number_of_samples_in_10ms/2
        counter = 0
        while (counter*step + number_of_samples_in_10ms < len(query)):
            piss = template[counter*step:(counter*step + number_of_samples_in_10ms)]
            distance_list.append(dtw.distance_fast(query, piss, use_pruning=True))
        
        # oblicz dystans, tyle ze dla malych kawalkow
        print("wyniki\n")
        [print(x) for x in distance_list]
        print("koniec wynikow\n")

    def compute_spectrogram(self, audio_data):
        sample_rate, samples = wavfile.read(audio_data)
        frequencies, times, spectrogram = signal.spectrogram(samples, sample_rate)

        plt.pcolormesh(times, frequencies, spectrogram)
        plt.imshow(spectrogram)
        plt.ylabel('Frequency [Hz]')
        plt.xlabel('Time [sec]')
        plt.show()
        pass