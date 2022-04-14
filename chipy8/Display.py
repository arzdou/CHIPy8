import pygame

BACKGROUND = (0,0,0)
COLOR = (255,255,255)
UPSCALE = 10

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
    
    def clear(self):
        self.screen.fill(BACKGROUND)
        return 0
