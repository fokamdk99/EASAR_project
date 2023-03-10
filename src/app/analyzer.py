import app.detect_notes_commented as dnc
import librosa
import matplotlib.pyplot as plt
import numpy as np
from dtaidistance import dtw
from dtaidistance import dtw_visualisation as dtwvis
from scipy import signal
from scipy.io import wavfile
import os
import math

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

    def analyze_dtw(self):
        reference_recording_path = './Patterns/'
        new_recording_path = './Recordings/'
        
        # C... nagrania od ludzi
        # R... nagrania rafalowe
        reference_recording, reference_recording_fs = librosa.load(reference_recording_path + self.current_pattern)
        new_recording, new_recording_fs = librosa.load(new_recording_path + self.current_recording)
        if (len(new_recording) < len(reference_recording)):
            tmp = new_recording
            new_recording = reference_recording
            reference_recording = tmp

        reference_recording = np.array(reference_recording, dtype = np.double)
        new_recording = np.array(new_recording, dtype = np.double)

        step = 0.03 * reference_recording_fs
        window = len(reference_recording)
        new_recording_length = len(new_recording)

        current_point = 0
        distance_list = []
        while(window + current_point*step <= new_recording_length):
            left_threshold = int(current_point*step)
            right_threshold = int(window + left_threshold)
            new_recording_sample = new_recording[left_threshold:right_threshold]
            distance = dtw.distance_fast(reference_recording, new_recording_sample, use_pruning=True)
            distance_list.append(distance)
            current_point += 1
        
        f = open(f"./calculation_results/dtw-{self.current_pattern}-{self.current_recording}.txt", "w")
        f.write(f'{self.current_pattern}\n')
        f.write(f'{self.current_recording}\n')
        [f.write(str(distance) + '\n') for distance in distance_list]
        f.close()

    def analyze_correlations(self):
        reference_recording_path = './Patterns/'
        new_recording_path = './Recordings/'
        
        # C... nagrania od ludzi
        # R... nagrania rafalowe
        reference_recording, reference_recording_fs = librosa.load(reference_recording_path + self.current_pattern)
        new_recording, new_recording_fs = librosa.load(new_recording_path + self.current_recording)
        if (len(new_recording) < len(reference_recording)):
            tmp = new_recording
            new_recording = reference_recording
            reference_recording = tmp

        reference_recording = np.array(reference_recording, dtype = np.double)
        new_recording = np.array(new_recording, dtype = np.double)
        step = 0.03 * reference_recording_fs
        window = len(reference_recording)
        new_recording_length = len(new_recording)
        
        current_point = 0
        correlation_list = []

        while(window + current_point*step <= new_recording_length):
            left_threshold = int(current_point*step)
            right_threshold = int(window + left_threshold)
            new_recording_sample = new_recording[left_threshold:right_threshold]
            correlation = np.corrcoef(reference_recording, new_recording_sample)
            correlation_list.append(abs(correlation[0][1]))
            current_point += 1
        
        f = open(f"calculation_results/correlation-{self.current_pattern}-{self.current_recording}.txt", "w")
        f.write(f'{self.current_pattern}\n')
        f.write(f'{self.current_recording}\n')
        [f.write(str(correlation) + '\n') for correlation in correlation_list]
        f.close()

    def compute_spectrogram(self, audio_data):
        sample_rate, samples = wavfile.read(audio_data)
        frequencies, times, spectrogram = signal.spectrogram(samples, sample_rate)

        plt.pcolormesh(times, frequencies, spectrogram)
        plt.imshow(spectrogram)
        plt.ylabel('Frequency [Hz]')
        plt.xlabel('Time [sec]')
        plt.show()
        pass