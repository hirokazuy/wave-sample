# -*- coding: utf-8; -*-
import struct
import numpy as np
import scipy.signal as signal
import matplotlib.pyplot as plt

def create_sin_wave(A, f0, fs, length):
    """サイン波データを作成する.
    
    :param A: 振幅(0.0-1.0)
    :param f0: 基本周波数
    :param fs: サンプリング周波数
    :param length: 長さ
    """
    data = []
    for n in range(length * fs):
        s = A * np.sin(2 * np.pi * f0 * n / fs)
        if s > 1.0: s = 1.0
        if s < -1.0: s = -1.0
        data.append(s)
    return np.array([int(x * 32767.0) for x in data], dtype='int16')

def plot_data(data, fs, length, fname=None):
#    plt.plot(data[100:200])
    pxx, freqs, bins, im = plt.specgram(data, NFFT=512, Fs=fs, noverlap=128)
    plt.axis([0, length, 0, fs / 2])
    if fname is None:
        plt.show()
    else:
        plt.savefig(fname, format='png')

def lowpass(data, cutoff, fs):
    b = signal.firwin(255, cutoff, fs=fs)
    return signal.lfilter(b, 1, data)

def highpass(data, cutoff, fs):
    b = signal.firwin(1023, cutoff, pass_zero=False, fs=fs)
    return signal.lfilter(b, 1, data)

FS=200
Length=100

if __name__ == '__main__':
    sin90 = create_sin_wave(0.3, 90, FS, Length)
    sin50 = create_sin_wave(0.3, 50, FS, Length)
    sin10 = create_sin_wave(0.3, 10, FS, Length)
    plot_data(sin90, FS, Length, 'sin90.png')
    plot_data(sin50, FS, Length, 'sin50.png')
    plot_data(sin10, FS, Length, 'sin10.png')
    plot_data(
        sin90 + sin50 + sin10,
        FS, Length,
        'input.png'
    )
    test_target = sin90 + sin50 + sin10
    print(test_target)
    with open('target.dat', 'wb') as f:
        data = [struct.pack('h', d) for d in test_target.tolist()]
        f.write(b''.join(data))
    plot_data(lowpass(test_target, 10, FS), FS, Length, 'lowpass.png')
    plot_data(highpass(test_target, 90, FS), FS, Length, 'highpass.png')
