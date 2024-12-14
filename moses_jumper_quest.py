import pygame
import sys
import sys
sys.path.append("path_to_conda_env_lib_site-packages")
import math
import pymunk
from enum import Enum

# Initialize Pygame and Pymunk
pygame.init()
pygame.mixer.init()
space = pymunk.Space()
space.gravity = (0.0, 0.0)  # No gravity for top-down racing
space.damping = 0.7  # Add some air resistance

# Constants
WINDOW_WIDTH = 1280
WINDOW_HEIGHT = 720
FPS = 60

# Physics constants
PLAYER_MASS = 1
PLAYER_MOMENT = 1000
PLAYER_ACCELERATION = 1200
PLAYER_TURN_SPEED = 4.0
FRICTION = 0.7

# Colors
WHITE = (255, 255, 255)
BLACK = (0, 0, 0)
RED = (255, 0, 0)
BLUE = (0, 0, 255)

# Game states
class GameState(Enum):
    MENU = 1
    CAR_SELECT = 2
    TRACK_SELECT = 3
    PLAYING = 4
    PAUSED = 5
    GAME_OVER = 6

class Car:
    def __init__(self, x, y):
        self.body = pymunk.Body(PLAYER_MASS, PLAYER_MOMENT)
        self.body.position = x, y
        
        # Create a box shape for the car
        size = (40, 80)
        self.shape = pymunk.Poly.create_box(self.body, size)
        self.shape.elasticity = 0.5
        self.shape.friction = FRICTION
        
        space.add(self.body, self.shape)
        
        # Car properties
        self.acceleration = 0
        self.steering = 0
        self.speed = 0
        
    def update(self):
        # Apply forces based on input
        force_x = math.cos(self.body.angle) * self.acceleration
        force_y = math.sin(self.body.angle) * self.acceleration
        self.body.apply_force_at_local_point((force_x, force_y), (0, 0))
        
        # Apply steering
        self.body.angular_velocity = self.steering * PLAYER_TURN_SPEED
        
        # Update speed
        self.speed = math.sqrt(self.body.velocity.x**2 + self.body.velocity.y**2)

class Game:
    def __init__(self):
        self.screen = pygame.display.set_mode((WINDOW_WIDTH, WINDOW_HEIGHT))
        pygame.display.set_caption("Speed Demons Racing")
        self.clock = pygame.time.Clock()
        self.game_state = GameState.MENU
        self.font_large = pygame.font.Font(None, 74)
        self.font_medium = pygame.font.Font(None, 48)
        self.font_small = pygame.font.Font(None, 36)
        
        # Initialize player car
        self.player = None

    def start_game(self):
        self.player = Car(WINDOW_WIDTH//2, WINDOW_HEIGHT//2)
        self.game_state = GameState.PLAYING

    def handle_playing_input(self):
        keys = pygame.key.get_pressed()
        
        # Reset forces
        self.player.acceleration = 0
        self.player.steering = 0
        
        # Handle acceleration
        if keys[pygame.K_UP]:
            self.player.acceleration = PLAYER_ACCELERATION
        if keys[pygame.K_DOWN]:
            self.player.acceleration = -PLAYER_ACCELERATION
        
        # Handle steering
        if keys[pygame.K_LEFT]:
            self.player.steering = -1
        if keys[pygame.K_RIGHT]:
            self.player.steering = 1

    def run(self):
        while True:
            if self.game_state == GameState.MENU:
                self.main_menu()
            elif self.game_state == GameState.PLAYING:
                self.game_loop()

    def game_loop(self):
        while self.game_state == GameState.PLAYING:
            # Handle events
            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    pygame.quit()
                    sys.exit()
                if event.type == pygame.KEYDOWN:
                    if event.key == pygame.K_ESCAPE:
                        self.game_state = GameState.MENU
            
            # Handle input
            self.handle_playing_input()
            
            # Update physics
            self.player.update()
            space.step(1/FPS)
            
            # Draw
            self.screen.fill(BLACK)
            
            # Draw car (simple rectangle for now)
            car_pos = self.player.body.position
            car_angle = math.degrees(self.player.body.angle)
            car_surface = pygame.Surface((40, 80))
            car_surface.fill(RED)
            rotated_car = pygame.transform.rotate(car_surface, -car_angle)
            self.screen.blit(rotated_car, (car_pos.x - rotated_car.get_width()//2,
                                         car_pos.y - rotated_car.get_height()//2))
            
            pygame.display.flip()
            self.clock.tick(FPS)

    def main_menu(self):
        title = self.font_large.render("Speed Demons Racing", True, WHITE)
        creator = self.font_small.render("Created by Moses Jackson", True, WHITE)
        start = self.font_medium.render("Start Game", True, WHITE)
        instructions = self.font_medium.render("Instructions", True, WHITE)
        exit_text = self.font_medium.render("Exit", True, WHITE)

        while self.game_state == GameState.MENU:
            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    pygame.quit()
                    sys.exit()
                if event.type == pygame.MOUSEBUTTONDOWN:
                    mouse_pos = pygame.mouse.get_pos()
                    # Start button
                    if WINDOW_WIDTH//2 - 100 <= mouse_pos[0] <= WINDOW_WIDTH//2 + 100 and \
                       290 <= mouse_pos[1] <= 350:
                        self.start_game()
                    # Exit button
                    elif WINDOW_WIDTH//2 - 100 <= mouse_pos[0] <= WINDOW_WIDTH//2 + 100 and \
                         490 <= mouse_pos[1] <= 550:
                        pygame.quit()
                        sys.exit()

            # Draw menu
            self.screen.fill(BLACK)
            self.screen.blit(title, (WINDOW_WIDTH//2 - title.get_width()//2, 100))
            self.screen.blit(creator, (WINDOW_WIDTH//2 - creator.get_width()//2, 200))
            self.screen.blit(start, (WINDOW_WIDTH//2 - start.get_width()//2, 300))
            self.screen.blit(instructions, (WINDOW_WIDTH//2 - instructions.get_width()//2, 400))
            self.screen.blit(exit_text, (WINDOW_WIDTH//2 - exit_text.get_width()//2, 500))

            pygame.display.flip()
            self.clock.tick(FPS)

if __name__ == "__main__":
    game = Game()
    game.run()