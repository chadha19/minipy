"""Tests for the parser."""

import unittest
from lexer import Lexer
from parser import Parser
from ast_nodes import Program, Assign, Print, If, While, BinOp, Number, Var


class TestParser(unittest.TestCase):
    """Test cases for parser."""
    
    def parse_source(self, source):
        """Helper to parse source code."""
        lexer = Lexer(source)
        tokens = lexer.tokenize()
        parser = Parser(tokens)
        return parser.parse_program()
    
    def test_number(self):
        """Test parsing number."""
        ast = self.parse_source("print(5)")
        self.assertIsInstance(ast, Program)
        self.assertIsInstance(ast.statements[0], Print)
        self.assertIsInstance(ast.statements[0].expr, Number)
        self.assertEqual(ast.statements[0].expr.value, 5)
    
    def test_assignment(self):
        """Test parsing assignment."""
        ast = self.parse_source("x = 10")
        self.assertIsInstance(ast.statements[0], Assign)
        self.assertEqual(ast.statements[0].name, "x")
        self.assertIsInstance(ast.statements[0].expr, Number)
        self.assertEqual(ast.statements[0].expr.value, 10)
    
    def test_binary_operation(self):
        """Test parsing binary operations."""
        ast = self.parse_source("x = 5 + 3")
        assign = ast.statements[0]
        self.assertIsInstance(assign.expr, BinOp)
        self.assertEqual(assign.expr.op, "+")
        self.assertIsInstance(assign.expr.left, Number)
        self.assertIsInstance(assign.expr.right, Number)
    
    def test_variable_reference(self):
        """Test parsing variable reference."""
        ast = self.parse_source("x = 5\ny = x")
        # First statement defines x
        # Second statement uses x
        assign_y = ast.statements[1]
        self.assertIsInstance(assign_y.expr, Var)
        self.assertEqual(assign_y.expr.name, "x")
    
    def test_if_statement(self):
        """Test parsing if statement."""
        source = """x = 5
if x > 3:
    print(1)
else:
    print(0)"""
        ast = self.parse_source(source)
        if_stmt = ast.statements[1]
        self.assertIsInstance(if_stmt, If)
        self.assertIsInstance(if_stmt.cond, BinOp)
        self.assertEqual(len(if_stmt.then_body), 1)
        self.assertEqual(len(if_stmt.else_body), 1)
    
    def test_while_statement(self):
        """Test parsing while statement."""
        source = """x = 0
while x < 3:
    x = x + 1"""
        ast = self.parse_source(source)
        while_stmt = ast.statements[1]
        self.assertIsInstance(while_stmt, While)
        self.assertIsInstance(while_stmt.cond, BinOp)
        self.assertEqual(len(while_stmt.body), 1)
    
    def test_operator_precedence(self):
        """Test operator precedence."""
        ast = self.parse_source("x = 2 + 3 * 4")
        # Should be: 2 + (3 * 4)
        assign = ast.statements[0]
        binop = assign.expr
        self.assertEqual(binop.op, "+")
        self.assertIsInstance(binop.right, BinOp)
        self.assertEqual(binop.right.op, "*")
    
    def test_comparison(self):
        """Test parsing comparisons."""
        ast = self.parse_source("x = 5 < 10")
        assign = ast.statements[0]
        self.assertIsInstance(assign.expr, BinOp)
        self.assertEqual(assign.expr.op, "<")


if __name__ == "__main__":
    unittest.main()

