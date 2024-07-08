import os
import utils
import pygame

# Assets folder
spritesheet = os.path.join(os.path.dirname(__file__),'assets/spritesheets')
fonts = os.path.join(os.path.dirname(__file__),'assets/fonts')
sounds = os.path.join(os.path.dirname(__file__),'assets/sounds')
backgrounds = os.path.join(os.path.dirname(__file__),'assets/backgrounds')

class ResourceManager:
    _instance = None
    
    def get_instance():
        if ResourceManager._instance is None:
            ResourceManager._instance = ResourceManager()
        return ResourceManager._instance
    
    def __init__(self):
        if ResourceManager._instance is not None:
            raise Exception("This class is a singleton!")
        else:
            try:
                ResourceManager._instance = self
                self.sprites = utils.load_sprites_from_xml(f"{spritesheet}/sheet.xml", f"{spritesheet}/sheet.png")
                self.backgrounds = utils.get_backgrounds(backgrounds)
                self.fonts = utils.get_fonts(fonts)
                self.sounds = utils.get_files_in_folder(sounds)     
            except Exception as e:
                print(f"An error occurred: {e}")
    
    def load_sprite(self, name, path):
        self.sprites[name] = path
    
    def get_font(self, name, size):
        font = pygame.font.Font(self.fonts[name], size)
        return font
    
    def get_sound(self, name):
        return self.sounds[name]
    
    def get_sprite(self, name):
        return self.sprites[name]
    
    def get_background(self, name):
        return self.backgrounds[name]