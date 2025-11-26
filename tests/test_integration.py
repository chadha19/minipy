"""Integration tests for the full compiler pipeline."""

import unittest
import sys
import os
from io import StringIO
from contextlib import redirect_stdout

# Add parent directory to path
sys.path.insert(0, os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

from lexer import Lexer
from parser import Parser
from compiler import compile_ast
from vm import VM


class TestIntegration(unittest.TestCase):
    """Integration tests for full pipeline."""
    
    def run_program(self, source):
        """Run a program and return output."""
        # Lex
        lexer = Lexer(source)
        tokens = lexer.tokenize()
        
        # Parse
        parser = Parser(tokens)
        ast = parser.parse_program()
        
        # Compile
        code, consts, names = compile_ast(ast)
        
        # Execute
        f = StringIO()
        with redirect_stdout(f):
            vm = VM(code, consts, names)
            vm.run()
        return f.getvalue().strip()
    
    def test_simple_print(self):
        """Test simple print statement."""
        source = "print(5)"
        output = self.run_program(source)
        self.assertEqual(output, "5")
    
    def test_assignment_and_print(self):
        """Test assignment and print."""
        source = """x = 10
print(x)"""
        output = self.run_program(source)
        self.assertEqual(output, "10")
    
    def test_arithmetic(self):
        """Test arithmetic operations."""
        source = "print(2 + 3 * 4)"
        output = self.run_program(source)
        self.assertEqual(output, "14")  # 2 + (3 * 4) = 14
    
    def test_if_true(self):
        """Test if statement with true condition."""
        source = """x = 10
if x > 5:
    print(1)
else:
    print(0)"""
        output = self.run_program(source)
        self.assertEqual(output, "1")
    
    def test_if_false(self):
        """Test if statement with false condition."""
        source = """x = 3
if x > 5:
    print(1)
else:
    print(0)"""
        output = self.run_program(source)
        self.assertEqual(output, "0")
    
    def test_while_loop(self):
        """Test while loop."""
        source = """x = 0
while x < 3:
    x = x + 1
print(x)"""
        output = self.run_program(source)
        self.assertEqual(output, "3")
    
    def test_comparison(self):
        """Test comparison operators."""
        source = """x = 5
if x == 5:
    print(1)
else:
    print(0)"""
        output = self.run_program(source)
        self.assertEqual(output, "1")
    
    def test_nested_expressions(self):
        """Test nested expressions."""
        source = "print((2 + 3) * 4)"
        output = self.run_program(source)
        self.assertEqual(output, "20")  # (2 + 3) * 4 = 20


if __name__ == "__main__":
    unittest.main()

