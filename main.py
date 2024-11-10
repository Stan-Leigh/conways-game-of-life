import pygame
import random

pygame.init()

BLACK = (0, 0, 0)
GREY = (128, 128, 128)
GREEN = (0, 128, 0)

WIDTH, HEIGHT = 800, 800
TILE_SIZE = 20
GRID_WIDTH = WIDTH // TILE_SIZE
GRID_HEIGHT = HEIGHT // TILE_SIZE
FPS = 60

screen = pygame.display.set_mode((WIDTH, HEIGHT))

clock = pygame.time.Clock()

def gen(num):
    return set([(random.randrange(0, GRID_HEIGHT), random.randrange(0, GRID_WIDTH)) for _ in range(num)])

def draw_grid(positions):
    # Draw a green rectangle over the selected grid to show that it has been clicked.
    for position in positions:
        col, row = position
        top_left = (col * TILE_SIZE, row * TILE_SIZE)
        pygame.draw.rect(screen, GREEN, (*top_left, TILE_SIZE, TILE_SIZE))

    # Draw the horizontal grid line, which is a black line on a grey background.
    for row in range(GRID_HEIGHT):
        pygame.draw.line(screen, GREY, (0, row * TILE_SIZE), (WIDTH, row * TILE_SIZE))

    # Draw the vertical grid line, which is a black line on a grey background.
    for col in range(GRID_WIDTH):
        pygame.draw.line(screen, GREY, (col * TILE_SIZE, 0), (col * TILE_SIZE, HEIGHT))

def adjust_grid(positions):
    all_neighbors = set()
    new_positions = set()

    for position in positions:
        # Get the positions of all the neighbors
        neighbors = get_neighbors(position)
        # Add these neighbors to the all_neighbors set. The set ensures that there are no duplicates.
        all_neighbors.update(neighbors)

        # Get which neighbors are live cells
        neighbors = list(filter(lambda x: x in positions, neighbors))

        # Check if we need to keep the cell, i.e. if the cell is alive. Remember that a live cell has two or three live neighbors.
        if len(neighbors) in [2, 3]:
            new_positions.add(position)
    
    # Loop through all the neighbors of the live cell and check if they can come back to life.
    for position in all_neighbors:
        neighbors = get_neighbors(position)
        neighbors = list(filter(lambda x: x in positions, neighbors))

        # Check if we need to bring a dead cell back to life. Remember that a dead cell becomes alive when it has exactly three live neighbors.
        if len(neighbors) == 3:
            new_positions.add(position)
    
    return new_positions

def get_neighbors(pos):
    '''
    Returns all the neighbors of the selected grid position.
    '''
    x, y = pos
    neighbors = []
    for dx in [-1, 0, 1]:
        if x + dx < 0 or x + dx > GRID_WIDTH: # Account for the end of the grid.
            continue
        for dy in [-1, 0, 1]:
            if y + dy < 0 or y + dy > GRID_HEIGHT: # Account for the end of the grid.
                continue
            if dx == 0 and dy == 0: # Skip the currently selected grid because we only want its neighbors, not the grid itself.
                continue

            neighbors.append((x + dx, y + dy))
    
    return neighbors

def main():
    running = True
    playing = False
    count = 0
    update_freq = 120

    positions = set()
    while running:
        clock.tick(FPS)

        if playing:
            count += 1
        
        if count >= update_freq:
            count = 0
            positions = adjust_grid(positions)

        pygame.display.set_caption("Playing" if playing else "Paused")

        for event in pygame.event.get():
            # If the user clicks on the 'x' button to exit the game.
            if event.type == pygame.QUIT:
                running = False
            
            # Capture the position of the mouse-click
            if event.type == pygame.MOUSEBUTTONDOWN:
                x, y = pygame.mouse.get_pos()

                # Translate the pixel position to the column and row that was clicked on.
                col = x // TILE_SIZE
                row = y // TILE_SIZE
                pos = (col, row)

                # Add or remove positions on the grid. Click a grid to add, click on the same grid to remove.
                if pos in positions:
                    positions.remove(pos)
                else:
                    positions.add(pos)
            
            # Create new events to clear screen and randomly generate positions
            if event.type == pygame.KEYDOWN:
                # Check if the space bar is pressed for pausing or playing the simulation
                if event.key == pygame.K_SPACE:
                    playing = not playing
                
                # 'c' is the clear key to clear the screen
                if event.key == pygame.K_c:
                    positions = set()
                    playing = False
                    count = 0
                
                # 'g' is the generate key to randomly generate positions
                if event.key == pygame.K_g:
                    positions = gen(random.randrange(4, 10) * GRID_WIDTH)
    
        screen.fill(BLACK)
        draw_grid(positions)
        pygame.display.update()


    pygame.quit()

if __name__ == "__main__":
    main()