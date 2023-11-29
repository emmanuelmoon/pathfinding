from tkinter import messagebox, Tk
import pygame
import sys

window_width = 500
window_height = 500

window = pygame.display.set_mode((window_width, window_height))

columns = 20
rows = 20

box_width = window_width // columns
box_height = window_height // rows

grid = []
path = []


class Box:
    def __init__(self, i, j):
        self.x = i
        self.y = j
        self.start = False
        self.wall = False
        self.target = False
        self.queued = False
        self.visited = False
        self.neighbours = []
        self.prior = None

    def draw(self, win, color):
        pygame.draw.rect(win, color, (self.x * box_width, self.y * box_height, box_width-2, box_height-2))

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
start_box.visited = False


def floyd_warshall(target_box):
    u = 0
    v = 0
    nodes = []
    for i in range(columns):
        for j in range(rows):
            nodes.append(grid[i][j])

    V = len(nodes)
    distance = [[float("inf") for _ in range(V)] for _ in range(V)]
    prev = [[None for _ in range(V)] for _ in range(V)]

    for i in range(V):
        for j in range(V):
            if nodes[i].target:
                v = i
            # If the nodes are neighbors, set the distance to 1
            if nodes[i] in nodes[j].neighbours and not nodes[i].wall and not nodes[j].wall:
                distance[i][j] = 1
                prev[i][j] = i

    # If the two nodes are the same, set the distance to 0
    for i in range(V):
        distance[i][i] = 0
        prev[i][i] = i
    # Iterate through all nodes in the list
    for k in range(V):
        # Update the distance matrix based on the current node
        if nodes[k].wall:
            continue
        for i in range(V):
            if nodes[i].wall:
                continue
            for j in range(V):
                if distance[i][j] > distance[i][k] + distance[k][j]:
                    distance[i][j] = distance[i][k] + distance[k][j]
                    prev[i][j] = prev[k][j]
    if prev[u][v] is None:
        Tk().wm_withdraw()
        messagebox.showinfo("No Solution", "There is no solution!")
    path.insert(0, nodes[v])
    while u != v:
        v = prev[u][v]
        path.insert(0, nodes[v])


def main():
    target_box_set = False
    target_box = None

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
            elif event.type == pygame.MOUSEBUTTONDOWN:
                if event.button == 3 and not target_box_set:
                    i = x // box_width
                    j = y // box_height
                    target_box = grid[i][j]
                    target_box.target = True
                    target_box_set = True
                elif event.button == 1:
                    i = x // box_width
                    j = y // box_height
                    grid[i][j].wall = True
            # Start Algorithm
            if event.type == pygame.KEYDOWN and target_box_set:
                floyd_warshall(target_box)

        window.fill((0, 0, 0))

        for i in range(columns):
            for j in range(rows):
                box = grid[i][j]
                box.draw(window, (100, 100, 100))

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
