import pygame
from constant import WIDTH,HEIGHT,BLUE,RED
from behaviors import *

class Player(pygame.sprite.Sprite):
  def __init__(self, x, y):
    # call the parent class (Sprite) consturctor      
    pygame.sprite.Sprite.__init__(self)
    
    self.image = pygame.Surface([32, 32])
    self.image.fill(BLUE)
    self.rect = self.image.get_rect(topleft =(x, y))
    self.speed = 50

  def draw(self, screen):
    screen.blit(self.image, self.rect)

  def update(self, dt):
    # Handle keyboard input for movement
    keys = pygame.key.get_pressed()
    dx = 0  # Change in x position
    dy = 0  # Change in y position
        
    if keys[pygame.K_LEFT]:
      dx -= self.speed
    if keys[pygame.K_RIGHT]:
      dx += self.speed
    if keys[pygame.K_UP]:
      dy -= self.speed
    if keys[pygame.K_DOWN]:  
      dy += self.speed
      
    # Move the player by the calculated offset based on dt for smooth movement
    self.rect.x += dx * dt
    self.rect.y += dy * dt

    # Keep player within screen boundaries
    self.rect.clamp_ip((0, 0, WIDTH, HEIGHT))

class EnemyBase(pygame.sprite.Sprite):
  def __init__(self, x, y):
    # call the parent class (Sprite) consturctor      
    pygame.sprite.Sprite.__init__(self)
    
    self.image = pygame.Surface([32, 32])
    self.image.fill(RED)
    self.rect = self.image.get_rect(topleft =(x, y))
    # IA
    self.speed = 5
    self.dx = 0
    self.dy = 0

  def draw(self, screen):
    screen.blit(self.image, self.rect)

  def update(self, dt):
    self.rect.x += self.dx * self.speed
    self.rect.y += self.dy * self.speed 
    
class EnemyChase(EnemyBase):
    def __init__(self, x, y, player):
        EnemyBase.__init__(self, x, y)
        self.speed = 1
        self.player = player
        
    def update(self, dt):
        chase_player(self, self.player)
        super().update(dt)
        
        
class EnemyPatrolling(EnemyBase):
    def __init__(self, x, y, start_pos, patrol_range):
        EnemyBase.__init__(self, x, y)
        self.speed = 1
        self.dx = 1
        self.start_pos = start_pos
        self.patrol_range = patrol_range
        
    def update(self, dt):
        patrolling(self,self.start_pos, self.patrol_range, dt)
        super().update(dt)