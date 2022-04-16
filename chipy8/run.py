import sys
import pygame
from threading import Thread

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

        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                chip.running = False
                break

    pygame.quit()
    return 0

def decrease_counters(chip: Chip8):
    """
    Decrease counters of the Chip8 instance at a steady rate. This is separated
    from the main execution loop so that it runs in an independent thread allowing
    a more accurate CHIP8 behaviour.
    """
    while chip.running:
        pygame.time.wait(WAITING_TIME)
        chip.decrease_counters()

def run(romfile=""):
    chip = Chip8()
    chip.load_into_memory(FONT_FILE, 0x0)

    # Load input file or wait until a file is dropped into the window
    if romfile == "":
        chip.wait_and_load(INITIAL_PC)
    else:
        chip.load_into_memory(romfile, INITIAL_PC)
    
    main_thread = Thread(target=main_loop, args=(chip,))
    counter_thread = Thread(target=decrease_counters, args=(chip,))

    main_thread.start()
    counter_thread.start()

    main_thread.join()
    counter_thread.join()

    return 0