import math
import random
from constant import WIDTH, HEIGHT


# Define enemy movement behaviors
def patrolling(enemy, start_pos, patrol_range, dt):
  if (enemy.rect.left <= (start_pos[0] - patrol_range)):
      enemy.dx = 1
  elif(enemy.rect.right >= (start_pos[0] - patrol_range)):
      enemy.dx = -1
  # movement in the direction x
  enemy.rect.x += enemy.speed * enemy.dx * dt
  
  

def chase_player(enemy, player):
  # Calculate direction vector towards player
  dx = player.rect.x - enemy.rect.x
  dy = player.rect.y - enemy.rect.y

  # Normalize the direction vector (optional for smooth movement)
  length = math.sqrt(dx**2 + dy**2)
  if length != 0:
    dx /= length
    dy /= length

  # Update enemy position based on direction and speed
  enemy.rect.x += dx * enemy.speed
  enemy.rect.y += dy * enemy.speed
  
  
def boundaries(enemy):
  # ... (movement logic as before)
  # Check and adjust if going beyond left/right boundaries
  if enemy.rect.left < 0:
    enemy.rect.left = 0
  elif enemy.rect.right > WIDTH:
    enemy.rect.right = WIDTH

  # Check and adjust if going beyond top/bottom boundaries
  if enemy.rect.top < 0:
    enemy.rect.top = 0
  elif enemy.rect.bottom > HEIGHT:
    enemy.rect.bottom = HEIGHT  