from tkinter import messagebox, Tk
import pygame
import sys

# Height and width of dialog box
window_width = 500
window_height = 500

# Sets the width and height for pygame dialog box
window = pygame.display.set_mode((window_width, window_height))

columns = 25
rows = 25

box_width = window_width // columns
box_height = window_height // rows

# Stores the boxes
grid = []


class Box:
    # Holds the position of the boxes
    def __init__(self, i, j):
        self.x = i
        self.y = j
        self.start = False
        self.wall = False
        self.target = False

    # Subtract 2 to create border between boxes
    def draw(self, win, color):
        pygame.draw.rect(win, color, (self.x * box_width, self.y * box_height, box_width - 2, box_height - 2))


# Create the actual grid
for i in range(columns):
    arr = []
    for j in range(rows):
        arr.append(Box(i, j))
    grid.append(arr)


start_box = grid[0][0]
start_box.start = True


def main():
    begin_search = False
    target_box_set = False

    while True:
        for event in pygame.event.get():
            # Allows to close the window
            if event.type == pygame.QUIT:
                pygame.quit()
                sys.exit()

            # Mouse controls
            elif event.type == pygame.MOUSEMOTION:
                x = pygame.mouse.get_pos()[0]
                y = pygame.mouse.get_pos()[1]

                # Draw wall
                if event.buttons[0]:
                    i = x // box_width
                    j = y // box_height
                    grid[i][j].wall = True

                # Set target
                if event.buttons[2] and not target_box_set:
                    i = x // box_width
                    j = y // box_width
                    target_box = grid[i][j]
                    target_box.target = True
                    target_box_set = True

            # Start searching
            if event.type == pygame.KEYDOWN and target_box_set:
                begin_search = True

        # Fills with color black
        window.fill((0, 0, 0))

        for i in range(columns):
            for j in range(rows):
                box = grid[i][j]
                box.draw(window, (50, 50, 50))
                if box.start:
                    box.draw(window, (0, 200, 200))
                if box.wall:
                    box.draw(window, (90, 90, 90))
                if box.target:
                    box.draw(window, (200, 200, 0))

        # Updates the display
        pygame.display.flip()


main()
