import math
import random
import pygame
from constants import *
from resourcemanager import ResourceManager
from utils import get_angle_between

class ShieldBar(pygame.sprite.Sprite):
  def __init__(self, x: int , y: int)->None:
    pygame.sprite.Sprite.__init__(self)
    self.bar_length: int = 200
    self.bar_height: int = 25
    self.fill: float = 200
    self.outline_rect: pygame.rect.Rect = pygame.Rect(x, y, self.bar_length, self.bar_height)
    self.fill_rect: pygame.rect.Rect = pygame.rect.Rect(x, y, self.fill, self.bar_height)
    
  def increment_bar(self, value: int)->None:
    if (self.fill < self.bar_length):
      self.fill += value
      self.fill_rect.width = int(self.fill)
  
  def decrease_bar(self, value: int)->None:
    if(self.fill >= 10):
      self.fill -= value
      self.fill_rect.width = int(self.fill)  
    
  def draw(self, screen : pygame.surface.Surface):
    pygame.draw.rect(screen, WHITE, self.outline_rect, 2)
    pygame.draw.rect(screen, GREEN, self.fill_rect)
    
class Bullet(pygame.sprite.Sprite):
  def __init__(self, res_manager, position, angle, *groups):
    super().__init__(*groups)
    self.res_manager = res_manager
    surf = pygame.transform.scale(self.res_manager.get_sprite('effect_yellow.png'),(8, 64))
    self.original_image = surf
    self.image = self.original_image
    self.rect = self.image.get_rect(center = position)
    self.angle = math.radians(angle)
    self.speed = 10

  def update(self, dt):    
    self.image = pygame.transform.rotate(self.original_image, self.angle)
    self.rect = self.image.get_rect(center = self.rect.center)
    
    #  angle_rad = math.radians(self.angle)    
    self.rect.x += math.cos(self.angle) * self.speed 
    self.rect.y += -math.sin(self.angle) * self.speed 
    
class Player(pygame.sprite.Sprite):
  def __init__(self, res_manager: ResourceManager, *groups):
    super().__init__(*groups)
    # sprite propertys
    self.res_manager = res_manager
    self.position = (SCREEN_WIDTH // 2, SCREEN_HEIGHT // 2)
    self.original_image: pygame.surface.Surface = self.res_manager.get_sprite('ship_J.png')
    self.image = self.original_image
    self.rect = self.image.get_rect(center = self.position)
    self.angle = 0
    self.all_sprite, self.bullet_groups = groups
    
  def rotate(self, angle):
    self.angle += angle
    self.image = pygame.transform.rotate(self.original_image, self.angle)
    self.rect = self.image.get_rect(center = self.rect.center)
  
  def shoot(self):    
    bullet = Bullet(self.res_manager, self.rect.center, self.angle, self.all_sprite, self.bullet_groups)
    return bullet  
    
  def update(self, dt):
    keys = pygame.key.get_pressed()
    if keys[pygame.K_LEFT]:
      self.rotate(10)
    if keys[pygame.K_RIGHT]:
      self.rotate(-10)
    if keys[pygame.K_SPACE]:
      self.shoot()
    
    
class Metor(pygame.sprite.Sprite):
  def __init__(self, res_manager, *groups):
    super().__init__(*groups)
    
    self.name_img = random.choice(METEOR_LIST)    
    self.res_manager = res_manager
    self.original_image = self.res_manager.get_sprite(f'{self.name_img}')
    self.image = self.original_image
    self.position = (random.randint(10, SCREEN_WIDTH),random.randint(10, SCREEN_HEIGHT))
    self.rect = self.image.get_rect(center = self.position)
    self.rotation = 0
    self.rotation_speed = random.randrange(-8, 8)
    self.speedx = random.randrange(-10, 30)
    self.speedy = random.randrange(10, 30)
    self.last_update = pygame.time.get_ticks()

  def rotate(self):
    time_now = pygame.time.get_ticks()
    if time_now - self.last_update > 50:
      self.last_update = time_now
      self.rotation = (self.rotation + self.rotation_speed) % 360
      new_image = pygame.transform.rotate(self.original_image, self.rotation)
      self.image = new_image
      self.rect = self.image.get_rect(center = self.rect.center)


  def update(self, dt):    
    self.rotate()
    self.rect.x += self.speedx
    self.rect.y += self.speedy