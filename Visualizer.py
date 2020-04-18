import pygame
import operator


class Visualizer:

    def __init__(self, simulation):
        pygame.init()
        self.width = 1000
        self.height = 1000
        self.screen = pygame.display.set_mode((self.width, self.height))
        self.done = False

        self.simulation = simulation

        self.clock = pygame.time.Clock()

        self.black = (0, 0, 0)
        self.white = (255, 255, 255)
        self.blue = (0, 0, 255)

        self.font = pygame.font.SysFont("calibri", 8)

        self.player_offset = {
            "1": (0, 0),
            "2": (self.width * 1 / 80, 0),
            "3": (self.width * 2 / 80, 0),
            "4": (self.width * 3 / 80, 0),
            "5": (0, self.height / 80),
            "6": (self.width * 1 / 80, self.height / 80),
            "7": (self.width * 2 / 80, self.height / 80),
            "8": (self.width * 3 / 80, self.height / 80),
        }

    def draw_board(self):
        self.screen.fill((192, 226, 202))

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
            self.draw_property(position, self.simulation.look_up[str(i+21)], self.black, self.font, self.screen)
            # Labels the tile on the top of the board

        for i in range(0, 9):
            position = [
                (self.width*.2) + self.width * i * .6 / 9 + self.width * .3 / 9,
                self.width * .81
            ]
            self.draw_property(position, self.simulation.look_up[str(i + (9-2*i))], self.black, self.font, self.screen)
            # Labels the tile on the bottom of the board

        for i in range(0, 9):
            position = [
                self.width * .15,
                (self.width * .2) + self.width * i * .6 / 9 + self.width * .1 / 9
            ]
            self.draw_property(position, self.simulation.look_up[str(i+10+(9-2*i))], self.black, self.font, self.screen)
            # Labels the tile on the left of the board

        for i in range(0, 9):
            position = [
                self.width * .85,
                (self.width * .2) + self.width * i * .6 / 9 + self.width * .1 / 9
            ]
            self.draw_property(position, self.simulation.look_up[str(i+31)], self.black, self.font, self.screen)
            # Labels the tile on the right of the board

        self.draw_property(
            [self.width * .85, self.width * .81], self.simulation.look_up["0"], self.black, self.font, self.screen)
        # Label the lower left corner tile

        self.draw_property(
            [self.width * .15, self.width * .81], self.simulation.look_up["10"], self.black, self.font, self.screen)
        # Label the lower left corner tile

        self.draw_property(
            [self.width * .15, self.width * .11], self.simulation.look_up["20"], self.black, self.font, self.screen)
        # Label the upper left cornet tile

        self.draw_property(
            [self.width * .85, self.width * .11], self.simulation.look_up["30"], self.black, self.font, self.screen)
        # Label the upper right corner tile

    def draw_player(self, position, player_number, color="Black"):
        if color == "Blue":
            color = self.blue
        elif color == "Black":
            color = self.black
        offset = self.player_offset[str(player_number)]
        if position == 0:
            pygame.draw.polygon(self.screen, color, [
                (self.width * 0.83125 - self.width / 200 + offset[0],
                 self.height * 0.86 + self.height / 200 + offset[1]),
                (self.width * 0.83125 + self.width / 200 + offset[0],
                 self.height * 0.86 + self.height / 200 + offset[1]),
                (self.width * 0.83125 + self.width / 200 + offset[0],
                 self.height * 0.86 - self.height / 200 + offset[1]),
                (self.width * 0.83125 - self.width / 200 + offset[0],
                 self.height * 0.86 - self.height / 200 + offset[1])])
        # pygame.draw.polygon(self.screen, self.black, [
        #     (self.width * 0.2 + self.width * .3 / 9 - self.width / 200, self.height * 0.14 + self.height / 200),
        #     (self.width * 0.2 + self.width * .3 / 9 + self.width / 200, self.height * 0.14 + self.height / 200),
        #     (self.width * 0.2 + self.width * .3 / 9 + self.width / 200, self.height * 0.14 - self.height / 200),
        #     (self.width * 0.2 + self.width * .3 / 9 - self.width / 200, self.height * 0.14 - self.height / 200)])

    @staticmethod
    def draw_property(position, name, color, font, screen):
        label = font.render(name, True, color)
        position[0] = position[0]-label.get_width() / 2
        screen.blit(label, position)

    def update(self):
        self.draw_board()
        self.draw_player(0, 1, color="Blue")
        self.draw_player(0, 2)
        self.draw_player(0, 3, color="Blue")
        self.draw_player(0, 4)
        self.draw_player(0, 5)
        self.draw_player(0, 6, color="Blue")
        self.draw_player(0, 7)
        self.draw_player(0, 8, color="Blue")
        pygame.display.flip()
        self.clock.tick(60)

