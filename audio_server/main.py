import pyaudio
import numpy as np
import math
import binascii
#from server import sendMessage
import server
import time
import sys

from argparse import ArgumentParser

parser = ArgumentParser()
parser.add_argument("-i", "--index", dest="index",
                    help="Audio Device Index", metavar="INDEX")
args = parser.parse_args()

def listDevices():
    pyaudio_instance = pyaudio.PyAudio()
    for i in range(pyaudio_instance.get_device_count()):
        print pyaudio_instance.get_device_info_by_index(i)

if(args.index == None):
    listDevices()
    index = 0
else:
    index = args.index


print(index)

# print('\navailable devices:')



def compactArrayWithAverage(inputArray, endSize):
    n_averaged_elements = int(len(inputArray)/(endSize/3))
    averaged_array = []
    
    for i in range(0, len(inputArray), n_averaged_elements):
        slice_from_index = i
        slice_to_index = slice_from_index + n_averaged_elements
        averaged_array.append(np.max(inputArray[slice_from_index:slice_to_index]))
    return averaged_array[0:endSize]
    

np.set_printoptions(suppress=True) # don't use scientific notation

CHUNK = 2048 # number of data points to read at a time
RATE = 44100 # time resolution of the recording device (Hz)

p=pyaudio.PyAudio() # start the PyAudio class

channelIndex = 1

stream=p.open(  format=pyaudio.paInt16,
                channels=1,
                rate=RATE,
                input=True,
                output=False,
                input_device_index=2,
                frames_per_buffer=CHUNK)

def getAudioSpectrum():
    data = np.fromstring(stream.read(CHUNK),dtype=np.int16)
    #data = data * np.hanning(len(data)) # smooth the FFT by windowing data
    fft = abs(np.fft.fft(data).real)

    halfResultFtt = fft[100:int(len(fft/2))] 
    fullResultFtt = halfResultFtt + np.flip(halfResultFtt)

    # freq = np.fft.fftfreq(CHUNK,1.0/RATE)
    # freq = freq[:int(len(freq)/2)] # keep only first half
    fft = compactArrayWithAverage(fft, 168)
    return fft


lastMessage = None


# create a numpy array holding a single read of audio data
while True: #to it a few times just to see

    #Filter FFT Result
    output = [ max((int(dataPoint/1024)**(2.5))/16, 0) for dataPoint in getAudioSpectrum()]

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

        #g =- r/4096

        r = max([min([r, 255]), 0])
        g = max([min([g, 255]), 0])
        b = max([min([b, 255]), 0])

        message.append(int(r))
        message.append(int(g))
        message.append(int(b))

    message = message[0:168]

    #print message

    if(lastMessage):
        for index, lastVal in enumerate(message):
            worstCaseFrameToDrop = 3
            message[index] = max([message[index], lastMessage[index] - (255/worstCaseFrameToDrop)])

    server.sendMessage(bytearray(message))
    lastMessage = message
    #print("outputRange: ({}\t: {})\tfftRange: ({}\t: {})".format(min(message), max(message), min(output), max(output)))
    #print message
    time.sleep(1.0/24)
    

    # uncomment this if you want to see what the freq vs FFT looks like
    # plt.plot(freq,fft)
    # plt.axis([0,4000,None,None])
    # plt.show()
    # plt.close()

    # close the stream gracefully


def exit():
    stream.stop_stream()
    stream.close()
    p.terminate()
signal.signal(signal.SIGINT, exit)
signal.signal(signal.SIGTERM, exit)