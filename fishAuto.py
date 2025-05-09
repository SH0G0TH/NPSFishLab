import pygame
import time
import csv
import threading
import heapq

mouthFile = "mouth_anchors.csv"
headFile = "head_anchors.csv"
tailFile = "tail_anchors.csv"
song = "anchors.wav"

headLock = threading.Lock()

def readData(file_path):
    data = []
    source = "mouth"
    if "head" == file_path[0:4]:
        source = "head"
    elif "tail" == file_path[0:4]:
        source = "tail"
    with open(file_path, 'r', newline='') as file:
        csv_reader=csv.reader(file)
        for row in csv_reader:

            data.append([float(row[0]),float(row[1])])
    for d in data:
        d.append(source)
    return data


def controlMouth(data):
    currentTime = 0
    for d in data:
        time.sleep(d[0]-currentTime)
        print("Mouth Open")
        time.sleep(d[1])
        currentTime = d[0]+d[1]
        print("Mouth Closed")

def controlHead(data):
    currentTime = 0
    for d in data:
        time.sleep(d[0]-currentTime)
        headLock.acquire()
        print("Head Up")
        time.sleep(d[1])
        currentTime = d[0]+d[1]
        headLock.release()
        print("Body Neutral")


def controlTail(data):
    currentTime = 0
    for d in data:
        time.sleep(d[0]-currentTime)
        if not headLock.locked():
            print("Tail Up")
        time.sleep(d[1])
        currentTime = d[0]+d[1]
        if not headLock.locked(): print("Body Neutral")

def songTime():
    pygame.mixer.music.play()

mouthData = readData(mouthFile)
headData = readData(headFile)
tailData = readData(tailFile)



mouthThread = threading.Thread(target=controlMouth(mouthData))
headThread = threading.Thread(target=controlHead(headData))
tailThread = threading.Thread(target=controlTail(tailData))
songThread = threading.Thread(target=songTime())

pygame.init()
pygame.mixer.music.load("anchors.wav")
songThread.start()
#mouthThread.start()
headThread.start()
#tailThread.start()

#mouthThread.join()
headThread.join()
#tailThread.join()





