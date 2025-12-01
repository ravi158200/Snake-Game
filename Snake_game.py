# snake_game.py


import pygame
import sys
import random

# --- Configuration ---


CELL_SIZE = 20                                  # size of one grid cell in pixels
GRID_WIDTH = 30                                 # number of cells horizontally
GRID_HEIGHT = 20                                # number of cells vertically
SCREEN_WIDTH = CELL_SIZE * GRID_WIDTH
SCREEN_HEIGHT = CELL_SIZE * GRID_HEIGHT
FPS = 5                                        # game speed (frames per second). Increase to make it harder

# Colors (R,G,B)


WHITE = (255, 255, 255)
BLACK = (0, 0, 0)
GREEN = (0, 200, 0)
DARK_GREEN = (0, 120, 0)
RED = (200, 0, 0)
GRAY = (40, 40, 40)

# --- Helper functions ---


def random_food_position(snake):
    """Return a random grid position not occupied by the snake."""
    while True:
        pos = (random.randint(0, GRID_WIDTH - 1), random.randint(0, GRID_HEIGHT - 1))
        if pos not in snake:
            return pos

def draw_rect_at(surface, color, grid_pos):
    x, y = grid_pos
    rect = pygame.Rect(x * CELL_SIZE, y * CELL_SIZE, CELL_SIZE, CELL_SIZE)
    pygame.draw.rect(surface, color, rect)

# --- Game initialization ---


pygame.init()
screen = pygame.display.set_mode((SCREEN_WIDTH, SCREEN_HEIGHT))
clock = pygame.time.Clock()
pygame.display.set_caption("Snake Game (Python / Pygame)")

# --- Initial game state ---


snake = [(GRID_WIDTH // 2, GRID_HEIGHT // 2),
         (GRID_WIDTH // 2 - 1, GRID_HEIGHT // 2),
         (GRID_WIDTH // 2 - 2, GRID_HEIGHT // 2)]
direction = (1, 0)  # moving right initially
food = random_food_position(snake)
score = 0
game_over = False
font = pygame.font.SysFont(None, 30)

# --- Main loop ---


while True:
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            pygame.quit()
            sys.exit()
        elif event.type == pygame.KEYDOWN:
            # Prevent reversing direction directly
            if event.key == pygame.K_UP and direction != (0, 1):
                direction = (0, -1)
            elif event.key == pygame.K_DOWN and direction != (0, -1):
                direction = (0, 1)
            elif event.key == pygame.K_LEFT and direction != (1, 0):
                direction = (-1, 0)
            elif event.key == pygame.K_RIGHT and direction != (-1, 0):
                direction = (1, 0)
            elif event.key == pygame.K_r and game_over:
                # restart
                snake = [(GRID_WIDTH // 2, GRID_HEIGHT // 2),
                         (GRID_WIDTH // 2 - 1, GRID_HEIGHT // 2),
                         (GRID_WIDTH // 2 - 2, GRID_HEIGHT // 2)]
                direction = (1, 0)
                food = random_food_position(snake)
                score = 0
                game_over = False

    if not game_over:

        
        # Move snake: compute new head

        
        head_x, head_y = snake[0]
        dx, dy = direction
        new_head = (head_x + dx, head_y + dy)

        # Check wall collision

        
        if (new_head[0] < 0 or new_head[0] >= GRID_WIDTH or
            new_head[1] < 0 or new_head[1] >= GRID_HEIGHT):
            game_over = True

        # Check self collision

        
        elif new_head in snake:
            game_over = True
        else:
            # Insert new head

            
            snake.insert(0, new_head)

            # Check if food eaten

            
            if new_head == food:
                score += 1

                
                # place new food

                
                food = random_food_position(snake)
            else:
                
                # remove tail

                
                snake.pop()

    # --- Rendering ---

    
    screen.fill(BLACK)

    # Draw grid (optional)

    
    for x in range(0, SCREEN_WIDTH, CELL_SIZE):
        pygame.draw.line(screen, GRAY, (x, 0), (x, SCREEN_HEIGHT))
    for y in range(0, SCREEN_HEIGHT, CELL_SIZE):
        pygame.draw.line(screen, GRAY, (0, y), (SCREEN_WIDTH, y))

    # Draw food

    
    draw_rect_at(screen, RED, food)

    # Draw snake (head darker)

    
    if snake:
        draw_rect_at(screen, DARK_GREEN, snake[0])
        for segment in snake[1:]:
            draw_rect_at(screen, GREEN, segment)

    # Draw score

    score_surf = font.render(f"Score: {score}", True, WHITE)
    screen.blit(score_surf, (10, 10))

    # Game over message

    
    if game_over:
        over_surf = font.render("Game Over! Press R to restart.", True, WHITE)
        rect = over_surf.get_rect(center=(SCREEN_WIDTH // 2, SCREEN_HEIGHT // 2))
        screen.blit(over_surf, rect)

    pygame.display.flip()
    clock.tick(FPS)
