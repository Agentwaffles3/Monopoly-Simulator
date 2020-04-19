import pygame
import operator


class Visualizer:

    def __init__(self, simulation):
        pygame.init()
        self.width = 1500
        self.height = 1000
        self.screen = pygame.display.set_mode((self.width, self.height))
        self.done = False

        self.simulation = simulation

        self.clock = pygame.time.Clock()

        self.black = (0, 0, 0)
        self.red = (255, 0, 0)
        self.orange = (255, 128, 0)
        self.yellow = (255, 255, 0)
        self.magenta = (255, 0, 127)
        self.green = (0, 255, 0)
        self.cyan = (0, 255, 255)
        self.blue = (0, 0, 255)
        self.purple = (127, 0, 255)
        self.white = (255, 255, 255)

        self.font = pygame.font.SysFont("calibri", 10)

        self.player_offset = {
            "Player 1": (0, 0),
            "Player 2": (self.width * 1 / 80, 0),
            "Player 3": (self.width * 2 / 80, 0),
            "Player 4": (self.width * 3 / 80, 0),
            "Player 5": (0, self.height / 80),
            "Player 6": (self.width * 1 / 80, self.height / 80),
            "Player 7": (self.width * 2 / 80, self.height / 80),
            "Player 8": (self.width * 3 / 80, self.height / 80),
        }

    def draw_board(self):
        self.screen.fill((192, 226, 202))

        pygame.draw.lines(self.screen, self.black, True, [
            (self.width * .1, self.height * .05),
            (self.width * .9, self.height * .05),
            (self.width * .9, self.height * .95),
            (self.width * .1, self.height * .95)
        ], 2)
        # Draws the outer lines of the board

        pygame.draw.lines(self.screen, self.black, True, [
            (self.width * .2, self.height * .15),
            (self.width * .8, self.height * .15),
            (self.width * .8, self.height * .85),
            (self.width * .2, self.height * .85)
        ])
        # Draws the inner lines of the board

        for i in range(0, 10):
            pygame.draw.line(
                self.screen, self.black,
                (operator.mul(i, .6 * self.width) / 9 + self.width * .2, self.height * .05),
                (operator.mul(i, (.6 * self.width)) / 9 + self.width * .2, self.height * .15))
            # Draws the tile separation lines for tiles on the top of the board

        for i in range(0, 10):
            pygame.draw.line(
                self.screen, self.black,
                (operator.mul(i, .6 * self.width) / 9 + self.width * .2, self.height * .95),
                (operator.mul(i, (.6 * self.width)) / 9 + self.width * .2, self.height * .85))
            # Draws the tile separation lines for tiles on the bottom of the board

        for i in range(0, 10):
            pygame.draw.line(
                self.screen, self.black,
                (self.width * .1, operator.mul(i, (.7 * self.height)) / 9 + self.height * .15),
                (self.width * .2, operator.mul(i, (.7 * self.height)) / 9 + self.height * .15))
            # Draws the tile separation lines for tiles on the left of the board

        for i in range(0, 10):
            pygame.draw.line(
                self.screen, self.black,
                (self.width * .8, operator.mul(i, (.7 * self.height)) / 9 + self.height * .15),
                (self.width * .9, operator.mul(i, (.7 * self.height)) / 9 + self.height * .15))
            # Draws the tile separation lines for tiles on the right of the board

        for i in range(0, 9):
            position = [
                (self.width*.2) + self.width * i * .6 / 9 + self.width * .3 / 9,
                self.height * .06
            ]
            self.draw_property(position, self.simulation.look_up[str(i+21)], self.black, self.font, self.screen)
            # Label the tiles on the top of the board

        for i in range(0, 9):
            position = [
                (self.width*.2) + self.width * i * .6 / 9 + self.width * .3 / 9,
                self.height * .86
            ]
            self.draw_property(position, self.simulation.look_up[str(i + (9-2*i))], self.black, self.font, self.screen)
            # Label the tiles on the bottom of the board

        for i in range(0, 9):
            position = [
                self.width * .15,
                (self.height * .15) + self.height * i * .7 / 9 + self.height * .1 / 9
            ]
            self.draw_property(position, self.simulation.look_up[str(i+10+(9-2*i))], self.black, self.font, self.screen)
            # Label the tiles on the left of the board

        for i in range(0, 9):
            position = [
                self.width * .85,
                (self.height * .15) + self.height * i * .7 / 9 + self.height * .1 / 9
            ]
            self.draw_property(position, self.simulation.look_up[str(i+31)], self.black, self.font, self.screen)
            # Label the tiles on the right of the board

        self.draw_property(
            [self.width * .85, self.height * .86], self.simulation.look_up["0"], self.black, self.font, self.screen)
        # Label the lower left corner tile

        self.draw_property(
            [self.width * .15, self.height * .86], self.simulation.look_up["10"], self.black, self.font, self.screen)
        # Label the lower left corner tile

        self.draw_property(
            [self.width * .15, self.height * .06], self.simulation.look_up["20"], self.black, self.font, self.screen)
        # Label the upper left cornet tile

        self.draw_property(
            [self.width * .85, self.height * .06], self.simulation.look_up["30"], self.black, self.font, self.screen)
        # Label the upper right corner tile

    def draw_player(self, position, player_number, color="Black"):
        if color == "Black":
            color = self.black
        elif color == "Red":
            color = self.red
        elif color == "Orange":
            color = self.orange
        elif color == "Yellow":
            color = self.yellow
        elif color == "Magenta":
            color = self.magenta
        elif color == "Green":
            color = self.green
        elif color == "Cyan":
            color = self.cyan
        elif color == "Blue":
            color = self.blue
        elif color == "Purple":
            color = self.purple

        offset = self.player_offset[str(player_number)]
        if position == 0:
            pygame.draw.polygon(self.screen, color, [
                (self.width * 0.83125 - self.width / 200 + offset[0],
                 self.height * 0.925 + self.height / 200 + offset[1]),
                (self.width * 0.83125 + self.width / 200 + offset[0],
                 self.height * 0.925 + self.height / 200 + offset[1]),
                (self.width * 0.83125 + self.width / 200 + offset[0],
                 self.height * 0.925 - self.height / 200 + offset[1]),
                (self.width * 0.83125 - self.width / 200 + offset[0],
                 self.height * 0.925 - self.height / 200 + offset[1])])
        elif 9 >= position > 0:
            pygame.draw.polygon(self.screen, color, [
                (self.width * (0.7479 - (position - 1) / 15) - self.width / 200 + offset[0],
                 self.height * 0.925 + self.height / 200 + offset[1]),
                (self.width * (0.7479 - (position - 1) / 15) + self.width / 200 + offset[0],
                 self.height * 0.925 + self.height / 200 + offset[1]),
                (self.width * (0.7479 - (position - 1) / 15) + self.width / 200 + offset[0],
                 self.height * 0.925 - self.height / 200 + offset[1]),
                (self.width * (0.7479 - (position - 1) / 15) - self.width / 200 + offset[0],
                 self.height * 0.925 - self.height / 200 + offset[1])])
        elif position == 10:
            pygame.draw.polygon(self.screen, color, [
                (self.width * 0.13125 - self.width / 200 + offset[0],
                 self.height * 0.925 + self.height / 200 + offset[1]),
                (self.width * 0.13125 + self.width / 200 + offset[0],
                 self.height * 0.925 + self.height / 200 + offset[1]),
                (self.width * 0.13125 + self.width / 200 + offset[0],
                 self.height * 0.925 - self.height / 200 + offset[1]),
                (self.width * 0.13125 - self.width / 200 + offset[0],
                 self.height * 0.925 - self.height / 200 + offset[1])])
        elif 20 >= position > 10:
            pygame.draw.polygon(self.screen, color, [
                (self.width * 0.13125 - self.width / 200 + offset[0],
                 self.height * (0.825 - (position - 11) * .7 / 9) + self.height / 200 + offset[1]),
                (self.width * 0.13125 + self.width / 200 + offset[0],
                 self.height * (0.825 - (position - 11) * .7 / 9) + self.height / 200 + offset[1]),
                (self.width * 0.13125 + self.width / 200 + offset[0],
                 self.height * (0.825 - (position - 11) * .7 / 9) - self.height / 200 + offset[1]),
                (self.width * 0.13125 - self.width / 200 + offset[0],
                 self.height * (0.825 - (position - 11) * .7 / 9) - self.height / 200 + offset[1])])
        elif 30 > position > 20:
            pygame.draw.polygon(self.screen, color, [
                (self.width * (0.215 + (position - 21) / 15) - self.width / 200 + offset[0],
                 self.height * 0.125 + self.height / 200 + offset[1]),
                (self.width * (0.215 + (position - 21) / 15) + self.width / 200 + offset[0],
                 self.height * 0.125 + self.height / 200 + offset[1]),
                (self.width * (0.215 + (position - 21) / 15) + self.width / 200 + offset[0],
                 self.height * 0.125 - self.height / 200 + offset[1]),
                (self.width * (0.215 + (position - 21) / 15) - self.width / 200 + offset[0],
                 self.height * 0.125 - self.height / 200 + offset[1])])
        elif position >= 30:
            pygame.draw.polygon(self.screen, color, [
                (self.width * 0.83125 - self.width / 200 + offset[0],
                 self.height * (0.125 + (position - 30) * .7 / 9) + self.height / 200 + offset[1]),
                (self.width * 0.83125 + self.width / 200 + offset[0],
                 self.height * (0.125 + (position - 30) * .7 / 9) + self.height / 200 + offset[1]),
                (self.width * 0.83125 + self.width / 200 + offset[0],
                 self.height * (0.125 + (position - 30) * .7 / 9) - self.height / 200 + offset[1]),
                (self.width * 0.83125 - self.width / 200 + offset[0],
                 self.height * (0.125 + (position - 30) * .7 / 9) - self.height / 200 + offset[1])])


    @staticmethod
    def draw_property(position, name, color, font, screen):
        label = font.render(name, True, color)
        position[0] = position[0]-label.get_width() / 2
        screen.blit(label, position)

    def update(self):
        self.draw_board()
        pygame.display.flip()
        self.clock.tick(20)
