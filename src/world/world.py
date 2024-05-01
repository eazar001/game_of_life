from random import choice
from copy import deepcopy


class World:
    choices = [True, False]

    def __init__(self, width):
        self.width = width
        self.height = width

        self.cells = [[choice(World.choices) for _x in range(self.width)] for _y in range(self.height)]
        self.population = len([cell for row in self.cells for cell in row if cell])
        self.next_cells = deepcopy(self.cells)
        self.neighbors = []
        self.live_neighbors = [[0 for _x in range(self.width)] for _y in range(self.height)]
        self.changed = []
        self.generation = 0

        for y, row in enumerate(self.cells):
            self.neighbors.append([])

            for x, cell_state in enumerate(row):
                left = (x - 1) % self.width
                right = (x + 1) % self.width
                up = (y - 1) % self.width
                down = (y + 1) % self.width

                self.neighbors[y].append([(left, y), (right, y), (x, up), (x, down), (left, up), (right, up), (left, down), (right, down)])

                if cell_state:
                    for i, j in self.neighbors[y][x]:
                        self.live_neighbors[j][i] += 1

    def tick(self):
        self.calculate_next_cells()
        self.transition()

    def calculate_next_cells(self):
        self.changed = []

        # update the next state of all cells, using the current state of all the cells only, without updating the
        # current state
        for y, row in enumerate(self.cells):
            for x, cell_state in enumerate(row):
                live_neighbors = self.live_neighbors[y][x]

                match cell_state:
                    case True:
                        # death by underpopulation or overcrowding (becomes a dead cell)
                        if live_neighbors < 2 or live_neighbors > 3:
                            self.next_cells[y][x] = False
                            self.changed.append((x, y))
                    case _:
                        # is born (becomes a live cell)
                        if live_neighbors == 3:
                            self.next_cells[y][x] = True
                            self.changed.append((x, y))

    def transition(self):
        # now, we can finally transition all the changed cells to the next state
        for x, y in self.changed:
            self.cells[y][x] = self.next_cells[y][x]
            delta = 1 if self.cells[y][x] else -1

            self.population += delta

            for i, j in self.neighbors[y][x]:
                self.live_neighbors[j][i] += delta

        self.generation += 1
