import logging
import os, os.path
import numpy as np
import wave
import glob
from deepspeech import Model
import wave
import soundfile as sf
import sounddevice as sd
from time import sleep
from scipy.io.wavfile import write
import vlc
from random import randint
import serial



logging.basicConfig(level=20)


def float2pcm(sig, dtype='int16'):

    sig = np.asarray(sig)
    dtype = np.dtype(dtype)
    i = np.iinfo(dtype)
    abs_max = 2 ** (i.bits - 1)
    offset = i.min + abs_max
    return (sig * abs_max + offset).clip(i.min, i.max).astype(dtype)


def load_model(models, scorer):
    ds = Model(models)
    model_load_end = 11
    ds.enableExternalScorer(scorer)
    scorer_load_end = 12
    return [ds, model_load_end, scorer_load_end]
 

def resolve_models(dirName):
    pb = glob.glob(dirName + "/*.pbmm")[0]
    scorer = glob.glob(dirName + "/*.scorer")[0]
    print("Found scorer: %s" % scorer)
    return pb, scorer


def rec_and_transcribe(duration, freq = 16000):
    stream = model_retval[0].createStream()
    print("recording")
    recording = sd.rec(int(duration * freq), samplerate=freq, channels=1)
    # Record audio for the given number of seconds
    sd.wait()
    print("finished recording")
    file_name = 'test_audio'
    saving_dir = os.getcwd()
    #remember to change the directory where we are saving the audio in deployment to the current working directory
    write(os.path.join(saving_dir, f"{file_name}.wav"), freq, float2pcm(recording))

    send_command("thinking", serialArduino)
    text = transcribe_streaming(os.path.join(saving_dir, f"{file_name}.wav"), stream)
    return text

model = os.getcwd()
dirName = os.path.expanduser(model)

# Resolve all the paths of model files
output_graph, scorer = resolve_models(dirName)

# Load output_graph, alphabet and scorer
model_retval = load_model(output_graph, scorer)



def read_wav_file(filename):
    with wave.open(filename, 'rb') as w:
        rate = w.getframerate()
        frames = w.getnframes()
        buffer = w.readframes(frames)

    return buffer, rate



def transcribe_streaming(audio_file, stream):
    buffer, rate = read_wav_file(audio_file)
    offset=0
    batch_size=8196
    text=''

    while offset < len(buffer):
      end_offset=offset+batch_size
      chunk=buffer[offset:end_offset]
      data16 = np.frombuffer(chunk, dtype=np.int16)

      stream.feedAudioContent(data16)
      text=stream.intermediateDecode()
      print(text)
      offset=end_offset
      
    stream.finishStream()
    return text


def ugo_speak(filename, channels=[2]):
    sounds_dir = os.path.join(os.getcwd(), "ugo sounds")
    filepath = os.path.join(sounds_dir, filename)
    data, fs = sf.read(filepath)
    # print("fs: ", data)
    sd.play(data, samplerate=fs, mapping=channels, blocking=True)
    sd.wait


def send_command(command, serialArduino):
    serialArduino.write(command.encode('ascii'))
    


serialArduino = serial.Serial("COM3", 9600)
def main():

    sports = [
        ["football", "foot but", "but"],
        ["swimming", "ming", "ing", "ming swimming", "ing swimming"],
    ]

    jobs = [
        ["police"],
        ["artist"]
    ]

    i = 0
    while True:
        repeat_flag = 1
        ugo_speak("Im Ugo.wav", [1])
        text = rec_and_transcribe(5)
        if text in ["ugo start the game", "go start the game", "o start the game", " start the game",
                    "start the game", "ostart the game", "gostart the game", "ustart the game", "uo start the game", "state the game",
                    "to start the game"]:
                    while repeat_flag == 1:

                        send_command("ugo lets play", serialArduino)
                        ugo_speak("pick topics.wav")
                        sleep(0.5)
                        text = rec_and_transcribe(3)
                        if text in ["sports", "sport", "port", "ports", "its port"]:
                            repeat_flag = 0
                            send_command("whisper mode", serialArduino)
                            i = randint(0, len(sports)-1)
                            sleep(2.5)
                            if(sports[i][0] == "football"):
                                ugo_speak("football.wav")
                            elif (sports[i][0] == "swimming"):
                                ugo_speak("swimming.wav")
                            send_command("home", serialArduino)
                            ugo_speak("what was the word.wav")
                            text = rec_and_transcribe(3)
                            if text in sports[i]:
                                ugo_speak("yay.wav")
                                send_command("happy", serialArduino)
                                
                            
                            sleep(5.5)
                            if(sports[i][0] == "football"):
                                ugo_speak("explaining - football.wav")
                            elif (sports[i][0] == "swimming"):
                                ugo_speak("explaining - swimming.wav")
                            sleep(1)
                            send_command("restart", serialArduino)
                            ugo_speak("bye.wav")
                            sleep(1)

                        if text in ["jobs", "job", "john", "johns", "obs", "bob"]:
                            # don't forget to put this in every vocabulary category.
                            repeat_flag = 0
                            send_command("whisper mode", serialArduino)
                            i = randint(0, len(jobs)-1)
                            sleep(2.5)
                            if(jobs[i][0] == "police"):
                                ugo_speak("police.wav")
                            elif (jobs[i][0] == "artist"):
                                ugo_speak("artist.wav")
                            send_command("home", serialArduino)
                            ugo_speak("what was the word.wav")
                            text = rec_and_transcribe(3)
                            if text in jobs[i]:
                                ugo_speak("yay.wav")
                                send_command("happy", serialArduino)
                                
                            
                            sleep(5.5)
                            if(jobs[i][0] == "police"):
                                ugo_speak("explaining - police.wav")
                            elif (jobs[i][0] == "artist"):
                                ugo_speak("explaining - artist.wav")
                            sleep(1)
                            send_command("restart", serialArduino)
                            ugo_speak("bye.wav")
                            sleep(1)
                               
    
    


if __name__ == '__main__':
    main()
