"""CPU functionality."""
import sys

LDI = 0b10000010
PRN = 0b01000111
HLT = 0b00000001
ADD = 0b10100000
SUB = 0b10100001
MUL = 0b10100010
DIV = 0b10100011
MOD = 0b10100100
PUSH = 0b01000101
POP = 0b01000110
CALL = 0b01010000
RET = 0b00010001
# SPRINT INST:
CMP = 0b10100111
JMP = 0b01010100
JEQ = 0b01010101
JNE = 0b01010110


class CPU:
    """Main CPU class."""

    def __init__(self):
        """Construct a new CPU."""
        self.pc = 0
        self.SP = 7  # SP - Stack Pointer
        self.reg = [0] * 8  # reg - Register
        self.reg[self.SP] = 0xF4
        self.ram = [0] * 256  # ram - Memory
        self.branch_table = {
            LDI: self.ldi_handler,
            PRN: self.prn_handler,
            HLT: self.hlt_handler,
            ADD: self. add_handler,
            SUB: self.sub_handler,
            MUL: self.mul_handler,
            PUSH: self.push_handler,
            POP: self.pop_handler,
            CALL: self.call_handler,
            RET: self.ret_handler,
            CMP: self.cmp_handler,
            JMP: self.jmp_handler,
            JEQ: self.jeq_handler,
            JNE: self.jne_handler,
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
        elif op == "CMP":
            if reg_a == reg_b:
                self.flag = 0b00000001
            elif reg_a < reg_b:
                self.flag = 0b00000100
            elif reg_a > reg_b:
                self.flag = 0b00000010
        else:
            raise Exception("Unsupported ALU operation")

# NON-MATHEMATICAL DATA HANDLING BELOW:
    def ldi_handler(self):
        self.ram_write(self.ram[self.pc + 2], self.ram[self.pc + 1])
        self.pc += 3

    def prn_handler(self):
        value = self.ram_read(self.ram[self.pc + 1])
        print(f'Value: {value}')
        self.pc += 2

    def hlt_handler(self):
        sys.exit(0)

# CALL/RET FUNCS BELOW:
    def call_handler(self):
        return_addr = self.pc + 2

        self.reg[self.SP] -= 1
        self.ram[self.reg[self.SP]] = return_addr

        reg_num = self.ram[self.pc + 1]
        subr_addr = self.reg[reg_num]

        self.pc = subr_addr

    def ret_handler(self):
        return_addr = self.ram[self.reg[self.SP]]
        self.reg[self.SP] += 1

        self.pc = return_addr

# ALU MATHEMATICAL FUNCS BELOW:
    def add_handler(self):
        self.alu("ADD", self.ram[self.pc + 1], self.ram[self.pc + 2])
        self.pc += 3

    def sub_handler(self):
        self.alu("SUB", self.ram[self.pc + 1], self.ram[self.pc + 2])
        self.pc += 3

    def mul_handler(self):
        self.alu("MUL", self.ram[self.pc + 1], self.ram[self.pc + 2])
        self.pc += 3

# RAM READING/WRITING FUNCS BELOW:
    def ram_read(self, MAR):
        return self.reg[MAR]

    def ram_write(self, MDR, MAR):
        self.reg[MAR] = MDR

# STACK IMPLEMENTATION BELOW:
    def push_handler(self):
        self.reg[self.SP] -= 1
        self.reg[self.SP] &= 0xff  # keep R7 in the range 00-FF
        # get register value
        reg_num = self.ram[self.pc + 1]
        value = self.reg[reg_num]
        address_to_push_to = self.reg[self.SP]
        self.ram[address_to_push_to] = value
        self.pc += 2

    def pop_handler(self):
        address_to_pop_from = self.reg[self.SP]
        value = self.ram[address_to_pop_from]
        # Store in the given register
        reg_num = self.ram[self.pc + 1]
        self.reg[reg_num] = value
        # Increment SP
        self.reg[self.SP] += 1
        self.pc += 2

# SPRINT IMPLEMENTATIONS BELOW:
    def cmp_handler(self):
        # Flags: 00000LGE
        reg1 = self.ram_read(self.ram[self.pc + 1])
        reg2 = self.ram_read(self.ram[self.pc + 2])

        self.alu("CMP", reg1, reg2)

        self.pc += 3

    def jmp_handler(self):
        print('hi')

    def jeq_handler(self):
        if self.flag == 0b00000001:
            reg_num = self.ram[self.pc + 1]
            self.pc = self.reg[reg_num]

        self.pc += 2

    def jne_handler(self):
        print('hola')

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
