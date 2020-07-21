"""CPU functionality."""
import sys

LDI = 0b10000010
PRN = 0b01000111
HLT = 0b00000001
SUB = 0b10100001
MUL = 0b10100010
DIV = 0b10100011
MOD = 0b10100100


class CPU:
    """Main CPU class."""

    def __init__(self):
        """Construct a new CPU."""
        self.pc = 0
        self.reg = [0] * 8
        self.ram = [0] * 256

    def load(self):
        """Load a program into memory."""

        address = 0

        if len(sys.argv) != 2:
            print('Incorrect format. Format => ls8.py <filename>')
            sys.exit(1)

        try:
            with open(sys.argv[1]) as f:
                for line in f:
                    try:
                        line = line.split('#', 1)[0]
                        line = int(line, 2)
                        self.ram[address] = line
                        address += 1
                    except ValueError:
                        pass

        except FileNotFoundError:
            print(f'Couldn\'t find file {sys.argv[1]}')

        # For now, we've just hardcoded a program:

        # program = [
        #     # From print8.ls8
        #     0b10000010,  # LDI R0,8
        #     0b00000000,
        #     0b00001000,
        #     0b01000111,  # PRN R0
        #     0b00000000,
        #     0b00000001,  # HLT
        # ]
        #
        # for instruction in program:
        #     self.ram[address] = instruction
        #     address += 1

    def alu(self, op, reg_a, reg_b):
        """ALU operations."""

        if op == "ADD":
            self.reg[reg_a] += self.reg[reg_b]
        elif op == "SUB":
            self.reg[reg_a] -= self.reg[reg_b]
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
            # self.fl,
            # self.ie,
            self.ram_read(self.pc),
            self.ram_read(self.pc + 1),
            self.ram_read(self.pc + 2)
        ), end='')

        for i in range(8):
            print(" %02X" % self.reg[i], end='')

        print()

    def ram_read(self, MAR):
        return self.reg[MAR]

    def ram_write(self, MDR, MAR):
        self.reg[MAR] = MDR

    def run(self):
        """Run the CPU."""
        running = True

        while running:
            inst = self.ram[self.pc]
            if inst == LDI:
                self.ram_write(self.ram[self.pc + 2], self.ram[self.pc + 1])
                self.pc += 3
            elif inst == PRN:
                value = self.ram_read(self.ram[self.pc + 1])
                # print(f'Stored Value at Reg index: [{self.ram[self.pc + 2]}] is:', value)
                print(f'Value: {value}')
                self.pc += 2
            elif inst == MUL:
                # self.alu("MUL", self.ram_read(self.pc + 1), self.ram_read(self.pc + 2))
                value = self.ram_read(self.ram[self.pc + 1])
                value2 = self.ram_read(self.ram[self.pc + 2])
                self.reg[self.ram[self.pc + 1]] *= self.reg[self.ram[self.pc + 2]]
                print(f'Multiplied: {self.reg[self.ram[self.pc + 1]]}')
                self.pc += 3
            elif inst == HLT:
                running = False
            else:
                # print(f'Invalid instruction: {inst}')
                sys.exit(f'Invalid instruction: {inst}')
