import random
from typing import List
import math
import pygame
from constants import *
from resourcemanager import ResourceManager


class Bullet(pygame.sprite.Sprite):
    def __init__(self, res_manager: ResourceManager, position, direction, *groups):
        pygame.sprite.Sprite.__init__(self, *groups)
        
        self.res_manager = res_manager       
        self.image = self.res_manager.get_sprite('ship_J.png')
        self.image.fill(YELLOW)
        self.rect = self.image.get_rect()
        self.rect.center = position
        self.direction = direction
        self.speed = 500  # Pixels per second

    def update(self, dt):
        self.rect.move_ip(self.direction * self.speed * dt)
        if (self.rect.bottom < 0 or self.rect.top > SCREEN_HEIGHT or
            self.rect.right < 0 or self.rect.left > SCREEN_HEIGHT):
            self.kill()

class Player(pygame.sprite.Sprite):
  def __init__(self, res_manager: ResourceManager, *groups):
    pygame.sprite.Sprite.__init__(self, *groups)
    
    self.res_manager = res_manager
    self.image_original:pygame.Surface = self.res_manager.get_sprite('ship_J.png')
    self.image = self.image_original
    self.rect:pygame.rect.Rect = self.image.get_rect()
    self.rect.center = (SCREEN_WIDTH // 2, SCREEN_HEIGHT // 2)
    self.angle: int = 0
    self.speed: int = 300 #Pixels per second
    self.velocity = pygame.math.Vector2(0, 0)
    self.bullets:pygame.sprite.Group = groups[1]
    self.lives = 3 # lives
    self.points = 0  # Points for the player

  def rotate(self, angle):
    # rotation images
    self.angle += angle
    self.image = pygame.transform.rotate(self.image_original, self.angle)
    self.rect = self.image.get_rect(center=self.rect.center)
    

  def update(self, dt):
    # Handle keyboard input for movement
    keys = pygame.key.get_pressed()
    if keys[pygame.K_LEFT]:
      self.rotate(5)
    if keys[pygame.K_RIGHT]:
      self.rotate(-5)
    if keys[pygame.K_SPACE]:
      self.shoot()
    
    # self.velocity.x = keys[pygame.K_RIGHT] - keys[pygame.K_LEFT]
    self.velocity.y = keys[pygame.K_DOWN] - keys[pygame.K_UP]
    
    # Normalize the velocity vector to ensure consistent speed
    if self.velocity.length() > 0:
        self.velocity = self.velocity.normalize()
        
    # Update position based on velocity and delt time
    self.rect.move_ip(self.velocity * self.speed * dt)
    
    # Fire bullet
    self.bullets.update(dt)
    
    # Keep player within screen boundaries
    self.rect.clamp_ip((0, 0, SCREEN_WIDTH, SCREEN_HEIGHT))
    
  def shoot(self):
    angle_rad = math.radians(self.angle)
    direction = pygame.math.Vector2(math.cos(self.angle), -math.sin(angle_rad))
    bullet = Bullet(self.rect.center, direction, self.bullets)
    return bullet
  
  def lose_life(self):
    self.lives -= 1
    self.rect.center = (random.randint(0, SCREEN_WIDTH), random.randint(0, SCREEN_HEIGHT))
    if self.lives <= 0:
        self.kill()

  def add_points(self, points):
    self.points += points
      
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
    