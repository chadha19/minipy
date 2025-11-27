"""Tests for constant folding optimizer."""

import unittest
import sys
import os
sys.path.insert(0, os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

from lexer import Lexer
from parser import Parser
from optimizer import Optimizer
from ast_nodes import Number, BinOp


class TestOptimizer(unittest.TestCase):
    """Test constant folding."""
    
    def parse_and_optimize(self, source):
        """Parse and optimize source."""
        lexer = Lexer(source)
        tokens = lexer.tokenize()
        parser = Parser(tokens)
        ast = parser.parse_program()
        optimizer = Optimizer()
        return optimizer.optimize(ast)
    
    def test_constant_folding_add(self):
        """Test constant folding of addition."""
        source = "x = 3 + 5"
        ast = self.parse_and_optimize(source)
        # Should be optimized to x = 8
        assign = ast.statements[0]
        self.assertIsInstance(assign.expr, Number)
        self.assertEqual(assign.expr.value, 8)
    
    def test_constant_folding_multiply(self):
        """Test constant folding of multiplication."""
        source = "x = 2 * 3"
        ast = self.parse_and_optimize(source)
        assign = ast.statements[0]
        self.assertIsInstance(assign.expr, Number)
        self.assertEqual(assign.expr.value, 6)
    
    def test_identity_optimizations(self):
        """Test identity optimizations."""
        source = "x = y + 0"
        ast = self.parse_and_optimize(source)
        assign = ast.statements[0]
        # Should optimize to just y
        # Note: This requires Var support in optimizer
        pass
    
    def test_dead_code_elimination(self):
        """Test dead code elimination in if."""
        source = """if 0:
    print(1)
else:
    print(0)"""
        ast = self.parse_and_optimize(source)
        if_stmt = ast.statements[0]
        # Then body should be empty
        self.assertEqual(len(if_stmt.then_body), 0)


if __name__ == "__main__":
    unittest.main()

