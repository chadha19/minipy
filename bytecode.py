"""Bytecode instruction definitions for MiniPy VM."""


# Opcodes
LOAD_CONST = "LOAD_CONST"
LOAD_NAME = "LOAD_NAME"
STORE_NAME = "STORE_NAME"
ADD = "ADD"
SUB = "SUB"
MUL = "MUL"
DIV = "DIV"
CMP_LT = "CMP_LT"
CMP_GT = "CMP_GT"
CMP_LE = "CMP_LE"
CMP_GE = "CMP_GE"
CMP_EQ = "CMP_EQ"
CMP_NEQ = "CMP_NEQ"
JUMP = "JUMP"
JUMP_IF_FALSE = "JUMP_IF_FALSE"
JUMP_IF_TRUE = "JUMP_IF_TRUE"
POP = "POP"
PRINT = "PRINT"
HALT = "HALT"


class Instruction:
    """Represents a single bytecode instruction."""
    def __init__(self, opcode, arg=None):
        self.opcode = opcode
        self.arg = arg
    
    def __repr__(self):
        if self.arg is not None:
            return f"{self.opcode}({self.arg})"
        return self.opcode
    
    def __eq__(self, other):
        if not isinstance(other, Instruction):
            return False
        return self.opcode == other.opcode and self.arg == other.arg


def format_bytecode(code):
    """Format bytecode for display."""
    lines = []
    for i, instr in enumerate(code):
        if isinstance(instr, tuple):
            opcode, arg = instr
            if arg is not None:
                lines.append(f"{i:4d}: {opcode:20s} {arg}")
            else:
                lines.append(f"{i:4d}: {opcode}")
        else:
            if instr.arg is not None:
                lines.append(f"{i:4d}: {instr.opcode:20s} {instr.arg}")
            else:
                lines.append(f"{i:4d}: {instr.opcode}")
    return "\n".join(lines)

