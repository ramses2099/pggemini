import os
import pygame
import math
from typing import List
import xml.etree.ElementTree as ET
from constants import *

# Function to load sprites from a sprite sheet using an XML file
def load_sprites_from_xml(xml_file, sprite_sheet_image):
    tree = ET.parse(xml_file)
    root = tree.getroot()
    sprite_sheet = pygame.image.load(sprite_sheet_image).convert_alpha()

    sprites = {}
    for sub_texture in root.findall('SubTexture'):
        name = sub_texture.get('name')
        x = int(sub_texture.get('x'))
        y = int(sub_texture.get('y'))
        width = int(sub_texture.get('width'))
        height = int(sub_texture.get('height'))
        
        sprite = pygame.Surface((width, height), pygame.SRCALPHA)
        sprite.blit(sprite_sheet, (0, 0), (x, y, width, height))
        sprites[name] = sprite

    return sprites

def get_files_in_folder(folder_path):
    files_dict = {}

    # Walk through the folder
    for root, _, files in os.walk(folder_path):
        for file in files:
            full_path = os.path.join(root, file)
            files_dict[file] = full_path

    return files_dict

def get_fonts(folder_path) -> dict:
    fonts_dict = {}

    # Walk through the folder
    for root, _, files in os.walk(folder_path):
        for file in files:
            full_path = os.path.join(root, file)
            fonts_dict[file] = full_path

    return fonts_dict

def get_backgrounds(folder_path) -> dict:
    bg_rs_dict = {}    
      # Walk through the folder
    for root, _, files in os.walk(folder_path):
        for file in files:
            full_path = os.path.join(root, file)
            bg_rs_dict[file] =  pygame.image.load(full_path).convert_alpha()
    
    return bg_rs_dict

def draw_text(screen, font_name, text, size, x, y) ->None:
    font = pygame.font.Font(font_name, size)
    text_surface = font.render(text, True, WHITE)
    text_rect = text_surface.get_rect()
    text_rect.midtop = (x, y)
    screen.blit(text_surface, text_rect)
    
def draw_lives(screen, x, y, lives, img) -> None:
    for i in range(lives):
        img_rect = img.get_rect()
        img_rect.x = x + 30 * i
        img_rect.y = y
        screen.blit(img, img_rect)

def get_angle_between(position1 : List[int | float], position2 : List[int | float]) -> float:
    dx = position2[0] - position1[0]
    dy = position2[1] - position1[1]
    return math.atan2(dy, dx)