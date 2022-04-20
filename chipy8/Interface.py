import sys
import pygame
from .config import *

class Interface():
    def __init__(self):
        self.screen = None

    def start(self):
        pygame.init()
        
        self.screen = pygame.display.set_mode((64*UPSCALE, 32*UPSCALE))
        pygame.display.set_caption(WINDOW_NAME)

        icon = pygame.image.load(ICON_FILE)
        pygame.display.set_icon(icon)

        pygame.mixer.init()
        self.beep = pygame.mixer.Sound(SOUND_FILE)

        self.clear()
        self.update()
        
    def update(self):
        pygame.display.update()
        return 0

    def draw_pixel(self, x, y, c=COLOR):
        width = (
            UPSCALE*x,
            UPSCALE*y,
            UPSCALE,
            UPSCALE
        ) 
        pygame.draw.rect(self.screen, c, width)
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
    
    def draw_logo(self):
        for y in range(32):
            for x in range(32):
                color_index = INDEX_ICON[x+y*32]
                self.draw_pixel(x+16, y, LOGO_COLORS[color_index])
            pygame.event.wait(10)
            pygame.display.update()

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
            event = pygame.event.wait(WAITING_TIME)
            if event.type == pygame.QUIT:
                pygame.quit()
                sys.exit() 
            elif event.type == pygame.KEYDOWN:
                key = event.key
                if key in KEY_MAP.values():
                    break
            
        return INVERTED_KEY_MAP[key]

    def wait_for_drop(self):
        waiting_for_rom = True
        while waiting_for_rom:
            pygame.time.wait(WAITING_TIME)
            for e in pygame.event.get():
                if e.type == pygame.QUIT:
                    return 1
                elif e.type == pygame.DROPFILE:
                    file = e.file
                    if file.endswith((".ch8", ".chip8", ".c8")):
                        waiting_for_rom = False
        return file

    def make_beep(self):
        self.beep.play()
        return 0
    
    def clear(self):
        self.screen.fill(BACKGROUND)
        pygame.display.update()
        return 0
