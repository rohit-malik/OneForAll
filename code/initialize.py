from moviepy.editor import VideoFileClip, concatenate_videoclips
from datetime import datetime
from video import Video
import re


def initialize():
    videoList = []
    endTime = 0
    file = open("testfile.txt")
    line = file.readline()

    min_start = 0
    count = 1
    while line:
        l = re.split(r'\t+', line)
        modified_date = l[0].strip()
        date = datetime.strptime(modified_date, "%m/%d/%Y %H:%M:%S")
        end = (date - datetime(1970, 1, 1)).total_seconds()
        li = re.split(r'/', l[1])
        length = li.__len__()
        name = li[length - 1].strip()
        clip = VideoFileClip(name)
        start = end - clip.duration
        if count == 1:
            min_start = start
        if start < min_start:
            min_start = start
        count = 0
        line = file.readline()
        clip.close()

    file.close()

    file = open("testfile.txt")
    line = file.readline()

    while line:
        l = re.split(r'\t+',line)
        modified_date = l[0].strip()
        date = datetime.strptime(modified_date, "%m/%d/%Y %H:%M:%S")
        end = (date - datetime(1970, 1, 1)).total_seconds()
        li = re.split(r'/', l[1])
        length = li.__len__()
        name = li[length-1].strip()
        clip = VideoFileClip(name)
        start = end - clip.duration
        rel_start = start - min_start
        rel_end = rel_start + clip.duration
        if rel_end>=endTime:
            endTime=rel_end
        obj = Video(name, rel_start, rel_end,1)
        videoList.append(obj)
        line = file.readline()
        clip.close()

    file.close()
    return [videoList, endTime]
