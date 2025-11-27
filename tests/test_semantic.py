"""Tests for semantic analysis."""

import unittest
import sys
import os
sys.path.insert(0, os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

from lexer import Lexer
from parser import Parser
from semantic import SemanticAnalyzer


class TestSemantic(unittest.TestCase):
    """Test semantic analysis."""
    
    def parse_and_check(self, source):
        """Parse source and run semantic analysis."""
        lexer = Lexer(source)
        tokens = lexer.tokenize()
        parser = Parser(tokens)
        ast = parser.parse_program()
        semantic = SemanticAnalyzer()
        return semantic.check(ast)
    
    def test_undefined_variable(self):
        """Test undefined variable error."""
        source = "print(x)"
        errors = self.parse_and_check(source)
        self.assertEqual(len(errors), 1)
        self.assertIn("Undefined variable", str(errors[0]))
    
    def test_type_mismatch_arithmetic(self):
        """Test arithmetic on non-ints."""
        # This test would need bool literals - skip for now
        pass
    
    def test_condition_must_be_bool(self):
        """Test that if condition must be bool."""
        source = """x = 5
if x:
    print(1)"""
        errors = self.parse_and_check(source)
        # x is int, not bool - should error
        self.assertGreater(len(errors), 0)
    
    def test_variable_scope(self):
        """Test variable scoping."""
        source = """x = 5
if x > 3:
    y = 10
print(y)"""
        errors = self.parse_and_check(source)
        # y is in inner scope, should error
        self.assertGreater(len(errors), 0)
    
    def test_valid_program(self):
        """Test valid program passes semantic checks."""
        source = """x = 5
if x > 3:
    print(1)
else:
    print(0)"""
        errors = self.parse_and_check(source)
        self.assertEqual(len(errors), 0)


if __name__ == "__main__":
    unittest.main()

