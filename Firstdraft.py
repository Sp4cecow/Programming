import pygame
import time
import random

# Initialize Pygame
pygame.init()

# Screen dimensions
width, height = 600, 400
block_size = 20  # Size of the snake block
fps = 5  # Frames per second

# Colors
white = (255, 255, 255)
black = (0, 0, 0)
red = (200, 0, 0)
green = (0, 200, 0)
blue = (0, 0, 255)

#levels 
level = 1
score_to_next_level = 10 # the score increasews every ten levels

# Initialize the screen
screen = pygame.display.set_mode((width, height))
pygame.display.set_caption("Snake Game")

# Clock for controlling the game speed
clock = pygame.time.Clock()

# Font for displaying score
font_style = pygame.font.SysFont("bahnschrift", 25)
score_font = pygame.font.SysFont("comicsansms", 35)

# Display the score
def display_score(score, level):
    score_text = score_font.render(f"Score: {score}", True, green)
    level_text = score_font.render(f"Level: {level}", True, blue)
    screen.blit(score_text, [0, 0])
    screen.blit(level_text, [0, 30])

# Display a message
def message(msg, color):
    mesg = font_style.render(msg, True, color)
    screen.blit(mesg, [width / 6, height / 3])

# Main game loop
def game_loop():
    global fps, level
    
    game_over = False
    game_close = False

    x, y = width // 2, height // 2  # Initial position of the snake
    x_change, y_change = 0, 0

    snake_list = []
    snake_length = 1

    # Food position
    food_x = round(random.randrange(0, width - block_size) / block_size) * block_size
    food_y = round(random.randrange(0, height - block_size) / block_size) * block_size

    while not game_over:
       
        while game_close:
            screen.fill(black)
            message("You lost! Press Q-Quit or C-Play Again", red)
            display_score(snake_length - 1)
            pygame.display.update()

            for event in pygame.event.get():
                if event.type == pygame.KEYDOWN:
                    if event.key == pygame.K_q:
                        game_over = True
                        game_close = False
                    if event.key == pygame.K_c:
                        game_loop()

        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                game_over = True
            if event.type == pygame.KEYDOWN:
                if event.key == pygame.K_LEFT and x_change == 0:
                    x_change = -block_size
                    y_change = 0
                elif event.key == pygame.K_RIGHT and x_change == 0:
                    x_change = block_size
                    y_change = 0
                elif event.key == pygame.K_UP and y_change == 0:
                    y_change = -block_size
                    x_change = 0
                elif event.key == pygame.K_DOWN and y_change == 0:
                    y_change = block_size
                    x_change = 0

        if x >= width or x < 0 or y >= height or y < 0:
            game_close = True

        x += x_change
        y += y_change
        screen.fill(black)
        pygame.draw.rect(screen, blue, [food_x, food_y, block_size, block_size])

        snake_head = [x, y]
        snake_list.append(snake_head)
        if len(snake_list) > snake_length:
            del snake_list[0]

        for block in snake_list[:-1]:
            if block == snake_head:
                game_close = True

        for segment in snake_list:
            pygame.draw.rect(screen, green, [segment[0], segment[1], block_size, block_size])

        # Level progression
        if (snake_length - 1) % score_to_next_level == 0 and snake_length > 1:
            level += 1
            fps += 5  # Increase speed

        
        display_score(snake_length - 1, level)
        pygame.display.update()

        if x == food_x and y == food_y:
            food_x = round(random.randrange(0, width - block_size) / block_size) * block_size
            food_y = round(random.randrange(0, height - block_size) / block_size) * block_size
            snake_length += 1

        clock.tick(fps)

    pygame.quit()
    quit()

# Run the game
game_loop()
