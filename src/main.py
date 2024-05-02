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

    height = width = 100
    scale = 0.75

    font = pygame.font.SysFont('consolas', size=17)

    w = World(width)

    paused = False

    frame_rate = 20

    while running:
        for event in pygame.event.get():
            if event.type == pygame.QUIT or (event.type == pygame.KEYDOWN and event.key == pygame.K_ESCAPE):
                running = False
            elif event.type == pygame.KEYDOWN and event.key == pygame.K_SPACE:
                paused = not paused
            elif event.type == pygame.KEYDOWN and event.key == pygame.K_UP:
                frame_rate += 1
            elif event.type == pygame.KEYDOWN and event.key == pygame.K_DOWN:
                frame_rate -= 1
            elif event.type == pygame.KEYDOWN and event.key == pygame.K_MINUS and width - 10 > 0:
                width -= 10
                height -= 10
                screen.fill("black")
                w = World(width)
            elif event.type == pygame.KEYDOWN and event.key == pygame.K_EQUALS and width + 100 < 601:
                width += 10
                height += 10
                screen.fill("black")
                w = World(width)
            elif event.type == pygame.KEYDOWN and event.key == pygame.K_RETURN:
                w = World(width)

        if paused:
            time.sleep(0.05)
            continue

        w.tick()

        cell_width, cell_height = screen.get_width() / width, screen.get_height() / height
        top = scale * screen.get_height()
        volume = width * width

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

        frame_rate_limit = font.render(f'Frame rate limit: {frame_rate}', True, (0xFF, 0xFF, 0xFF))
        fps = font.render(f'FPS: {clock.get_fps():.2f}', True, (0xFF, 0xFF, 0xFF))
        gens = font.render(f'Generation: {w.generation}', True, (0xFF, 0xFF, 0xFF))
        pop = font.render(f'Population: {w.population}', True, (0xFF, 0xFF, 0xFF))
        den = font.render(f'Density: {(w.population / volume):.2f}', True, (0xFF, 0xFF, 0xFF))
        n_count = font.render(f'Average neighbor count: {w.mean_neighbor_count:.2f}', True, (0xFF, 0xFF, 0xFF))
        dim = font.render(f'Dimensions: {w.width} x {w.height}', True, (0xFF, 0xFF, 0xFF))
        instr = font.render(f'Instructions: [ENTER] = new random configuration, [ESC] = quit, [-/=] = increase/decrease board size', True, (0xFF, 0xFF, 0xFF))
        instr2 = font.render(f'[UP/DOWN] = increase/decrease frame rate limit, [SPACE] = pause/play', True, (0xFF, 0xFF, 0xFF))

        bottom = top
        screen.blit(frame_rate_limit, (0, top))
        bottom += frame_rate_limit.get_height()

        screen.blit(fps, (0, bottom))
        bottom += fps.get_height()

        screen.blit(gens, (0, bottom))
        bottom += gens.get_height()

        screen.blit(pop, (0, bottom))
        bottom += pop.get_height()

        screen.blit(den, (0, bottom))
        bottom += pop.get_height()

        screen.blit(n_count, (0, bottom))
        bottom += n_count.get_height()

        screen.blit(dim, (0, bottom))
        bottom += dim.get_height()

        screen.blit(instr, (0, bottom))
        bottom += instr.get_height()

        screen.blit(instr2, (0, bottom))

        pygame.display.flip()
        clock.tick(frame_rate)

        screen.fill(
            "black",
            (0, top, max(fps.get_width(), gens.get_width(), pop.get_width(), den.get_width(), frame_rate_limit.get_width(), dim.get_width(), instr.get_width(), instr2.get_width(), n_count.get_width()),
             sum([fps.get_height(), gens.get_height(), pop.get_height(), den.get_height(), frame_rate_limit.get_height(), dim.get_height(), instr.get_height(), instr2.get_height(), n_count.get_height()]))
        )


if __name__ == '__main__':
    main()
