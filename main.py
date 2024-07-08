import os
import pygame
import pygame.font  # Import the font library (e.g., pygame.font or external library)
from constant import *
from objects import *

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
    self.player = Player(WIDTH/2, 200)
    
    self.player_group = pygame.sprite.Group()
    self.npc_group = pygame.sprite.Group()
    
    # Initialize the first level
    self.player, self.current_level_number, self.current_level = self.reset_game(self.player_group, self.npc_group)
    
  def reset_game(self, player_group, npc_group):
    # Reset player state
    player = Player(WIDTH/2, 200)
    player_group.empty()
    player_group.add(player)

    # Clear NPCs
    npc_group.empty()

    # Initialize the first level
    current_level_number = 1
    current_level = Level(current_level_number, player, npc_group)

    return player, current_level_number, current_level
  
  def showPlayerLives(self):    
    lives = self.player.lives    
    lives_text = self.font.render(f"LIVES: {lives}", True, WHITE)   
    self.screen.blit(lives_text, ((WIDTH-110), 5))
  
  def showGameOver(self):       
    gover_text = self.font.render("- Game Over -", True, WHITE)
    pagain_text = self.font.render("- Press Enter to play Again -", True, WHITE)   
    self.screen.blit(gover_text, ((WIDTH //2) - 50, (HEIGHT // 2)- 20))
    self.screen.blit(pagain_text, ((WIDTH //2) - 150, (HEIGHT // 2)+ 20))
   
  def showPlayerPoints(self):    
    points = self.player.points    
    points_text = self.font.render(f"POINTS: {points}", True, WHITE)   
    self.screen.blit(points_text, ((WIDTH-120), 25))
      
  def showLevel(self):    
    lvl = self.current_level_number    
    lvl_text = self.font.render(f"LEVEL: {lvl}", True, WHITE)   
    self.screen.blit(lvl_text, (5, 25))
       
  def showFPS(self):
    # Calculate and render FPS text
    fps = int(self.clock.get_fps())  # Get FPS as integer
    # Render FPS text with font
    fps_text = self.font.render(f"FPS: {fps}", True, WHITE)  

    # Draw FPS text on top-left corner
    self.screen.blit(fps_text, (5, 5))

  def run(self):
    running = True
    game_over = False
    
    while running:
        
        # Get the delta time (time passed since last frame) in seconds
        dt = self.clock.tick(FPS) / 1000  # Target 60 FPS, convert milliseconds to seconds

        # Handle events (similar to basic Pygame program)
        # Check for events
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                running = False
            elif event.type == pygame.KEYDOWN:
                if event.key == pygame.K_SPACE:
                    # Player shoot
                    self.player.shoot()
                elif event.key == pygame.K_RETURN and game_over:
                    # Initialize the first level
                    self.player, self.current_level_number, current_level = self.reset_game(self.player_group, self.npc_group)
                    game_over = False
        
        # Fill the screen with black color
        self.screen.fill(BLACK)
            
        # Show LEVEL
        self.showLevel()
        self.showPlayerLives()
        self.showPlayerPoints()
        
        # DEBUG SHOW FPS
        if (DEBUG):
            self.showFPS()
         
        # Game over          
        if not game_over:
            # Update game objects (call update methods)
            # Update player and npc with delta time
            self.player_group.update(dt)
            for npc in self.npc_group:
                npc.update(self.player, dt)
                    
            # Update spawer
            # Update current level
            if self.current_level.update(dt):
                # Move to the next level
                self.current_level_number += 1
                self.current_level = Level(self.current_level_number, self.player, self.npc_group)
                self.npc_group.empty()  # Clear NPCs from the previous level

            # Update bullet collisions
            for bullet in self.player.bullets:
                if pygame.sprite.spritecollide(bullet, self.npc_group, True):
                    bullet.kill()
                    self.player.add_points(10)  # Add points for killing an NP

            for npc in self.npc_group:
                for bullet in npc.bullets:
                    if pygame.sprite.spritecollide(bullet, self.player_group, False):
                        bullet.kill()
                        self.player.lose_life()
                        
            # End game if player is out of lives
            if not self.player.alive():
                game_over = True


        # Draw game objects (call draw methods)
        self.player_group.draw(self.screen)
        self.npc_group.draw(self.screen)
        self.player.bullets.draw(self.screen)
        for npc in self.npc_group:
            npc.bullets.draw(self.screen)
            
        if game_over:
            self.showGameOver()
            
        # Update the display
        pygame.display.flip()

if __name__ == "__main__":
  os.system('clear')
  game = Game()
  game.run()
