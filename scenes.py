import sys, os
import pygame
from abc import ABC, abstractmethod
from constants import *
from objects import *
from utils import *

# class base Scene
class Scene:
    def __init__(self):
        self.next_scene = self
    
    @abstractmethod        
    def process_events(self, events):
        pass
    
    @abstractmethod
    def update(self, dt):
        pass
    
    @abstractmethod
    def draw(self, screen):
        pass
   
# Main menu scene
class MainMenu(Scene):
    def __init__(self, *args):
        super().__init__()
        self.mg_resource = args[0]
        self.bg = self.mg_resource.get_background('purple.png')
        
        self.menu_items = ['Start Game','Options','Quit']
        self.selected_item = 0

    def process_events(self, events):
        for event in events:
            if event.type == pygame.QUIT:
                pygame.quit()
                sys.exit()
            elif event.type == pygame.KEYDOWN:
                if event.key == pygame.K_UP:
                    self.selected_item = (self.selected_item - 1) % len(self.menu_items)
                elif event.key == pygame.K_DOWN:
                    self.selected_item = (self.selected_item + 1) % len(self.menu_items)
                if event.key == pygame.K_RETURN:
                    if self.menu_items[self.selected_item] == 'Start Game':
                        self.next_scene = GameScene(self.mg_resource)
                    elif self.menu_items[self.selected_item] == 'Options':
                        pass
                    elif self.menu_items[self.selected_item] == 'Quit':
                        pygame.quit()
                        sys.exit()
                    
    def update(self, dt):
        pass

    def draw(self, screen):
        # screen.fill(WHITE)
        bg = pygame.transform.scale(self.bg,(SCREEN_WIDTH, SCREEN_HEIGHT))
        screen.blit(bg, (0, 0))        
        font = self.mg_resource.get_font('kenvector_future.ttf', 74)
        text = font.render("Main Menu", True, WHITE)
        screen.blit(text, (SCREEN_WIDTH//2 - text.get_width()//2, SCREEN_HEIGHT//4 - text.get_height()//2))
        
        # Create the screen
        for index, item in enumerate(self.menu_items):
            if index == self.selected_item:
                color = HIGHLIGHT_COLOR
            else:
                color = WHITE
            # text
            font_option = self.mg_resource.get_font('kenvector_future.ttf', 22)
            text = font_option.render(item, True, color)
            text_rect = text.get_rect(center=(SCREEN_WIDTH // 2, SCREEN_HEIGHT // 2 + index * 50))
            screen.blit(text, text_rect)

# Game scene
class GameScene(Scene):
    def __init__(self, *args):
        super().__init__()
        self.res_manager = args[0]
        self.current_level_number = 1
        #  groups
        self.all_sprites = pygame.sprite.Group()
        self.bullet_group = pygame.sprite.Group()
                
        self.player = Player(self.res_manager, self.all_sprites, self.bullet_group)
        for m in range(10):
            met = Metor(self.res_manager, self.all_sprites, self.bullet_group)
        
        self.bar = ShieldBar(5, 50)
        
    def showPlayerPoints(self, screen):    
        points = 0 
        font = self.res_manager.get_font('kenvector_future.ttf', 22)   
        points_text = font.render(f"POINTS: {points}", True, WHITE)   
        screen.blit(points_text, ((SCREEN_WIDTH-190), 43))
        
    def showLevel(self, screen):    
        lvl = self.current_level_number
        font = self.res_manager.get_font('kenvector_future.ttf', 22)    
        lvl_text = font.render(f"LEVEL: {lvl}", True, WHITE)   
        screen.blit(lvl_text, (5, 25))
        
    def showLives(self, screen):
        image = self.res_manager.get_sprite('ship_J.png')
        rect = image.get_rect()
        sprite = pygame.transform.scale(image, (rect.width//2, rect.height//2))
        
        font = self.res_manager.get_font('kenvector_future.ttf', 22) 
        lives = 3   
        lv_text = font.render(f"LIVES: {lives} x", True, WHITE)   
        screen.blit(lv_text, (SCREEN_WIDTH - 190, 20))
        screen.blit(sprite, (SCREEN_WIDTH - 50, 20))
        
    def process_events(self, events):
        for event in events:
            if event.type == pygame.QUIT:
                pygame.quit()
                sys.exit()
            elif event.type == pygame.KEYDOWN:
                if event.key == pygame.K_ESCAPE:
                    self.next_scene = MainMenu(self.res_manager)
                if event.key == pygame.K_0:
                    self.bar.decrease_bar(5)
                if event.key == pygame.K_1:
                    self.bar.increment_bar(5)

    def update(self, dt):
        # update sprites
        self.all_sprites.update(dt)
        

    def draw(self, screen):
        screen.fill(BLACK)
        # Show info Game
        self.showLevel(screen)
        self.showPlayerPoints(screen)
        self.showLives(screen)
                        
        
        
        # draw sprite
        
        self.all_sprites.draw(screen)
        self.bullet_group.draw(screen)
        
        # bar
        self.bar.draw(screen)
        

# Scene manager
class SceneManager:
    def __init__(self, start_scene):
        self.current_scene = start_scene

    def process_events(self, events):
        self.current_scene.process_events(events)
        if self.current_scene.next_scene != self.current_scene:
            self.current_scene = self.current_scene.next_scene

    def update(self, dt):
        self.current_scene.update(dt)

    def draw(self, screen):
        self.current_scene.draw(screen)