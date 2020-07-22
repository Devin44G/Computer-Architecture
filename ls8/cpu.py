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
        self.branch_table = {
            LDI: self.ldi_handler,
            PRN: self.prn_handler,
            HLT: self.hlt_handler,
            MUL: self.mul_handler,
        }

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

    def ldi_handler(self):
        self.ram_write(self.ram[self.pc + 2], self.ram[self.pc + 1])
        self.pc += 3

    def prn_handler(self):
        value = self.ram_read(self.ram[self.pc + 1])
        print(f'Value: {value}')
        self.pc += 2

    def hlt_handler(self):
        sys.exit(0)

    def mul_handler(self):
        self.alu("MUL", self.ram[self.pc + 1], self.ram[self.pc + 2])
        self.pc += 3

    def ram_read(self, MAR):
        return self.reg[MAR]

    def ram_write(self, MDR, MAR):
        self.reg[MAR] = MDR

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

    def run(self):
        """Run the CPU."""
        running = True

        while running:
            inst = self.ram[self.pc]
            if inst in self.branch_table:
                self.branch_table[inst]()
            else:
                sys.exit(f'Invalid instruction: {inst}')
