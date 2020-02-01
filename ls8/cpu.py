# initial setup code to follow....

import sys

"""CPU functionality."""


HLT = 0b00000001
PRN = 0b01000111
LDI = 0b10000010
MUL = 0b10100010
PUSH = 0b01000101
POP = 0b01000110
CALL = 0b01010000
RET = 0b00010001
ADD = 0b10100000
CMP = 0b10100111
JMP = 0b01010100
JEQ = 0b01010101
JNE = 0b01010110


class CPU:
    """Main CPU class."""

    def __init__(self, file):
        """Construct a new CPU."""
        self.ram = [0] * 256
        self.reg = [0] * 8
        self.pc = 0
        self.sp = 7
        self.file = file
        self.less = 0
        self.greater = 0
        self.equal = 0

    def ram_read(self, mar):
        return self.ram[mar]

    def ram_write(self, mdr, mar):
        self.ram[mdr] = mdr

    def load(self):
        """Load a program into memory."""
        address = 0

        try:

            with open(self.file) as f:

                for line in f:
                    comment_split = line.split("#")

                    num = comment_split[0].strip()

                    try:
                        val = int(num, 2)
                        self.ram[address] = val
                        address += 1
                    except ValueError:
                        continue

        except FileNotFoundError:
            print(f"{sys.argv[0]}: {sys.argv[1]} Not Found")
            sys.exit(2)

    def alu(self, op, reg_a, reg_b):
        """ALU operations."""

        if op == "ADD":
            self.reg[reg_a] += self.reg[reg_b]
        # elif op == "SUB": etc
        elif op == "MUL":
            self.reg[reg_a] *= self.reg[reg_b]
        elif op == "CMP":
            self.equal = 0
            self.less = 0
            self.greater = 0
            reg_a = self.reg[self.ram[self.pc + 1]]
            reg_b = self.reg[self.ram[self.pc + 2]]

            if reg_a == reg_b:
                self.equal = 1
            elif reg_a < reg_b:
                self.less = 1
            elif reg_a > reg_b:
                self.greater = 1

        else:
            raise Exception("Unsupported ALU operation")

    def trace(self):
        """
        Handy function to print out the CPU state. You might want to call this
        from run() if you need help debugging.
        """

        print(f"TRACE: %02X | %02X %02X %02X |" % (
            self.pc,
            self.ram_read(self.pc),
            self.ram_read(self.pc + 1),
            self.ram_read(self.pc + 2)
        ), end='')

        for i in range(8):
            print(" %02X" % self.reg[i], end='')

        print()

    def run(self):
        """Run the CPU."""

        running = True

        while running:

            IR = self.ram[self.pc]

            if IR == LDI:
                self.reg[self.ram[self.pc + 1]] = self.ram[self.pc + 2]
                move = (IR >> 6) + 1
                self.pc += move

            elif IR == PRN:
                print(self.reg[self.ram[self.pc + 1]])
                move = (IR >> 6) + 1
                self.pc += move

            elif IR == MUL:
                self.alu("MUL", self.ram[self.pc + 1], self.ram[self.pc + 2])
                move = (IR >> 6) + 1
                self.pc += move

            elif IR == ADD:
                self.alu("ADD", self.ram[self.pc + 1], self.ram[self.pc + 2])
                move = (IR >> 6) + 1
                self.pc += move

            elif IR == PUSH:
                self.sp -= 1
                self.ram[self.sp] = self.reg[self.ram[self.pc + 1]]
                move = (IR >> 6) + 1
                self.pc += move

            elif IR == POP:
                self.reg[self.ram[self.pc + 1]] = self.ram[self.sp]
                self.sp += 1
                move = (IR >> 6) + 1
                self.pc += move

            elif IR == CALL:
                self.sp -= 1
                self.ram[self.sp] = self.pc + 2
                address = self.reg[self.ram[self.pc + 1]]
                self.pc = address

            elif IR == RET:
                self.pc = self.ram[self.sp]
                self.sp += 1

            elif IR == JMP:
                jump = self.reg[self.ram[self.pc + 1]]
                self.pc = jump

            elif IR == JEQ:
                if self.equal == 1:
                    self.pc = self.reg[self.ram[self.pc + 1]]
                else:
                    move = (IR >> 6) + 1
                    self.pc += move

            elif IR == JNE:
                if self.equal == 0:
                    self.pc = self.reg[self.ram[self.pc + 1]]
                else:
                    move = (IR >> 6) + 1
                    self.pc += move

            elif IR == CMP:
                self.alu("CMP", self.ram[self.pc + 1], self.ram[self.pc + 2])
                move = (IR >> 6) + 1
                self.pc += move

            elif IR == HLT:
                running = False

            else:
                sys.exit(1)
