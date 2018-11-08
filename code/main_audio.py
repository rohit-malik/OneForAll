from hashlib import sha1
import numpy as np
from pydub import AudioSegment
import fingerprint
import warnings
import json
warnings.filterwarnings("ignore")
import work

filename = "C:/Users/Nitin Malik/PycharmProjects/audio_matching/audio.mp3"

"""
def unique_hash(filepath, blocksize=2**20):
     Small function to generate a hash to uniquely generate
    a file. Inspired by MD5 version here:
    http://stackoverflow.com/a/1131255/712997

    Works with large files.
    
    s = sha1()
    with open(filepath, "rb") as f:
        while True:
            buf = f.read(blocksize)
            if not buf:
                break
            s.update(buf)
    return s.hexdigest().upper()
"""

def audio_main():
    file_file = open("audio_names.txt", "r")
    line = file_file.readline()
    list_videos = []
    while line:
        line = line.rstrip()
        list_videos.append(line)
        line = file_file.readline()

    #list_videos = ["video1.mp4", "video2.mp4"]
    print(list_videos)
    list_time = []
    audiofile1 = AudioSegment.from_mp3(filename)
    i = 1
    result_previous = None
    if(list_videos.__len__()==1):
        audio_file = AudioSegment.from_file(list_videos[0], "mp4")
        final_audio = audio_file
        final_audio.export("mashup.mp3", format="mp3")
        return
    while i< list_videos.__len__():
        filename1 = list_videos[i-1]
        filename2 = list_videos[i]

        audio1 = AudioSegment.from_file(filename1, "mp4")
        audio2 = AudioSegment.from_file(filename2, "mp4")

        if result_previous is not None:
            result1_1 = result_previous
        else:
            result1_1 = work.work_audio(audio1, filename1)

        result2_2 = work.work_audio(audio2, filename2)
        result1 = result1_1[0]
        result2 = result2_2[0]
        frame_rate = result1_1[1]
        result_previous = result2_2


        res2 = list(result2)
        res2.sort(key=lambda x: x[1])
        res1 = list(result1)

        l = {}
        for tup in res2:
            for tu in res1:
                if tu[0] == tup[0]:
                    if (tu[1] - tup[1]) in l:
                        l[tu[1] - tup[1]] = l[tu[1] - tup[1]] + 1
                    else:
                        l[tu[1] - tup[1]] = 1

        maxi = 0
        max_index = 0
        for key in l:
            if l[key] > maxi:
                maxi = l[key]
                max_index = key

        print(maxi)
        print(max_index)
        match_value = (2048 * max_index * 1000)/frame_rate

        if match_value < 0:
            list_videos[i-1], list_videos[i] = list_videos[i], list_videos[i-1]
        print(match_value)
        list_time.append(abs(match_value))
        i = i + 1

    print(list_videos)
    i = 1
    final_audio_temp = AudioSegment.from_file(list_videos[0], "mp4")
    final_audio = final_audio_temp[:list_time[0]]

    while i < list_time.__len__():
        audio_file = AudioSegment.from_file(list_videos[i], "mp4")
        final_audio = final_audio + audio_file[:list_time[i]]
        i = i + 1

    audio_file = AudioSegment.from_file(list_videos[i], "mp4")
    final_audio = final_audio + audio_file
    final_audio.export("mashup.mp3", format="mp3")
    return


