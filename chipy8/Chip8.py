from .Display import Display

INITIAL_PC = 0x200

class Chip8():
    def __init__(self):
        # Declare all registers
        self.memory = bytearray(4096) # Memory of 4kB
        self.var = bytearray(16)      # 16 8-bit Variable registers
        self.stack = []               # Stack for 16-bit addresses
        self.pc = INITIAL_PC          # Program Counter 
        self.ic = 0x0          # 16-bit Index Register
        
        self.d_timer = 0              # 8-bit Delay Timer
        self.s_timer = 0              # 8-bit Sound timer

        self.display = Display()      # Screen display
        
        # Declare all operational codes
        self.opcodes_c8 = {
            0x0: self.clear,
            0x1: self.jump,
            0x2: None,
            0x3: None,
            0x4: None,
            0x5: None,
            0x6: self.set_vx,
            0x7: self.add_vx,
            0x8: None,
            0x9: None,
            0xA: self.set_ic,
            0xB: None,
            0xC: None,
            0xD: self.draw,
            0xE: None,
            0xF: None,
        }

        """
        # Load the font into memory
        font = [
            0xF0, 0x90, 0x90, 0x90, 0xF0, # 0
            0x20, 0x60, 0x20, 0x20, 0x70, # 1
            0xF0, 0x10, 0xF0, 0x80, 0xF0, # 2
            0xF0, 0x10, 0xF0, 0x10, 0xF0, # 3
            0x90, 0x90, 0xF0, 0x10, 0x10, # 4
            0xF0, 0x80, 0xF0, 0x10, 0xF0, # 5
            0xF0, 0x80, 0xF0, 0x90, 0xF0, # 6
            0xF0, 0x10, 0x20, 0x40, 0x40, # 7
            0xF0, 0x90, 0xF0, 0x90, 0xF0, # 8
            0xF0, 0x90, 0xF0, 0x10, 0xF0, # 9
            0xF0, 0x90, 0xF0, 0x90, 0x90, # A
            0xE0, 0x90, 0xE0, 0x90, 0xE0, # B
            0xF0, 0x80, 0x80, 0x80, 0xF0, # C
            0xE0, 0x90, 0x90, 0x90, 0xE0, # D
            0xF0, 0x80, 0xF0, 0x80, 0xF0, # E
            0xF0, 0x80, 0xF0, 0x80, 0x80  # F
        ]

        for i, byte in enumerate(font):
            self.memory[i] = byte
        """
        
    def iterate(self):
        """
        Main execution loop. Fetches two bytes from memory then
        calls the appropiate opcode depending on the first nibble
        """
        # Fetch from memory
        b1, b2 = (
            self.memory[self.pc],
            self.memory[self.pc+1]
        )
        self.pc+=2

        # Get the operation nibble
        n = b1 >> 4
        
        # Run the corresponding opcode
        self.opcodes_c8[n](
            X = b1 & 0x0F,
            Y = b2 >> 4,
            N = b2 & 0x0F,
            NN = b2,
            NNN = (b1 & 0x0F)*256 + b2
        )
        return 0
    
    def clear(self, X, Y, N, NN, NNN):
        """
        0x0 instruction.
        This instruction is associated with the following opcodes:
            - 0x00E0 : Clear the display screen
        """
        if NNN == 0x0e0:
            self.display.clear()
            self.display.update()
        return 0
    
    def jump(self, NNN, **kwarg):
        """
        0x1NNN instruction. 
        Sets the value of the program counter to NNN
        """
        self.pc = NNN
        return 0
    
    def set_vx(self, X, NN, **kwarg):
        """
        0x6XNN instruction.
        Set the value of the VX register to NN
        """
        self.var[X] = NN
        return 0
    
    def add_vx(self, X, NN, **kwarg):
        """
        0x7XNN instruction.
        Add NN to the VX register. The carry flag is not used.
        """
        self.var[X] = (self.var[X] + NN) % 256
        return 0
    
    def set_ic(self, NNN, **kwarg):
        """
        0xANNN instruction.
        """
        self.ic = NNN
        return 0
    
    def draw(self, X, Y, N, **kwarg):
        """
        0xDXYN instruction.
        Draws an N pixel tall sprite from the memory location that 
        the ic register is holding at the VX and VY coordinates
        The drawing will be performed as an XOR operation between 
        the sprite data and the value of the pixels on the screen.
        """
        x_coord = self.var[X] % 64
        y_coord = self.var[Y] % 32
        
        # Set the flag to 0
        self.var[0xF] = 0
        
        for row in range(N):
            sprite_byte = self.memory[self.ic + row]
            sprite_bits = bin(sprite_byte)[2:].zfill(8)

            for b in sprite_bits:
                pixel = self.display.get_pixel(x_coord, y_coord)
                
                if b=='1' and pixel:
                    self.display.errase_pixel(x_coord, y_coord)
                    self.var[0xF] = 1
                elif b=='1' and not pixel:
                    self.display.draw_pixel(x_coord, y_coord)
                    
                x_coord += 1
                if x_coord > 63:
                    break
                
            x_coord = self.var[X] % 64
            y_coord += 1
            if y_coord > 31:
                break
        
        self.display.update()
        return 0
    
    def load_into_memory(self, rom_file, location):
        """
        Load into memory the a rom file at the specified location.
        There is also a sanitary check to see if we are using 
        unavailable memory.
        """
        rom = open(rom_file, 'rb').read()

        if location + len(rom) >= len(self.memory):
            raise RuntimeError("Memory to load rom is not available, check size and offset")

        for i, byte in enumerate(rom):
            self.memory[location+i] = byte
        
        return 0

    def start_screen(self):
        self.display.start()