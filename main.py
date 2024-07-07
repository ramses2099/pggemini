import os
import pygame
import pygame.font  # Import the font library (e.g., pygame.font or external library)
from constant import *
from objects import *
from behaviors import *

class Game:
  def __init__(self):
    # Initialize Pygame and create the screen    
    pygame.init()
    
    # Create a font object (adjust font size as needed)
    self.font = pygame.font.Font(None, 32)
    
    self.screen = pygame.display.set_mode((WIDTH, HEIGHT))

    # Set the window title
    pygame.display.set_caption("Pygame Game and Gimini")
    
    self.clock = pygame.time.Clock()  # Create clock to track time

    # Create player and other game objects
    self.player = Player(100, 200)
    
    self.all_sprite = pygame.sprite.Group()
    self.all_sprite.add(self.player)
    
    # enemy test
    self.enemy = EnemyChase(250,25, self.player)
    self.enemy2 = EnemyPatrolling(700,25,[700,0],700)
        
    self.all_sprite.add(self.enemy,self.enemy2)

  def showFPS(self):
    # Calculate and render FPS text
    fps = int(self.clock.get_fps())  # Get FPS as integer
    # Render FPS text with font
    fps_text = self.font.render(f"FPS: {fps}", True, WHITE)  

    # Draw FPS text on top-left corner
    self.screen.blit(fps_text, (5, 5))

  def run(self):
    running = True
    while running:
        
        # Get the delta time (time passed since last frame) in seconds
        dt = self.clock.tick(FPS) / 1000  # Target 60 FPS, convert milliseconds to seconds

        # Handle events (similar to basic Pygame program)
        # Check for events
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                running = False
                
        # Fill the screen with black color
        self.screen.fill(BLACK)
        
        # DEBUG SHOW FPS
        if (DEBUG):
            self.showFPS()

        # Update game objects (call update methods)
        self.all_sprite.update(dt)

        # Draw game objects (call draw methods)
        self.all_sprite.draw(self.screen)

        # Update the display
        pygame.display.flip()

if __name__ == "__main__":
  os.system('clear')
  game = Game()
  game.run()
