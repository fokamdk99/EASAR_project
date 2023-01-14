import app.audio_tools_commented
import librosa
import matplotlib.pyplot as plt
import numpy as np
from scipy.signal import find_peaks, savgol_filter


def compute_local_average(x, m): # co to za parametr m? #średnia wartość próbek w oknie czasowym -
    "# doczytać w FMP"  #m to połowa szerokości okna [próbek]

    N = len(x) #liczba równa długości ścieżki
    local_average = np.zeros(N)
    for n in range(N): #dla każdej próbki ze ścieżki
        a = max(n - m, 0) # m próbek na lewo od ścieżki, ale nie mniej niż 0.
        b = min(n + m + 1, n) #m próbek w prawo, ale nie więcej niż N
        local_average[n] = (1 / (2*m+1)) * np.sum(x[a:b]) #tablica średnich dla każdej próbki
    return local_average

                     #dane wejściowe, częstotliwość próbkowania, jakiś krok przesunięcia okna, szerokość okna(funkcja wpływająca na widmo), jakieś parametry
def compute_spectral_novelty(audio_data, fs=22050, stft_hop=256, stft_win=1024, gamma=1,  #posprawdzać parametry, ponagrywać swoje lub po prostu do innego nagrania i dopasować
        #rozdział II FMP                     #doczytać w FMP                                    #gamma dotyczy kompresji
                             averaging_window=0.1, normalise=True):
    stft = librosa.stft(audio_data, n_fft=stft_win, hop_length=stft_hop, win_length=stft_win, window='hanning') #transformowanie danych wejściowych
    fs_nov = fs / stft_hop #Nowe okna o dł 1024 są co 256 próbek i w wyniku tego otrzymujemy 1 liczbę na okno. Fs_nov jest zatem mniejsza od fs
    if gamma > 0: #czemu? FMP... Metoda kompresji w sensie realizacji dźwieku. Im większa liczba, tym silniejsza kompresja - tym większe wyrównanie, 0 - brak kompresji
        stft = np.log(1 + gamma * np.abs(stft))
    stft_diff = np.diff(stft) #detekcja zmian w sygnale
    stft_diff[stft_diff < 0] = 0 #tłumienie składowej oznacza, że nas taki sygnał już nie interesuje, polujemy na peaki
    nov = np.sum(stft_diff, axis=0) #sumowanie po częstotliwościach pochodnych stft
    nov = np.concatenate((nov, np.array([0.0])))
    if averaging_window > 0:
        local_average = compute_local_average(nov, int(np.ceil(averaging_window * fs_nov)))
        nov = nov - local_average # uwydatnienie peaków
        nov[nov < 0] = 0
    if normalise:
        nov = nov / max(nov)
    return nov, fs_nov


def zrob(pattern):

    wavdir = 'Patterns' #folder, od directory
    fname = pattern
    x, Fs = librosa.load(f'{wavdir}/{fname}') #czemu wpisuje się w Fs - częstotliwość próbkowania - floaty z piosenki?

    onsets = librosa.onset.onset_detect(x, sr=Fs, units='time', hop_length=32) #detekcja pobudzenia Parametry do pobawienia się, poczytać o funkcji
    #teraz to samo, ale na piechotę
    nov_spect, Fs_nov = compute_spectral_novelty(x, fs=Fs, stft_win=512, stft_hop=32, gamma=13, averaging_window=0.1) # pobawić się parametrami
    nov_spect = savgol_filter(nov_spect, window_length=25, polyorder=3)  #W Fs_nov zostawiamy transformatę, w nov_spect nakładamy okno (filtr) wygładzający
    onsets_spectral = find_peaks(nov_spect, prominence=0.2) #szuakmy peaków #tutaj zmieniałem z 0.04
    onsets_spectral = onsets_spectral[0] / Fs_nov #to samo, co w audio_tools, nagrane w matlabie

    t_nov = np.arange(nov_spect.size) / Fs_nov #taki linspace, tablica od 0 do liczby próbek w nov_spect, następnie tablice dzielimy przez Fs_nov
    #plt.figure(1000) #obrazek nr 1000
    #plt.plot(t_nov, nov_spect)
    #plt.draw()

    #audio_tools_commented.plot_audio(x, sample_rate=Fs, markers=onsets, fign=1, marker_color='red')
    audio_tools_commented.plot_audio(x, sample_rate=Fs, markers=onsets_spectral, fign=2, marker_color='green')

    plt.show()
