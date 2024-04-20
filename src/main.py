from world.world import World
import pygame


def main():
    pygame.init()
    screen = pygame.display.set_mode((1000, 1000))
    pygame.display.set_caption("Game of Life")
    clock = pygame.time.Clock()
    running = True

    screen.fill("black")

    w = World(screen, 100)

    while running:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                running = False

        w.tick()
        print(f'FPS: {clock.get_fps()}, generations: {w.generation}, population: {w.population}')
        pygame.display.flip()
        clock.tick(20)


if __name__ == '__main__':
    main()
