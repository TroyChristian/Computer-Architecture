"""CPU functionality."""

import sys

class CPU:
    """Main CPU class."""

    def __init__(self):
        """Construct a new CPU."""
        self.pc = 0 # Program Counter
        self.reg = [0] * 8 # 8 Registers
        self.ram = [0] * 256 # Represents 2^8, 8 bit architecture 
        self.running = True 

    def read_ram(self, mar): # Takes in Memory Address Register (MAR holds a copy of the current instruc.)
        return self.ram[mar] 

    def write_ram(self, mar, mdr): #Write MDR (current value) to Memory Address Register
        self.ram[mar] = mdr

    def load(self):
        """Load a program into memory."""

        address = 0

        # For now, we've just hardcoded a program:

        program = [
            # From print8.ls8
            0b10000010, # LDI R0,8 2 operands, is not ALU, does not move PC, code 2, set val of reg to int
            0b00000000, # register number register 0 in this case
            0b00001000, # integer arg, 8 in this case in base 10
            0b01000111, # PRN R0, takes 1 arg, is not Alu, does not move PC code 7, print val of int at reg
            0b00000000, # Reg 0 being passed in as argument to to PRN
            0b00000001, # HLT Code 1, exit emulator
        ]

        for instruction in program:
            self.ram[address] = instruction
            address += 1
            # Pass the above binary numbers into indexes of self.ram
            """
          0  [0b10000010]
          1 [ 0b00000000]
          2 [0b00001000]
          3 [ 0b01000111]
          4  [0b00000000]
          5  [0b00000001]




            """


    def alu(self, op, reg_a, reg_b):
        """ALU operations."""

        if op == "ADD":
            self.reg[reg_a] += self.reg[reg_b]
        #elif op == "SUB": etc
        else:
            raise Exception("Unsupported ALU operation")

    def trace(self):
        """
        Handy function to print out the CPU state. You might want to call this
        from run() if you need help debugging.
        """

        print(f"TRACE: %02X | %02X %02X %02X |" % (
            self.pc,
            #self.fl,
            #self.ie,
            self.ram_read(self.pc),
            self.ram_read(self.pc + 1),
            self.ram_read(self.pc + 2)
        ), end='')

        for i in range(8):
            print(" %02X" % self.reg[i], end='')

        print()

    def run(self):
        """Run the CPU."""
        LDI = 0b10000010
        HLT = 0b00000001 
        PRN = 0b01000111

        while self.running:
            IR = self.read_ram(self.pc) # Instruction Register, get instruction out of where the pc is pointing in ram
            if IR == LDI: #If PC is pointing at an index in ram that holds LDI #0b10000010
                register_number = self.read_ram(self.pc + 1) # Read the next register number
                value_read = self.read_ram(self.pc + 2) # read the value at pc + 2
                self.write_ram(register_number, value_read)
                self.pc += 3
            
            elif IR == PRN:
                register_number = self.read_ram(self.pc + 1)
                print(self.ram[register_number])
                self.pc += 2
            elif IR == HLT:
                self.running = False
            
            else:
                print("Bad instruction at {} indexed at address {}".format(ir, self.pc))
                sys.exit(1)

