import os
os.environ['PYGAME_HIDE_SUPPORT_PROMPT'] = "hide"
import statistics
import pygame
import math
import random
#serial for the arduino comunication
# Doc https://pyserial.readthedocs.io/en/latest/pyserial_api.html
import serial
print("started")

# comm set up 
port = 'COM4'	# nano every is set to COM4 UNO is set to COM3
baud = 19200		# set arduino to same baud rate

Com = serial.Serial(port, baud)

#locating lines
LineStart1 = (75,560)		#bottom left
LineStart2 = (350,560)		#bottom Right
LineStart3 = (560,350)		#Right wall bottom
LineStart4 = (560,75)		#Right wall Top


#,[LineStart2[0],LineStart2[1]],[LineStart3[0],LineStart3[1]],[LineStart4[0],LineStart4[1]]



FPS = 0
#start pygame
pygame.init()
pygame.font.init()

font = pygame.font.SysFont("Arial", 18)

#color for pointing lines
LineColor = [0,200,200]
AngleColor = [250,250,0]





BackgroundColor = [50,50,50] # set the background color to a gray
clock = pygame.time.Clock() 

# var set up for vars in statments 
done = False
keys = pygame.key.get_pressed()
MouseButton = pygame.mouse.get_pressed()
MousePos = (150,150)
Random = False # if the angles are being randomized by adding or suptracting 1 degree 

#set the screan up 
screen = pygame.display.set_mode((600, 600)) # set the windo size
screen.fill(BackgroundColor)


#set up background with lines
Background = pygame.surface.Surface((600,600))
BackLineColor = [200,200,200]
pygame.draw.lines(Background, BackLineColor, False, [(25,560),(400,560),(560,400),(560,25)],3) # draw walls
pygame.draw.lines(Background, BackLineColor, False, [(25,275),(175,275),(275,175),(275,25)],2) # draw stage

# set up Distance because it does not need to be caulated evry loop

def Distance(LA,LB):
	Dis = math.sqrt((LA[0]-LB[0])**2+(LA[1]-LB[1])**2)
	return(Dis)
	
Dis1 = Distance(LineStart1,LineStart2)
Dis2 = Distance(LineStart1,LineStart3)
Dis3 = Distance(LineStart1,LineStart4)
Dis4 = Distance(LineStart2,LineStart3)
Dis5 = Distance(LineStart2,LineStart4)
Dis6 = Distance(LineStart3,LineStart4)
#print(Dis1,Dis2,Dis3,Dis4,Dis5,Dis6)

#X and Y set up 
'''
XY1 = (0,0) 
XY2 = (0,0)
XY3 = (0,0)
XY4 = (0,0)
XY5 = (0,0)
XY6 = (0,0)
XY7 = (0,0)
XY8 = (0,0)
XY9 = (0,0)
XY10 = (0,0)
XY11 = (0,0)
XY12 = (0,0)
'''
def LineAngle(MousePos):
	#lines for viewing angle of receviors 
	pygame.draw.line(screen, LineColor, LineStart1, MousePos, 2) #line for receiver 1-4
	pygame.draw.line(screen, LineColor, LineStart2, MousePos, 2) 
	pygame.draw.line(screen, LineColor, LineStart3, MousePos, 2)
	pygame.draw.line(screen, LineColor, LineStart4, MousePos, 2)
	#pygame.draw.line(screen, [255,0,0], (487,487), MousePos, 2) # camera
	
	#finding where the mouse is based on where the line starts
	PosFor1 = (LineStart1[0]-MousePos[0],LineStart1[1]-MousePos[1])
	PosFor2 = (LineStart2[0]-MousePos[0],LineStart2[1]-MousePos[1])
	PosFor3 = (LineStart3[0]-MousePos[0],LineStart3[1]-MousePos[1])
	PosFor4 = (LineStart4[0]-MousePos[0],LineStart4[1]-MousePos[1])
	# finding the angle of the lines
	Angle1 = math.degrees(math.atan2(PosFor1[1],PosFor1[0]))
	Angle2 = math.degrees(math.atan2(PosFor2[1],PosFor2[0]))
	Angle3 = math.degrees(math.atan2(PosFor3[1],PosFor3[0]))
	Angle4 = math.degrees(math.atan2(PosFor4[1],PosFor4[0]))
	
	#adding 90 degrees to 3 and 4 to line up angles with the walls
	#if Angle3 >
	Angle3-=90
	Angle4-=90
	
	# add 180 to chang the swing from -180 to 180 to 0 to 360
	Angle1=abs(Angle1-180)
	Angle2=abs(Angle2-180) 
	Angle3*=-1
	Angle4*=-1
	
	if Angle3 < 0:
		Angle3+=360
	if Angle4 < 0:
		Angle4+=360
	# set -0.0 to 0.0 because of wheared math
	if round(Angle3,1) == -0.0:
		Angle3 *= -1
	if round(Angle4,1) == -0.0:
		Angle4 *= -1
	
	
	return Angle1, Angle2, Angle3, Angle4

def update_fps(FPS):
	fps = str(int(FPS))
	fps_text = font.render(fps, 1, (0,200,0))
	return fps_text
	
def Rand(A1, A2, A3, A4):
	A1 = A1+round(random.randrange(-75,75,5)*0.01,2)
	A2 = A2+round(random.randrange(-75,75,5)*0.01,2)
	A3 = A3+round(random.randrange(-75,75,5)*0.01,2)
	A4 = A4+round(random.randrange(-75,75,5)*0.01,2)
	return A1, A2, A3, A4

def DesplayAngle(Angle1, Angle2, Angle3, Angle4):
	Angle1T=str(float(round(Angle1,1)))
	Angle2T=str(float(round(Angle2,1)))
	Angle3T=str(float(round(Angle3,1)))
	Angle4T=str(float(round(Angle4,1)))
	Angle = font.render(Angle1T, 1, AngleColor)
	screen.blit(Angle, LineStart1)
	Angle = font.render(Angle2T, 1, AngleColor)
	screen.blit(Angle, LineStart2)
	Angle = font.render(Angle3T, 1, AngleColor)
	screen.blit(Angle, (LineStart3[0]+3,LineStart3[1]))
	Angle = font.render(Angle4T, 1, AngleColor)
	screen.blit(Angle, (LineStart4[0]+3,LineStart4[1]))
	return Angle
	
	
def MathFile(LineStart1,LineStart2,LineStart3,LineStart4,Angle1,Angle2,Angle3,Angle4,Dis1,Dis2,Dis3,Dis4,Dis5,Dis6):
	
	RecAngle66 = -math.degrees(math.atan2((LineStart1[0]-LineStart3[0]),(LineStart1[1]-LineStart3[1])))
	RecAngle23 = 90-RecAngle66
	
	XY1,XY2=Math(Angle1,Angle2,Dis1,LineStart1,LineStart2,0,180,0,0)
	XY3,XY4=Math(Angle1,Angle3,Dis2,LineStart1,LineStart3,RecAngle23,-RecAngle66+180,0,90)
	XY5,XY6=Math(Angle1,Angle4,Dis3,LineStart1,LineStart4,45,45+90,0,90)
	XY7,XY8=Math(Angle2,Angle3,Dis4,LineStart2,LineStart3,45,45+90,0,90)
	XY9,XY10=Math(Angle2,Angle4,Dis5,LineStart2,LineStart4,RecAngle66,-RecAngle23+180,0,90)
	XY11,XY12=Math(Angle3,Angle4,Dis6,LineStart3,LineStart4,0,180,90,90)
	

			# to fix this aline all the angles together the right side is offset 90 degrease 

	
																# mostly good is at the line between the points it reverses 
	screen.set_at((int(XY1[0]),int(XY1[1])),[255,255,255]) 	#mostly Good
	screen.set_at((int(XY2[0]),int(XY2[1])),[255,255,255])		# Bad
	screen.set_at((int(XY3[0]),int(XY3[1])),[255,255,255]) 	#mostly Good
	screen.set_at((int(XY4[0]),int(XY4[1])),[255,255,255])		# Bad
	screen.set_at((int(XY5[0]),int(XY5[1])),[255,255,255])		#mostly Good
	screen.set_at((int(XY6[0]),int(XY6[1])),[255,255,255])		# bad
	screen.set_at((int(XY7[0]),int(XY7[1])),[255,255,255])		#mostly good
	screen.set_at((int(XY8[0]),int(XY8[1])),[255,255,255])		# bad
	screen.set_at((int(XY9[0]),int(XY9[1])),[255,255,255])		#mostly good
	screen.set_at((int(XY10[0]),int(XY10[1])),[255,255,255])	# bad
	screen.set_at((int(XY11[0]),int(XY11[1])),[255,255,255])	# bad
	screen.set_at((int(XY12[0]),int(XY12[1])),[255,255,255])	# bad 
	
	
	#making arrays so they can be sorted  
	ArrayX = [XY1[0],XY2[0],XY3[0],XY4[0],XY5[0],XY6[0],XY7[0],XY8[0],XY9[0],XY10[0],XY11[0],XY12[0]]		
	ArrayY = [XY1[1],XY2[1],XY3[1],XY4[1],XY5[1],XY6[1],XY7[1],XY8[1],XY9[1],XY10[1],XY11[1],XY12[1]]
	
	
	#sorting the arrays so the middle can be averageed because it has 12 points
	ArrayX.sort()
	ArrayY.sort()
	
	#print(ArrayX,ArrayY)
	
	#averageing the center numbers
	PasterX,PasterY=StandardDev(ArrayX,ArrayY)
	
	pygame.draw.circle(screen,[0,255,0],(int(PasterX),int(PasterY)),10,1)
	
	
	
	
	
	
	
	
	# #,XY3,XY4,XY5,XY6,XY7,XY8,XY9,XY10,XY11,XY12
	'''print(0,			# print the angles being used for finding the angles from recever to recever to transmitter
	      math.degrees(math.atan(((LineStart1[0]-LineStart3[0])/(LineStart1[1]-LineStart3[1])))),
	      math.degrees(math.atan(((LineStart1[0]-LineStart4[0])/(LineStart1[1]-LineStart4[1])))),
	      math.degrees(math.atan(((LineStart2[0]-LineStart3[0])/(LineStart2[1]-LineStart3[1])))),
	      math.degrees(math.atan(((LineStart2[0]-LineStart4[0])/(LineStart2[1]-LineStart4[1])))),
	      270)'''

def StandardDev(ArrayX,ArrayY):
	MidX = (ArrayX[5] + ArrayX[6])/2
	MidY = (ArrayY[5] + ArrayY[6])/2
	return(MidX,MidY)




def Math(A1,A2,Dis,LA,LB,AA,AB,Add1,Add2):
	#making the angles based on the incoming angle form the other point
	MA1=A1
	MA2=A2
	A1-=AA
	A2-=AB
	A1=abs(A1)
	A2=abs(A2)
	A3 = 180-A1-A2
	
	S2=(Dis/math.sin(math.radians(A3)))*math.sin(math.radians(A1)) 		# finding side 2 the side connected to point 2
	S1=(Dis/math.sin(math.radians(A3)))*math.sin(math.radians(A2)) 		# finding side 1 the side connected to point 1
	
	#angles and vecters to cordent system 
	X1=math.cos(math.radians(MA1+Add1))*S1
	Y1=math.sin(math.radians(MA1+Add1))*S1
	X2=math.cos(math.radians(MA2+Add2))*(S2)		#second angles are not telling the same point
	Y2=math.sin(math.radians(MA2+Add2))*(S2)		#
	
	#translating it to global cordients 
	X1+=LA[0]
	Y1=abs(Y1-LA[1])
	X2+=LB[0]
	Y2=abs(Y2-LB[1])
	#print(X1,Y1)
	#print(X2,Y2)
	
	
	XY1 = X1,Y1
	XY2 = X2,Y2
	return(XY1,XY2)


while not done:
	for event in pygame.event.get():
		if event.type == pygame.MOUSEBUTTONDOWN:
			MouseButton = pygame.mouse.get_pressed()[0]
		elif pygame.MOUSEBUTTONUP:
			MouseButton = pygame.mouse.get_pressed()[0]
		if event.type == pygame.KEYDOWN:
			keys = pygame.key.get_pressed()
			if event.type == keys[pygame.K_r] or keys[pygame.K_w]:
				if Random == False:
					Random = True
					print("on")
				elif Random == True:
					Random = False
					print("off")
		if event.type == pygame.QUIT or keys[pygame.K_ESCAPE] or keys[pygame.K_q]:
			done = True
			print("Done")
	
	#screen.fill(BackgroundColor)	#clear skrean with gray
	screen.blit(Background, (0,0))
	
	if MouseButton == (1):
		MousePos = pygame.mouse.get_pos()
	
	Angle1, Angle2, Angle3, Angle4 = LineAngle(MousePos)
	
	if Random == True:
		Angle1, Angle2, Angle3, Angle4 = Rand(Angle1, Angle2, Angle3, Angle4)
	
	
	#angle side angle solver >> https://www.mathsisfun.com/algebra/trig-solving-asa-triangles.html
	MathFile(LineStart1,LineStart2,LineStart3,LineStart4,Angle1, Angle2, Angle3, Angle4,Dis1,Dis2,Dis3,Dis4,Dis5,Dis6)
	

	
	
	#print angles
	#print('Angle1:',round(Angle1,2),'	Angle2:',round(Angle2,2),'	Angle3:',round(Angle3,2),'	Angle4:',round(Angle4,2),'			', sep = '', end='\r')
	# desplay angeles
	Angle = DesplayAngle(Angle1, Angle2, Angle3, Angle4)
	
	
	
	# fps show and limet fps 
	FPS = clock.get_fps()
	screen.blit(update_fps(FPS), (10,0))
	clock.tick(60)
	#must be last for fps to work
	pygame.display.update()