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