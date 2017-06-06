#!/usr/bin/python
import warnings
warnings.simplefilter("ignore", DeprecationWarning)
warnings.simplefilter("ignore", UserWarning)
from scikits.audiolab import Format, Sndfile
from scipy.signal import firwin, lfilter
from tempfile import mkstemp
import numpy as np
import urllib2
import math
import sys
import re
import os
import subprocess


#For for English Speech Recognizer
Lang="en-US"


#NOw for google speech V2
url='https://www.google.com/speech-api/v2/recognize?output=json&key=AIzaSyBOti4mM-6x9WDnZIjIeyEU21OpBXqWBgw&lang='+Lang

#Places where to find binaries
binaries_path="/home/roothome/Speaker-recognition-Asterisk"
registering_bin=binaries_path+"/binarytest.out"
checking_bin=binaries_path+"/binarytest.out"

#register or check modes
#they are given as input
mode = sys.argv[1]

#Identifier extension will be added like a caller id
caller_id = sys.argv[2]

#General path
path="/res"
models=path+"/models"
default_name_model="model"

#TODO
#sys.stdout.write("EXEC " + "\"" + "NOOP" + "\" \"" + "Hello Waiting For Speech ..."+os.getcwd() + str(sys.argv[1]) + "\" " + "\n")
#path="/res/"
#os.rename(path+"model",path+"model"+ str(sys.argv[1]))


silence=True
env = {}
RawRate=8000
chunk=1024

#http://en.wikipedia.org/wiki/Vocal_range
#Assuming Vocal Range Frequency upper than 75 Hz
VocalRange = 75.0


#cd, FileNameTmp    = mkstemp('TmpSpeechFile.flac')

#Assuming Energy threshold upper than 15 dB
Threshold = 15

#10 seconds x 16000 samples/second x ( 16 bits / 8bits/byte ) = 160000 bytes
#160000/1024 = +/- 157
#157*1024 = 160768
TimeoutSignal = 160768

#then 1 second x 16000 = 16000
#16000/1024 = 15,625 round to 16
#16*1024 = 16384
Timeout_NoSpeaking=16384

#normalization for RMS Calc
SHORT_NORMALIZE = (1.0/32768.0)

#
LastBlock=''

#File Descriptor delivery in Asterisk
FD=3

#Open File Descriptor
file=os.fdopen(FD, 'rb')

signal=0

all=[]


while 1:
        line = sys.stdin.readline().strip()

        if line == '':
                break
        key,data = line.split(':')
        if key[:4] <> 'agi_':
                sys.stderr.write("Did not work!\n");
                sys.stderr.flush()
                continue
        key = key.strip()
        data = data.strip()
        if key <> '':
                env[key] = data



for key in env.keys():
        sys.stderr.write(" -- %s = %s\n" % (key, env[key]))
        sys.stderr.flush()



def SendSpeech(File):
    if mode == "register":
        RegisterUser(File)
    else:
        CheckVoiceID(File)
                

def RegisterUser(File):
        #to test
        args = (registering_bin,"Salut Fernando")
        #flac=open(File,"rb").read()
        #os.remove(File)
        #real command: args= (registering_bin, File)
        popen = subprocess.Popen(args, stdout=subprocess.PIPE)
        try:
                result = popen.stdout.read()# to wait that the analysis is complete
        except:
                sys.stdout.write("EXEC " + "\"" + "NOOP" + "\" \"" + "speech not recognized ..." + "\" " + "\n")
                sys.stdout.flush()
        if result:
                #TODO change path model in function of the teacher binary
                os.rename(binaries_path,models+"/"+caller_id)
                sys.stdout.write('SET VARIABLE NumberAssigned "%s"\n'% caller_id)
                sys.stdout.write('You have been assigned number : "%s"\n'% caller_id)
                sys.stdout.flush()
                sys.stdout.write("EXEC " + "\"" + "NOOP" + "\" \"" "%s \n"% caller_id)
                sys.stdout.flush()

def CheckVoiceID(File):
        args = (checking_bin,"1")
        #real command: args= (checking_bin, File, models + "/" + caller_id)
        popen = subprocess.Popen(args, stdout=subprocess.PIPE)
        try:
            result = popen.stdout.read()# to wait that the analysis is complete
        except:
            sys.stdout.write("EXEC " + "\"" + "NOOP" + "\" \"" + "speech not recognized ..." + "\" " + "\n")
            sys.stdout.flush()
        if str(result) == "1": 
            sys.stdout.write('SET VARIABLE CallerFound "%s"\n'% caller_id)
            sys.stdout.flush()
            sys.stdout.write("EXEC " + "\"" + "NOOP" + "\" \"" "%s \n"% caller_id)
            sys.stdout.flush()



def Filter(samps):
        FC = 0.05/(0.5*RawRate)
        N = 200
        a = 1
        b = firwin(N, cutoff=FC, window='hamming')
        return lfilter(b, a, samps)

def Pitch(signal):
        if sys.version_info < (2, 6):
                crossing =[]
                for s in signal:
                        crossing.append(s)
        else:
                crossing = [math.copysign(1.0, s) for s in signal]
        #index = find(np.diff(crossing));
        index = np.nonzero(np.diff(crossing));
        index=np.array(index)[0].tolist()
        f0=round(len(index) *RawRate /(2*np.prod(len(signal))))
        return f0;

def rms(shorts):
        rms2=0
        count = len(shorts)/2
        sum_squares = 0.0
        for sample in shorts:
                n = sample * SHORT_NORMALIZE
                sum_squares += n*n
                rms2 = math.pow(sum_squares/count,0.5)
        return rms2 * 1000

def speaking(data):
        rms_value = rms(data)
        if rms_value > Threshold:
                return True
        else:
                return False

def VAD(SumFrequency, data2):
        AVGFrequency = SumFrequency/(Timeout_NoSpeaking+1);
        if AVGFrequency > VocalRange/2:
                S=speaking(data2)
                if S:
                        return True;
                else:
                        return False;


        else:
                return False;

def RecordSpeech(TimeoutSignal, LastBlock, LastLastBlock):
        for s in LastLastBlock:
                all.append(s)
        for s in LastBlock:
                all.append(s)
        signal=0;
        while signal <= TimeoutSignal:
                RawSamps = file.read(Timeout_NoSpeaking)
                samps = np.fromstring(RawSamps, dtype=np.int16)
                for s in samps:
                        all.append(s)
                signal = signal + Timeout_NoSpeaking;
                #rms_value=rms(samps)
                Speech=speaking(samps)
                #sys.stdout.write("EXEC NOOP %s \"\"\"\n"% str(rms_value))
                #sys.stdout.flush()

                #if rms_value > Threshold:
                if Speech:
                        sys.stdout.write("EXEC " + "\"" + "NOOP" + "\" \"" + "Speech Found ..." + "\" " + "\n")
                        sys.stdout.flush()
                else:
                        sys.stdout.write("EXEC " + "\"" + "NOOP" + "\" \"" + "End of the Speech..." + "\" " + "\n")
                        sys.stdout.flush()
                        signal=TimeoutSignal+1

def PlayStream (params):
        sys.stderr.write("STREAM FILE %s \"\"\n" % str(params))
        sys.stderr.flush()
        sys.stdout.write("STREAM FILE %s \"\"\n" % str(params))
        sys.stdout.flush()
        result = sys.stdin.readline().strip()


sys.stdout.write("EXEC " + "\"" + "NOOP" + "\" \"" + "Hello Waiting For Speech ..." + "\" " + "\n")
sys.stdout.flush()



PlayStream("beep");
sys.stdout.flush()


while silence:
        #Input Real-time Data Raw Audio from Asterisk
        RawSamps = file.read(chunk)
        samps = np.fromstring(RawSamps, dtype=np.int16)
        samps2=Filter(samps)
        Frequency=Pitch(samps2)
        rms_value=rms(samps)
        signal = signal + chunk;
        if (rms_value > Threshold) and (Frequency > VocalRange):
                silence=False
                LastLastBlock=LastBlock
                LastBlock=samps
                sys.stdout.write("EXEC " + "\"" + "NOOP" + "\" \"" + "Speech Detected Recording..." + "\" " + "\n")
                sys.stdout.flush()
        if (signal > TimeoutSignal):
                sys.stdout.write("EXEC " + "\"" + "NOOP" + "\" \"" + "Time Out No Speech Detected ..." + "\" " + "\n")
                sys.stdout.flush()
                sys.exit()

RecordSpeech(TimeoutSignal, LastBlock, LastLastBlock)


array = np.array(all)


fmt         = Format('flac', 'pcm16')
nchannels   = 1

cd, FileNameTmp    = mkstemp('TmpSpeechFile.flac')


# making the file .flac
afile =  Sndfile(FileNameTmp, 'w', fmt, nchannels, RawRate)

#writing in the file
afile.write_frames(array)

SendSpeech(FileNameTmp)
