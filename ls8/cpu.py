

import sys
MUL = 0b10100010
HLT = 0b00000001
PRN = 0b01000111
NOP = 0b00000000
LDI = 0b10000010
PUSH = 0b01000101 
POP = 0b01000110
CALL = 0b01010000 #80
RET = 0b00010001
ADD = 0b10101000 #168
class CPU:
    """Main CPU class."""
    


    def __init__(self):
        """Construct a new CPU."""

        """
        * R5 is reserved as the interrupt mask (IM)
        * R6 is reserved as the interrupt status (IS)
        * R7 is reserved as the stack pointer (SP)
        """
        self.pc = 0 # Program Counter
        self.reg = [0] * 8 # 8 Registers
        self.ram = [0] * 256 # Represents 2^8, 8 bit architecture 
        self.running = True 
        self.ir = 0
        self.SP = 7 #index of reserved register Stack Pointer
        self.IM = 5 #index of reserved register Intertupt Mask
        self.IS = 6 #index of reserved register Stack Pointer
        


    def LDI_instruction(self):
        index = self.read_ram(self.pc + 1)
        value = self.read_ram(self.pc + 2)
        self.reg[index] = value
        self.pc += 3

    def PUSH_instruction(self):
        index = self.read_ram(self.pc + 1)
        value = self.reg[index]
        self.reg[self.SP] -= 1
        self.ram[self.reg[self.SP]] = value
        self.pc += 2 

    def POP_instruction(self):
        index = self.read_ram(self.pc + 1)
        value = self.ram[self.reg[self.SP]]
        self.reg[index] = value 

        self.reg[self.SP] += 1
        self.pc += 2
        

    def MUL_instruction(self):
        reg_a = self.read_ram(self.pc + 1)
        reg_b = self.read_ram(self.pc + 2)
        self.alu("MUL", reg_a, reg_b)
        self.pc += 3

    def HLT_instruction(self):
        self.running = False
    
    def PRN_instruction(self):
        index = self.read_ram(self.pc + 1)
        print(self.reg[index])
        self.pc += 2 
    
    def CALL_instruction(self): # grab 
        address_to_continue_from = self.pc + 2 
        self.reg[self.SP] -= 1
        self.ram[self.reg[self.SP]] = address_to_continue_from

        register_index = self.ram[self.pc + 1]
        address_of_subroutine = self.reg[register_index] 
        self.pc = address_of_subroutine

    def RET_instruction(self):
        resume_address = self.ram[self.reg[self.SP]] # currently pointing at address to coninue from
        self.reg[self.SP] += 1
        self.pc = resume_address # so execution resumes here.

    def ADD_instruction(self):
        reg_a = self.read_ram(self.pc + 1)
        reg_b = self.read_ram(self.pc + 2)
        self.alu("ADD", reg_a, reg_b)
        self.pc += 3



    

    def NOP_instruction(self):
        self.pc += 1
    #Instruction Set
    def instruction_set(self, code):
        instruction_table = {
            MUL: self.MUL_instruction,
            HLT: self.HLT_instruction,
            PRN: self.PRN_instruction,
            NOP: self.NOP_instruction,
            LDI: self.LDI_instruction,
            PUSH: self.PUSH_instruction,
            POP: self.POP_instruction,
            CALL: self.CALL_instruction,
            RET: self.RET_instruction,
            ADD: self.ADD_instruction
        }

        function = instruction_table[code]
        if instruction_table[code] != None:
           function()
       
        else:
            print("unknown function call {} at ram[{}]".format(self.pc))
            sys.exit(1)


    def read_ram(self, mar): # Takes in Memory Address Register (MAR holds a copy of the current instruc.)
        return self.ram[mar] 

    def write_ram(self, mar, mdr): #Write MDR (current value) to Memory Address Register
        self.ram[mar] = mdr
    
    


    def load(self):
        program = sys.argv[1]
        try:
            with open(program) as open_program:
                for index, instruction in enumerate(open_program):# Tuple unpacking (0, 0b111)
                    instruction_no_comment = instruction.split('#') # Strip comments from program.py ^^
              
                    instruction_no_comment_no_whitespace = instruction_no_comment[0].strip() 
                    print("INSTRUCTION:{}".format(instruction_no_comment_no_whitespace))
                    #if instruction_no_comment_no_whitespace == '':
                        #continue
                    
                    try:
                        value = int(instruction_no_comment_no_whitespace, 2) #Get base 10 representation of the binary string
                    except ValueError:
                            continue 
                    self.write_ram(index, value) # Place instruction at specified index in memory array
                    print("{} is the binary instruction, the index is in ram array is {}".format(self.read_ram(index), index))
                    print(type(self.read_ram(index)))
                open_program.close() 
                        
        except FileNotFoundError:
                print("File specified in input, as {} not found".format(program))
               
        
       


                  





       

    def alu(self, op, reg_a, reg_b):
        """ALU operations."""
        print("op passed into alu is: {}".format(op))
        print(type(op))
        if op == 0b10101000:
            self.reg[reg_a] += self.reg[reg_b]
        if op == "MUL":
            self.reg[reg_a] *= self.reg[reg_b]
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
            self.read_ram(self.pc),
            self.read_ram(self.pc + 1),
            self.read_ram(self.pc + 2)
        ), end='')

        for i in range(8):
            print(" %02X" % self.reg[i], end='')

        print()



    def run(self):
        """Run the CPU."""




        while self.running:
            #self.trace()
            #print(self.pc) 
            instruction_register = self.read_ram(self.pc)
            #print(instruction_register)
            self.instruction_set(instruction_register)
            


