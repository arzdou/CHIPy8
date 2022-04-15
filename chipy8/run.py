import pygame
from time import sleep

from .Chip8 import Chip8
from .config import FONT_FILE, INITIAL_PC

def run(rom):
    chip = Chip8()
    chip.load_into_memory(FONT_FILE, 0x0)
    chip.load_into_memory(rom, INITIAL_PC)
    
    running = True
    while running:
        sleep(1/60) # Run at 60Hz
        chip.iterate()
        chip.decrease_counters() # This is not correct and has to be updated
        
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                running = False
                break

    pygame.quit()
    return 0