import pygame

BACKGROUND = (0,0,0)
COLOR = (255,255,255)
UPSCALE = 10

def drawXY(screen, X, Y):
    width = (
        UPSCALE*X,
        UPSCALE*Y,
        UPSCALE,
        UPSCALE
    )
    pygame.draw.rect(screen, COLOR, width)
    return 0
    
def clear(screen):
    screen.fill(BACKGROUND)
    pygame.display.update()
    return 0

def run():
    pygame.init()
    screen = pygame.display.set_mode((64*UPSCALE, 32*UPSCALE))
    clear(screen)
    
    running = True
    while running:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                running = False
                break

    pygame.quit()
    return 0