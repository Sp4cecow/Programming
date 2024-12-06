import pygame
import time
import random

# Initialize Pygame
pygame.init()

# Screen dimensions
base_width, base_height = 600, 400
block_size = 20  # Size of the snake block
fps = 5  # Frames per second

# Generate new food position
def generate_food(grid_width, grid_height, obstacles):
    while True:
        x = random.randrange(0, grid_width) * block_size
        y = random.randrange(0, grid_height) * block_size
        if (x, y) not in obstacles:
            return x, y

# Colors
white = (255, 255, 255)
black = (0, 0, 0)
red = (200, 0, 0)
green = (0, 200, 0)
blue = (0, 0, 255)
gray = (169, 169, 169)

# Levels 
level = 1
score_to_next_level = 2  # The score increases every two levels

# Obstacles
max_obstacles = 5

def generate_obstacles(level, grid_width, grid_height, snake_list, food_x, food_y):
    obstacles = []
    if level > 1:
        num_obstacles = min(level, max_obstacles)  # Limit number of obstacles
        for _ in range(num_obstacles):
            while True:
                x = random.randrange(0, grid_width) * block_size
                y = random.randrange(0, grid_height) * block_size
                if (x, y) not in snake_list and (x, y) != (food_x, food_y):
                    obstacles.append((x, y))
                    break
    return obstacles

# Check if the snake collides with any obstacle
def check_collision_with_obstacles(snake_head, obstacles):
    return tuple(snake_head) in obstacles

# Initialize the screen
screen = pygame.display.set_mode((base_width, base_height))
pygame.display.set_caption("Snake Game")

# Clock for controlling the game speed
clock = pygame.time.Clock()

# Font for displaying score
font_style = pygame.font.SysFont("bahnschrift", 25)
score_font = pygame.font.SysFont("comicsansms", 35)

# Random color generator
def random_color():
    return random.randint(0, 255), random.randint(0, 255), random.randint(0, 255)

# Display the score
def display_score(score, level):
    score_text = score_font.render(f"Score: {score}", True, green)
    level_text = score_font.render(f"Level: {level}", True, blue)
    screen.blit(score_text, [0, 0])
    screen.blit(level_text, [0, 30])

# Display a message
def message(msg, color):
    mesg = font_style.render(msg, True, color)
    screen.blit(mesg, [base_width / 6, base_height / 3])

# Main game loop
def game_loop():
    global fps, level, max_obstacles, block_size, screen, score_to_next_level
    
    game_over = False
    game_close = False

    x, y = base_width // 2, base_height // 2  # Initial position of the snake
    x_change, y_change = 0, 0

    snake_list = []
    snake_length = 1
    score = 0

    # Food position
    grid_width = base_width // block_size
    grid_height = base_height // block_size
    food_x, food_y = generate_food(grid_width, grid_height, [])

    obstacles = generate_obstacles(level, grid_width, grid_height, snake_list, food_x, food_y)  # Initialize obstacles list

    snake_color = green
    food_color = blue

    while not game_over:
       
        while game_close:
            screen.fill(black)
            message("You lost! Press Q-Quit or C-Play Again", red)
            display_score(score, level)
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

        if x >= base_width or x < 0 or y >= base_height or y < 0:
            game_close = True

        x += x_change
        y += y_change
        
        screen.fill(black)
        pygame.draw.rect(screen, food_color, [food_x, food_y, block_size, block_size])

        snake_head = [x, y]
        snake_list.append(snake_head)
        if len(snake_list) > snake_length:
            del snake_list[0]

        for block in snake_list[:-1]:
            if block == snake_head:
                game_close = True

        for segment in snake_list:
            pygame.draw.rect(screen, snake_color, [segment[0], segment[1], block_size, block_size])

        # Check if snake collides with obstacles
        if check_collision_with_obstacles(snake_head, obstacles):
            game_close = True

        # Level progression
        if score >= score_to_next_level:
            level += 1
            fps += 2  # Gradual speed increase
            score_to_next_level += 2  # Update score needed for next level
            snake_length = 1  # Reset score
            max_obstacles += 1

            # Generate new obstacles and food position based on the new level
            obstacles = generate_obstacles(level, grid_width, grid_height, snake_list, food_x, food_y)
            food_x, food_y = generate_food(grid_width, grid_height, obstacles)

            # Change snake and food colors
            snake_color = random_color()
            food_color = random_color()

        # Draw obstacles
        for obstacle in obstacles:
            pygame.draw.rect(screen, gray, [obstacle[0], obstacle[1], block_size, block_size])

        display_score(score, level)
        pygame.display.update()

        if x == food_x and y == food_y:
            food_x, food_y = generate_food(grid_width, grid_height, obstacles)  # Generate new food
            snake_length += 1
            score += 1

        clock.tick(fps)

    pygame.quit()
    quit()

# Run the game
game_loop()

#tests
import unittest
import random
import pygame

# Assuming the functions generate_food, generate_obstacles, and game_loop are available
# Also assuming check_collision_with_obstacles is available

class TestSnakeGame(unittest.TestCase):

    def setUp(self):
        self.grid_width = 30
        self.grid_height = 20
        self.block_size = 20
        self.snake_list = [(100, 100), (120, 100), (140, 100)]
        self.food_x, self.food_y = 60, 80

    def test_food_and_obstacles_not_collide(self):
        # Generate obstacles
        level = 3
        obstacles = generate_obstacles(level, self.grid_width, self.grid_height, self.snake_list, self.food_x, self.food_y)

        # Generate food
        food_x, food_y = generate_food(self.grid_width, self.grid_height, obstacles)

        # Check that the food is not placed on any obstacle
        self.assertNotIn((food_x, food_y), obstacles, "Food spawned on an obstacle")

    def test_food_and_snake_not_collide(self):
        # Generate food
        obstacles = []
        food_x, food_y = generate_food(self.grid_width, self.grid_height, obstacles)

        # Check that the food is not placed on the snake
        self.assertNotIn((food_x, food_y), self.snake_list, "Food spawned on the snake")

    def test_obstacles_and_snake_not_collide(self):
        # Generate obstacles
        level = 3
        obstacles = generate_obstacles(level, self.grid_width, self.grid_height, self.snake_list, self.food_x, self.food_y)

        # Check that no obstacle is placed on the snake
        for obstacle in obstacles:
            self.assertNotIn(obstacle, self.snake_list, "Obstacle spawned on the snake")

    def test_obstacles_and_food_not_collide(self):
        # Generate obstacles
        level = 3
        obstacles = generate_obstacles(level, self.grid_width, self.grid_height, self.snake_list, self.food_x, self.food_y)

        # Check that no obstacle is placed on the food
        self.assertNotIn((self.food_x, self.food_y), obstacles, "Obstacle spawned on the food")
    
    def test_snake_spawns_correctly(self):
        # Check that the snake spawns in the initial position
        expected_initial_snake = [(100, 100), (120, 100), (140, 100)]
        self.assertEqual(self.snake_list, expected_initial_snake, "Snake did not spawn in the correct initial position")
        
    def test_food_spawns_correctly(self):
        # Check that the food spawns in the initial position
        expected_initial_food = (60, 80)
        self.assertEqual((self.food_x, self.food_y), expected_initial_food, "Food did not spawn in the correct initial position")

    def test_game_ends_on_obstacle_collision(self):
        # Simulate game scenario where the snake collides with an obstacle
        snake_head = [100, 100]
        obstacles = [(100, 100), (120, 120), (140, 140)]

        # Check collision
        collision = check_collision_with_obstacles(snake_head, obstacles)

        # Ensure game ends on collision
        self.assertTrue(collision, "Game did not end on obstacle collision")

if __name__ == "__main__":
    unittest.main()
