import pygame

FONT_FILE = "roms/font.ch8"
INITIAL_PC = 0x200
COSMAC_VIP = False

BACKGROUND = (0,0,0)
COLOR = (255,255,255)
UPSCALE = 10

KEY_MAP = {
    0x0: pygame.K_1,
    0x1: pygame.K_2,
    0x2: pygame.K_3,
    0x3: pygame.K_4,
    0x4: pygame.K_q,
    0x5: pygame.K_w,
    0x6: pygame.K_e,
    0x7: pygame.K_r,
    0x8: pygame.K_a,
    0x9: pygame.K_s,
    0xA: pygame.K_d,
    0xB: pygame.K_f,
    0xC: pygame.K_z,
    0xD: pygame.K_x,
    0xE: pygame.K_c,
    0xF: pygame.K_v,
}

INVERTED_KEY_MAP = {key: idx for idx, key in KEY_MAP.items()}