import sys, os
import pygame
from abc import ABC, abstractmethod
from constants import *
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
        self.mg_resource = args[0]
        self.sprite = self.mg_resource.get_sprite('enemyRed1.png')
        
    def process_events(self, events):
        for event in events:
            if event.type == pygame.QUIT:
                pygame.quit()
                sys.exit()
            elif event.type == pygame.KEYDOWN:
                if event.key == pygame.K_ESCAPE:
                    self.next_scene = MainMenu()

    def update(self, dt):
        pass

    def draw(self, screen):
        screen.fill(BLACK)        
        font = self.mg_resource.get_font('kenvector_future.ttf', 74)
        text = font.render("Game Scene", True, WHITE)
        screen.blit(text, (SCREEN_WIDTH//2 - text.get_width()//2, SCREEN_HEIGHT//2 - text.get_height()//2))
        screen.blit(self.sprite,(100,100))

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