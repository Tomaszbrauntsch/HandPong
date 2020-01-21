#KEY:
#Everything is being built like a gui, layer over layer
#displaySurf = Main window
#
#WORK ON OPENCV NOW
import pygame, sys
from pygame.locals import *

import random
from time import sleep
#number of frames per second
#value determines speed of game
FPS = 300 #default 200
FPSCLOCK = pygame.time.Clock()
global increaseSpeed
increaseSpeed = 3
windowWidth = 1200 #default 400
windowHeight = 800#default 300
lineThickness = 6
paddleSize = 100
paddleOffset = 20

BLACK = (0,0,0)
WHITE = (255,255,255)
arenaColor = (137,52,235)
playerOneColor = (18,235,14)
playerTwoColor = (235,14,165)

directionBall = random.randint(0,10)

def game_intro():
    pygame.init()
    gameDisplay = pygame.display.set_mode((windowWidth,windowHeight), pygame.FULLSCREEN)
    while True:
        for event in pygame.event.get():
            if event.type == QUIT:
                pygame.quit()
                sys.exit()
            #Start game
            #Click Button y for multiplayer or click x for singleplayer
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
        textTitle = titleFont.render("Welcome to HandDraw", True, BLACK)
        textSingle = singleFont.render("Click Down on the mouse button to play", True, BLACK)
        titleRect = textTitle.get_rect()
        singleRect = textSingle.get_rect()
        titleRect.center = ((windowWidth/2),(windowHeight/3))
        singleRect.center = ((windowWidth/2), windowHeight-100)
        gameDisplay.blit(textTitle, titleRect)
        gameDisplay.blit(textSingle, singleRect)
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
    if ballDirX == -1 and ((playerOne.right >= ball.left and playerOne.top <= ball.top and playerOne.bottom >= ball.bottom)):
        return -1
    elif ballDirX == 1 and ((playerTwo.left <= ball.right and playerTwo.top <= ball.top and playerTwo.bottom >= ball.bottom)):
        return -1
    else:
        return 1

def pointScoredp1(ball, scoreLeft, directionBall, ballDirX, ballDirY):
    #if player-side wall gets hit give score opposite side
    #ball hits left side
    if ball.right >= (windowWidth - lineThickness):
        scoreLeft += 1
        ball.x = (windowWidth/2) - 3 #moves to default x #400 = 197
        ball.y = (windowHeight/2) - 3 #moves to default y #300 = 147
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
    if ball.left <= (lineThickness):
        scoreRight += 1
        ball.x = (windowWidth/2) - 3 #moves to default x
        ball.y = (windowHeight/2) - 3 #moves to default y
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
    #insert Show score animation
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
    #starting in 3...2...1
    countDown()
    while True:
        for event in pygame.event.get():
            if event.type == QUIT:
                pygame.quit()
                sys.exit()
            #Player Movement
            elif event.type == pygame.KEYDOWN:
                if event.key == K_q:
                    pygame.quit()
                    sys.exit()
            elif event.type == MOUSEMOTION:
                mousex, mousey = event.pos
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
