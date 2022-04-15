import pygame

BACKGROUND = (0,0,0)
COLOR = (255,255,255)
UPSCALE = 10

KEY_MAP = {
    0x0: pygame.K_g,
    0x1: pygame.K_4,
    0x2: pygame.K_5,
    0x3: pygame.K_6,
    0x4: pygame.K_7,
    0x5: pygame.K_r,
    0x6: pygame.K_t,
    0x7: pygame.K_y,
    0x8: pygame.K_u,
    0x9: pygame.K_f,
    0xA: pygame.K_h,
    0xB: pygame.K_j,
    0xC: pygame.K_v,
    0xD: pygame.K_b,
    0xE: pygame.K_n,
    0xF: pygame.K_m,
}

class Display():
    def __init__(self):
        # Display
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
    
    def clear(self):
        self.screen.fill(BACKGROUND)
        return 0
