import time
import serial
import platform
import os
import pygame
import threading
from pygame.locals import *

#rs485 arduino to arduino
#https://create.arduino.cc/projecthub/maurizfa-13216008-arthur-jogy-13216037-agha-maretha-13216095/modbus-rs-485-using-arduino-c055b5

#arduino to raspberry pi gpio serial
#https://roboticsbackend.com/raspberry-pi-arduino-serial-communication/

#raspberry pi serial on gpio https://pimylifeup.com/raspberry-pi-serial/

print("start")
ColumOneText = "Lane Number"
ColumTwoText = "Time"
ColumThreeText = "Position"

RED = [255,0,0]
GREEN = [0,255,0]
BLUE = [0,100,255]
YELLOW = [220,220,50]

white = (255, 255, 255)
green = (0, 255, 0)
blue = (0, 0, 128)
backgroundColor = (20,20,20)

#words
WinNumbers = ["FIRST","SECOND","THIRD","FOURTH","FIFTH","SIXTH"]
WinColors = {"FIRST": [201, 176, 55],"SECOND":[215, 215, 215],"THIRD":[173, 138, 86],"FOURTH":[150,150,150],"FIFTH":[100,100,100],"SIXTH":[50,50,50],"":[0,0,0]}

LaneW = ["ONE","TWO","THREE","FOUR","FIVE","SIX"]
LaneColor = [RED,BLUE,GREEN,YELLOW,BLUE,GREEN]

#Seraial Setup

if(platform.system()=='Windows'):
  PWDSERAL = "COM4"
elif(platform.system()=='Linux'):
  PWDSERAL = '/dev/ttyACM0'
else:
  print("But why?")
  exit()

# pygame setup

lanes = 4 

if(lanes<=4):
  lanOffset = 1
else:
  lanOffset = 0
print(lanOffset)


Y = 720
X = Y*16//9
FPSBool = False
FrameRate = 60
Border = 5

RightSideStart = 0

PYGAME_BLEND_ALPHA_SDL2 = 1

pygame.init()

pygame.event.set_allowed([QUIT, KEYDOWN])

flags = pygame.RESIZABLE | pygame.DOUBLEBUF

clock = pygame.time.Clock()
keys = pygame.key.get_pressed()
if(os.getlogin()=='pi'):
  pygame.mouse.set_visible(False) # Hide cursor here
  X=pygame.display.Info().current_w
  Y=pygame.display.Info().current_h
  flags = pygame.FULLSCREEN | pygame.DOUBLEBUF


startTime = 0

TIME=[0,0,0,0,0,0,0]
POSITION=["","","","","",""]

start = int(time.time()*1000)

def UIsetup(Background,extralanes,fontMed,x,y):
  Background.fill(backgroundColor)
  Tital = pygame.font.Font(os.path.join('LiberationMono-Regular.ttf'),int(60*y/720))
  fontMed = pygame.font.Font(os.path.join('LiberationMono-Regular.ttf'),int(80*y/720))
  #if(lanes==4):
  # words
  xoffset = 25
  timeWidth = 0
  if(extralanes>0):
    #lane number 
    lanetext = Tital.render(ColumOneText, True, white)
    lanetextpos = lanetext.get_rect()
    lanetextpos.centery = (y/((lanes+extralanes)*2))+10
    lanetextpos.x = xoffset
    Background.blit(lanetext,lanetextpos)
    
    
    # time colom 
    timetext = Tital.render(ColumTwoText, True, white)
    timetextpos = timetext.get_rect()
    timetextpos.centery = (y/((lanes+extralanes)*2))+10
    timetextpos.centerx = x/2-timetextpos.w/4
    Background.blit(timetext,timetextpos)
    
    
    # time Position 
    Positiontext = Tital.render(ColumThreeText, True, white)
    Positiontextpos = Positiontext.get_rect()
    Positiontextpos.centery = (y/((lanes+extralanes)*2))+10
    Positiontextpos.x = x-Positiontextpos.w-xoffset*3
    Background.blit(Positiontext,Positiontextpos)
    pygame.draw.line(Background,white,(5,5),(5,y-6),2)
    pygame.draw.line(Background,white,(x-6,5),(x-6,y-6),2)
    pygame.draw.line(Background,white,(timetextpos.x-timetextpos.w/2,5),(timetextpos.x-timetextpos.w/2,y-6),2)
    pygame.draw.line(Background,white,(timetextpos.x-timetextpos.w/2-10,5),(timetextpos.x-timetextpos.w/2-10,y-6),2)
    pygame.draw.line(Background,white,(timetextpos.x+(timetextpos.w*2),5),(timetextpos.x+(timetextpos.w*2),y-6),2)
    pygame.draw.line(Background,white,(timetextpos.x+(timetextpos.w*2)+10,5),(timetextpos.x+(timetextpos.w*2)+10,y-6),2)
    RightSideStart=timetextpos.x+(timetextpos.w*2)+10
    



  for i in range(0,lanes):
    text = fontMed.render(LaneW[i], True, LaneColor[i])
    textpos = text.get_rect()
    textpos.centery = (y/((lanes+extralanes)*2))*(((i+extralanes)*2)+1)+10
    textpos.x = 25
    Background.blit(text,textpos)
    #print(LaneW[i],textpos)


  # boxes
  for i in range(0,lanes+extralanes):
    box = pygame.Rect(5,((y)/(lanes+extralanes)*i)+5,x-5*2,(y-(5*(lanes+extralanes+5)))/(lanes+extralanes))
    pygame.draw.rect(Background,white,box,2)
    #pygame.draw.rect(Background,white,pygame.Rect(5,(y)/(lanes+extralanes)*i+5,x-5*2,(y-40)/(lanes+extralanes)),5)
  print(f"Call {x}x{y}")

  pygame.Surface.convert(Background)
  return RightSideStart

def mainLoop(lock):
  done = 0
  preInTime = 0
  Window = pygame.display.set_mode((X, Y),flags,depth=8)
  Background = pygame.surface.Surface((X, Y),flags)
  Window.set_alpha(None)
  Background.set_alpha(None)
  x, y = Window.get_size()
  
  # global TIME
  # global POSITION

  font8 = pygame.font.Font(os.path.join('LiberationMono-Regular.ttf'),8)
  fontLarge = pygame.font.Font(os.path.join('LiberationMono-Regular.ttf'),int(120*y/720))
  fontMed = pygame.font.Font(os.path.join('LiberationMono-Regular.ttf'),int(80*y/720))
  FontFPS = pygame.font.Font(os.path.join('LiberationMono-Regular.ttf'),int(20*y/720))

  extralanes = 1

  
  RightSideStart=UIsetup(Background,extralanes,fontMed,x,y)

  pygame.display.set_caption('AWANA Timer')
  while not done:
    for event in pygame.event.get():
      if event.type == pygame.KEYDOWN:
        keys = pygame.key.get_pressed()
        if (event.type == pygame.QUIT) or keys[pygame.K_ESCAPE] or keys[pygame.K_q]:
           done = 1
      elif event.type == VIDEORESIZE:
        # print("UPDATE")
        x, y = event.size
        Background = pygame.surface.Surface((x, y),pygame.RESIZABLE)
        RightSideStart=UIsetup(Background,extralanes,fontMed,x,y)
        
        fontLarge = pygame.font.Font(os.path.join('LiberationMono-Regular.ttf'),int(110*y/720))
        fontMed = pygame.font.Font(os.path.join('LiberationMono-Regular.ttf'),int(80*y/720))
        FontFPS = pygame.font.Font(os.path.join('LiberationMono-Regular.ttf'),int(20*y/720))

    #serail stuff


    # pygame stuff
    # pygame.display.update()
    Window.blit(Background,(0,0))
    timestat = ((int(time.time()*1000)-start)/1000)-TIME[6]
    lock.acquire()
    res = sorted(range(len(TIME)))
    for i in range(lanOffset,lanes+lanOffset):
      if(TIME[i]!=0):
        text = fontMed.render(f'{TIME[i]:0.3f}', True, white)
        text2 = fontLarge.render(POSITION[i],True,WinColors[POSITION[i]])
        text2Rect = text2.get_rect()
        text2Rect.x =RightSideStart+7
        text2Rect.centery = (y/((lanes+extralanes)*2))*((((i-lanOffset)+extralanes)*2)+1)+7
        Window.blit(text2,text2Rect)
      else:
       text = fontMed.render(f'{timestat:0.2f}', True, white)
      textRect = text.get_rect()
      textRect.centerx = x/2
      textRect.centery = (y/((lanes+extralanes)*2))*((((i-lanOffset)+extralanes)*2)+1)+7
      Window.blit(text,textRect)

      

      # pygame.display.update(textRect)
    lock.release()
    

    if FPSBool:
      fpsCount = FontFPS.render(f'{clock.get_fps():.1f}',True,green)
      fpsRect = fpsCount.get_rect()
      fpsRect.x = 20
      fpsRect.y = 20
      Window.blit(fpsCount,fpsRect)
      pygame.draw.rect(Window,green,fpsRect,1)
      # pygame.display.update(fpsRect)
    else:
      print(f'{clock.get_fps():.1f}',end="\r")
    pygame.display.flip()
    clock.tick_busy_loop(FrameRate)

def ReadSerial(lock,mainTr):
  #varis
  binaryLane=0
  timeFinal = [0,0,0,0,0,0,0]
  timeStop = [0,0,0,0,0,0,0]
  OverFlow = 4294967296
  timeSize = 1000000 # per second
  timeThr = timeSize//10 # 1/10 of a second
  HallTimeThr = timeSize//20 # 1/20 of a second
  pinoffset = 3
  prehall = 0

  global TIME
  global POSITION

  positionLocal = ["","","","","",""]

  # serial setup
  ser = serial.Serial(PWDSERAL, 115200)
  data = ser.readline().decode()
  timeFinal[6] = int("0x"+data.split(',')[0],16)
  print(data)
  while mainTr.is_alive():
    data = ser.readline().decode()
    splitline = data.split(',')
    inTime = int("0x"+splitline[0],16)
    lane = int("0x"+splitline[1],16)
    #time
    if(inTime<=timeFinal[6]):
      inTime = abs(timeFinal[6]-OverFlow)+inTime
    #lane
    binaryLane = format(lane,'b')
    for i in range(lanOffset,lanes+lanOffset):
      if(binaryLane[i+pinoffset]=="0" and (timeStop[i]==0)):
        timeFinal[i] = inTime-timeFinal[6]
        lock.acquire()
        TIME[i] = timeFinal[i]/timeSize
        lock.release()
        timeStop[i]=1
      # if ((timeFinal[i]!=0) and (binaryLane[i+pinoffset]=="1") and (inTime-timeFinal[i] >= timeThr) and (timeStop[i]==0)):
        
    # need to set if electro magnet is a 1 or a 0 to set for rising or falling
    #electro magnet is pin 7 starting from 0 so check 2 bit from left
    if((binaryLane[1]=="0") and (binaryLane[1]!=prehall)):
      timeFinal[6] = inTime
      lock.acquire()
      TIME = [0,0,0,0,0,0,timeFinal[6]/timeSize]
      POSITION = ["","","","","",""]
      lock.release()
      timeFinal = [0,0,0,0,0,0,timeFinal[6]]
      timeStop = [0,0,0,0,0,0,0]

      positionLocal = ["","","","","",""]
      print(f'{inTime : 010d} | {binaryLane} | {timeFinal} | {timeStop} | {positionLocal}')
      print("START!!!-")
    # elif((binaryLane[1]=="1") and (binaryLane[1]!=prehall) and (inTime-timeFinal[6] >= HallTimeThr)):


      
      print("START!!!2")
    for i in range(lanOffset,lanes+lanOffset):
      if(timeStop[i]!=0 and positionLocal[i]==""):
        positionLocal[i] = WinNumbers[sum(timeStop)-1]
        lock.acquire()
        POSITION[i]=positionLocal[i]
        lock.release()
      
    print(f'{inTime : 010d} | {binaryLane} | {timeFinal} | {timeStop} | {positionLocal}')
    prehall = binaryLane[1]

lock = threading.Lock()

mainTr = threading.Thread(target=mainLoop,args=(lock,))
SerialTr = threading.Thread(target=ReadSerial,args=(lock,mainTr))

mainTr.start()
SerialTr.start()

mainTr.join()
SerialTr.join()


print("\nEnd :)")