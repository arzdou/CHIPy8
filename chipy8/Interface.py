import sys
import pygame
from .config import UPSCALE, COLOR, BACKGROUND, KEY_MAP, INVERTED_KEY_MAP, WINDOW_NAME, ICON_FILE

class Interface():
    def __init__(self):
        self.screen = None

    def start(self):
        pygame.init()
        self.screen = pygame.display.set_mode((64*UPSCALE, 32*UPSCALE))
        pygame.display.set_caption(WINDOW_NAME)
        icon = pygame.image.load(ICON_FILE)
        pygame.display.set_icon(icon)
        self.clear()
        self.update()
        
    def update(self):
        pygame.display.update()
        return 0

    def draw_pixel(self, x, y):
        width = (
            UPSCALE*x,
            UPSCALE*y,
            UPSCALE,
            UPSCALE
        ) 
        pygame.draw.rect(self.screen, COLOR, width)
        return 0
    
    def errase_pixel(self, x, y):
        width = (
            UPSCALE*x,
            UPSCALE*y,
            UPSCALE,
            UPSCALE
        ) 
        pygame.draw.rect(self.screen, BACKGROUND, width)
        return 0
    
    def get_pixel(self, x, y):
        pixel = True
        color = self.screen.get_at((x*UPSCALE,y*UPSCALE))
        if color == BACKGROUND:
            pixel = False
        return pixel

    def is_key_pressed(self, key_index):
        key = KEY_MAP[key_index]
        pressed_keys = pygame.key.get_pressed()
        return pressed_keys[key]

    def wait_for_keypress(self):
        """
        Code inspired from https://stackoverflow.com/questions/20748326
        """
        pygame.event.clear()
        while True:
            event = pygame.event.wait()
            if event.type == pygame.QUIT:
                pygame.quit()
                sys.exit() 
            elif event.type == pygame.KEYDOWN:
                key = event.key
                if key in KEY_MAP.values():
                    break
            
        return INVERTED_KEY_MAP[key]

    def make_beep(self):
        #print("beep")
        return 0
    
    def clear(self):
        self.screen.fill(BACKGROUND)
        return 0
