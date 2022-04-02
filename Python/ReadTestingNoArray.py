import math
import serial
import sys
import os
import numpy
import platform

if(platform.system()=='Windows'):
  PWDSERAL = "COM4"
elif(platform.system()=='Linux'):
  PWDSERAL = '/dev/ttyACM0'
else:
  print("But why?")
  exit()

lanes = 6

timeFinal = [0,0,0,0,0,0,0]
timeStop = [0,0,0,0,0,0,0]

prehall = 0

inTime=[]
binaryLane=[]
OverFlow = 4294967296
startTime = 0

timeSize = 100000 # per second

timeThr = timeSize//10 # 1/10 of a second
HallTimeThr = timeSize//2 # 1/4 of a second

pinoffset = 3

def get_digit(number, n):
    return number // 10**n % 10

# serial setup
ser = serial.Serial(PWDSERAL, 115200)
data = ser.readline().decode()
print(data)
while 1:
  data = ser.readline().decode()
  splitline = data.split(',')
  inTime = int("0x"+splitline[0],16)
  lane = int("0x"+splitline[1],16)
  #time
  if(inTime<=startTime):
    inTime = abs(startTime-OverFlow)+inTime
  #lane
  binaryLane = format(lane,'b')
  print(f'{inTime : 010d} | {binaryLane} | {timeFinal} | {timeStop}')
  for i in range(0,lanes):
    if(binaryLane[i+pinoffset]=="0" and (timeStop[i]==0)):
      timeFinal[i] = inTime-startTime
    elif ((timeFinal[i]!=0) and (binaryLane[i+pinoffset]=="1") and (inTime-timeFinal[i] >= timeThr) and (timeStop[i]==0)):
      print(f"AAAAAAAAAAA{i}")
      timeStop[i]=1
  # need to set if electro magnet is a 1 or a 0 to set for rising or falling
  #electro magnet is pin 7 starting from 0 so check 2 bit from left
  if((binaryLane[1]=="0") and (binaryLane[1]!=prehall)):
    timeFinal[6] = inTime
    print("START!!!")
  elif((binaryLane[1]=="1") and (binaryLane[1]!=prehall) and (inTime-timeFinal[6] >= HallTimeThr)):
    startTime = timeFinal[6]
    timeFinal = [0,0,0,0,0,0,startTime]
    timeStop = [0,0,0,0,0,0,0]
    print(f'{inTime : 010d} | {binaryLane} | {timeFinal} | {timeStop}')
    print("START!!!2")

  prehall = binaryLane[1]
  
  # print(timeFinal)


time/=timeSize #making the time in second insted of nano seconds

# bits = int(max(8, math.log(num, 2)+1))
# out = [1 if num & (1 << (bits-1-n)) else 0 for n in range(bits)]
