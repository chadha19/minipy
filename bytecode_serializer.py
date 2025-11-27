"""Serialize bytecode to file format for C++ VM."""

from typing import List
from bytecode import Instruction


def serialize_bytecode(code: List[Instruction], consts: List, names: List[str], filename: str) -> None:
    """Serialize bytecode to text format for C++ VM."""
    with open(filename, 'w') as f:
        # Write code
        f.write(f"{len(code)}\n")
        for instr in code:
            if instr.arg is not None:
                f.write(f"{instr.opcode} {instr.arg}\n")
            else:
                f.write(f"{instr.opcode}\n")
        
        # Write constants
        f.write(f"{len(consts)}\n")
        for const in consts:
            f.write(f"{const}\n")
        
        # Write names
        f.write(f"{len(names)}\n")
        for name in names:
            f.write(f"{name}\n")

