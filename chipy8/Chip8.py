from random import randint
from .Interface import Interface
from .config import INITIAL_PC, COSMAC_VIP

class Chip8():
    def __init__(self):
        self.running = True
        # Declare all registers
        self.memory = bytearray()     # Memory of 4kB
        self.var = bytearray()        # 16 8-bit Variable registers
        self.stack = []               # Stack for 16-bit addresses

        self.pc = 0x0                 # Program Counter 
        self.ic = 0x0                 # 16-bit Index Register
        
        self.delay_counter = 0        # 8-bit Delay counter
        self.sound_counter = 0        # 8-bit Sound counter

        self.interface = Interface()  # User interface: screen and keyboard
        self.interface_off = True

        # Set all the variables to their initial value
        self.reset()  
        
        # Declare all operational codes
        self.opcodes_c8 = {
            0x0: self.clear,
            0x1: self.jump,
            0x2: self.call,
            0x3: self.skip_XNN_equal,
            0x4: self.skip_XNN_notequal,
            0x5: self.skip_XY_equal,
            0x6: self.set_vx,
            0x7: self.add_vx,
            0x8: self.logic_instructions,
            0x9: self.skip_XY_notequal,
            0xA: self.set_ic,
            0xB: self.jump_with_offset,
            0xC: self.random,
            0xD: self.draw,
            0xE: self.skip_if_key,
            0xF: self.extra_operations,
        }

    def reset(self):
        self.memory = bytearray(4096) # Memory of 4kB
        self.var = bytearray(16)      # 16 8-bit Variable registers
        self.stack = []               # Stack for 16-bit addresses

        self.pc = INITIAL_PC          # Program Counter 
        self.ic = 0x0                 # 16-bit Index Register
        
        self.delay_counter = 0        # 8-bit Delay counter
        self.sound_counter = 0        # 8-bit Sound counter

        if self.interface_off:
            self.start_interface()
        else:
            self.interface.clear()
        
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
            - 0x0NNN :  Pause the execution and the program located 
                        at NNN (Not implemented)
            - 0x00E0 :  Clear the interface screen
            - 0x00EE :  Returns form a subrutine and sets the pc to 
                        the last value from the stack
        """
        if NNN == 0x0E0:
            self.interface.clear()
            self.interface.update()
        elif NNN == 0x0EE:
            self.pc = self.pop()
        return 0
    
    def jump(self, NNN, **kwarg):
        """
        0x1NNN instruction. 
        Sets the value of the program counter to NNN
        """
        self.pc = NNN
        return 0
    
    def call(self, NNN, **kwarg):
        """
        0x2NNN instruction. 
        Push the program counter to the stack and then sets its 
        value to NNN.
        """
        self.push(self.pc)
        self.pc = NNN
        return 0

    def skip_XNN_equal(self, X, NN, **kwarg):
        """
        0x3XNN instruction. 
        Skips the next two byte instruction if the values of VX
        and NN are equal
        """
        if self.var[X] == NN:
            self.pc += 2
        return 0

    def skip_XNN_notequal(self, X, NN, **kwarg):
        """
        0x4XNN instruction. 
        Skips the next two byte instruction if the values of VX
        and NN are NOT equal
        """
        if self.var[X] != NN:
            self.pc += 2
        return 0

    def skip_XY_equal(self, X, Y, N, **kwarg):
        """
        0x5XY0 instruction. 
        Skips the next two byte instruction if the values of VX
        and VY are equal
        """
        if (self.var[X] == self.var[Y]) and N == 0x0:
            self.pc += 2
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

    def logic_instructions(self, X, Y, N, **kwarg):
        """
        0x8XYN instruction.
        This instruction is associated with the following logical operations:
            - 0x8XY0 :  Set the value of VX to VY.        
            - 0x8XY1 :  Set the value of VX to VX OR VY. 
            - 0x8XY2 :  Set the value of VX to VX AND VY. 
            - 0x8XY3 :  Set the value of VX to VX XOR VY. 
            - 0x8XY4 :  Set the value of VX to VX + VY. The carry flag is set to 1 
                        if the result of the operation overflows and viceversa
            - 0x8XY5 :  Set the value of VX to VX - VY. The carry flag is set to 1
                        if VX is larger than VY and viceversa. 
            - 0x8XY6 :  Sets the value of VX to VY and then shifts VX 1 bit to the 
                        right. Set the flag to the last bit of VY
            - 0x8XY7 :  Set the value of VX to VY - VX. The carry flag is set to 1
                        if VY is larger than VX and viceversa. 
            - 0x8XYE :  Sets the value of VX to VY and then shifts VX 1 bit to the 
                        left. Set the flag to the last bit of VY
        """
        VX, VY = self.var[X], self.var[Y]
        if N == 0x0:
            self.var[X] = VY

        elif N == 0x1:
            self.var[X] = VX | VY

        elif N == 0x2:
            self.var[X] = VX & VY

        elif N == 0x3:
            self.var[X] = VX ^ VY

        elif N == 0x4:
            res = VX + VY
            self.var[X] = res % 256
            self.var[0xF] = 0
            if res>255:
                self.var[0xF] = 1 

        elif N == 0x5:
            if VX > VY:
                self.var[X] = VX - VY
                self.var[0xF] = 1
            else: 
                self.var[X] = 256 + VX - VY
                self.var[0xF] = 0

        elif N == 0x6: # Fails
            self.var[X] = (VX >> 1) % 256
            self.var[0xF] = VX & 0x1

        elif N == 0x7:
            if VY > VX:
                self.var[X] = VY - VX
                self.var[0xF] = 1
            else: 
                self.var[X] = 256 + VY - VX
                self.var[0xF] = 0

        elif N == 0xE: # Fails
            self.var[X] = (VX << 1) % 256
            self.var[0xF] = VX & 0x1
        
        else:
            raise RuntimeError("Operational code used is not valid")

        return 0

    def skip_XY_notequal(self, X, Y, N, **kwarg):
        """
        0x9XY0 instruction. 
        Skips the next two byte instruction if the values of VX
        and VY are NOT equal.
        """
        if (self.var[X] != self.var[Y]) and N == 0x0:
            self.pc += 2
        return 0
    
    def set_ic(self, NNN, **kwarg):
        """
        0xANNN instruction.
        Sets the index counter to NNN.
        """
        self.ic = NNN
        return 0

    def jump_with_offset(self, NNN, **kwarg):
        """
        0xBNNN instruction.
        Jumps to the NNN + V0 adress. From the CHIP-48 implementation
        forward this behaviour is changed but it has not been added yet.
        """
        self.pc = NNN + self.var[0x0]
        return 0

    def random(self, X, NN, **kwarg):
        """
        0xCNNN instruction.
        Generates a random number, ANDs it with the value NN and 
        puts it to the VX register
        """
        self.var[X] = randint(0, 31) & NN
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
                pixel = self.interface.get_pixel(x_coord, y_coord)
                
                if b=='1' and pixel:
                    self.interface.errase_pixel(x_coord, y_coord)
                    self.var[0xF] = 1
                elif b=='1' and not pixel:
                    self.interface.draw_pixel(x_coord, y_coord)
                    
                x_coord += 1
                if x_coord > 63:
                    break
                
            x_coord = self.var[X] % 64
            y_coord += 1
            if y_coord > 31:
                break
        
        self.interface.update()
        return 0

    def skip_if_key(self, X, NN, **kwarg):
        """
        0xENNN instruction.
        This instruction is associated with two conditional skips:
            - 0xEX9E :  Skip one instruction if the key corresponding 
                        to the value VX is being pressed        
            - 0xEXA1 :  Skip one instruction if the key corresponding 
                        to the value VX is NOT being pressed  
        """
        VX = self.var[X]

        if NN == 0x9E:
            if self.interface.is_key_pressed(VX):
                self.pc += 2

        elif NN == 0xA1:
            if not self.interface.is_key_pressed(VX):
                self.pc += 2

        return 0

    def extra_operations(self, X, NN, **kwarg):
        """
        0xFNNN instructions.
        This code compiles the following miscelanea routines:
            - 0xFX07 :  Sets VX to the current value of the delay counter        
            - 0xFX15 :  Sets the delay counter to the value in VX
            - 0xFX18 :  Sets the sound counter to the value in VX
            - 0xFX1E :  The index register I will get the value in VX added 
                        to it. The carry flag is set to 1 if the result 
                        overflows, that is if the register is larger than 0xFFF
            - 0xFX0A :  This instruction “blocks”; it stops execution and waits 
                        for key input.
            - 0xFX29 :  The index register I is set to the address of the 
                        hexadecimal character in VX. When pressed, its 
                        hexadecimal value will be put in VX and execution continues.
            - 0xFX33 :  It takes the number in VX (which is one byte, so it can 
                        be any number from 0 to 255) and converts it to three 
                        decimal digits, storing these digits in memory at the 
                        address in the index register I.
            - 0xFX55 :  The value of each variable register from V0 to VX inclusive 
                        (if X is 0, then only V0) will be stored in successive 
                        memory addresses, starting with the one that is stored in I.
                        The original CHIP-8 interpreter for the COSMAC VIP actually 
                        incremented the I register while it worked. Each time it 
                        stored or loaded one register, it incremented I. After the 
                        instruction was finished, I would be set to the new value 
                        I + X + 1
            - 0xFX65 :  The same as 0xFX55 but takes the value stored at the memory 
                        addresses and loads them into the variable registers instead.
        """
        VX = self.var[X]
        I = self.ic

        if NN == 0x07:
            self.var[X] = self.delay_counter

        elif NN == 0x15:
            self.delay_counter = self.var[X]
        
        elif NN == 0x18:
            self.sound_counter = self.var[X]

        elif NN == 0x1E:
            res = self.ic + VX
            if res > 0xFFF:
                self.ic = res - 0xFFF
                self.var[0xF] = 1
            else:
                self.ic = res
                self.var[0xF] = 0
        
        elif NN == 0x0A:
            input_key = self.interface.wait_for_keypress()    
            self.var[X] = input_key

        elif NN == 0x29:
            last_nib = VX & 0x0F
            self.ic = last_nib*5

        elif NN == 0x33:
            ones = VX // 10**0 % 10
            tens = VX // 10**1 % 10
            hundreds = VX // 10**2 % 10

            self.memory[I:I+3] = (hundreds, tens, ones)

        elif NN == 0x55:
            self.memory[I:I+X+1] = self.var[:X+1]
            if COSMAC_VIP:
                self.ic += X+1
        
        elif NN == 0x65:
            self.var[:X+1] = self.memory[I:I+X+1]
            if COSMAC_VIP:
                self.ic += X+1

        else:
            raise RuntimeError("Operational code used is not valid")

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

    def wait_and_load(self, location):
        romfile = self.interface.wait_for_drop()
        self.load_into_memory(romfile, location)
        return 0
    
    def decrease_counters(self):
        """
        Decrease both counters and make a sound if the sound counter is 0.
        
        UPDATE:
        This process should happen at a steady 60 Hz rate, independant of 
        the main loop. This is not the case yet and has to be implemented
        """
        if self.delay_counter > 0:
            self.delay_counter -= 1
        
        if self.sound_counter > 0:
            self.sound_counter -= 1
            self.interface.make_beep()
            

    def push(self, b):
        """
        Push b into the stack
        """
        self.stack.append(b)
        return 0

    def pop(self):
        """
        Pops the last value in from the stack
        """
        b = self.stack.pop(-1)
        return b

    def start_interface(self):
        self.interface_off = False
        self.interface.start()