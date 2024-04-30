from world.world import World
import pygame


def main():
    pygame.init()
    screen = pygame.display.set_mode((1000, 1000))
    pygame.display.set_caption("Game of Life")
    clock = pygame.time.Clock()
    running = True

    screen.fill("black")

    height = width = 400
    w = World(width)

    while running:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                running = False

        w.tick()
        w.transition()

        cell_width, cell_height = screen.get_width() / width, screen.get_height() / height

        for x, y in w.changed:
            if w.cells[y][x]:
                pygame.draw.rect(
                    screen,
                    "green",
                    (cell_width * x, cell_height * y, cell_width, cell_height),
                    0
                )
            else:
                pygame.draw.rect(
                    screen,
                    "black",
                    (cell_width * x, cell_height * y, cell_width, cell_height),
                    0
                )

        print(f'FPS: {clock.get_fps()}, generations: {w.generation}, population: {w.population}')
        pygame.display.flip()
        clock.tick()


if __name__ == '__main__':
    main()
