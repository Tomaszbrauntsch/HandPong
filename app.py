#KEY:
#Everything is being built like a gui, layer over layer
#displaySurf = Main window
#
#WORK ON OPENCV NOW
import pygame, sys
from pygame.locals import *
#camera manipulation
import numpy as np
import cv2
#random
import random
#threading
import threading
#number of frames per second
#value determines speed of game
FPS = 300 #default 200
windowWidth = 400 #default 400
windowHeight = 300 #default 300
lineThickness = 6
paddleSize = 50
paddleOffset = 20

BLACK = (0,0,0)
WHITE = (255,255,255)
arenaColor = (137,52,235)
playerOneColor = (18,235,14)
playerTwoColor = (235,14,165)

directionBall = random.randint(0,10)

cap = cv2.VideoCapture(0)
objectPos = 0



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
    ball.x += ballDirX
    ball.y += ballDirY
    return ball

def checkEdgeCollision(ball, ballDirX, ballDirY):
    #Checks if top or bottom of ball then changes the ball direction by negative (x or y)
    if ball.top == (lineThickness) or ball.bottom == (windowHeight - lineThickness):
        ballDirY = ballDirY * -1
        #Add scoreboard when it gets completed when hits left or right and resets position
    return ballDirX, ballDirY

def AI(ball, ballDirX, playerTwo):
    #AI for player 2
    #if ball is moving away from paddle, center paddle
    if ballDirX == -1:
        if playerTwo.centery < (windowHeight/2):
            playerTwo.y += 1
        elif playerTwo.centery > (windowHeight/2):
            playerTwo.y -= 1
    #if ball is moving towards paddle, track movement
    elif ballDirX == 1:
        if playerTwo.centery < ball.centery:
            playerTwo.y += 1
        else:
            playerTwo.y -= 1
    return playerTwo

def checkHitBall(ball, playerOne, playerTwo, ballDirX):
    #If if statment is true (if ball collides with paddle) changes the ballDirX by negative if all false leave it in its current form
    if ballDirX == -1 and ((playerOne.right == ball.left and playerOne.top <= ball.top and playerOne.bottom >= ball.bottom)):

        return -1
    elif ballDirX == 1 and ((playerTwo.left == ball.right and playerTwo.top <= ball.top and playerTwo.bottom >= ball.bottom)):
        return -1
    else:
        return 1

def pointScoredp1(ball, scoreLeft, directionBall, ballDirX, ballDirY):
    #if player-side wall gets hit give score opposite side
    #ball hits left side
    if ball.right == (windowWidth - lineThickness):
        scoreLeft += 1
        ball.x = 197 #moves to default x
        ball.y = 147 #moves to default y
        directionBall = random.randint(0,6)
        ballDirX = -1
        if directionBall <= 3:
            ballDirY = -1
        else:
            ballDirY = 1
        return scoreLeft
    else:
        return scoreLeft

def pointScoredp2(ball, scoreRight, directionBall, ballDirX, ballDirY):
    if ball.left == (lineThickness):
        scoreRight += 1
        ball.x = 197 #moves to default x
        ball.y = 147 #moves to default y
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
    #display text
    resultSurf = basicFont.render(str(scoreLeft) + ' | ' + str(scoreRight), True, WHITE)
    resultRect = resultSurf.get_rect()
    resultRect.topleft = (windowWidth - 150, 25)
    displaySurf.blit(resultSurf, resultRect)

def cameraWork():
    ret, frame = cap.read()
    hsv = cv2.cvtColor(frame, cv2.COLOR_BGR2HSV)
    lower_range = np.array([7,130,130])
    upper_range = np.array([50,255,255])

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
    cv2.imshow('frame', frame)
    return int(x)

def main():
    pygame.init()
    global displaySurf
    #used for score text
    global basicFont, basicFontSize
    basicFontSize = 20
    basicFont = pygame.font.Font('freesansbold.ttf', basicFontSize)

    FPSCLOCK = pygame.time.Clock()
    displaySurf = pygame.display.set_mode((windowWidth,windowHeight))
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
    #spygame.mouse.set_visible(0) # make cursor invisible
    cameraThread = threading.Thread(target=cameraWork)
    while True:
        #camera searching
        for event in pygame.event.get():
            if event.type == QUIT:
                pygame.quit()
                sys.exit()
                cap.release()
            #Player Movement
        else:
            if not cameraThread.is_alive():
                userXPos = cameraThread.start()
                if userXPos is None:
                    objectPos = 0
                else:
                    objectPos = int(userXPos)

            if (objectPos < 341):     #341 is the center X coord
                playerMoveY = (341 - objectPos - 147)
            elif (objectPos > 341):
                playerMoveY = (objectPos - 341 + 147)
            playerOne.y = playerMoveY

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
    main()
