import os
import pygame
import pygame.font  
from resourcemanager import ResourceManager
from utils import *
from constants import *
from scenes import *

# Initialize Pygame and create the screen    
pygame.init()

# Assets folder
spritesheet = os.path.join(os.path.dirname(__file__),'assets/spritesheets')
fonts = os.path.join(os.path.dirname(__file__),'assets/fonts')
sounds = os.path.join(os.path.dirname(__file__),'assets/sounds')
backgrounds = os.path.join(os.path.dirname(__file__),'assets/backgrounds')
    
screen = pygame.display.set_mode((SCREEN_WIDTH, SCREEN_HEIGHT))

# Resource Manager
resource_manager = ResourceManager.get_instance()

# Set the window title
pygame.display.set_caption(TITLE)
    
clock = pygame.time.Clock()  # Create clock to track time

def showFPS(self, screen):
  fps = int(self.clock.get_fps())
  font_name = self.fonts['kenvector_future.ttf']
  text = f"FPS: {fps}"
  draw_text(screen, font_name, text, 16, 5, 5)     


def main():
    
  running = True
  manager = SceneManager(MainMenu(resource_manager))
    
  while running:        
    # Get the delta time (time passed since last frame) in seconds
    dt = clock.tick(FPS) / 1000  # Target 60 FPS, convert milliseconds to seconds
    events = pygame.event.get()
    manager.process_events(events)
    manager.update(dt)
    manager.draw(screen)
    pygame.display.flip()
    clock.tick(FPS)
  
  # Friendly exit
  pygame.quit()
  sys.exit(0)

if __name__ == "__main__":
  os.system('clear')
  main()
