import pygame

from .Chip8 import Chip8
from .config import FONT_FILE, INITIAL_PC, WAITING_TIME

def run(rom):
    chip = Chip8()
    chip.load_into_memory(FONT_FILE, 0x0)
    chip.load_into_memory(rom, INITIAL_PC)
    
    running = True
    while running:
        pygame.time.wait(WAITING_TIME)
        chip.iterate()
        chip.decrease_counters() # This is not correct and has to be updated
        
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                running = False
                break

    pygame.quit()
    return 0