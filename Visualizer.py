import pygame
import operator


class Visualizer:

    def __init__(self, tile_names):
        pygame.init()
        self.width = 600
        self.height = 600
        self.screen = pygame.display.set_mode((self.width, self.height))
        self.done = False

        self.tile_names = tile_names

        self.clock = pygame.time.Clock()

        self.black = (0, 0, 0)
        self.white = (255, 255, 255)

        self.font = pygame.font.SysFont("calibri", 10)

    def draw_board(self, tile_names):
        self.screen.fill((192, 226, 202))

        # TODO add in names of actual spaces
        pygame.draw.lines(self.screen, self.black, True, [
            (self.width * .1, self.width * .1),
            (self.width * .9, self.width * .1),
            (self.width * .9, self.width * .9),
            (self.width * .1, self.width * .9)
        ], 2)
        # Draws the outer lines of the board

        pygame.draw.lines(self.screen, self.black, True, [
            (self.width * .2, self.width * .2),
            (self.width * .8, self.width * .2),
            (self.width * .8, self.width * .8),
            (self.width * .2, self.width * .8)
        ])
        # Draws the inner lines of the board

        for i in range(0, 10):
            pygame.draw.line(
                self.screen, self.black,
                (operator.mul(i, .6 * self.width) / 9 + self.width * .2, self.width * .1),
                (operator.mul(i, (.6 * self.width)) / 9 + self.width * .2, self.width * .2))
            # Draws the tile separation lines for tiles on the top of the board

        for i in range(0, 10):
            pygame.draw.line(
                self.screen, self.black,
                (operator.mul(i, .6 * self.width) / 9 + self.width * .2, self.width * .9),
                (operator.mul(i, (.6 * self.width)) / 9 + self.width * .2, self.width * .8))
            # Draws the tile separation lines for tiles on the bottom of the board

        for i in range(0, 10):
            pygame.draw.line(
                self.screen, self.black,
                (self.width * .1, operator.mul(i, (.6 * self.width)) / 9 + self.width * .2),
                (self.width * .2, operator.mul(i, (.6 * self.width)) / 9 + self.width * .2))
            # Draws the tile separation lines for tiles on the left of the board

        for i in range(0, 10):
            pygame.draw.line(
                self.screen, self.black,
                (self.width * .8, operator.mul(i, (.6 * self.width)) / 9 + self.width * .2),
                (self.width * .9, operator.mul(i, (.6 * self.width)) / 9 + self.width * .2))
            # Draws the tile separation lines for tiles on the right of the board

        for i in range(0, 9):
            position = [
                (self.width*.2) + self.width * i * .6 / 9 + self.width * .3 / 9,
                self.width * .11
            ]
            self.draw_property(position, tile_names[i], self.black, self.font, self.screen)
            # Labels the tile on the top of the board TODO add in colored rectangles where appropriate

        for i in range(0, 9):
            position = [
                (self.width*.2) + self.width * i * .6 / 9 + self.width * .3 / 9,
                self.width * .81
            ]
            self.draw_property(position, tile_names[i], self.black, self.font, self.screen)
            # Labels the tile on the bottom of the board TODO add in colored rectangles where appropriate

        for i in range(0, 9):
            position = [
                self.width * .15,
                (self.width * .2) + self.width * i * .6 / 9 + self.width * .1 / 9
            ]
            self.draw_property(position, tile_names[i], self.black, self.font, self.screen)
            # Labels the tile on the left of the board TODO add in colored rectangles where appropriate

        for i in range(0, 9):
            position = [
                self.width * .85,
                (self.width * .2) + self.width * i * .6 / 9 + self.width * .1 / 9
            ]
            self.draw_property(position, tile_names[i], self.black, self.font, self.screen)
            # Labels the tile on the right of the board TODO add in colored rectangles where appropriate

    @staticmethod
    def draw_property(position, name, color, font, screen):
        label = font.render(name, True, color)
        position[0] = position[0]-label.get_width() / 2
        screen.blit(label, position)

    def update(self):
        self.draw_board(self.tile_names)
        pygame.display.flip()
        self.clock.tick(60)


def __main__():
    # TODO Eventually this will be removed and the visualizer
    # TODO will be able to be called from an external script
    spots = ["one", "two", "three", "four", "five", "six", "seven", "eight", "nine"]

    vis = Visualizer(spots)

    while not vis.done:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                vis.done = True
            if event.type == pygame.KEYDOWN and event.key == pygame.K_ESCAPE:
                vis.done = True

        vis.update()


__main__()
