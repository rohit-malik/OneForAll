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
from main_audio import audio_main
from Mashup import Mashup
from audio_tuning import audio_making
import warnings
warnings.filterwarnings("ignore")
import work


#Important variables--------------------------
videoList = []
#endTime=0
videoGap=5
lastCount=5
#videoList contains the all Video objects  

Tuple = initialize()

list_videos = Tuple[0]

list_videos.sort(key=lambda x: x.start_time)
i = 0
while i < list_videos.__len__():
    print(list_videos[i].video_clip)
    print(list_videos[i].start_time)
    print(list_videos[i].end_time)
    i = i + 1

result_previous = None
i = 1
starting = 1
while i < list_videos.__len__():
    flag = 0
    save = None

    if list_videos[i-1].end_time < list_videos[i].start_time:
        j = 0
        while j < i-1:
            if list_videos[j].end_time > list_videos[i].start_time:
                save = j
            j = j + 1
    else:
        flag = 1

    if flag == 0:
        if save is not None:
            filename1 = list_videos[save].video_clip
            save_object = list_videos[save]
            result_previous = None
        else:
            i = i + 1
            result_previous = None
            continue
    else:
        filename1 = list_videos[i-1].video_clip

    filename2 = list_videos[i].video_clip

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
    print(match_value)
    match_value = match_value/1000.0
    #print(match_value)
    #print(abs(match_value))

    if maxi <= 5:
        print("No match")
        list_videos[i].start_time = list_videos[i-1].end_time
        list_videos[i].end_time = list_videos[i].start_time + audio2.duration_seconds
        i = i + 1
        continue

    if flag == 1:
        if match_value < 0:
            list_videos[i-1], list_videos[i] = list_videos[i], list_videos[i-1]
            if starting == 1:
                list_videos[i-1].start_time = 0
                list_videos[i-1].end_time = audio2.duration_seconds
                starting = 0

            list_videos[i].start_time = abs(match_value) + list_videos[i - 1].start_time
            list_videos[i].end_time = list_videos[i].start_time + audio1.duration_seconds
        else:
            list_videos[i].start_time = abs(match_value) + list_videos[i-1].start_time
            list_videos[i].end_time = list_videos[i].start_time + audio2.duration_seconds
    else:
        if match_value < 0:
            save_object.start_time = abs(match_value) + list_videos[i].start_time
            save_object.end_time = save_object.start_time + audio1.duration_seconds
        else:
            list_videos[i].start_time = match_value + save_object.start_time
            list_videos[i].end_time = list_videos[i].end_time + audio2.duration_seconds

    i = i + 1


#endTime = Tuple[1]
endTime = list_videos[0].end_time
i = 0
while i < list_videos.__len__():
    print(list_videos[i].video_clip)
    print(list_videos[i].start_time)
    print(list_videos[i].end_time)
    if list_videos[i].end_time > endTime:
        endTime = list_videos[i].end_time
    i = i + 1


print(endTime)
audio_making(list_videos, endTime)
audio_main()
#Merge(list_videos,endTime,videoGap,lastCount)

mash = Mashup(list_videos,endTime,lastCount)
mash.merge("C:/Users/Nitin Malik/PycharmProjects/untitled5/mashup")
mash.mash("C:/Users/Nitin Malik/PycharmProjects/untitled5/mashup.mp3")

"""
video1 = VideoFileClip("video3.flv").subclip(0,10)
video1.write_videofile("vid_test1.mp4")

video2 = VideoFileClip("video3.flv").subclip(7.5,16)
video2.write_videofile("vid_test2.mp4")

video3 = VideoFileClip("video3.flv").subclip(13,18)
video3.write_videofile("vid_test3.mp4")

check_list = []
object1 = Video("vid_test1.mp4",0,10,1)
object2 = Video("vid_test2.mp4",7,16,1)
object3 = Video("vid_test3.mp4",13,18,1)
check_list.append(object1)
check_list.append(object2)
check_list.append(object3)
endTime = 18
audio_making(check_list, endTime)





count = 1
final_clip = None
for vid in videoList:
    print(vid.video_clip)
    print(vid.start_time)
    print(vid.end_time)
    clip = VideoFileClip(vid.video_clip).resize((1280,720))
    if count ==1:
        final_clip = clip
    else:
        final_clip = concatenate_videoclips([final_clip , clip])
    count = 0

final_clip.write_videofile("testing_concat.mp4")
"""