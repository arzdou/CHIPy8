import pygame

WINDOW_NAME = "CHIPy8"
ICON_FILE = "chipy8/rsc/icon.png"
FONT_FILE = "chipy8/rsc/font.ch8"
SOUND_FILE = "chipy8/rsc/beep.mp3"

WAITING_TIME = 1
INITIAL_PC = 0x200
COSMAC_VIP = False

BACKGROUND = (0,0,0)
COLOR = (255,255,255)
UPSCALE = 10

"""
The standard keymap is as follows
    
        PAD             KEYBOARD  
    1  2  3  C         1  2  3  4
    4  5  6  D   -->   q  w  e  r
    7  8  9  E   -->   a  s  d  f
    A  0  B  F         z  x  c  v

"""

KEY_MAP = {
    0x0: pygame.K_x,
    0x1: pygame.K_1,
    0x2: pygame.K_2,
    0x3: pygame.K_3,
    0x4: pygame.K_q,
    0x5: pygame.K_w,
    0x6: pygame.K_e,
    0x7: pygame.K_a,
    0x8: pygame.K_s,
    0x9: pygame.K_d,
    0xA: pygame.K_z,
    0xB: pygame.K_c,
    0xC: pygame.K_4,
    0xD: pygame.K_r,
    0xE: pygame.K_f,
    0xF: pygame.K_v,
}

INVERTED_KEY_MAP = {key: idx for idx, key in KEY_MAP.items()}