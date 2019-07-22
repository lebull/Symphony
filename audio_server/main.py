
import pyaudio
import numpy as np
import math
import time
import sys
import signal
from argparse import ArgumentParser
from symphony import Symphony



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

thread = Symphony(index)
thread.setName("Symphony.py")

def close(a, b):
    print("Closing Stream")
    thread.exit()

signal.signal(signal.SIGINT, close)
signal.signal(signal.SIGTERM, close)
thread.start()
thread.join()

