import pygame
import sys
 
screenSize = (400, 300)
gameScreen = pygame.display.set_mode(screenSize)
pygame.init()
 
gameloopCount = 0

running =True
while running:
    for event in pygame.event.get():
        gameloopCount += 1
        print(gameloopCount, ":", event)
        if event.type == pygame.QUIT:
            running = False
 
pygame.quit()
sys.exit()  
