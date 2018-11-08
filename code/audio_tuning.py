from moviepy.editor import VideoFileClip, concatenate_videoclips
from datetime import datetime
from video import Video
from merge import Merge
from initialize import initialize
from pydub import AudioSegment
from pydub.utils import get_array_type
import array
import wave
import re
import math


def audio_making(video_list, endTime):
    print(video_list)
    aud_list = []
    index_list = []
    index_start = []
    maxi_start = 0
    t = 0
    while t < endTime - 1:
        maxi = 0
        for video in video_list:
            if video.start_time <= t:
                if video.end_time > maxi:
                    maxi = video.end_time
                    maxi_start = video.start_time
                    vid = video.video_clip
                    video_save = video
        print(video_save.video_clip)
        print(video_save.start_time)
        print(video_save.end_time)
        aud_list.append(vid)
        index_start.append(maxi_start)
        index_list.append(t)
        t = maxi - 1

    file_vid = open("audio_names.txt", "w")
    for ele in aud_list:
        file_vid.write(ele)
        file_vid.write("\n")
    """
    #print(aud_list)
    #print(index_list)

    i = 0
    while i < aud_list.__len__():
        name = "aud" + str(i) + ".wav"
        temp = index_list[i] - index_start[i]
        temp = math.floor(temp)
        video_temp = VideoFileClip(aud_list[i]).subclip(temp)
        audio_temp = video_temp.audio
        audio_temp.write_audiofile(name)
        i = i + 1
        video_temp.close()
        audio_temp.close()

    with wave.open('aud0.wav') as fd:
        params = fd.getparams()
        frames = fd.readframes(100000000)  # 1 million frames max

    final_list = list(frames)
    i = 1

    while i < aud_list.__len__():
        name = "aud" + str(i) + ".wav"

        with wave.open(name) as fd:
            params1 = fd.getparams()
            frames1 = fd.readframes(100000000)  # 1 million frames max

        frame_list1 = list(frames1)
        count = final_list.__len__() - 200000
        count_final = count
        count1 = 0

        diff_list = []
        while count < final_list.__len__():
            count1 = count
            count2 = 0
            diff = 0
            while count1 < final_list.__len__() and count2 < frame_list1.__len__():
                diff = (final_list[count1] - frame_list1[count2]) ** 2 + diff
                count1 = count1 + 1
                count2 = count2 + 1
            diff = diff / count2
            if final_list.__len__() - count > 1000:
                diff_list.append(diff)
            count = count + 1000

        mini = diff_list[0]
        index = 0
        j = 0
        while j < diff_list.__len__():
            if diff_list[j] < mini:
                mini = diff_list[j]
                index = j
            j = j + 1

        print(index)
        print(mini)
        index = index * 1000
        index = index + count2/2
        print(index)
        j = 0
        temp_list = []
        index = index + count_final
        while j < index:
            temp_list.append(final_list[j])
            j = j + 1

        j = math.floor(count2/2)
        while j < frame_list1.__len__():
            temp_list.append(frame_list1[j])
            j = j + 1

        final_list = temp_list
        i = i + 1

    new_frame = bytes(final_list)
    with wave.open('output_new.wav', 'wb') as fd:
        fd.setparams(params)
        fd.writeframes(new_frame)


    
    
    
    
    
    video1 = VideoFileClip("video1.mp4").subclip(0,5)
    video2 = VideoFileClip("video1.mp4").subclip(2.5,7.5)
    audio1 = video1.audio
    audio2 = video2.audio
    audio1.write_audiofile("audio1.wav")
    audio2.write_audiofile("audio2.wav")
    
    
    sound1 = AudioSegment.from_wav("audio1.wav")
    # sound._data is a bytestring
    sound2 = AudioSegment.from_wav("audio2.wav")
    bit_depth1 = sound1.sample_width * 8
    array_type1 = get_array_type(bit_depth1)
    numeric_array1 = array.array(array_type1, sound1._data)
    
    bit_depth2 = sound2.sample_width * 8
    array_type2 = get_array_type(bit_depth2)
    numeric_array2 = array.array(array_type2,sound2._data)
    
    with wave.open('audio1.wav') as fd:
        params1 = fd.getparams()
        frames1 = fd.readframes(100000000) # 1 million frames max
    
    with wave.open('audio2.wav') as fd:
        params2 = fd.getparams()
        frames2 = fd.readframes(100000000) # 1 million frames max
    
    
    
    #print(frames1)
    print(type(frames1))
    frame_list1 = list(frames1)
    frame_list2 = list(frames2)
    #print(li)
    frame_list = []
    diff_list = []
    print(frame_list1.__len__())
    print(frame_list2.__len__())
    count = 0
    count1 = 0
    
    while count<frame_list1.__len__():
        count1 = count
        count2 = 0
        diff = 0
        while count1<frame_list1.__len__() and count2<frame_list2.__len__():
            diff = (frame_list1[count1]-frame_list2[count2])**2 + diff
            count1 = count1 + 1
            count2 = count2 + 1
        diff = diff/count2
        if frame_list1.__len__()- count >1000:
                diff_list.append(diff)
        count = count + 1000
    
    print(diff_list)
    mini = diff_list[0]
    index = 0
    i = 0
    while i<diff_list.__len__():
        if diff_list[i] < mini:
            mini = diff_list[i]
            index = i
        i = i+1
    
    print(index)
    print(mini)
    index = index*1000
    index = index-500
    print(index)
    i = 0
    while i<index:
        frame_list.append(frame_list1[i])
        i = i+1
    
    i = 0
    while i < frame_list2.__len__():
        frame_list.append(frame_list2[i])
        i = i+1
    
    new_frame = bytes(frame_list)
    #print(newframe)
    #print(frame)
    with wave.open('output.wav', 'wb') as fd:
        fd.setparams(params1)
        fd.writeframes(new_frame)
    """