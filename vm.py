"""Stack-based virtual machine for MiniPy."""

from bytecode import (
    LOAD_CONST, LOAD_NAME, STORE_NAME, ADD, SUB, MUL, DIV,
    CMP_LT, CMP_GT, CMP_EQ, JUMP, JUMP_IF_FALSE, PRINT, HALT
)
from errors import VMError


class VM:
    """Stack-based virtual machine."""
    
    def __init__(self, code, consts, names):
        self.code = code
        self.consts = consts
        self.names = names
        self.stack = []
        self.globals = {}
        self.ip = 0  # Instruction pointer
    
    def push(self, value):
        """Push value onto stack."""
        self.stack.append(value)
    
    def pop(self):
        """Pop value from stack."""
        if not self.stack:
            raise VMError("Stack underflow", self.ip)
        return self.stack.pop()
    
    def peek(self):
        """Peek at top of stack without popping."""
        if not self.stack:
            raise VMError("Stack underflow", self.ip)
        return self.stack[-1]
    
    def run(self):
        """Execute the bytecode."""
        self.ip = 0
        
        while self.ip < len(self.code):
            instr = self.code[self.ip]
            opcode = instr.opcode
            arg = instr.arg
            
            if opcode == LOAD_CONST:
                self.push(self.consts[arg])
                self.ip += 1
            
            elif opcode == LOAD_NAME:
                name = self.names[arg]
                if name not in self.globals:
                    raise VMError(f"Undefined variable: {name}", self.ip)
                self.push(self.globals[name])
                self.ip += 1
            
            elif opcode == STORE_NAME:
                value = self.pop()
                name = self.names[arg]
                self.globals[name] = value
                self.ip += 1
            
            elif opcode == ADD:
                b = self.pop()
                a = self.pop()
                self.push(a + b)
                self.ip += 1
            
            elif opcode == SUB:
                b = self.pop()
                a = self.pop()
                self.push(a - b)
                self.ip += 1
            
            elif opcode == MUL:
                b = self.pop()
                a = self.pop()
                self.push(a * b)
                self.ip += 1
            
            elif opcode == DIV:
                b = self.pop()
                a = self.pop()
                if b == 0:
                    raise VMError("Division by zero", self.ip)
                self.push(a // b)  # Integer division
                self.ip += 1
            
            elif opcode == CMP_LT:
                b = self.pop()
                a = self.pop()
                self.push(1 if a < b else 0)
                self.ip += 1
            
            elif opcode == CMP_GT:
                b = self.pop()
                a = self.pop()
                self.push(1 if a > b else 0)
                self.ip += 1
            
            elif opcode == CMP_EQ:
                b = self.pop()
                a = self.pop()
                self.push(1 if a == b else 0)
                self.ip += 1
            
            elif opcode == JUMP:
                self.ip = arg
            
            elif opcode == JUMP_IF_FALSE:
                value = self.pop()
                if value == 0:  # False
                    self.ip = arg
                else:
                    self.ip += 1
            
            elif opcode == PRINT:
                value = self.pop()
                print(value)
                self.ip += 1
            
            elif opcode == HALT:
                break
            
            else:
                raise VMError(f"Unknown opcode: {opcode}", self.ip)
        
        return self.globals


def run_bytecode(code, consts, names):
    """Convenience function to run bytecode."""
    vm = VM(code, consts, names)
    return vm.run()

