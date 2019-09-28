
import pyaudio
import numpy as np
import math
import time
import sys
import signal
from argparse import ArgumentParser
from symphony import Symphony

import socket

UDP_IP = "192.168.1.128"
UDP_PORT = 4210
# MESSAGE = "Hello, World!"

# print "UDP target IP:", UDP_IP
# print "UDP target port:", UDP_PORT
# print "message:", MESSAGE
                    # Internet       # UDP
sock = socket.socket(socket.AF_INET, socket.SOCK_DGRAM) 


#Get args
parser = ArgumentParser()
parser.add_argument("-i", "--index", dest="index",
                    help="Audio Device Index", metavar="INDEX")
args = parser.parse_args()

#List devices
pyaudio_instance = pyaudio.PyAudio()
for i in range(pyaudio_instance.get_device_count()):
    print("{}\n\n".format(pyaudio_instance.get_device_info_by_index(i)))

if(args.index == None):
    index = 0
else:
    index = int(args.index)

print("Using Device with index {}".format(index))

#np setup
np.set_printoptions(suppress=True) # don't use scientific notation

CHUNK = 1024 # number of data points to read at a time
RATE = 44100 # time resolution of the recording device (Hz)

p=pyaudio.PyAudio() # start the PyAudio class

channelIndex = 1

stream=p.open(  format=pyaudio.paInt16,
                channels=1,
                rate=RATE,
                input=True,
                output=True,
                input_device_index=1,
                frames_per_buffer=CHUNK)

def sendMessage(message):
    #print("send {} things".format(len(message)))
    sock.sendto(message, (UDP_IP, UDP_PORT))

def getAudioSpectrum():
    data = np.fromstring(stream.read(CHUNK),dtype=np.int16)
    #data = data * np.hanning(len(data)) # smooth the FFT by windowing data
    fft = abs(np.fft.fft(data).real)

    #halfResultFtt = fft[100:int(len(fft/2))] 
    #fullResultFtt = halfResultFtt + np.flip(halfResultFtt)

    # freq = np.fft.fftfreq(CHUNK,1.0/RATE)
    # freq = freq[:int(len(freq)/2)] # keep only first half
    #fft = compactArrayWithAverage(fft, 168)
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
    sendMessage(bytearray(message))

    # if(lastMessage):
    #     for index, lastVal in enumerate(message):
    #         worstCaseFrameToDrop = 3
    #         message[index] = max([message[index], lastMessage[index] - (255/worstCaseFrameToDrop)])

    #lastMessage = message
    #print("outputRange: ({}\t: {})\tfftRange: ({}\t: {})".format(min(message), max(message), min(output), max(output)))
    #print message
    time.sleep(1.0/24)
    
    # uncomment this if you want to see what the freq vs FFT looks like
    # plt.plot(freq,fft)
    # plt.axis([0,4000,None,None])
    # plt.show()
    # plt.close()

def close(a, b):
    print("Closing Stream")
    thread.exit()

thread = Symphony(index)
thread.setName("Symphony.py")

signal.signal(signal.SIGINT, close)
signal.signal(signal.SIGTERM, close)
thread.start()
thread.join()

