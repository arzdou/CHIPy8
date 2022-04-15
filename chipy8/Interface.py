import sys
import pygame

BACKGROUND = (0,0,0)
COLOR = (255,255,255)
UPSCALE = 10

KEY_MAP = {
    0x0: pygame.K_1,
    0x1: pygame.K_2,
    0x2: pygame.K_3,
    0x3: pygame.K_4,
    0x4: pygame.K_q,
    0x5: pygame.K_w,
    0x6: pygame.K_e,
    0x7: pygame.K_r,
    0x8: pygame.K_a,
    0x9: pygame.K_s,
    0xA: pygame.K_d,
    0xB: pygame.K_f,
    0xC: pygame.K_z,
    0xD: pygame.K_x,
    0xE: pygame.K_c,
    0xF: pygame.K_v,
}

INVERTED_KEY_MAP = {key: idx for idx, key in KEY_MAP.items()}

class Interface():
    def __init__(self):
        self.screen = None

    def start(self):
        pygame.init()
        self.screen = pygame.display.set_mode((64*UPSCALE, 32*UPSCALE))
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
        print("beep")
        return 0
    
    def clear(self):
        self.screen.fill(BACKGROUND)
        return 0
