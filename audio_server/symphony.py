import pyaudio
import numpy as np
import math
import time
import matplotlib
import matplotlib.pyplot as plt

from threading import Thread
from server import sendMessage

#Const
CHUNK = 2048 # number of data points to read at a time
RATE = 44100 # time resolution of the recording device (Hz)
LIGHTCOUNT= 7 * 8

def compactArrayWithAverage(inputArray, endSize):
    n_averaged_elements = int(len(inputArray)/(endSize/3))
    averaged_array = []  
    for i in range(0, len(inputArray), n_averaged_elements):
        slice_from_index = i
        slice_to_index = slice_from_index + n_averaged_elements
        averaged_array.append(np.max(inputArray[slice_from_index:slice_to_index]))
    return averaged_array[0:endSize]


class Symphony(Thread):
    def __init__(self, index, *args, **kwargs):

        super(Symphony, self).__init__()

        self._pyAudio=pyaudio.PyAudio() # start the PyAudio class

        self.stream=self._pyAudio.open(  
                format=pyaudio.paInt16,
                channels=2,
                rate=RATE,
                input=True,
                output=False,
                input_device_index=index,
                frames_per_buffer=CHUNK)
        #self.stream.start_stream()

        self.active = True
        
        self.ftt = [0] * LIGHTCOUNT * 3
        self.lastMessage = None

    def getAudioSpectrum(self):
        data = np.fromstring(self.stream.read(CHUNK),dtype=np.int16)
        #data = data * np.hanning(len(data)) # smooth the FFT by windowing data
        self.fft = abs(np.fft.fft(data).real)

        halfResultFtt = self.fft[100:int(len(self.fft/2))] 
        fullResultFtt = halfResultFtt + np.flip(halfResultFtt)
        self.fft = compactArrayWithAverage(self.fft, LIGHTCOUNT * 3)

        freq = np.fft.fftfreq(CHUNK,1.0/RATE)
        freq = freq[:int(len(freq)/2)] # keep only first half
        
        # uncomment this if you want to see what the freq vs FFT looks like
        if(self.fft == None):
            plt.plot(freq,self.fft)
            plt.axis([0,4000,None,None])
            plt.show()


    def run(self):
        while (True):
            if(self.stream.is_stopped()):
                break
            self.getAudioSpectrum()
            #Filter FFT Result
            output = [ max((int(dataPoint/1024)**(2.5))/16, 0) for dataPoint in self.ftt]

            #What gets sent
            message = []

            for i in output:
                r = (i/2) ** 1.5 + (i/16) ** 3
                g = (i/2) ** 2
                b = (i/1) ** 1.4     

                #Max Via Scale
                maxV = max([max([r, g, b]), 1])
                r = int(((float(r))/maxV) * 255)
                g = int(((float(g))/maxV) * 255) * .8
                b = int(((float(b))/maxV) * 255) * .7

                r = max([min([r, 255]), 0])
                g = max([min([g, 255]), 0])
                b = max([min([b, 255]), 0])

                message.append(int(r))
                message.append(int(g))
                message.append(int(b))

            message = message[0:168]

            if(self.lastMessage):
                for index, lastVal in enumerate(message):
                    worstCaseFrameToDrop = 3
                    message[index] = max([message[index], self.lastMessage[index] - (255/worstCaseFrameToDrop)])

            #server.sendMessage(bytearray(message))
            self.lastMessage = message
            time.sleep(1.0/24)

    # close the stream gracefully
    def exit(self):
        self.stream.stop_stream()
        self.stream.close()
        self._pyAudio.terminate()
        plt.close()
        
        