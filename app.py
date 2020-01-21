#
#Change the increase Speed to change speed of ball
#If changing increase speed, and want to use AI, change playerTwo.y as well
#If changing HSV for different color, change the hsv of lower and upper range
#
#Everything is being built like a gui, layer over layer
#displaySurf = Main window
#
#orange lego piece
#lower_range = np.array([7,130,130])
#upper_range = np.array([50,255,255])
import pygame, sys
from pygame.locals import *
#camera manipulation
import numpy as np
import cv2
#random
import random
#sleep
from time import sleep
#number of frames per second
#value determines speed of game
FPS = 300 #default 200
increaseSpeed = 5
FPSCLOCK = pygame.time.Clock()
windowWidth = 1920 #default 400
windowHeight = 1080 #default 300
lineThickness = 6
paddleSize = 50
paddleOffset = 20

BLACK = (0,0,0)
WHITE = (255,255,255)
arenaColor = (137,52,235)
playerOneColor = (18,235,14)
playerTwoColor = (235,14,165)

directionBall = random.randint(0,10)


def game_intro():
    pygame.init()
    FPSCLOCK = pygame.time.Clock()
    gameDisplay = pygame.display.set_mode((windowWidth,windowHeight), pygame.FULLSCREEN)
    while True:
        for event in pygame.event.get():
            if event.type == QUIT:
                pygame.quit()
                sys.exit()
            #Start game
            #Click Button y for multiplayer or click x for singleplayer
            #If button y is clicked down (GPIO RPI), then play this game
            #Maybe light an led
            elif event.type == pygame.KEYDOWN:
                if event.key == K_q:
                    pygame.quit()
                    sys.exit()
            elif event.type == MOUSEBUTTONDOWN:
                pygame.display.quit()
                main()

        gameDisplay.fill(WHITE)
        titleFont = pygame.font.Font('freesansbold.ttf', 25)
        singleFont = pygame.font.Font('freesansbold.ttf', 20)
        multiFont = pygame.font.Font('freesansbold.ttf', 20)
        textTitle = titleFont.render("Welcome to HandDraw", True, BLACK)
        textSingle = singleFont.render("Click Button Y for SinglePlayer", True, BLACK)
        textMulti = singleFont.render("Click Button X for Multiplayer", True, BLACK)
        titleRect = textTitle.get_rect()
        singleRect = textSingle.get_rect()
        multiRect = textMulti.get_rect()
        titleRect.center = ((windowWidth/2),(windowHeight/3))
        singleRect.center = ((windowWidth/2), windowHeight-100)
        multiRect.center = ((windowWidth/2), windowHeight-50)
        gameDisplay.blit(textTitle, titleRect)
        gameDisplay.blit(textSingle, singleRect)
        gameDisplay.blit(textMulti, multiRect)
        pygame.display.update()
        FPSCLOCK.tick(15)


def drawArena():
    displaySurf.fill((0,0,0))
    #draw outline of arena
    pygame.draw.rect(displaySurf, arenaColor, ((0,0),(windowWidth,windowHeight)),lineThickness)
    #draw center line of arena
    pygame.draw.line(displaySurf, arenaColor, ((windowWidth/2),0),((windowWidth/2),windowHeight),int((lineThickness/4)))

def drawPaddle(paddle, color):
    #paddle moving too low (windowheight - lineThickness is the max for the bottom)
    if paddle.bottom > windowHeight - lineThickness:
        paddle.bottom = windowHeight - lineThickness
    #paddle moving too high (linethickness is greater then paddle.top so it re-adjusts)
    elif paddle.top < lineThickness:
        paddle.top = lineThickness
    #draw paddle
    pygame.draw.rect(displaySurf, color, paddle)

def drawBall(ball):
    pygame.draw.rect(displaySurf, WHITE, ball)

#Keeps track of ball direction
def moveBall(ball, ballDirX, ballDirY):
    ball.x += ballDirX * increaseSpeed
    ball.y += ballDirY * increaseSpeed
    return ball

def checkEdgeCollision(ball, ballDirX, ballDirY):
    #Checks if top or bottom of ball then changes the ball direction by negative (x or y)
    if ball.top <= (lineThickness) or ball.bottom >= (windowHeight - lineThickness):
        ballDirY = ballDirY * -1
        #Add scoreboard when it gets completed when hits left or right and resets position
    return ballDirX, ballDirY

def AI(ball, ballDirX, playerTwo):
    #AI for player 2
    #if ball is moving away from paddle, center paddle
    if ballDirX <= -1:
        if playerTwo.centery < (windowHeight/2):
            playerTwo.y += 5
        elif playerTwo.centery > (windowHeight/2):
            playerTwo.y -= 5
    #if ball is moving towards paddle, track movement
    elif ballDirX >= 1:
        if playerTwo.centery < ball.centery:
            playerTwo.y += 5
        else:
            playerTwo.y -= 5
    return playerTwo

def checkHitBall(ball, playerOne, playerTwo, ballDirX):
    #If if statment is true (if ball collides with paddle) changes the ballDirX by negative if all false leave it in its current form
    if ballDirX == -1 and ((playerOne.right >= ball.left and playerOne.top <= ball.top and playerOne.bottom >= ball.bottom)):

        return -1
    elif ballDirX == 1 and ((playerTwo.left <= ball.right and playerTwo.top <= ball.top and playerTwo.bottom >= ball.bottom)):
        return -1
    else:
        return 1

def pointScoredp1(ball, scoreLeft, directionBall, ballDirX, ballDirY, increaseSpeed):
    #if player-side wall gets hit give score opposite side
    #ball hits left side
    if ball.right >= (windowWidth - lineThickness):
        scoreLeft += 1
        ball.x = (windowWidth/2) - 3#moves to default x
        ball.y = (windowHeight/2) - 3 #moves to default y
        directionBall = random.randint(0,6)
        ballDirX = -1
        if directionBall <= 3:
            ballDirY = -1
        else:
            ballDirY = 1
        increaseSpeed += 1
        return scoreLeft
    else:
        return scoreLeft

def pointScoredp2(ball, scoreRight, directionBall, ballDirX, ballDirY, increaseSpeed):
    if ball.left <= (lineThickness):
        scoreRight += 1
        ball.x = (windowWidth/2) - 3 #moves to default x
        ball.y = (windowHeight/2) - 3  #moves to default y
        directionBall = random.randint(0,6)
        ballDirX = 1
        if directionBall <= 3:
            ballDirY = -1
        else:
            ballDirY = 1
        return scoreRight
    else:
        return scoreRight
        #ball hits right side
#TODO: Score is not working left and right will each get different score
def displayScore(scoreLeft, scoreRight):
    #used for score text
    global basicFont, basicFontSize
    basicFontSize = 120
    basicFont = pygame.font.Font('freesansbold.ttf', basicFontSize)
    if scoreLeft == 5:
        mainText = "Left is the Winner"
        basicFontSize = 35
        basicFont = pygame.font.Font('freesansbold.ttf', basicFontSize)
    elif scoreRight == 5:
        mainText = "Right is the Winner"
        basicFontSize = 35
        basicFont = pygame.font.Font('freesansbold.ttf', basicFontSize)
    else:
        mainText = (str(scoreLeft) + '   ' + str(scoreRight))

    updateText(mainText, basicFontSize)

    if scoreLeft == 5 or scoreRight == 5:
        sleep(2)
        pygame.quit()
        sys.exit()

def countDown():
    drawArena()
    updateText("3", 120)
    sleep(1)
    displaySurf.fill((0,0,0))
    drawArena()
    updateText("2", 120)
    sleep(1)
    displaySurf.fill((0,0,0))
    drawArena()
    updateText("1", 120)
    sleep(1)
    displaySurf.fill((0,0,0))
    drawArena()
    updateText("START", 120)
    sleep(0.5)

def updateText(stringInput, fontSize):
    basicFontSize = fontSize
    basicFont = pygame.font.Font('freesansbold.ttf', basicFontSize)
    textSurf = basicFont.render(stringInput, True, WHITE)
    textRect = textSurf.get_rect()
    textRect.center = (windowWidth/2, windowHeight/2)
    #if one is bigger then the other, then do Left wins / Right wins
    displaySurf.blit(textSurf, textRect)
    pygame.display.update()

def main():
    pygame.init()
    global displaySurf
    #used for score text
    displaySurf = pygame.display.set_mode((windowWidth,windowHeight), pygame.FULLSCREEN)

    pygame.display.set_caption('Pong')

    #initialize and setting starting positions of ball and paddle
    ballX  = windowWidth/2 - lineThickness/2
    ballY = windowHeight/2 - lineThickness/2
    playerOnePos = (windowHeight - paddleSize)/2
    playerTwoPos = (windowHeight - paddleSize)/2
    scoreLeft = 0
    scoreRight = 0
    #Track of ball direction  || RNG system
    # When X is - = left || + = right
    # When Y is - = up || + = down
    if directionBall <= 5:
        ballDirX = -1
        if directionBall <= 3:
            ballDirY = -1
        else:
            ballDirY = 1
    else:
        ballDirX = 1
        if directionBall <= 8 and directionBall > 5:
            ballDirY = -1
        else:
            ballDirY = 1
    #creating rectangles for paddles and ball
    playerOne = pygame.Rect(paddleOffset,playerOnePos, lineThickness,paddleSize)
    playerTwo = pygame.Rect(windowWidth - paddleOffset - lineThickness, playerTwoPos, lineThickness, paddleSize)
    ball = pygame.Rect(ballX, ballY, lineThickness, lineThickness)
    print("ball x: " + str(ball.x))
    print("ball y: " + str(ball.y))
    pygame.mouse.set_visible(0) # make cursor invisible
    sleep(5)
    countDown()
    cap = cv2.VideoCapture(0)
    while True:
        #camera searching
        for event in pygame.event.get():
            if event.type == QUIT:
                pygame.quit()
                sys.exit()
                cap.release()
            #Player Movement
            elif event.type == pygame.KEYDOWN:
                if event.key == K_q:
                    pygame.quit()
                    sys.exit()
            else:
                    ret, frame = cap.read()
                    hsv = cv2.cvtColor(frame, cv2.COLOR_BGR2HSV)
                    #Color of pink highlighter
                    lower_range = np.array([49,85,143])
                    upper_range = np.array([180,255,255])
                    mask = cv2.inRange(hsv, lower_range, upper_range)
                    mask = cv2.erode(mask, None, iterations=2)
                    mask = cv2.dilate(mask, None, iterations=2)
                    cnts = cv2.findContours(mask.copy(), cv2.RETR_EXTERNAL, cv2.CHAIN_APPROX_SIMPLE)[-2]
                    center = None

                    if len(cnts)>0:
                        c = max(cnts, key=cv2.contourArea)
                        ((x,y), radius) = cv2.minEnclosingCircle(c)
                        M = cv2.moments(c)
                        center = (int(M["m10"] / M["m00"]), int(M["m01"] / M["m00"]))

                        if radius > 10:
                            cv2.circle(frame, (int(x), int(y)) , int(radius), (0,255,255), 2)
                            cv2.circle(frame, center, 5, (0,0,255), -1)
                            mousey = ((int(x)/682)*(windowHeight - (lineThickness)*2)) #ground position = 300 #top position = 0
                    else:
                        mousey = playerOne.y
                    cv2.imshow('frame', frame)

                    playerOne.y = mousey

        drawArena()
        drawPaddle(playerOne, playerOneColor)
        drawPaddle(playerTwo, playerTwoColor)
        drawBall(ball)

        ball = moveBall(ball, ballDirX, ballDirY)
        ballDirX, ballDirY = checkEdgeCollision(ball, ballDirX, ballDirY)
        scoreLeft = pointScoredp1(ball, scoreLeft, directionBall, ballDirX, ballDirY)
        scoreRight = pointScoredp2(ball, scoreRight, directionBall, ballDirX, ballDirY)
        #ball hit detection
        ballDirX = ballDirX * checkHitBall(ball, playerOne, playerTwo, ballDirX)
        playerTwo = AI(ball, ballDirX, playerTwo)
        displayScore(scoreLeft, scoreRight)

        pygame.display.update()
        FPSCLOCK.tick(FPS)

if __name__=='__main__':
    game_intro()
