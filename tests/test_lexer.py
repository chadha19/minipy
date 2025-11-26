"""Tests for the lexer."""

import unittest
from lexer import Lexer, Token, IDENT, NUMBER, KEYWORD, PLUS, MINUS, MUL, DIV
from lexer import LT, GT, EQEQ, ASSIGN, LPAREN, RPAREN, COLON, NEWLINE, INDENT, DEDENT, EOF


class TestLexer(unittest.TestCase):
    """Test cases for lexer."""
    
    def test_numbers(self):
        """Test number tokenization."""
        lexer = Lexer("123")
        tokens = lexer.tokenize()
        self.assertEqual(len(tokens), 2)  # NUMBER + EOF
        self.assertEqual(tokens[0].type, NUMBER)
        self.assertEqual(tokens[0].value, 123)
    
    def test_identifiers(self):
        """Test identifier tokenization."""
        lexer = Lexer("x")
        tokens = lexer.tokenize()
        self.assertEqual(tokens[0].type, IDENT)
        self.assertEqual(tokens[0].value, "x")
    
    def test_keywords(self):
        """Test keyword recognition."""
        lexer = Lexer("if else while print")
        tokens = lexer.tokenize()
        keywords = [t for t in tokens if t.type == KEYWORD]
        self.assertEqual(len(keywords), 4)
        self.assertEqual(keywords[0].value, "if")
        self.assertEqual(keywords[1].value, "else")
        self.assertEqual(keywords[2].value, "while")
        self.assertEqual(keywords[3].value, "print")
    
    def test_operators(self):
        """Test operator tokenization."""
        lexer = Lexer("+ - * / < >")
        tokens = lexer.tokenize()
        ops = [t for t in tokens if t.type != EOF]
        self.assertEqual(ops[0].type, PLUS)
        self.assertEqual(ops[1].type, MINUS)
        self.assertEqual(ops[2].type, MUL)
        self.assertEqual(ops[3].type, DIV)
        self.assertEqual(ops[4].type, LT)
        self.assertEqual(ops[5].type, GT)
    
    def test_equality_vs_assignment(self):
        """Test == vs = distinction."""
        lexer = Lexer("== =")
        tokens = lexer.tokenize()
        ops = [t for t in tokens if t.type != EOF]
        self.assertEqual(ops[0].type, EQEQ)
        self.assertEqual(ops[1].type, ASSIGN)
    
    def test_indentation(self):
        """Test indentation handling."""
        source = """x = 1
    y = 2
z = 3"""
        lexer = Lexer(source)
        tokens = lexer.tokenize()
        token_types = [t.type for t in tokens]
        self.assertIn(INDENT, token_types)
        self.assertIn(DEDENT, token_types)
    
    def test_simple_expression(self):
        """Test tokenizing a simple expression."""
        lexer = Lexer("x + 5")
        tokens = lexer.tokenize()
        types = [t.type for t in tokens if t.type != EOF]
        self.assertEqual(types, [IDENT, PLUS, NUMBER])
    
    def test_print_statement(self):
        """Test tokenizing print statement."""
        lexer = Lexer("print(x)")
        tokens = lexer.tokenize()
        types = [t.type for t in tokens if t.type != EOF]
        self.assertEqual(types, [KEYWORD, LPAREN, IDENT, RPAREN])


if __name__ == "__main__":
    unittest.main()

