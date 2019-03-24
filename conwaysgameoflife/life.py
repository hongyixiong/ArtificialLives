
# alive_neighbours will return the number of neighbours alive for (cell_x, cell_y)
def alive_neighbours(self, cell_x, cell_y):
    alive = 0
    if cell_y > 0:
        if cell_x > 0:
            # diagonal left above
            alive += self.cells[cell_y - 1][cell_x - 1]
        # straight above
        alive += self.cells[cell_y - 1][cell_x]
        if cell_x < len(self.cells[0]) - 1:
            # diagonal right above
            alive += self.cells[cell_y - 1][cell_x + 1]
    if cell_y < len(self.cells) - 1:
        if cell_x > 0:
            # diagonal left below
            alive += self.cells[cell_y + 1][cell_x - 1]
        # straight below
        alive += self.cells[cell_y + 1][cell_x]
        if cell_x < len(self.cells[0]) - 1:
            # diagonal right below
            alive += self.cells[cell_y + 1][cell_x + 1]
    if cell_x > 0:
        # left
        alive += self.cells[cell_y][cell_x - 1]
    if cell_x < len(self.cells[0]) - 1:
        # right
        alive += self.cells[cell_y][cell_x + 1]
    return alive


# find_new_cell will determine if the cell (cell_x, cell_y) will be alive in the next generation
# it will return 1 if the cell will be alive in the next generation or 0 if the cell will be dead
# in the next generation
def find_new_cell(self, cell_x, cell_y):
    # calculate number of alive neighbours
    n = alive_neighbours(x, y)
    if self.cells[y][x] == 1:
        if n <= 1 or n >= 4:
            # cell dies in next generation
            return 0
        else:
            # cell lives
            return 1
    else:
        if n == 3:
            # a cell will be born
            return 1
        else:
            # cell stays dead
            return 0


def new_generation(self):
    # create a new cells list which is initialized to 0
    new_cells = [[0 * len(self.cells[0])] for _ in range(len(self.cells))]
    for y in range(len(self.cells)):
        for x in range(len(self.cells[0])):
            new_cells[y][x] = find_new_cell(x, y)

    self.cells = new_cells
