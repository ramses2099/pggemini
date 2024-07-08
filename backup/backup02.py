import pygame
import random
from abc import ABC, abstractmethod
from constants import WIDTH,HEIGHT,BLUE,YELLOW


class Player(pygame.sprite.Sprite):
  def __init__(self, x, y):
    # call the parent class (Sprite) consturctor      
    pygame.sprite.Sprite.__init__(self)
    
    self.image = pygame.Surface([32, 32])
    self.image.fill(BLUE)
    self.rect = self.image.get_rect()
    self.rect.center = (WIDTH // 2, HEIGHT // 2)
    self.speed = 300 #Pixels per second
    self.velocity = pygame.math.Vector2(0, 0)
    self.bullets = pygame.sprite.Group()
    self.lives = 3 # lives
    self.points = 0  # Points for the player

  def update(self, dt):
    # Handle keyboard input for movement
    keys = pygame.key.get_pressed()
    self.velocity.x = keys[pygame.K_RIGHT] - keys[pygame.K_LEFT]
    self.velocity.y = keys[pygame.K_DOWN] - keys[pygame.K_UP]
    
    # Normalize the velocity vector to ensure consistent speed
    if self.velocity.length() > 0:
        self.velocity = self.velocity.normalize()

    # Update position based on velocity and delt time
    self.rect.move_ip(self.velocity * self.speed * dt)
    
    # Fire bullet
    self.bullets.update(dt)
    
    # Keep player within screen boundaries
    self.rect.clamp_ip((0, 0, WIDTH, HEIGHT))
    
  def shoot(self):
    bullet = Bullet(self.rect.center, pygame.math.Vector2(0, -1))
    self.bullets.add(bullet)
    
  def lose_life(self):
    self.lives -= 1
    self.rect.center = (random.randint(0, WIDTH), random.randint(0, HEIGHT))
    if self.lives <= 0:
        self.kill()

  def add_points(self, points):
    self.points += points

class Bullet(pygame.sprite.Sprite):
    def __init__(self, position, direction):
        super().__init__()
        self.image = pygame.Surface((10, 10))
        self.image.fill(YELLOW)
        self.rect = self.image.get_rect()
        self.rect.center = position
        self.direction = direction
        self.speed = 500  # Pixels per second

    def update(self, dt):
        self.rect.move_ip(self.direction * self.speed * dt)
        if (self.rect.bottom < 0 or self.rect.top > HEIGHT or
            self.rect.right < 0 or self.rect.left > WIDTH):
            self.kill()

class Behavior(ABC):
    @abstractmethod
    def update(self, npc, player, dt):
        pass

class PatrolBehavior(Behavior):
    def __init__(self, path):
        self.path = path
        self.path_index = 0

    def update(self, npc, player, dt):
       target = pygame.math.Vector2(self.path[self.path_index])
       direction = target - pygame.math.Vector2(npc.rect.center)
       if direction.length() > 0:
           direction = direction.normalize() * npc.speed * dt
           
       npc.rect.move_ip(direction)
       if npc.rect.collidepoint(target):
           self.path_index = (self.path_index + 1) % len(self.path)
           
       self.handle_collision(npc, player, dt)
        
    def handle_collision(self, npc, player, dt):
        if pygame.sprite.collide_rect(player, npc):
            collision_vector = pygame.math.Vector2(player.rect.center) - pygame.math.Vector2(npc.rect.center)
            if collision_vector.length() > 0:
                collision_vector = collision_vector.normalize()
            push_strength = 100  # Arbitrary push strength value

            player.rect.move_ip(collision_vector * push_strength * dt)
            npc.rect.move_ip(-collision_vector * push_strength * dt)

            if player.rect.left < 0:
                player.rect.left = 0
            if player.rect.right > WIDTH:
                player.rect.right = WIDTH
            if player.rect.top < 0:
                player.rect.top = 0
            if player.rect.bottom > HEIGHT:
                player.rect.bottom = HEIGHT

            if npc.rect.left < 0:
                npc.rect.left = 0
            if npc.rect.right > WIDTH:
                npc.rect.right = WIDTH
            if npc.rect.top < 0:
                npc.rect.top = 0
            if npc.rect.bottom > HEIGHT:
                npc.rect.bottom = HEIGHT
        
class ChaseBehavior(Behavior):
    def __init__(self, target):
        self.target = target
    
    def update(self, npc, player, dt):
       target_pos = pygame.math.Vector2(self.target.rect.center)
       direction = target_pos - pygame.math.Vector2(npc.rect.center)
       if direction.length() > 0:
           direction = direction.normalize() * npc.speed * dt
       npc.rect.move_ip(direction)
       
       self.handle_collision(npc, player, dt)
    
    def handle_collision(self, npc, player, dt):
        if pygame.sprite.collide_rect(player, npc):
            collision_vector = pygame.math.Vector2(player.rect.center) - pygame.math.Vector2(npc.rect.center)
            if collision_vector.length() > 0:
                collision_vector = collision_vector.normalize()
            push_strength = 100  # Arbitrary push strength value

            player.rect.move_ip(collision_vector * push_strength * dt)
            npc.rect.move_ip(-collision_vector * push_strength * dt)

            if player.rect.left < 0:
                player.rect.left = 0
            if player.rect.right > WIDTH:
                player.rect.right = WIDTH
            if player.rect.top < 0:
                player.rect.top = 0
            if player.rect.bottom > HEIGHT:
                player.rect.bottom = HEIGHT

            if npc.rect.left < 0:
                npc.rect.left = 0
            if npc.rect.right > WIDTH:
                npc.rect.right = WIDTH
            if npc.rect.top < 0:
                npc.rect.top = 0
            if npc.rect.bottom > HEIGHT:
                npc.rect.bottom = HEIGHT

class IdleBehavior(Behavior):
    def update(self, npc, player, dt):
        self.handle_collision(npc, player, dt)

    def handle_collision(self, npc, player, dt):
        if pygame.sprite.collide_rect(player, npc):
            collision_vector = pygame.math.Vector2(player.rect.center) - pygame.math.Vector2(npc.rect.center)
            if collision_vector.length() > 0:
                collision_vector = collision_vector.normalize()
            push_strength = 100  # Arbitrary push strength value

            player.rect.move_ip(collision_vector * push_strength * dt)
            npc.rect.move_ip(-collision_vector * push_strength * dt)

            if player.rect.left < 0:
                player.rect.left = 0
            if player.rect.right > WIDTH:
                player.rect.right = WIDTH
            if player.rect.top < 0:
                player.rect.top = 0
            if player.rect.bottom > HEIGHT:
                player.rect.bottom = HEIGHT

            if npc.rect.left < 0:
                npc.rect.left = 0
            if npc.rect.right > WIDTH:
                npc.rect.right = WIDTH
            if npc.rect.top < 0:
                npc.rect.top = 0
            if npc.rect.bottom > HEIGHT:
                npc.rect.bottom = HEIGHT
   
class NPC(pygame.sprite.Sprite):
    def __init__(self, behavior, position):
        pygame.sprite.Sprite.__init__(self)
        self.image = pygame.Surface([32,64])
        self.image.fill(self.random_color())
        self.rect = self.image.get_rect()
        self.rect.center = position       
        self.speed = 100
        self.behavior = behavior
        self.bullets = pygame.sprite.Group()
        self.shoot_interval = random.uniform(1, 3)  # Random shooting interval between 1 and 3 seconds
        self.time_since_last_shot = 0
            
    def update(self, player, dt):
        self.behavior.update(self, player, dt)
        self.bullets.update(dt)
        self.shoot_timer(dt)

    def shoot(self):
        bullet = Bullet(self.rect.center, pygame.math.Vector2(0, 1))
        self.bullets.add(bullet)
        
    def shoot_timer(self, dt):
        self.time_since_last_shot += dt
        if self.time_since_last_shot >= self.shoot_interval:
            self.time_since_last_shot = 0
            self.shoot()
        
    @staticmethod
    def random_color():
        return (random.randint(0, 255), random.randint(0, 255), random.randint(0, 255))
             
class Spawner:
    def __init__(self, npc_group, spawn_interval, behaviors):
        self.npc_group = npc_group
        self.spawn_interval = spawn_interval
        self.behaviors = behaviors
        self.time_since_last_spawn = 0
        
    def update(self, player, dt):
        self.time_since_last_spawn += dt
        if self.time_since_last_spawn >= self.spawn_interval:
            self.time_since_last_spawn = 0
            self.spawn_npc(player)
    
    def spawn_npc(self, player):
        position = (random.randint(32, WIDTH),
                    random.randint(32, HEIGHT))
        behavior = random.choice(self.behaviors)
        npc = NPC(behavior, position)
        self.npc_group.add(npc)        
        
class Level:
    def __init__(self, level_number, player, npc_group):
        self.level_number = level_number
        self.player = player
        self.npc_group = npc_group
        self.behaviors = self.create_behaviors()
        self.spawner = Spawner(npc_group, 5, self.behaviors)
        self.level_duration = 30  # seconds
        self.time_in_level = 0

    def create_behaviors(self):
        # Define different behaviors for different levels
        if self.level_number == 1:
            return [PatrolBehavior([(100, 100), (700, 100), (700, 500), (100, 500)])]
        elif self.level_number == 2:
            return [ChaseBehavior(self.player)]
        elif self.level_number == 3:
            return [IdleBehavior(),PatrolBehavior([(100, 100), (700, 100), (700, 500), (100, 500)])]
        else:
            return [PatrolBehavior([(100, 100), (700, 100), (700, 500), (100, 500)]), ChaseBehavior(self.player)]

    def update(self, dt):
        self.time_in_level += dt
        self.spawner.update(self.player, dt)
        if self.time_in_level >= self.level_duration:
            return True  # Indicate that the level is complete
        return False