import os
from scipy import signal
from pydub import AudioSegment
from scipy.io import wavfile
import pydub
from matplotlib import pyplot as plt
import numpy as np

class Input():
    def __init__(self, base_path='data/mp3'):
        self.base_path = base_path
        self.filenames = os.listdir(base_path)

    def extractRawData(self, path):
        path = os.path.join(self.base_path, path)
        # read mp3 file
        mp3 = pydub.AudioSegment.from_mp3(path)
        # convert to wav
        mp3.export("temp.wav", format="wav")
        # read wav file
        rate, data = wavfile.read("temp.wav")
        return rate, data

if __name__ == "__main__":
    input = Input(base_path='data/mp3')
    rate, data = input.extractRawData(input.filenames[0])
    data = data[1000000:2000000]
    times = np.arange(len(data))/float(rate)

    # Make the plot
    # You can tweak the figsize (width, height) in inches
    plt.figure(figsize=(30, 4))
    plt.fill_between(times, data[:,0], data[:,1], color='k') 
    plt.xlim(times[0], times[-1])
    plt.xlabel('time (s)')
    plt.ylabel('amplitude')
    # You can set the format by changing the extension
    # like .pdf, .svg, .eps
    plt.savefig('plot.png', dpi=100)
    plt.show()
