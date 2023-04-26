## THIS ENDEAVOUR IS SCRAPED BECAUSED:
##    Not All audio, has a text associated with it in
##    the books.


# %%
# IMPORTS

#from pocketsphinx import Segmenter, Pocketsphinx,Decoder
import wave
import os

# %%
# Define File name variable
file_in = r'C:\Users\Mubarak Salley\Documents\Accede\Tenacity-Book-11\src\assets\audio\SB11 R1 G1 P91.mp3'
file_out = r'C:\Users\Mubarak Salley\Documents\Accede\Tenacity-Book-11\src\assets\audio\SB11 R1 G1 P91.wav'

# %%
# Generate .wav file from mp3
# if not os.path.exists(file_out):
  # os.system(f"ffmpeg -i \"{file_in}\" -vn -acodec pcm_s16le -ac 1 -ar 44100 -f wav \"{file_out}\"")


# %%
# Configure Pocket Sphix
# decoder = Decoder()

# with wave.open(file_out , 'rb') as audi:
#     decoder.start_utt()
#     total_frames = audi.getnframes()
#     output = audi.readframes(total_frames)
#     #output = audi.readframes(2048)
#     decoder.process_raw(output)
#     decoder.end_utt()
#     #print(dir(decoder))



# %%
# Extract Text From Wave
# import math
# import wave
# from vosk import KaldiRecognizer, Model, SetLogLevel
# import json

# model = Model(r"C:\Users\Mubarak Salley\Downloads\vosk-model-en-us-0.22\vosk-model-en-us-0.22")
# SetLogLevel(0)

# cached_data = []
# textdata = "";

# with wave.open(file_out , 'rb') as audi:
#     recognizer = KaldiRecognizer(model, audi.getframerate())
#     total_data = audi.getnframes()
#     remainder = total_data % 1000000
#     num_of_loops = math.floor(total_data/ 1000000)

#     count = 0
#     for i in range( num_of_loops + 1):
#         data = audi.readframes(1000000) if count < num_of_loops else audi.readframes(remainder)
#         if recognizer.AcceptWaveform(data):
#             print("Wave Form Accepted")
#             text = json.loads(recognizer.Result())
#             print(text["text"])
#             textdata = textdata + " " + text["text"]
#         else:
#             print("beans")
#             text = json.loads(recognizer.PartialResult())
#             print(text["partial"])
#             textdata = textdata + " " + text["partial"]
#         count += 1



# %%
# os.system(f"del \"{file_out}\"")
#print(f"del '{file_out}'")

# %%
# Getting All The Paths To Audio

#IMPORTS
import glob, math, wave, os, json
from vosk import KaldiRecognizer, Model, SetLogLevel

#SET UP VOICE RECOGNIZER
model = Model(r"C:\Users\Mubarak Salley\Downloads\vosk-model-en-us-0.22\vosk-model-en-us-0.22")
SetLogLevel(1)

AUDIO_BASE_PATH = r'C:\Users\Mubarak Salley\Documents\Accede\Tenacity-Book-11\src\assets\audio'
audioPathList = glob.glob(AUDIO_BASE_PATH + "\*.mp3")

# %%
# CONVERT AUDIO TO TEXT
# textdata = ""
# counttt = -1
# print("STARTING FOR LOOP")
# for audioPath in audioPathList :
#     counttt  = counttt + 1
#     if counttt > 3:
#         break
#     audioPathOut = audioPath[0:-3] + "wav"

#     audio_name = audioPath.split("audio")[1].strip("\\")
#     #print("The SPLIT ", audio_name.strip("\\"))


#     #Convert To Wave file
#     result = os.system(f"ffmpeg -i \"{audioPath}\" -vn -acodec pcm_s16le -ac 1 -ar 44100 -f wav \"{audioPathOut}\"")

#     #Extract Text
#     if result == 0:
#         print("STARTING FOR LOOP")
#         # EXTRACTING WAVE FILES, 1000000 bytes at a time
#         textdata = textdata + "\""+audio_name + "\""+ ":" + "\""
#         with wave.open(audioPathOut , 'rb') as audi:
#             recognizer = KaldiRecognizer(model, audi.getframerate())
#             total_data = audi.getnframes()
#             remainder = total_data % 1000000
#             num_of_loops = math.floor(total_data/ 1000000)
#             count = 0



#             for i in range( num_of_loops + 1):
#                 data = audi.readframes(1000000) if count < num_of_loops else audi.readframes(remainder)
#                 if recognizer.AcceptWaveform(data):
#                     print("Wave Form Accepted")
#                     text = json.loads(recognizer.Result())
#                     print(text["text"])
#                     textdata = textdata + " " + text["text"]
#                 else:
#                     print("beans")
#                     text = json.loads(recognizer.PartialResult())
#                     print(text["partial"])
#                     textdata = textdata + " " + text["partial"]
#                 count += 1
#                 break

#         #Delete Wave File
#         textdata = textdata + "\","
#         result = os.system(f"del \"{audioPathOut}\"")
#         if result != 0:
#             print("OS failed to delete wave file ")

#     else:
#         print(" ffmpeg command could not convert mp3 to wav file")

# print(textdata)





# %%

def convert_audio_to_text( audioPath):
    audioPathOut = audioPath[0:-3] + "wav"

    audio_name = audioPath.split("audio")[1].strip("\\")
    #print("The SPLIT ", audio_name.strip("\\"))


    #Convert To Wave file
    result = os.system(f"ffmpeg -y -i \"{audioPath}\" -vn -acodec pcm_s16le -ac 1 -ar 44100 -f wav \"{audioPathOut}\"")

    #Extract Text
    if result == 0:
        print("STARTING FOR LOOP")
        # EXTRACTING WAVE FILES, 1000000 bytes at a time
        #textdata = textdata + "\""+audio_name + "\""+ ":" + "\""
        textdata = ""
        with wave.open(audioPathOut , 'rb') as audi:
            recognizer = KaldiRecognizer(model, audi.getframerate())
            total_data = audi.getnframes()
            #am= 1000000
            am = total_data
            remainder = total_data % am
            num_of_loops = math.floor(total_data/ am)
            count = 0



            for i in range( num_of_loops + 1):
                data = audi.readframes(am) if count < num_of_loops else audi.readframes(remainder)
                if recognizer.AcceptWaveform(data):
                    print("Wave Form Accepted")
                    text = json.loads(recognizer.Result())
                    print(text["text"])
                    textdata = textdata + " " + text["text"]
                else:
                    print("beans")
                    text = json.loads(recognizer.PartialResult())
                    print(text["partial"])
                    textdata = textdata + " " + text["partial"]
                count += 1
                break

        #Delete Wave File
        #textdata = textdata + "\","
        result = os.system(f"del \"{audioPathOut}\"")
        if result != 0:
            print("OS failed to delete wave file ")
        return textdata

    else:
        print(" ffmpeg command could not convert mp3 to wav file")
