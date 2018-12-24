import pygame
import MonoSim

width = 400
height = 400
pygame.init()
screen = pygame.display.set_mode((width, height))
done = False
is_blue = True
x = 30
y = 30

clock = pygame.time.Clock()

font = pygame.font.SysFont("comicsansms", 16)

simulation = MonoSim.Simulation(num_players = 4)

while not done:
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            done = True
        if event.type == pygame.KEYDOWN and event.key == pygame.K_SPACE:
            is_blue = not is_blue
        if event.type == pygame.KEYDOWN and event.key == pygame.K_ESCAPE:
            done = True

    pygame.draw.lines(screen, (255, 255, 255), True, [(width*.1, width*.1), (width*.9, width*.1),
                                                      (width*.9, width*.9), (width*.1, width*.9)])
    pygame.draw.lines(screen, (255, 255, 255), True, [(width * .2, width * .2), (width * .8, width * .2),
                                                      (width * .8, width * .8), (width * .2, width * .8)])
    for i in range(0, 10):
        pygame.draw.line(screen, (255, 255, 255), (i*.6*width/9+width*.2, width*.1), (i*.6*width/9+width*.2, width*.2))
    for i in range(0, 10):
        pygame.draw.line(screen, (255, 255, 255), (i*.6*width/9+width*.2, width*.9), (i*.6*width/9+width*.2, width*.8))
    for i in range(0, 10):
        pygame.draw.line(screen, (255, 255, 255), (width*.1, i*.6*width/9+width*.2), (width*.2, i*.6*width/9+width*.2))
    for i in range(0, 10):
        pygame.draw.line(screen, (255, 255, 255), (width*.8, i*.6*width/9+width*.2), (width*.9, i*.6*width/9+width*.2))

    pygame.display.flip()
    clock.tick(60)


