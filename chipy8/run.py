import pygame

from .Chip8 import Chip8
from .config import FONT_FILE, INITIAL_PC, WAITING_TIME

def main_loop(chip: Chip8):
    """
    Main emulation loop, once every WAITING_TIME the iterate method of the 
    input Chip8 instance will be executed. After that it will check all pygame
    events and exit if the QUIT event was recieved.
    """
    while chip.running:
        pygame.time.wait(WAITING_TIME)
        chip.iterate()
        chip.decrease_counters()
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                chip.running = False
                break

    pygame.quit()
    return 0

def run(romfile=""):
    chip = Chip8()
    chip.load_into_memory(FONT_FILE, 0x0)

    # Load input file or wait until a file is dropped into the window
    if romfile == "":
        chip.wait_and_load(INITIAL_PC)
    else:
        chip.load_into_memory(romfile, INITIAL_PC)
    
    main_loop(chip)

    return 0