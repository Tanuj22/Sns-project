import matplotlib.pyplot as plt
import numpy as np
from findpeaks import findpeaks
import pyaudio
import wave
# from smoothing import smoothing
from pylab import *
from scipy.io import wavfile


def plot(data):
    plt.plot(data, color='steelblue')


def smoothing(wav_data):
    r = 3
    wav = np.zeros(len(wav_data))
    for i in range(r, len(wav) - r):
        wav[i] = sum(wav_data[i - r:i + r + 1]) / (2 * r + 1)

    return wav


FILENAME1 = "source.wav"
FILENAME2 = "map.wav"
FILENAME3 = "target.wav"
rate1, wav_data1 = wavfile.read(FILENAME1)
rate2, wav_data2 = wavfile.read(FILENAME2)  # isko dekhna hai
rate3, wav_data3 = wavfile.read(FILENAME3)

wav1 = smoothing(wav_data1)
wav2 = smoothing(wav_data2)
wav3 = smoothing(wav_data3)


L1 = len(wav1)
f1 = np.linspace(0, 8000, L1)
x1 = np.fft.fft(wav1)
X1 = np.abs(x1) / L1  # magnitude of coefficient of FFT of source voice
L2 = len(wav2)
f2 = np.linspace(0, 8000, L2)
x2 = np.fft.fft(wav2)
X2 = np.abs(x2) / L2  # magnitude of  coefficient of FFT of target voice to be replicated
ratio = abs(x2) / abs(x1)  # ratio of coefficients r=d/c
Freq = np.linspace(0, 8000, L1)
plt.plot(Freq, ratio)  # plot ratio over double sided FFT spectrum

# This will help us cut down on the ratio .
# You need to pick values of h>1.
# The closer to 1 , the more it shrinks
# The farther h is from 1 , a the smaller the reduction

h = 1.25
Ratio = np.zeros(len(ratio))

for i in range(len(ratio)):
    Ratio[i] = ((h - 1) * ratio[i] + 1) / h
plt.plot(Freq , Ratio)
# plt.show()

# Apply ratio multipilcation on third audio sample

L3 = len(wav3)
f3 = np.linspace(0, 8000, L3)
x3 = np.fft.fft(wav3)
x3 = x3 * Ratio
ifftplot=np.fft.ifft(x3)
# ifftplot=smoothing(ifftplot)
filteredwrite=np.round(ifftplot).astype('int16')
wavfile.write('pleasework.wav', rate3, filteredwrite)
ifftplot=smoothing(ifftplot)

plt.plot(ifftplot)
plt.show()

