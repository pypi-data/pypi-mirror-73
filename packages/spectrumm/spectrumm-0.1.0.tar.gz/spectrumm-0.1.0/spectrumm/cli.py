#!/usr/bin/env python3
#-*- coding: utf-8 -*-

import sys
import os, re
from scipy.io import wavfile # scipy library to read wav files
import numpy as np
from scipy import signal
from scipy.fftpack import fft
import matplotlib
import matplotlib.pyplot as plt
import pydub

matplotlib.use('TkAgg')
np.seterr(divide = 'ignore')


FLAGPATTERN = re.compile(r"-([a-z]*)")

FLAGS = {
    "help"        : ("h", re.compile(r"(--help)")),
    "spectrogram" : ("s", re.compile(r"(--spectrogram)")),
    "waveform"    : ("w", re.compile(r"(--waveform)")),
    "frequency"   : ("f", re.compile(r"(--frequency)"))
}


def read(f, normalized=False):
    """MP3 to numpy array"""
    a = pydub.AudioSegment.from_mp3(f)
    y = np.array(a.get_array_of_samples())
    if a.channels == 2:
        y = y.reshape((-1, 2))
    if normalized:
        return a.frame_rate, np.float32(y) / 2**15
    else:
        return a.frame_rate, y


def plot(path: str, flags: dict):
    """
    Decide which plots to create, if the file doesn't exist print a warning and
    exit.
    """
    if not os.path.isfile(path):
        if os.path.isdir(path):
            print("Error: {} is a directory, use a audio file".format(path))
            exit()
        print("Error: {} doesn't exist".format(path))
        exit()

    # Read Samples
    fs, samples = read(path)
    filename = os.path.basename(path)

    if flags["waveform"]:
        plot_waveform(samples, filename)

    if flags["frequency"]:
        plot_frequency(fs, samples, filename)

    if flags["spectrogram"]:
        plot_spectrogram(fs, samples, filename)

    plt.show()



def plot_waveform(samples, filename):
    """
    Plot Waveforms
    """
    plt.style.use(['seaborn-pastel'])
    plt.plot(samples)
    plt.title('Waveform ({})'.format(filename), size=16)



def plot_frequency(fs, samples, filename):
    """
    Plot frequency Spectrum of the file
    """
    plt.style.use(['seaborn-pastel'])
    n = len(samples) 
    AudioFreq = fft(samples)
    AudioFreq = AudioFreq[0:int(np.ceil((n+1)/2.0))] #Half of the spectrum
    MagFreq = np.abs(AudioFreq) # Magnitude
    MagFreq = MagFreq / float(n)
    # power spectrum
    MagFreq = MagFreq**2
    if n % 2 > 0: 
        # fft odd 
        MagFreq[1:len(MagFreq)] = MagFreq[1:len(MagFreq)] * 2
    else:
        # fft even
        MagFreq[1:len(MagFreq) -1] = MagFreq[1:len(MagFreq) - 1] * 2 

    plt.figure(figsize=(12, 4))
    freqAxis = np.arange(0,int(np.ceil((n+1)/2.0)), 1.0) * (fs / n)
    plt.plot(freqAxis/1000.0, 10*np.log10(MagFreq)) #Power spectrum
    plt.xlabel('Frequency (kHz)'); plt.ylabel('Power spectrum (dB)')
    plt.title('Frequency ({})'.format(filename), size=16)



def plot_spectrogram(fs, samples, filename):
    """
    Plot Spectrogram of the File
    """
    plt.style.use(['seaborn-pastel'])
    # Number of point in the fft
    N = 512 
    f, t, Sxx = signal.spectrogram(samples, fs, window = signal.blackman(N), nfft=N)
    plt.figure(figsize=(12, 4))
    # dB spectrogram

    plt.pcolormesh(t, f, 10*np.log10(Sxx)) 
    plt.ylabel('Frequency [Hz]')
    plt.xlabel('Time [seg]')
    plt.title('Spectrogram ({})'.format(filename), size=16)



def help():
    h = """============================ SPECTRUMM ================================
Display the spectrum of audio files

Usage:
    spectrum [Options] [audiofile ...]

Flags:
    --help/-h  . . . . . . .  Display this help message
    --spectrogram/-s . . . .  Show spectrogram
    --waveform/-w  . . . . .  Show waveform
    --frequency/-f . . . . .  Show frequency plot
"""
    print(h)



def match_flags() -> dict:
    """
    Match the Options and return a dictionary with bools
    """
    flags = {}
    arguments = sys.argv[1:]
    for flagname, (flagshort, flagpatternlong) in FLAGS.items():
        flags[flagname] = any(re.match(flagpatternlong, a) or match_shot_flags(a, flagshort) for a in sys.argv)

    return flags



def match_shot_flags(argument: str, letter: str):
    """
    Match Short Options
    """
    matches = re.search(FLAGPATTERN, argument) 
    if not matches:
        return False
    else:
        return letter in matches.group(1)



def main():
    # If nothing in STDIN print help
    if len(sys.argv) < 2:
        help()
        exit()

    files = list(set([a for a in sys.argv[1:] if not a.startswith("-")]))

    flags = match_flags()

    # If help flag is present, no flag is set or no file paths are given show help
    if flags["help"] or not any([o for o in flags.values()]) or len(files) == 0:
        help()
    else:
        for file in files:
            plot(file, flags)


                

if __name__ == "__main__":
    main()