import sys
import pygame

def run():
    pygame.init()
    screen = pygame.display.set_mode((640, 240))
    
    running = True
    while running:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                running = False

    pygame.quit()
    return 0

if __name__ == "__main__":
    sys.exit(run())