import pygame
import time
import random

pygame.init()

white=(255,255,255)
red=(255,0,0)
green=(0,155,0)
black=(0,0,0)

displayWidth=1000
displayHeight=600  

gameDisplay=pygame.display.set_mode([displayWidth,displayHeight])
pygame.display.set_caption('Slither')
icon=pygame.image.load('Images/snakeIcon.jpg')
pygame.display.set_icon(icon)

img=pygame.image.load('Images/snakeHead.png')

appleImg=pygame.image.load('Images/apple.png')
raspberryImg=pygame.image.load('Images/raspberry.png')
pineappleImg=pygame.image.load('Images/pineapple.jpeg')
strawberryImg=pygame.image.load('Images/strawberry.jpg')
bananaImg=pygame.image.load('Images/banana.png')

noOfFruits=5

listOfFruits=[appleImg,raspberryImg,pineappleImg,strawberryImg,bananaImg]

mainSound=pygame.mixer.Sound('Sounds/main.wav')
boundaryHit=pygame.mixer.Sound('Sounds/boundaryHit.wav')
eatSound=pygame.mixer.Sound('Sounds/eatSound.wav')


clock = pygame.time.Clock()

blockSize=20

FPS=20

FruitThickness=30

direction='right'

smallFont=pygame.font.SysFont("comicsansms",25)
medFont=pygame.font.SysFont("comicsansms",50)
largeFont=pygame.font.SysFont("comicsansms",80)

def randFruit():
    r=random.randrange(0,noOfFruits)
    return listOfFruits[r]
    

def pause():

    paused=True
    messageToScreen("Paused",
                        black,
                        -100,
                        "large")
    messageToScreen("Press C to continue or Q to quit.",
                        black,
                        25)
    pygame.display.update()
    while paused:
        for event in pygame.event.get():
            if event.type==pygame.QUIT:
                pygame.quit()
                quit

            if event.type==pygame.KEYDOWN:
                if event.key==pygame.K_c:
                    paused=False
                elif event.key==pygame.K_q:
                    pygame.quit()
                    quit()
            
            pygame.display.update()
            clock.tick(5)
            
                       

def score(score):
    text=smallFont.render('Score: '+str(score), True,black)
    gameDisplay.blit(text,[0,0])

def randFruitGen():
    randFruitX=round(random.randrange(0,displayWidth-FruitThickness))#/10.0)*10.0
    randFruitY=round(random.randrange(0,displayHeight-FruitThickness))#/10.0)*10.0

    return randFruitX,randFruitY


def game_intro():
    intro=True

    while intro:

        for event in pygame.event.get():
            if event.type==pygame.QUIT:
                pygame.quit()
                quit()

            if event.type==pygame.KEYDOWN:
                if event.key==pygame.K_c:
                    intro=False
                if event.key==pygame.K_q:
                    pygame.quit()
                    quit()
        
        gameDisplay.fill(white)
        messageToScreen("Welcome to Slither",
                          green,
                          -100,
                          'large')
        messageToScreen("The objective of game is to eat red apples",
                          black,
                          -30)
        messageToScreen("The more apples you eat, the longer you get",
                          black,
                          10)
        messageToScreen("If you run into yourself, or the edges, you die!",
                          black,
                          50)
        messageToScreen("Press C to play or P to pause or Q to quit",
                          black,
                          180)
        pygame.display.update()
        clock.tick(15)
        


def snake(blockSize,snakeList):

    if direction=='right':
        head=pygame.transform.rotate(img,270)
    if direction=='left':
        head=pygame.transform.rotate(img,90)
    if direction=='up':
        head=img
    if direction=='down':
        head=pygame.transform.rotate(img,180)    
    
    gameDisplay.blit(head,(snakeList[-1][0],snakeList[-1][1]))
    
    for XnY in snakeList[:-1]:
        pygame.draw.rect(gameDisplay,green,[XnY[0],XnY[1],blockSize,blockSize])

def textObjects(text,color,size):
    if size=='small':
        textSurface=smallFont.render(text,True,color)
    elif size=='medium':
        textSurface=medFont.render(text,True,color)
    elif size=='large':
        textSurface=largeFont.render(text,True,color)
        
    return textSurface, textSurface.get_rect()

def messageToScreen(msg,color,y_displace=0,size="small"):
    textSurf,textRect=textObjects(msg,color,size)
    textRect.center=(displayWidth/2),(displayHeight/2)+y_displace
    gameDisplay.blit(textSurf,textRect)
    

def gameLoop():

    global direction
    direction='right'
    
    gameExit=False
    gameOver=False

    lead_x=displayWidth/2
    lead_y=displayHeight/2
    
    lead_x_change=10
    lead_y_change=0

    snakeList=[]
    
    snakeLength=1

    pygame.mixer.Sound.play(mainSound)

    randFruitX,randFruitY=randFruitGen()
    randomFruit=randFruit()
    
    while not gameExit:

        if gameOver==True:
            messageToScreen("Game over",
                              red,
                              y_displace=-50,
                              size='large')
            
            messageToScreen("Press C to play again or Q to quit",
                              black,
                              50,
                              size='medium')
            pygame.display.update()
            
        
        while gameOver==True:
             
            for event in pygame.event.get():
                if event.type==pygame.QUIT:
                    gameOver=False
                    gameExit=True
                elif event.type==pygame.KEYDOWN:
                    if event.key==pygame.K_q:
                        gameExit=True
                        gameOver=False
                    if event.key==pygame.K_c:
                        gameLoop()
            
        
        for event in pygame.event.get():
            if event.type==pygame.QUIT:
                gameExit=True
            if event.type==pygame.KEYDOWN:
                if event.key==pygame.K_LEFT:
                    lead_x_change=-blockSize
                    lead_y_change=0
                    direction='left'
                elif event.key==pygame.K_RIGHT:
                    lead_x_change=blockSize
                    lead_y_change=0
                    direction='right'
                elif event.key==pygame.K_UP:
                    lead_y_change=-blockSize
                    lead_x_change=0
                    direction='up'
                elif event.key==pygame.K_DOWN:
                    lead_y_change=blockSize
                    lead_x_change=0
                    direction='down'
                elif event.key==pygame.K_p:
                    pause()
                  
        if lead_x>=displayWidth or lead_x<=0 or lead_y>=displayHeight or lead_y<=0:
            pygame.mixer.Sound.play(boundaryHit)
            gameOver=True
            
        lead_x+=lead_x_change
        lead_y+=lead_y_change
        
        gameDisplay.fill(white)


        gameDisplay.blit(randomFruit,(randFruitX,randFruitY))
        
        snakeHead=[]
        snakeHead.append(lead_x)
        snakeHead.append(lead_y)
        snakeList.append(snakeHead)

        if len(snakeList) > snakeLength:
            del snakeList[0]

        for eachSegment in snakeList[:-1]:
            if eachSegment==snakeHead:
                pygame.mixer.Sound.play(boundaryHit)
                gameOver=True
        
        snake(blockSize,snakeList)

        score(snakeLength-1)
        
        pygame.display.update()

   
        if (lead_x>randFruitX and lead_x<randFruitX+FruitThickness) or (lead_x+blockSize>randFruitX and lead_x+blockSize<randFruitX+FruitThickness):
            if (lead_y>randFruitY and lead_y<randFruitY+FruitThickness) or (lead_y+blockSize>randFruitY and lead_y+blockSize<randFruitY+FruitThickness):
                pygame.mixer.Sound.play(eatSound)
                randFruitX,randFruitY=randFruitGen()
                randomFruit=randFruit()
                snakeLength+=1
             

        clock.tick(FPS)
        
    pygame.quit()
    
game_intro()
gameLoop()
   

