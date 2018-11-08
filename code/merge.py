from moviepy.editor import VideoFileClip, concatenate_videoclips,concatenate_audioclips
import math
from random import randint
import copy


def Merge(videoList,endTime,gap,lastCount):
    endTime=gap*int(endTime/gap)
    videoMap={}
    queue=[]
    countMap={}
    for i in range(0,endTime,gap):
        videoMap[i]=[]
    index=0
    for vid in videoList:
        startKey=gap*math.ceil((vid.start_time)/gap)
        endKey=gap*math.floor((vid.end_time)/gap)
        for i in range(startKey,endKey,gap):
            videoMap[i].append(index)
        countMap[index]=0
        index=index+1
        print(startKey)
        print(endKey)
        print(vid.start_time)
        print(vid.end_time)
        print("---------------------------")
    print(videoMap)
    #Getting first video
    #***availList=videoMap[0].copy()
    availList = copy.deepcopy(videoMap[0])
    vidSelectIndex=availList[randint(0,len(availList)-1)]
    mergeVideo=VideoFileClip(videoList[vidSelectIndex].video_clip).subclip(0,gap).resize((1280,720))
    #mergeAudio=mergeVideo.audio
    queue.append(vidSelectIndex)
    countMap[vidSelectIndex]=countMap[vidSelectIndex]+1
    for time in range(gap,endTime,gap):
        print("time is ",str(time))
        if len(videoMap[time])!=0:
            #***availList=videoMap[time].copy()
            availList = copy.deepcopy(videoMap[time])
    #NEED TO BE CONVERTED IN BINARY SEARCH TO IMPROVE TIME EFFICIENCY
            inqueue=[]
            for i in queue:
                for j in availList:
                    if i==j:
                        inqueue.append(i)
                        break
            #print("availList is  ")
            #print(availList)
            #print("queue is")
            #print(queue)
            #print("Elements in queue and available list is")
            #print(inqueue)
            if len(inqueue)==len(availList):
                vidSelectIndex=inqueue[0]
                tempVideo=videoList[vidSelectIndex]
                tempClip=VideoFileClip(tempVideo.video_clip).subclip(time-tempVideo.start_time,time-tempVideo.start_time+gap).resize((1280,720))
                #tempAudio=tempClip.audio
                #mergeAudio=concatenate_audioclips([mergeAudio,tempAudio])
                mergeVideo = concatenate_videoclips([mergeVideo , tempClip])
                #tempClip.close()
                #tempAudio.close()
                queue.remove(vidSelectIndex)
                queue.append(vidSelectIndex)
                countMap[vidSelectIndex]=countMap[vidSelectIndex]+1
            else:
                for i in inqueue:
                    availList.remove(i)
                minOccur=countMap[availList[0]]
                for i in range(1,len(availList)):
                    if countMap[availList[i]]<minOccur:
                        minOccur=countMap[availList[i]]
                minOccurList=[]
                for i in availList:
                    if countMap[i]==minOccur:
                        minOccurList.append(i)
                vidSelectIndex=minOccurList[randint(0,len(minOccurList)-1)]
                tempVideo=videoList[vidSelectIndex]
                tempClip=VideoFileClip(tempVideo.video_clip).subclip(time-tempVideo.start_time,time-tempVideo.start_time+gap).resize((1280,720))
                #tempAudio=tempClip.audio
                #mergeAudio=concatenate_audioclips([mergeAudio,tempAudio])
                mergeVideo = concatenate_videoclips([mergeVideo , tempClip])
                #tempClip.close()
                #tempAudio.close()
                if len(queue)==lastCount:
                    del queue[0]
                    queue.append(vidSelectIndex)
                else:
                    queue.append(vidSelectIndex)
                countMap[vidSelectIndex]=countMap[vidSelectIndex]+1
    #tempAudio.close()
    #mergeVideo=mergeVideo.set_audio(mergeAudio)
    mergeVideo.write_videofile("mashup.mp4",audio=False)
    #return mergeVideo