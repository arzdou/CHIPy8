import pygame

from .Chip8 import Chip8
from .config import FONT_FILE, INITIAL_PC, WAITING_TIME

def run(romfile=""):
    chip = Chip8()
    chip.load_into_memory(FONT_FILE, 0x0)

    # Wait until a file is dropped into the window
    if romfile == "":
        waiting_for_rom = True
        while waiting_for_rom:
            for e in pygame.event.get():
                if e.type == pygame.QUIT:
                    pygame.quit()
                    return 0
                elif e.type == pygame.DROPFILE:
                    if e.file.endswith((".ch8", ".chip8", ".c8")):
                        romfile = e.file
                        waiting_for_rom = False

    chip.load_into_memory(romfile, INITIAL_PC)
    
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