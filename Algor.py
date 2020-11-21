import pygame
pygame.init()
win = pygame.display.set_mode((900, 545))
pygame.display.set_caption("9qmq")
x = 100
y = 100
speed = 10
run = True
pygame.draw.circle(win, (255,255,255), (x,y), (9))
pygame.draw.circle(win, (255,255,255), (x,y+20), (9))
pygame.draw.circle(win, (255,255,255), (x,y+40), (9))
pygame.draw.circle(win, (255,255,255), (x,y+60), (9))
pygame.draw.circle(win, (255,255,255), (x,y+80), (9))
pygame.draw.circle(win, (255,255,255), (x,y+100), (9))
pygame.draw.circle(win, (255,255,255), (x,y+120), (9))
pygame.draw.circle(win, (255,255,255), (x,y+140), (9))
pygame.draw.circle(win, (255,255,255), (x,y+160), (9))
x+=20
pygame.draw.circle(win, (255,255,255), (x,y), (9))
pygame.draw.circle(win, (255,255,255), (x,y+20), (9))
pygame.draw.circle(win, (255,255,255), (x,y+40), (9))
pygame.draw.circle(win, (255,255,255), (x,y+60), (9))
pygame.draw.circle(win, (255,255,255), (x,y+80), (9))
pygame.draw.circle(win, (255,255,255), (x,y+100), (9))
pygame.draw.circle(win, (255,255,255), (x,y+120), (9))
pygame.draw.circle(win, (255,255,255), (x,y+140), (9))

while run:
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            run = False

    pygame.display.update()