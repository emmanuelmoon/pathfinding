from tkinter import messagebox, Tk
import pygame
import sys
import math

window_width = 800
window_height = 800

window = pygame.display.set_mode((window_width, window_height))

columns = 20
rows = 20

box_width = window_width // columns
box_height = window_height // rows

grid = []
open_set = []
closed_set = []
path = []


class Box:
    def __init__(self, i, j):
        self.x = i
        self.y = j
        self.start = False
        self.wall = False
        self.target = False
        self.visited = False
        self.neighbours = []
        self.g = float('inf')  # Cost from start node to current node
        self.h = 0  # Heuristic (Euclidean distance to target)
        self.f = float('inf')  # Total cost (g + h)
        self.prior = None

    def draw(self, win, color):
        pygame.draw.rect(win, color, (self.x * box_width, self.y * box_height, box_width - 2, box_height - 2))

    def set_neighbours(self):
        if self.x > 0:
            self.neighbours.append(grid[self.x - 1][self.y])
        if self.x < columns - 1:
            self.neighbours.append(grid[self.x + 1][self.y])
        if self.y > 0:
            self.neighbours.append(grid[self.x][self.y - 1])
        if self.y < rows - 1:
            self.neighbours.append(grid[self.x][self.y + 1])


# Create Grid
for i in range(columns):
    arr = []
    for j in range(rows):
        arr.append(Box(i, j))
    grid.append(arr)

# Set Neighbours
for i in range(columns):
    for j in range(rows):
        grid[i][j].set_neighbours()

start_box = grid[0][0]
start_box.start = True
start_box.visited = True
open_set.append(start_box)
start_box.g = 0
start_box.h = math.sqrt((start_box.x - (columns - 1)) ** 2 + (start_box.y - (rows - 1)) ** 2)
start_box.f = start_box.g + start_box.h


def heuristic(a, b):
    return math.sqrt((a.x - b.x) ** 2 + (a.y - b.y) ** 2)


def main():
    begin_search = False
    target_box_set = False
    searching = True
    target_box = grid[columns - 1][rows - 1]

    while True:
        for event in pygame.event.get():
            # Quit Window
            if event.type == pygame.QUIT:
                pygame.quit()
                sys.exit()
            # Mouse Controls
            elif event.type == pygame.MOUSEMOTION:
                x = pygame.mouse.get_pos()[0]
                y = pygame.mouse.get_pos()[1]
                # Draw Wall
                if event.buttons[0]:
                    i = x // box_width
                    j = y // box_height
                    grid[i][j].wall = True
                # Set Target
                if event.buttons[2] and not target_box_set:
                    i = x // box_width
                    j = y // box_height
                    target_box = grid[i][j]
                    target_box.target = True
                    target_box_set = True
            # Start Algorithm
            if event.type == pygame.KEYDOWN and target_box_set:
                begin_search = True

        if begin_search:
            if len(open_set) > 0 and searching:
                current_box = min(open_set, key=lambda x: x.f)
                open_set.remove(current_box)
                closed_set.append(current_box)

                if current_box == target_box:
                    searching = False
                    while current_box.prior is not None:
                        path.append(current_box.prior)
                        current_box = current_box.prior
                else:
                    for neighbour in current_box.neighbours:
                        if neighbour not in closed_set and not neighbour.wall:
                            tentative_g = current_box.g + 1  # Assuming a uniform cost of 1 for each step
                            if tentative_g < neighbour.g:
                                neighbour.prior = current_box
                                neighbour.g = tentative_g
                                neighbour.h = heuristic(neighbour, target_box)
                                neighbour.f = neighbour.g + neighbour.h
                                if neighbour not in open_set:
                                    open_set.append(neighbour)
            else:
                if searching:
                    Tk().wm_withdraw()
                    messagebox.showinfo("No Solution", "There is no solution!")
                    searching = False

        window.fill((0, 0, 0))

        for i in range(columns):
            for j in range(rows):
                box = grid[i][j]
                box.draw(window, (100, 100, 100))

                if box in open_set:
                    box.draw(window, (200, 0, 0))
                if box in closed_set:
                    box.draw(window, (0, 200, 0))
                if box in path:
                    box.draw(window, (0, 0, 200))

                if box.start:
                    box.draw(window, (0, 200, 200))
                if box.wall:
                    box.draw(window, (10, 10, 10))
                if box.target:
                    box.draw(window, (200, 200, 0))

        pygame.display.flip()


main()
