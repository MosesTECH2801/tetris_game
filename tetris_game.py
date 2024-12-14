import pygame
import random
from typing import List, Tuple

# Initialize Pygame
pygame.init()

# Constants
BLOCK_SIZE = 30
GRID_WIDTH = 10
GRID_HEIGHT = 20
SCREEN_WIDTH = BLOCK_SIZE * (GRID_WIDTH + 6)  # Extra space for next piece display
SCREEN_HEIGHT = BLOCK_SIZE * GRID_HEIGHT

# Colors
BLACK = (0, 0, 0)
WHITE = (255, 255, 255)
CYAN = (0, 255, 255)    # I piece
YELLOW = (255, 255, 0)  # O piece
PURPLE = (128, 0, 128)  # T piece
BLUE = (0, 0, 255)      # J piece
ORANGE = (255, 165, 0)  # L piece
GREEN = (0, 255, 0)     # S piece
RED = (255, 0, 0)       # Z piece

# Tetromino shapes and their colors
SHAPES = {
    'I': [['.....',
           '.....',
           'XXXX.',
           '.....',
           '.....'], CYAN],
    'O': [['.....',
           '.....',
           '.XX..',
           '.XX..',
           '.....'], YELLOW],
    'T': [['.....',
           '.....',
           '.XXX.',
           '..X..',
           '.....'], PURPLE],
    'L': [['.....',
           '.....',
           '.XXX.',
           '.X...',
           '.....'], BLUE],
    'J': [['.....',
           '.....',
           '.XXX.',
           '...X.',
           '.....'], ORANGE],
    'S': [['.....',
           '.....',
           '..XX.',
           '.XX..',
           '.....'], GREEN],
    'Z': [['.....',
           '.....',
           '.XX..',
           '..XX.',
           '.....'], RED]
}

class Tetris:
    def __init__(self):
        self.screen = pygame.display.set_mode((SCREEN_WIDTH, SCREEN_HEIGHT))
        pygame.display.set_caption('Tetris')
        self.clock = pygame.time.Clock()
        self.grid = [[BLACK for _ in range(GRID_WIDTH)] for _ in range(GRID_HEIGHT)]
        self.current_piece = None
        self.next_piece = None
        self.score = 0
        self.level = 1
        self.game_over = False
        self.fall_speed = 1000  # milliseconds
        self.last_fall_time = 0
        
    def new_piece(self) -> None:
        """Create a new tetromino piece"""
        if not self.next_piece:
            self.next_piece = random.choice(list(SHAPES.keys()))
        self.current_piece = {
            'shape': self.next_piece,
            'rotation': 0,
            'x': GRID_WIDTH // 2 - 2,
            'y': 0
        }
        self.next_piece = random.choice(list(SHAPES.keys()))
        
        # Check if game is over
        if self.check_collision():
            self.game_over = True

    def show_start_screen(self) -> None:
        """Display the welcome message"""
        self.screen.fill(BLACK)
        font = pygame.font.Font(None, 36)
        text1 = font.render("Welcome to Tetris Game", True, WHITE)
        text2 = font.render("The game is created by Moses Jackson", True, WHITE)
        
        text1_rect = text1.get_rect(center=(SCREEN_WIDTH//2, SCREEN_HEIGHT//2 - 20))
        text2_rect = text2.get_rect(center=(SCREEN_WIDTH//2, SCREEN_HEIGHT//2 + 20))
        
        self.screen.blit(text1, text1_rect)
        self.screen.blit(text2, text2_rect)
        pygame.display.flip()
        
        # Wait for a few seconds or key press
        waiting = True
        start_time = pygame.time.get_ticks()
        while waiting:
            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    pygame.quit()
                    exit()
                if event.type == pygame.KEYDOWN:
                    waiting = False
            if pygame.time.get_ticks() - start_time > 3000:  # 3 seconds
                waiting = False
    def check_collision(self) -> bool:
        """Check if the current piece collides with anything"""
        piece_shape = SHAPES[self.current_piece['shape']][0]
        for y, row in enumerate(piece_shape):
            for x, cell in enumerate(row):
                if cell == 'X':
                    abs_x = self.current_piece['x'] + x
                    abs_y = self.current_piece['y'] + y
                    
                    if (abs_x < 0 or abs_x >= GRID_WIDTH or 
                        abs_y >= GRID_HEIGHT or 
                        (abs_y >= 0 and self.grid[abs_y][abs_x] != BLACK)):
                        return True
        return False

    def rotate_piece(self) -> None:
        """Rotate the current piece"""
        original_rotation = self.current_piece['rotation']
        self.current_piece['rotation'] = (self.current_piece['rotation'] + 1) % 4
        
        if self.check_collision():
            self.current_piece['rotation'] = original_rotation

    def clear_rows(self) -> None:
        """Clear completed rows and update score"""
        rows_cleared = 0
        y = GRID_HEIGHT - 1
        while y >= 0:
            if all(color != BLACK for color in self.grid[y]):
                rows_cleared += 1
                # Move all rows above down
                for move_y in range(y, 0, -1):
                    self.grid[move_y] = self.grid[move_y - 1][:]
                self.grid[0] = [BLACK] * GRID_WIDTH
            else:
                y -= 1

        # Update score
        if rows_cleared == 1:
            self.score += 100
        elif rows_cleared == 2:
            self.score += 300
        elif rows_cleared == 3:
            self.score += 500
        elif rows_cleared == 4:
            self.score += 800

        # Update level
        if self.score >= self.level * 1000:
            self.level += 1
            self.fall_speed = max(100, 1000 - (self.level - 1) * 100)

    def draw_grid(self) -> None:
        """Draw the game grid and current piece"""
        # Draw the fixed blocks
        for y in range(GRID_HEIGHT):
            for x in range(GRID_WIDTH):
                pygame.draw.rect(self.screen, self.grid[y][x],
                               (x * BLOCK_SIZE, y * BLOCK_SIZE, BLOCK_SIZE - 1, BLOCK_SIZE - 1))

        # Draw the current piece
        if self.current_piece:
            piece_shape = SHAPES[self.current_piece['shape']][0]
            piece_color = SHAPES[self.current_piece['shape']][1]
            
            for y, row in enumerate(piece_shape):
                for x, cell in enumerate(row):
                    if cell == 'X':
                        pygame.draw.rect(self.screen, piece_color,
                                       ((self.current_piece['x'] + x) * BLOCK_SIZE,
                                        (self.current_piece['y'] + y) * BLOCK_SIZE,
                                        BLOCK_SIZE - 1, BLOCK_SIZE - 1))

    def draw_next_piece(self) -> None:
        """Draw the next piece preview"""
        # Clear the preview area
        preview_x = GRID_WIDTH * BLOCK_SIZE + 20
        preview_y = 50
        pygame.draw.rect(self.screen, BLACK, 
                        (preview_x, preview_y, 5 * BLOCK_SIZE, 5 * BLOCK_SIZE))

        # Draw the next piece
        if self.next_piece:
            piece_shape = SHAPES[self.next_piece][0]
            piece_color = SHAPES[self.next_piece][1]
            
            for y, row in enumerate(piece_shape):
                for x, cell in enumerate(row):
                    if cell == 'X':
                        pygame.draw.rect(self.screen, piece_color,
                                       (preview_x + x * BLOCK_SIZE,
                                        preview_y + y * BLOCK_SIZE,
                                        BLOCK_SIZE - 1, BLOCK_SIZE - 1))

    def draw_score(self) -> None:
        """Draw the score and level information"""
        font = pygame.font.Font(None, 36)
        score_text = font.render(f'Score: {self.score}', True, WHITE)
        level_text = font.render(f'Level: {self.level}', True, WHITE)
        
        self.screen.blit(score_text, (GRID_WIDTH * BLOCK_SIZE + 20, 200))
        self.screen.blit(level_text, (GRID_WIDTH * BLOCK_SIZE + 20, 240))

    def game_over_screen(self) -> bool:
        """Display game over screen and handle restart"""
        self.screen.fill(BLACK)
        font = pygame.font.Font(None, 48)
        game_over_text = font.render('GAME OVER', True, WHITE)
        score_text = font.render(f'Final Score: {self.score}', True, WHITE)
        restart_text = font.render('Press R to Restart', True, WHITE)
        quit_text = font.render('Press Q to Quit', True, WHITE)

        self.screen.blit(game_over_text, 
                        (SCREEN_WIDTH//2 - game_over_text.get_width()//2, SCREEN_HEIGHT//2 - 100))
        self.screen.blit(score_text, 
                        (SCREEN_WIDTH//2 - score_text.get_width()//2, SCREEN_HEIGHT//2))
        self.screen.blit(restart_text, 
                        (SCREEN_WIDTH//2 - restart_text.get_width()//2, SCREEN_HEIGHT//2 + 50))
        self.screen.blit(quit_text, 
                        (SCREEN_WIDTH//2 - quit_text.get_width()//2, SCREEN_HEIGHT//2 + 100))
        
        pygame.display.flip()

        while True:
            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    return False
                if event.type == pygame.KEYDOWN:
                    if event.key == pygame.K_r:
                        return True
                    if event.key == pygame.K_q:
                        return False
        
    def run(self) -> None:
        """Main game loop"""
        self.show_start_screen()
        
        while True:
            if not self.current_piece:
                self.new_piece()
                if self.game_over:
                    if self.game_over_screen():
                        # Reset game
                        self.__init__()
                        continue
                    else:
                        break

            current_time = pygame.time.get_ticks()

            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    return
                
                if event.type == pygame.KEYDOWN:
                    if event.key == pygame.K_LEFT:
                        self.current_piece['x'] -= 1
                        if self.check_collision():
                            self.current_piece['x'] += 1
                    
                    elif event.key == pygame.K_RIGHT:
                        self.current_piece['x'] += 1
                        if self.check_collision():
                            self.current_piece['x'] -= 1
                    
                    elif event.key == pygame.K_UP:
                        self.rotate_piece()
                    
                    elif event.key == pygame.K_DOWN:
                        self.current_piece['y'] += 1
                        if self.check_collision():
                            self.current_piece['y'] -= 1
                            self.freeze_piece()
                            self.clear_rows()
                            self.current_piece = None

            # Handle automatic falling
            if current_time - self.last_fall_time > self.fall_speed:
                self.current_piece['y'] += 1
                if self.check_collision():
                    self.current_piece['y'] -= 1
                    self.freeze_piece()
                    self.clear_rows()
                    self.current_piece = None
                self.last_fall_time = current_time

            # Draw everything
            self.screen.fill(BLACK)
            self.draw_grid()
            self.draw_next_piece()
            self.draw_score()
            pygame.display.flip()
            self.clock.tick(60)

    def freeze_piece(self) -> None:
        """Freeze the current piece in place"""
        piece_shape = SHAPES[self.current_piece['shape']][0]
        piece_color = SHAPES[self.current_piece['shape']][1]
        
        for y, row in enumerate(piece_shape):
            for x, cell in enumerate(row):
                if cell == 'X':
                    self.grid[self.current_piece['y'] + y][self.current_piece['x'] + x] = piece_color

# Start the game
if __name__ == "__main__":
    game = Tetris()
    game.run()
    pygame.quit()  
