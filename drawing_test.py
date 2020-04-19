import Visualizer
import pygame
import MonoSim


if __name__ == "__main__":
    sim = MonoSim.Simulation(4)

    board = Visualizer.Visualizer(sim)

    board.update()

    while not board.done:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                board.done = True
            if event.type == pygame.KEYUP and event.key == pygame.K_ESCAPE:
                board.done = True

        # board.update()
