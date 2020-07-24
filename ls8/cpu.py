

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
CMP = 0b10100111
JMP = 0b01010100
JEQ = 0b01010101
JNE = 0b01010110
JGT = 0b01010111


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
        self.SP = 7
        self.reg[self.SP] = 0xF4 #index of reserved register Stack Pointer
        self.IM = 5 #index of reserved register Intertupt Mask
        self.IS = 6 #index of reserved register Stack Pointer
        self.flag_registers = [0b00000000]
        self.equal_flag = False 

        self.lookup_table = {
            "0b10100010" : "MUL",
            "0b00000001" : "HLT",
            "0b01000111" : "PRN", 
            "0b00000000" : "NOP",
            "0b10000010" : "LDI",
            "0b01000101" : "PUSH",
            "0b01000110" : "POP",
            "0b01010000" : "CALL", #80
            "0b00010001" : "RET",
            "0b10101000"  : "ADD" ,#168
            "0b10100111" : "CMP",
            "0b01010100" : "JMP",
            "0b01010101" : "JEQ", 
            "0b01010110" : "JNE",
            "0b01010111" : "JGT"

        }

        self.instruction_table = {
            MUL: self.MUL_instruction,
            HLT: self.HLT_instruction,
            PRN: self.PRN_instruction,
            NOP: self.NOP_instruction,
            LDI: self.LDI_instruction,
            PUSH: self.PUSH_instruction,
            POP: self.POP_instruction,
            CALL: self.CALL_instruction,
            ADD: self.ADD_instruction,
            RET: self.RET_instruction,
            CMP: self.CMP_instruction,
            JEQ: self.JEQ_instruction,
            JMP: self.JMP_instruction,
            JNE: self.JNE_instruction,
        }
        


    def LDI_instruction(self):
        index = self.read_ram(self.pc + 1) #reg number to index
        value = self.read_ram(self.pc + 2) #Value to put in reg
        self.reg[index] = value
        print("REG #: {}. Holds a  value of {}".format([index], value))
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

    def ADD_instruction(self):
        reg_a = self.read_ram(self.pc + 1)
        reg_b = self.read_ram(self.pc + 2)
        self.alu("ADD", reg_a, reg_b)
        self.pc += 3

    def HLT_instruction(self):
        self.running = False
        sys.exit(0)
    
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

    def CMP_instruction(self):
        first_reg = self.read_ram(self.pc + 1)
  
        print("Value of first reg in CMP_instruction is {}".format(first_reg))
        second_reg = self.read_ram(self.pc + 2)
       
        print("Value of second reg in CMP_instruction is {}".format(second_reg))

        self.alu("CMP", first_reg, second_reg)
        self.pc += 3
    
    def JMP_instruction(self):
        index = self.read_ram(self.pc + 1)
        address = self.reg[index]
        self.pc = address

    def JEQ_instruction(self):
        if self.equal_flag == "EQUAL":
           register_number = self.ram[self.pc+1]
           index = self.reg[register_number]
           self.pc = index
        else:
            self.pc +=2 
       
    
    def JNE_instruction(self):
        if self.equal_flag != "EQUAL":
            register_number = self.ram[self.pc+1]
            index = self.reg[register_number]
            self.pc = index
            print("JNE jump has pc set to value of {}".format(self.pc))
        else:
            self.pc += 2
    
   

       




    

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
            ADD: self.ADD_instruction,
            RET: self.RET_instruction,
            CMP: self.CMP_instruction,
            JEQ: self.JEQ_instruction,
            JMP: self.JMP_instruction,
            JNE: self.JNE_instruction
            
        }

            
            if code in self.instruction_table:
               function = instruction_table[code]
               function()
       
            else:
                print("unknown function call {} at ram[{}]".format(code, self.pc))
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
                    if self.lookup_table.get(instruction_no_comment_no_whitespace): 
                        print("INSTRUCTION:{} AT INDEX: {}".format(self.lookup_table[instruction_no_comment_no_whitespace], index))
                    else:
                        try:
                            print("Value or Reg: {} AT INDEX: {}".format(int(instruction_no_comment_no_whitespace,2), index))
                        except ValueError:
                            continue 
                    
                    try:
                        value = int(instruction_no_comment_no_whitespace, 2) #Get base 10 representation of the binary string
                    except ValueError:
                            continue 
                    self.write_ram(index, value) # Place instruction at specified index in memory array
                    #print("{} is the binary instruction, the index is in ram array is {}".format(self.read_ram(index), index))
                    #print(type(self.read_ram(index)))
                open_program.close() 
                        
        except FileNotFoundError:
                print("File specified in input, as {} not found".format(program))
               
        
       


                  





       

    def alu(self, op, reg_a, reg_b):
        """ALU operations."""
        print("op passed into alu is: {}".format(op))
        print(type(op))
        if op == "ADD":
            self.reg[reg_a] += self.reg[reg_b]
        elif op == "MUL":
            self.reg[reg_a] *= self.reg[reg_b]
        elif op == "CMP":
            if self.reg[reg_a] == self.reg[reg_b]:
                self.flag_registers = [0b00000001] # 1
                self.equal_flag = "EQUAL"
                print("reg_A is {}, reg_B is {}, equal_flag is {}, the pc is {}".format(self.reg[reg_a], self.reg[reg_b], self.equal_flag, self.pc))
                print(self.flag_registers)
            elif self.reg[reg_a] < self.reg[reg_b]:
                self.flag_registers = [0b00000100] # 4
                self.equal_flag = "LESS"
                print("reg_A is {}, reg_B is {}, equal_flag is {}, the pc is {}".format(self.reg[reg_a], self.reg[reg_b], self.equal_flag, self.pc))
                print(self.flag_registers)
            elif self.reg[reg_a] > self.reg[reg_b]:
                self.flag_registers = [0b00000010] # 2
                self.equal_flag = "GREATER"
                print("reg_A is {}, reg_B is {}, equal_flag is {}, the pc is {}".format(self.reg[reg_a], self.reg[reg_b], self.equal_flag, self.pc))
                print(self.flag_registers)


        else:
            raise Exception("Unsupported ALU operation")
            
        

    def trace(self):
        """
        Handy function to print out the CPU state. You might want to call this
        from run() if you need help debugging.
        """

        print(f"TRACE: %02X | %02X %02X %02X |" % (
            self.pc,
            #self.flag_registers,
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
            
            self.trace()
            instruction = self.read_ram(self.pc)

           
            command = self.instruction_table[instruction]
            if command == self.instruction_table[JNE] or  command == self.instruction_table[JEQ] and self.equal_flag != "EQUAL":
                self.pc += 2
                continue
            if command == self.instruction_table[JEQ] and self.equal_flag == "EQUAL":
                self.pc += 2
                continue
            #instruction_in_bin = bin(instruction)
            #instruction_in_bin_str = str(instruction_in_bin)
            
            print("CALLING {}" .format(command.__name__))
            command()
            

        print("TERMINATED")


           
            
            


