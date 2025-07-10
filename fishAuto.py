import pygame
import time
import csv
import heapq
import os
import RPi.GPIO as GPIO
from adafruit_motorkit import MotorKit

GPIO.setmode(GPIO.BCM)
GPIO.setwarnings(False)
GPIO.setup(17, GPIO.OUT) #Mouth
GPIO.setup(27, GPIO.OUT) #Head
GPIO.setup(22, GPIO.OUT) #Tail

kit = MotorKit()
mouthMotor = kit.motor2
headTailMotor = kit.motor1

mouthFile = "mouth_anchors.csv"
headFile = "head_anchors.csv"
tailFile = "tail_anchors.csv"
song = "anchors.wav"


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


def longForm(inData):
    output = []
    for d in inData:
        if d[2] == "mouth":
            output.append([d[0],"Mouth Open", d[2]])
            output.append([d[0]+d[1], "Mouth Closed", d[2]])
        elif d[2] == "head":
            output.append([d[0], "Head Up", d[2]])
            if d[1] <= .15:
                d[1] = .2
            output.append([d[0] + d[1], "Head Down", d[2]])
        elif d[2] == "tail":
            if d[1] <= .15:
                d[1] = .2
            output.append([d[0], "Tail Up", d[2]])
            output.append([d[0] + d[1], "Tail Down", d[2]])
        else:
            print("Error Reading Data")
            return None
    return output


def combineData(mouth,head,tail):
    mouth = longForm(mouth)
    head = longForm(head)
    tail = longForm(tail)

    output = []
    headUp = False
    for d in heapq.merge(mouth,head,tail,key=lambda x:x[0]):
        print(d)
        if d[2] == "mouth":
            output.append(d)
        elif d[2] == "head":
            if d[1] == "Head Up":
                headUp = True
            else:
                headUp = False
            output.append(d)
        elif d[2] == "tail":
            if not headUp:
                output.append(d)
        else:
            print("The Data was incorrectly formatted")
            return None
    return output


def controlFish(data):
    currentTime = 0
    for d in data:
        if (d[0]-currentTime)-.15 > 0:
            time.sleep((d[0]-currentTime)-.15)
        if d[1] == "Mouth Open":
            time.sleep(.15)
            mouthMotor.throttle = 1
        elif d[1] == "Mouth Closed":
            time.sleep(.15)
            mouthMotor.throttle = 0
        elif d[1] == "Head Up":
            time.sleep(.15)
            headTailMotor.throttle = -1
        elif d[1] == "Tail Up":
            time.sleep(.15)
            headTailMotor.throttle = 1
        elif d[1] == "Head Down":
            headTailMotor.throttle = .8
            time.sleep(.15)
            headTailMotor.throttle = 0
        elif d[1] == "Tail Down":
            headTailMotor.throttle = -.8
            time.sleep(.15)
            headTailMotor.throttle = 0

        currentTime = d[0]



mouthData = readData(mouthFile)
headData = readData(headFile)
tailData = readData(tailFile)

fullSequence = combineData(mouthData, headData, tailData)

#pygame.init()
#pygame.mixer.music.load("anchors.wav")
#pygame.mixer.music.play()
os.system('cvlc anchors.wav &')
controlFish(fullSequence)
os.system('pkill vlc')





