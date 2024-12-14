import pygame
import random
import sys

# Initialize Pygame
pygame.init()

# Constants
SCREEN_WIDTH = 800
SCREEN_HEIGHT = 600
GRID_SIZE = 20
GRID_WIDTH = SCREEN_WIDTH // GRID_SIZE
GRID_HEIGHT = SCREEN_HEIGHT // GRID_SIZE

# Colors
BLACK = (0, 0, 0)
WHITE = (255, 255, 255)
RED = (255, 0, 0)
GREEN = (0, 255, 0)

# Initialize screen
screen = pygame.display.set_mode((SCREEN_WIDTH, SCREEN_HEIGHT))
pygame.display.set_caption('Snake Game')

class Snake:
    def __init__(self):
        self.positions = [(GRID_WIDTH // 2, GRID_HEIGHT // 2)]
        self.direction = (1, 0)
        self.grow_next = False

    def get_head_position(self):
        return self.positions[0]

    def update(self):
        current = self.get_head_position()
        x, y = self.direction
        new = ((current[0] + x) % GRID_WIDTH, (current[1] + y) % GRID_HEIGHT)
        
        if new in self.positions[1:]:
            return False  # Game Over
        
        self.positions.insert(0, new)
        if not self.grow_next:
            self.positions.pop()
        else:
            self.grow_next = False
        return True

    def grow(self):
        self.grow_next = True

class Food:
    def __init__(self):
        self.position = (0, 0)
        self.spawn()

    def spawn(self, snake_positions=None):
        if snake_positions is None:
            snake_positions = []
        while True:
            x = random.randint(0, GRID_WIDTH - 1)
            y = random.randint(0, GRID_HEIGHT - 1)
            if (x, y) not in snake_positions:
                self.position = (x, y)
                break

class Game:
    def __init__(self):
        self.snake = Snake()
        self.food = Food()
        self.score = 0
        self.font = pygame.font.Font(None, 36)
        self.welcome_font = pygame.font.Font(None, 32)  # Reduced welcome message font size
        self.game_over = False
        self.clock = pygame.time.Clock()

    def handle_events(self):
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                return False
            elif event.type == pygame.KEYDOWN:
                if self.game_over:
                    if event.key == pygame.K_r:
                        self.__init__()  # Reset game
                    elif event.key == pygame.K_q:
                        return False
                else:
                    if event.key == pygame.K_UP and self.snake.direction != (0, 1):
                        self.snake.direction = (0, -1)
                    elif event.key == pygame.K_DOWN and self.snake.direction != (0, -1):
                        self.snake.direction = (0, 1)
                    elif event.key == pygame.K_LEFT and self.snake.direction != (1, 0):
                        self.snake.direction = (-1, 0)
                    elif event.key == pygame.K_RIGHT and self.snake.direction != (-1, 0):
                        self.snake.direction = (1, 0)
        return True

    def update(self):
        if not self.game_over:
            if not self.snake.update():
                self.game_over = True
                return

            if self.snake.get_head_position() == self.food.position:
                self.snake.grow()
                self.food.spawn(self.snake.positions)
                self.score += 1

    def draw(self):
        screen.fill(BLACK)
        
        # Draw welcome message with smaller font
        welcome_text = self.welcome_font.render('Welcome Moses Jackson, This snake game is created by Moses Jackson', True, WHITE)
        welcome_rect = welcome_text.get_rect(center=(SCREEN_WIDTH/2, 40))
        screen.blit(welcome_text, welcome_rect)
        
        # Draw snake
        for position in self.snake.positions:
            rect = pygame.Rect(position[0] * GRID_SIZE, position[1] * GRID_SIZE,
                             GRID_SIZE - 2, GRID_SIZE - 2)
            pygame.draw.rect(screen, GREEN, rect)

        # Draw food
        food_rect = pygame.Rect(self.food.position[0] * GRID_SIZE,
                              self.food.position[1] * GRID_SIZE,
                              GRID_SIZE - 2, GRID_SIZE - 2)
        pygame.draw.rect(screen, RED, food_rect)

        # Draw score
        score_text = self.font.render(f'Score: {self.score}', True, WHITE)
        screen.blit(score_text, (10, 70))  # Moved down to accommodate welcome message

        if self.game_over:
            game_over_text = self.font.render('Game Over! Press R to restart or Q to quit', True, WHITE)
            text_rect = game_over_text.get_rect(center=(SCREEN_WIDTH/2, SCREEN_HEIGHT/2))
            screen.blit(game_over_text, text_rect)

        pygame.display.flip()

    def run(self):
        running = True
        while running:
            running = self.handle_events()
            self.update()
            self.draw()
            self.clock.tick(10)  # Control game speed

def main():
    game = Game()
    game.run()
    pygame.quit()
    sys.exit()

if __name__ == '__main__':
    main()