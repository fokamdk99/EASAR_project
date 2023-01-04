import simpleaudio #potrzebuje intów
import numpy as np
import matplotlib.pyplot as plt
from matplotlib.transforms import Bbox


def play_audio_buffer(audio_data, num_channels=1, sample_rate=22050, bit_rate=16): #zagraj to, co znajduje się w jakimś buforze #podaje się plik z dźwiękiem, jakiś kanał (?), częstotliwość
    #próbkowania tego pliku dźwiękowego  i przepływność

    "sample_rate - z jaką f został utwór spróbkowany"
    "Bit_rate - liczba bitów na próbkę -też już w jakiej rozdzielczości zostały wprowadzone do librosy wartości"


    y16 = (audio_data * 32767 / max(abs(audio_data))).astype(np.int16) # tutaj nie wiem, czemu coś się dzieje - konwersja na inty
             #tablica floatów [0,1] -odwzorowanie cisnienia akustycznego
                                                                        # #dane dźwiękowe mnożymy razy jakąś liczbę i dzielimy przez
                                                                       #największą z wartości macierzy/ w wektorze w module i każemy mu to uznać za 16-miejscowego inta
                                                                       # jest to jakieś skalowanie do maksimum, ale czemu *32767? To jest maksymalna wartość 16-bitowego inta -skalowanie

    play_obj = simpleaudio.play_buffer(y16, num_channels=num_channels, bytes_per_sample=bit_rate//8, sample_rate=sample_rate)
                #zmienna zawierająca polecenie zagrania przeskalowanego pliku dźwiękowego odpowiednio spróbkowanego i skwantyzowanego i przeskalowanego

    play_obj.wait_done() #niech gra, aż skończy i dopiero potem niech dzieje sie w programie coś innego


def plot_audio(audio_data, sample_rate=22050, markers=None, fign=None, marker_color='red'): #zapewne funkcja zwracająca przebieg czasowy nagrania
                                                #pionowe kreski                                            #co to jest to fign? Numer obrazka - FIGure Number
    plt.figure(num=fign, figsize=(8,2)) # wymiary wykresu?

    N = audio_data.size                     #rozmiar tablicy nagrania

    t = np.arange(0.0, N)/ sample_rate     #stworzenie tablicy na próbki z nagrania
    plt.plot(t, audio_data, color='black')    #hyc wykres

    if markers is not None:                  #jeśli kazałem pokazać jakieś markery, to
        plt.vlines(markers, -1, 1, colors=marker_color, linestyles='dashed')
    plt.ylim(-1, 1)
    plt.xlim(0, np.max(t))
    plt.xlabel('Time [s]')
    plt.yticks([])
    plt.gca().set_position(Bbox([[0.03, 0.25], [0.97, 0.95]])) #to wszystko pewnie ma związek z wykresami i ich ostateczną urodą
    plt.draw()
#plot_audio()