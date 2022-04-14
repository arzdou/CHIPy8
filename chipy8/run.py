import pygame
from .Chip8 import Chip8
from time import sleep


def run():
    chip = Chip8()
    chip.start_screen()
    chip.load_into_memory("roms/font.ch8", 0x0)
    chip.load_into_memory("roms/IBM_logo.ch8", 0x200)
    
    running = True
    while running:
        sleep(0.1)
        instruction = chip.fetch()
        chip.decode(instruction)

        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                running = False
                break

    pygame.quit()
    return 0