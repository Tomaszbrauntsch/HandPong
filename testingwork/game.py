#KEY:
#Everything is being built like a gui, layer over layer
#displaySurf = Main window
#
#WORK ON OPENCV NOW
import pygame, sys
from pygame.locals import *

import random
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

def game_intro():
    pygame.init()
    FPSCLOCK = pygame.time.Clock()
    gameDisplay = pygame.display.set_mode((windowWidth,windowHeight))
    while True:
        for event in pygame.event.get():
            if event.type == QUIT:
                pygame.quit()
                sys.exit()
            #Start game
            #Click Button y for multiplayer or click x for singleplayer
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
    while True:
        for event in pygame.event.get():
            if event.type == QUIT:
                pygame.quit()
                sys.exit()
            #Player Movement
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
