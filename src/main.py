import time

from world.world import World
import pygame


def main():
    pygame.init()
    screen = pygame.display.set_mode((1000, 1000))
    pygame.display.set_caption("Game of Life")
    clock = pygame.time.Clock()
    running = True

    screen.fill("black")

    height = width = 80
    scale = 0.7
    w = World(width)

    paused = False

    while running:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                running = False
            elif event.type == pygame.KEYDOWN and event.key == pygame.K_SPACE:
                paused = not paused

        if paused:
            time.sleep(0.05)
            continue

        w.tick()

        cell_width, cell_height = screen.get_width() / width, screen.get_height() / height

        for x, y in w.changed:
            if w.cells[y][x]:
                pygame.draw.rect(
                    screen,
                    "green",
                    (cell_width * x * scale, cell_height * y * scale, cell_width * scale, cell_height * scale),
                    0
                )
            else:
                pygame.draw.rect(
                    screen,
                    "black",
                    (cell_width * x * scale, cell_height * y * scale, cell_width * scale, cell_height * scale),
                    0
                )

        print(f'FPS: {clock.get_fps()}, generations: {w.generation}, population: {w.population}')
        pygame.display.flip()
        clock.tick(20)


if __name__ == '__main__':
    main()
