"""CPU functionality."""

import sys

SP = 7

class CPU:
    """Main CPU class."""

    def __init__(self):
        """Construct a new CPU."""
        self.ram = [0] * 256
        self.reg = [0] * 8   # RO-R7
        self.pc = 0
        self.reg[SP] = 0xF4

    def ram_read(self, MAR):
        return self.ram[MAR]

    def ram_write(self, MAR, MDR):
        self.ram[MAR] = MDR

    def load(self):
        """Load a program into memory."""

        # address = 0
        #
        # # For now, we've just hardcoded a program:
        #
        # program = [
        #     # From print8.ls8
        #     0b10000010, # LDI R0,8
        #     0b00000000,
        #     0b00001000,
        #     0b01000111, # PRN R0
        #     0b00000000,
        #     0b00000001, # HLT
        # ]
        #
        # for instruction in program:
        #     self.ram[address] = instruction
        #     address += 1

        if len(sys.argv) != 2:
            print("usage: python3 ls8.py examples/mult.ls8")
            sys.exit(1)

        address = 0

        try:
            with open(sys.argv[1]) as f:
                for line in f:
                    line_value = line.split("#")[0].strip()
                    if line_value == '':
                        continue
                    val = int(line_value, 2)
                    self.ram[address] = val
                    address += 1

        except FileNotFoundError:
            print(f"File not found: {sys.argv[1]}")
            sys.exit(2)

    def alu(self, op, reg_a, reg_b):
        """ALU operations."""

        if op == "ADD":
            self.reg[reg_a] += self.reg[reg_b]
        #elif op == "SUB": etc
        elif op == "MUL":
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
        PRN = 0b01000111
        HLT = 0b00000001
        MUL = 0b10100010
        PUSH = 0b01000101
        POP = 0b01000110

        running = True

        while running:

            ir = self.ram_read(self.pc)
            operand_a = self.ram_read(self.pc + 1)
            operand_b = self.ram_read(self.pc + 2)

            if ir == LDI:
                self.reg[operand_a] = operand_b
                # self.pc += 3

            elif ir == PRN:
                print_item = self.ram[self.pc + 1]
                print(self.reg[print_item])
                # self.pc += 2

            elif ir == MUL:
                self.alu("MUL", operand_a, operand_b)
                # self.pc += 3

            elif ir == PUSH:
                # Decrement SP
                self.reg[SP] -= 1

                # Get reg_num to push
                # reg_num = self.ram_read(self.pc + 1)
                # Same as operand_a

                # Get the value to push
                value = self.reg[operand_a]

                # Copy the value to the SP address
                top_of_stack_address = self.reg[SP]
                self.ram[top_of_stack_address] = value

            elif ir == POP:
                # Get reg to pop into
                # reg_num = self.ram_read(self.pc + 1)
                # Same as operand_a

                # Get the top stack of address
                top_of_stack_address = self.reg[SP]

                # Get the value of the top of the stack
                value = self.ram[top_of_stack_address]

                # Store the value in register
                self.reg[operand_a] = value

                #Increment the SP
                self.reg[SP] += 1

            elif ir == HLT:
                running = False

            else:
                print('Not working')
                running = False

            number_of_operands = (ir >> 6)
            self.pc += number_of_operands + 1