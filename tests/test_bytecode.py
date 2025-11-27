"""Tests for bytecode generation and new instructions."""

import unittest
import sys
import os
sys.path.insert(0, os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

from lexer import Lexer
from parser import Parser
from compiler import compile_ast
from bytecode import CMP_LE, CMP_GE, CMP_NEQ, JUMP_IF_TRUE, POP


class TestBytecode(unittest.TestCase):
    """Test bytecode generation."""
    
    def parse_and_compile(self, source):
        """Parse and compile source."""
        lexer = Lexer(source)
        tokens = lexer.tokenize()
        parser = Parser(tokens)
        ast = parser.parse_program()
        return compile_ast(ast)
    
    def test_le_instruction(self):
        """Test <= generates CMP_LE."""
        source = "x = 5 <= 10"
        code, consts, names = self.parse_and_compile(source)
        opcodes = [instr.opcode for instr in code]
        self.assertIn(CMP_LE, opcodes)
    
    def test_ge_instruction(self):
        """Test >= generates CMP_GE."""
        source = "x = 10 >= 5"
        code, consts, names = self.parse_and_compile(source)
        opcodes = [instr.opcode for instr in code]
        self.assertIn(CMP_GE, opcodes)
    
    def test_neq_instruction(self):
        """Test != generates CMP_NEQ."""
        source = "x = 5 != 10"
        code, consts, names = self.parse_and_compile(source)
        opcodes = [instr.opcode for instr in code]
        self.assertIn(CMP_NEQ, opcodes)


if __name__ == "__main__":
    unittest.main()

