import pygame
import operator


def draw_board(screen, black, white, font):
    screen.fill((192, 226, 202))

    spots = ["one", "two", "three", "four", "five", "six", "seven", "eight", "nine"]
    pygame.draw.lines(screen, black, True, [(screen.get_width() * .1, screen.get_width() * .1),
                                            (screen.get_width() * .9, screen.get_width() * .1),
                                            (screen.get_width() * .9, screen.get_width() * .9),
                                            (screen.get_width() * .1, screen.get_width() * .9)], 2)
    pygame.draw.lines(screen, black, True, [(screen.get_width() * .2, screen.get_width() * .2),
                                            (screen.get_width() * .8, screen.get_width() * .2),
                                            (screen.get_width() * .8, screen.get_width() * .8),
                                            (screen.get_width() * .2, screen.get_width() * .8), 2])
    for i in range(0, 10):
        pygame.draw.line(
            screen, black,
            (operator.mul(i, .6 * screen.get_width()) / 9 + screen.get_width() * .2, screen.get_width() * .1),
            (operator.mul(i, (.6 * screen.get_width())) / 9 + screen.get_width() * .2, screen.get_width() * .2))
    for i in range(0, 10):
        pygame.draw.line(
            screen, black,
            (operator.mul(i, .6 * screen.get_width()) / 9 + screen.get_width() * .2, screen.get_width() * .9),
            (operator.mul(i, (.6 * screen.get_width())) / 9 + screen.get_width() * .2, screen.get_width() * .8))
    for i in range(0, 10):
        pygame.draw.line(
            screen, black,
            (screen.get_width() * .1, operator.mul(i, (.6 * screen.get_width())) / 9 + screen.get_width() * .2),
            (screen.get_width() * .2, operator.mul(i, (.6 * screen.get_width())) / 9 + screen.get_width() * .2))
    for i in range(0, 10):
        pygame.draw.line(
            screen, black,
            (screen.get_width() * .8, operator.mul(i, (.6 * screen.get_width())) / 9 + screen.get_width() * .2),
            (screen.get_width() * .9, operator.mul(i, (.6 * screen.get_width())) / 9 + screen.get_width() * .2))

    for i in range(0, 9):
        position = [
            (screen.get_width()*.2) + screen.get_width() * i * .6 / 9 + screen.get_width() * .3 / 9,
            screen.get_width() * .11
        ]
        draw_property(position, spots[i], black, font, screen, False)
    for i in range(0, 9):
        position = [
            (screen.get_width()*.2) + screen.get_width() * i * .6 / 9 + screen.get_width() * .3 / 9,
            screen.get_width() * .81
        ]
        draw_property(position, spots[i], black, font, screen, False)
    for i in range(0, 9):
        position = [
            screen.get_width() * .15,
            (screen.get_width() * .2) + screen.get_width() * i * .6 / 9 + screen.get_width() * .1 / 9
        ]
        draw_property(position, spots[i], black, font, screen, False)
    for i in range(0, 9):
        position = [
            screen.get_width() * .85,
            (screen.get_width() * .2) + screen.get_width() * i * .6 / 9 + screen.get_width() * .1 / 9
        ]
        draw_property(position, spots[i], black, font, screen, False)


def draw_property(position, name, color, font, screen, vertical):
    label = font.render(name, True, color)
    position[0] = position[0]-label.get_width() / 2
    screen.blit(label, position)


def __main__():

    width = 600
    height = 600
    pygame.init()
    screen = pygame.display.set_mode((width, height))
    done = False

    black = (0, 0, 0)
    white = (255, 255, 255)

    clock = pygame.time.Clock()

    font = pygame.font.SysFont("calibri", 10)

    while not done:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                done = True
            if event.type == pygame.KEYDOWN and event.key == pygame.K_ESCAPE:
                done = True

        draw_board(screen, black, white, font)
        pygame.display.flip()
        clock.tick(60)


__main__()
