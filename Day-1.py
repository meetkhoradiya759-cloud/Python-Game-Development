import pygame
import sys

# Initialization
pygame.init()

WIDTH = 800
HEIGHT = 600
FPS = 60

screen = pygame.display.set_mode((WIDTH,HEIGHT))
pygame.display.set_caption("MY FIRST GAME WINDOW")
clock = pygame.time.Clock()

# colors
BLACK   = (0,0,0)
RED     = (255,0,0)
WHITE   = (255,255,255)
GREEN   = (0,200,0)

while True:
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            pygame.quit()
            sys.exit()
        
    # Draw
    screen.fill(BLACK)
    pygame.draw.rect(screen,RED,(500,100,200,100))
    pygame.draw.circle(screen,GREEN,(100,150),60)
    pygame.draw.line(screen,RED,(0,250),(800,250),3)

    # Exercise - Draw My name initials using line()
    # Draw 'M'
    pygame.draw.line(screen,WHITE,(100,300),(100,500),5)    # Left side "|"
    pygame.draw.line(screen,WHITE,(100,300),(200,400),5)    # \
    pygame.draw.line(screen,WHITE,(300,300),(200,400),5)    # /
    pygame.draw.line(screen,WHITE,(300,300),(300,500),5)    # Right side "|"
    pygame.draw.circle(screen,RED,(340,500),5)

    # Draw 'K'
    pygame.draw.line(screen,GREEN,(400,300),(400,500),5)    # Left side "|"
    pygame.draw.line(screen,GREEN,(400,400),(500,500),5)    # Up /
    pygame.draw.line(screen,GREEN,(400,400),(500,300),5)    # Down \
    pygame.draw.circle(screen,RED,(550,500),5)

    pygame.display.flip()
    clock.tick(FPS)