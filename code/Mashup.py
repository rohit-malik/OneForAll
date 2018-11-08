from moviepy.audio.io.AudioFileClip import AudioFileClip
from moviepy.editor import VideoFileClip, concatenate_videoclips,concatenate_audioclips
import math
import numpy as np
from random import randint
from decimal import Decimal
from bisect import bisect

class Mashup(object):
    """It creates mashup in three processes."""
#Constructor-----------------------------------
#Parameters-list of video Objects,end time of full mashup,size of queue to be maintained
    def __init__(self,list,time,size):
        self.videoMap={}
        self.queue=[]
        self.timeList=[]
        self.countMap={}
        self.videoList=list
        self.endTime=time
        self.queueSize=size
        self.finalClip=None
        t=0
        self.timeList.append(0);
        #Creating Timeline
        while(t<self.endTime):
            gap=0
            while(gap<1):
                gap=round(np.random.normal(2.3,1),2)
            final=gap+t
            final=round(final,2)
            if(t+gap>self.endTime):
                final=self.endTime
            self.videoMap[(t,final)]=[]
            t=final
            self.timeList.append(t)
        print(self.timeList)
        index=0
        #videomap contains list of tuples (video index in list ,duration (-1 if full duration),0 for duration from start,1 for duratio from end)
        #filling videomap, initialising countMap 
        for vid in self.videoList:
            start=vid.start_time
            end=vid.end_time
            startI=bisect(self.timeList,start)-1
            endI=bisect(self.timeList,end)-1
            if(endI+1==len(self.timeList)):
                endI=endI-1
            if(startI!=endI):
                if(self.timeList[startI]!=start):
                    self.videoMap[(self.timeList[startI],self.timeList[startI+1])].append((index,round(self.timeList[startI+1]-start,2),1))
                else:
                    self.videoMap[(self.timeList[startI],self.timeList[startI+1])].append((index,-1,-1))
                if(self.timeList[endI+1]!=end):
                    self.videoMap[(self.timeList[endI],self.timeList[endI+1])].append((index,round(end-self.timeList[endI],2),0))
                else:
                    self.videoMap[(self.timeList[endI],self.timeList[endI+1])].append((index,-1,-1))
                for timeI in range(startI+1,endI):
                    self.videoMap[(self.timeList[timeI],self.timeList[timeI+1])].append((index,-1,-1))
            self.countMap[index]=0
            index=index+1
#-----------------------------------------------------
#Method to handle queue
    def updateQueueAndCountMap(self,Index):
        isInqueue=0
        for i in self.queue:
            if(i==Index):
                isInqueue=1
                break
        if(isInqueue==1):
            self.queue.remove(Index)
            self.queue.append(Index)
        else:
            if len(self.queue)==self.queueSize:
                del self.queue[0]
                self.queue.append(Index)
            else:
                self.queue.append(Index)
        self.countMap[Index]=self.countMap[Index]+1
#Method to handle  vidos to concat
    def concatHandler(self,vidSelectIndex,start,end):
        if(self.numVideos==150):
            writePath=self.path + "/mashup"+str(self.numMashups)+".mp4"
            self.finalClip.write_videofile(writePath)
            self.finalClip.close
            self.finalClip=VideoFileClip(self.videoList[vidSelectIndex].video_clip).subclip(start,end).resize((1280,720))
            self.numVideos=0
            self.numMashups=self.numMashups+1
        else:
            tempClip=VideoFileClip(self.videoList[vidSelectIndex].video_clip).subclip(start,end).resize((1280,720))
            self.finalClip = concatenate_videoclips([self.finalClip , tempClip])
            self.numVideos=self.numVideos+1
#-----------------------------------------------------------------------
#This Function creates and save small mashups in the given folder path
#Input: path of folder where small mashups to be stored
    def merge(self,path):
        self.path=path
        self.numVideos=1
        self.numMashups=1
        #Getting first video------------------------------------------
        #-------------------------------------------------------------
        start=0
        end=self.timeList[1]
        fullVideoList=[]
        for vid in self.videoMap[(start,end)]:
            if vid[1]==-1:
                fullVideoList.append(vid[0])
        #if there is any full video
        if len(fullVideoList)!=0:
            #getting quality video
            vidSelectIndex=0
            qualityVideoList=[]
            for vidI in fullVideoList:
                if self.videoList[vidI].quality==1:
                    qualityVideoList.append(vidI)
            #If there is any good quality video
            if len(qualityVideoList)!=0:
                vidSelectIndex=qualityVideoList[randint(0,len(qualityVideoList)-1)]
            else:
                vidSelectIndex=fullVideoList[randint(0,len(fullVideoList)-1)]
            self.finalClip=VideoFileClip(self.videoList[vidSelectIndex].video_clip).subclip(0,end).resize((1280,720))
            self.updateQueueAndCountMap(vidSelectIndex)
        #if there is no full video
        else:
            fullList=self.videoMap[(start,end)].copy()
            leftVideos=[]
            rightVideos=[]
            for vid in fullList:
                if vid[2]==0:
                    leftVideos.append((vid[0],vid[1]))
                else:
                    rightVideos.append((vid[0],vid[1]))
            #If there is no video in right side 
            if len(rightVideos)==0:
                maxTime=0
                maxIndex=0
                for vidT in leftVideos:
                    if(vidT[1]>maxTime):
                        maxTime=vidT[1]
                        maxIndex=vidT[0]
                vidSelectIndex=maxIndex
                self.finalClip=VideoFileClip(self.videoList[vidSelectIndex].video_clip).resize((1280,720))
                self.updateQueueAndCountMap(vidSelectIndex)
            #If videos are on both side need to see if they overlap or not
            else:
                maxRightTime=0
                maxLeftTime=0
                maxLeftIndex=0
                maxRightIndex=0
                for vidT in leftVideos:
                    if(vidT[1]>maxLeftTime):
                        maxLeftTime=vidT[1]
                        maxLeftIndex=vidT[0]
                for vidT in rightVideos:
                    if(vidT[1]>maxRightTime):
                        maxRightTime=vidT[1]
                        maxRightIndex=vidT[0]
                #If these two don't overlap
                if(maxLeftTime+maxRightTime<end):
                    vidSelectIndex=maxLeftIndex
                    self.finalClip=VideoFileClip(self.videoList[vidSelectIndex].video_clip).resize((1280,720))
                    self.updateQueueAndCountMap(vidSelectIndex)
                #Merging video from right side
                    vidSelectIndex=maxRightIndex
                    tempClip=VideoFileClip(self.videoList[vidSelectIndex].video_clip).subclip(0,maxRightTime).resize((1280,720))
                    self.finalClip = concatenate_videoclips([self.finalClip , tempClip])
                    self.updateQueueAndCountMap(vidSelectIndex)
                #If these two overlap
                else:
                    vidSelectIndex=maxLeftIndex
                    self.finalClip=VideoFileClip(self.videoList[vidSelectIndex].video_clip).resize((1280,720))
                    self.updateQueueAndCountMap(vidSelectIndex)
                    #Adding video in the right side
                    vidSelectIndex=maxRightIndex
                    tempClip=VideoFileClip(self.videoList[vidSelectIndex].video_clip).subclip(start+maxLeftTime-self.videoList[vidSelectIndex].start_time,end-self.videoList[vidSelectIndex].start_time).resize((1280,720))
                    self.finalClip = concatenate_videoclips([self.finalClip , tempClip])
                    updateQueueAndCountMap(vidSelectIndex)
        #print("First Video is taken")
        #Video selecting and merging---------------------------------------------------------        
        for timeI in range(1,len(self.timeList)-1):
            start=self.timeList[timeI]
            end=self.timeList[timeI+1]
            gap=end-start
            fullVideoList=[]
            print("Concatination Time (%) is ",str(start*100/self.endTime))
            #If there are videos are available in given time gap
            if(len(self.videoMap[(start,end)])!=0):
                for vid in self.videoMap[(start,end)]:
                    if vid[1]==-1:
                        fullVideoList.append(vid[0])
                #If there are full length videos
                print(fullVideoList)
                if len(fullVideoList)!=0:
                    inqueue=[]
                    for i in self.queue:
                        for j in fullVideoList:
                            if i==j:
                                inqueue.append(i)
                                break
                    #If there all videos are recently added
                    if len(inqueue)==len(fullVideoList):
                        vidSelectIndex=inqueue[0]
                        self.concatHandler(vidSelectIndex,start-self.videoList[vidSelectIndex].start_time,end-self.videoList[vidSelectIndex].start_time)
                        self.updateQueueAndCountMap(vidSelectIndex)
                    #If there are vieos that are not recently added
                    else:
                        for i in inqueue:
                            fullVideoList.remove(i)
                        #getting list which are occured least 
                        minOccur=self.countMap[fullVideoList[0]]
                        #Getting the count of minimum occured video
                        for i in range(1,len(fullVideoList)):
                            if self.countMap[fullVideoList[i]]<minOccur:
                                minOccur=self.countMap[fullVideoList[i]]
                        minOccurList=[]
                        #Getting list of all videos that are least occured
                        for i in fullVideoList:
                            if self.countMap[i]==minOccur:
                                minOccurList.append(i)
                        #Getting videos of better quality
                        qualityVideoList=[]
                        for vidI in minOccurList:
                            if self.videoList[vidI].quality==1:
                                qualityVideoList.append(vidI)
                        if len(qualityVideoList)!=0:
                            vidSelectIndex=qualityVideoList[randint(0,len(qualityVideoList)-1)]
                        else:
                            vidSelectIndex=minOccurList[randint(0,len(minOccurList)-1)]
                        self.concatHandler(vidSelectIndex,start-self.videoList[vidSelectIndex].start_time,end-self.videoList[vidSelectIndex].start_time)
                        self.updateQueueAndCountMap(vidSelectIndex)
                else:
                    #If there is no full video available for this gap
                    fullList=self.videoMap[(start,end)].copy()
                    leftVideos=[]
                    rightVideos=[]
                    #Getting Left and Right videos
                    for vid in fullList:
                        if vid[2]==0:
                            leftVideos.append((vid[0],vid[1]))
                        else:
                            rightVideos.append((vid[0],vid[1]))
                    #If there is no video in right side 
                    if len(rightVideos)==0:
                        maxTime=0
                        maxIndex=0
                        for vidT in leftVideos:
                            if(vidT[1]>maxTime):
                                maxTime=vidT[1]
                                maxIndex=vidT[0]
                        vidSelectIndex=maxIndex
                        self.concatHandler(vidSelectIndex,start-self.videoList[vidSelectIndex],self.videoList[vidSelectIndex].end_time-self.videoList[vidSelectIndex].start_time)
                        self.updateQueueAndCountMap(vidSelectIndex)
                    #If there is no video in left side
                    elif len(leftVideos)==0:
                        maxTime=0
                        maxIndex=0
                        for vidT in rightVideos:
                            if(vidT[1]>maxTime):
                                maxTime=vidT[1]
                                maxIndex=vidT[0]
                        vidSelectIndex=maxIndex
                        self.concatHandler(vidSelectIndex,0,maxTime)
                        self.updateQueueAndCountMap(vidSelectIndex)
                    #If vidoes are in both side
                    else:
                        maxRightTime=0
                        maxLeftTime=0
                        maxLeftIndex=0
                        maxRightIndex=0
                        for vidT in leftVideos:
                            if(vidT[1]>maxLeftTime):
                                maxLeftTime=vidT[1]
                                maxLeftIndex=vidT[0]
                        for vidT in rightVideos:
                            if(vidT[1]>maxRightTime):
                                maxRightTime=vidT[1]
                                maxRightIndex=vidT[0]
                        vidSelectIndex=maxLeftIndex
                        self.concatHandler(vidSelectIndex,start-self.videoList[vidSelectIndex].start_time,self.videoList[vidSelectIndex].end_time-self.videoList[vidSelectIndex].start_time)
                        self.updateQueueAndCountMap(vidSelectIndex)
                        vidSelectIndex=maxRightIndex
                        #If both videos do not overlap
                        if(maxLeftTime+maxRightTime<gap):
                            self.concatHandler(vidSelectIndex,0,maxRightTime)
                            self.updateQueueAndCountMap(vidSelectIndex)
                        else:
                            self.concatHandler(vidSelectIndex,start+maxLeftTime-self.videoList[vidSelectIndex].start_time,end-self.videoList[vidSelectIndex].start_time)
                            self.updateQueueAndCountMap(vidSelectIndex)
        writePath=self.path + "/mashup"+str(self.numMashups)+".mp4"
        self.finalClip.write_videofile(writePath)
        self.finalClip.close
        print("Number of parts of mashups :",self.numMashups)
    def mash(self,audioPath):
        readPath=self.path + "/mashup1"+".mp4"
        mashup=VideoFileClip(readPath)
        if(self.numMashups==1):
            mashup=mashup.set_audio(AudioFileClip(audioPath))
            mashup.write_videofile(self.path+"/mashup.mp4")
        else:
            for i in range(2,self.numMashups+1):
                readPath=self.path + "/mashup"+str(i)+".mp4"
                tempClip=VideoFileClip(readPath)
                mashup=concatenate_videoclips([mashup,tempClip])
            mashup=mashup.set_audio(AudioFileClip(audioPath))
            mashup.write_videofile(self.path+"/mashup.mp4")
            
