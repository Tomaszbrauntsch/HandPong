#KEY:
#Everything is being built like a gui, layer over layer
#displaySurf = Main window
#

import pygame, sys
from pygame.locals import *

import random
#number of frames per second
#value determines speed of game
FPS = 200 #default 200
windowWidth = 400
windowHeight = 300
lineThickness = 6
paddleSize = 50
paddleOffset = 20

BLACK = (0,0,0)
WHITE = (255,255,255)
arenaColor = (137,52,235)
playerOneColor = (18,235,14)
playerTwoColor = (235,14,165)

directionBall = random.randint(0,10)


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
    if ball.left == (lineThickness) or ball.right == (windowWidth - lineThickness):
        #Add scoreboard when it gets completed when hits left or right and resets position
        ballDirX = ballDirX * -1
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
    #elif ballDirX == 1 and ((playerTwo.left == ball.right) or (playerTwo.top <= ball.top) or (playerTwo.bottom >= ball.bottom))
    if ballDirX == -1 and ((playerOne.right == ball.left and playerOne.top <= ball.top and playerOne.bottom >= ball.bottom)):
        return -1
    elif ballDirX == 1 and ((playerTwo.left == ball.right and playerTwo.top <= ball.top and playerTwo.bottom >= ball.bottom)):
        return -1
    else:
        return 1

def checkPointScored(playerOne, playerTwo, ball, scoreLeft, scoreRight, ballDirX):
    if ball.left == lineThickness:
        return 0
    #on hit
    elif ballDirX == -1 and ((playerOne.right == ball.left and playerOne.top <= ball.top and playerOne.bottom >= ball.bottom)):
        scoreLeft += 1
        print("scoreLeft: " + str(scoreLeft))
        return scoreLeft
    elif ballDirX == -1 and ((playerTwo.left == ball.right and playerTwo.top <= ball.top and playerTwo.bottom >= ball.bottom)):
        scoreRight += 1
        print("scoreRight: " + str(scoreRight))
        return scoreRight
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

    #spygame.mouse.set_visible(0) # make cursor invisible
    while True:
        for event in pygame.event.get():
            if event.type == QUIT:
                pygame.quit()
                sys.exit()
            #player movement
            elif event.type == MOUSEMOTION:
                mousex, mousey = event.pos
                playerOne.y = mousey

        drawArena()
        drawPaddle(playerOne, playerOneColor)
        drawPaddle(playerTwo, playerTwoColor)
        drawBall(ball)

        ball = moveBall(ball, ballDirX, ballDirY)
        ballDirX, ballDirY = checkEdgeCollision(ball, ballDirX, ballDirY)
        score = checkPointScored(playerOne, playerTwo, ball, scoreLeft, scoreRight, ballDirX)
        #ball hit detection
        ballDirX = ballDirX * checkHitBall(ball, playerOne, playerTwo, ballDirX)
        playerTwo = AI(ball, ballDirX, playerTwo)
        displayScore(scoreLeft, scoreRight)

        pygame.display.update()
        FPSCLOCK.tick(FPS)

if __name__=='__main__':
    main()
