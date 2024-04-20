from random import randint
from copy import deepcopy
import pygame


# increment the neighbor count of a cell state by n
def set_live_neighbors(cell_state, n):
    return ((cell_state >> 1) + n) << 1 if not cell_state & 1 else (((cell_state >> 1) + n) << 1) ^ 1


class World:
    def __init__(self, screen, width):
        self.width = width
        self.height = width

        self.cells = [[randint(0, 1) for _x in range(self.width)] for _y in range(self.height)]
        self.population = len([cell for row in self.cells for cell in row if cell])
        self.neighbors = []
        self.screen = screen
        self.generation = 0

        self.cell_width, self.cell_height = screen.get_width() / self.width, screen.get_height() / self.height

        for y, row in enumerate(self.cells):
            self.neighbors.append([])

            for x, cell_state in enumerate(row):
                left = (x - 1) % self.width
                right = (x + 1) % self.width
                up = (y - 1) % self.width
                down = (y + 1) % self.width

                self.neighbors[y].append([(left, y), (right, y), (x, up), (x, down), (left, up), (right, up), (left, down), (right, down)])

                if cell_state & 1:
                    for i, j in self.neighbors[y][x]:
                        self.cells[j][i] = set_live_neighbors(self.cells[j][i], 1)
                        # self.live_neighbors[j][i] += 1

        self.next_cells = deepcopy(self.cells)

    def tick(self):
        changed = []

        # update the next state of all cells, using the current state of all the cells only, without updating the
        # current state
        for y, row in enumerate(self.cells):
            for x, cell_state in enumerate(row):
                match cell_state:
                    case 1 | 3 | 9 | 11 | 13 | 15 | 17:
                        # death by underpopulation or overcrowding (becomes a dead cell)
                        self.next_cells[y][x] ^= 1

                        pygame.draw.rect(
                            self.screen,
                            "black",
                            (self.cell_width * x, self.cell_height * y, self.cell_width, self.cell_height),
                            0
                        )

                        changed.append((x, y))
                    case 6:
                        # is born (becomes a live cell)
                        self.next_cells[y][x] ^= 1

                        pygame.draw.rect(
                            self.screen,
                            "green",
                            (self.cell_width * x, self.cell_height * y, self.cell_width, self.cell_height),
                            0
                        )

                        changed.append((x, y))

        # now, we can finally transition all the changed cells to the next state
        for x, y in changed:
            self.cells[y][x] = self.next_cells[y][x]
            delta = 1 if self.cells[y][x] & 1 else -1

            self.population += delta

            for i, j in self.neighbors[y][x]:
                self.cells[j][i] = self.next_cells[j][i] = set_live_neighbors(self.next_cells[j][i], delta)

        self.generation += 1
