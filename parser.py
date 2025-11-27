"""Recursive descent parser for MiniPy."""

from lexer import (
    Token, IDENT, NUMBER, KEYWORD, PLUS, MINUS, MUL, DIV,
    LT, GT, LE, GE, EQEQ, NEQ, ASSIGN, LPAREN, RPAREN, COLON,
    NEWLINE, INDENT, DEDENT, EOF
)
from ast_nodes import (
    Program, Assign, Print, If, While,
    BinOp, Number, Var
)
from errors import ParserError, SemanticError


class Parser:
    """Recursive descent parser."""
    
    def __init__(self, tokens):
        self.tokens = tokens
        self.pos = 0
    
    def current_token(self):
        """Get current token or EOF."""
        if self.pos >= len(self.tokens):
            return Token(EOF, None)
        return self.tokens[self.pos]
    
    def peek_token(self, offset=1):
        """Peek ahead by offset tokens."""
        pos = self.pos + offset
        if pos >= len(self.tokens):
            return Token(EOF, None)
        return self.tokens[pos]
    
    def advance(self):
        """Move to next token."""
        if self.pos < len(self.tokens):
            self.pos += 1
    
    def expect(self, token_type, value=None):
        """Expect a specific token type and optionally value."""
        token = self.current_token()
        if token.type != token_type:
            raise ParserError(
                f"Expected {token_type}, got {token.type}",
                token.line, token.col
            )
        if value is not None and token.value != value:
            raise ParserError(
                f"Expected {value}, got {token.value}",
                token.line, token.col
            )
        self.advance()
        return token
    
    def skip_newlines(self):
        """Skip newlines only."""
        while self.current_token().type == NEWLINE:
            self.advance()
    
    def parse_program(self):
        """Parse a complete program."""
        statements = []
        self.skip_newlines()
        
        while self.current_token().type != EOF:
            stmt = self.parse_statement()
            if stmt:
                statements.append(stmt)
            self.skip_newlines()
        
        return Program(statements)
    
    def parse_statement(self):
        """Parse a single statement."""
        token = self.current_token()
        
        if token.type == KEYWORD:
            if token.value == "if":
                return self.parse_if()
            elif token.value == "while":
                return self.parse_while()
            elif token.value == "print":
                return self.parse_print()
        
        if token.type == IDENT:
            # Could be assignment
            if self.peek_token().type == ASSIGN:
                return self.parse_assignment()
        
        raise ParserError(
            f"Unexpected token in statement: {token.type}",
            token.line, token.col
        )
    
    def parse_block(self):
        """Parse an indented block."""
        # Expect INDENT
        self.expect(INDENT)
        statements = []
        
        self.skip_newlines()
        
        while self.current_token().type != DEDENT and self.current_token().type != EOF:
            stmt = self.parse_statement()
            if stmt:
                statements.append(stmt)
            self.skip_newlines()
        
        # Expect DEDENT
        if self.current_token().type == DEDENT:
            self.advance()
        
        return statements
    
    def parse_assignment(self):
        """Parse assignment: name = expression"""
        name_token = self.expect(IDENT)
        name = name_token.value
        self.expect(ASSIGN)
        expr = self.parse_expression()
        return Assign(name, expr, name_token.line)
    
    def parse_print(self):
        """Parse print statement: print(expression)"""
        print_token = self.expect(KEYWORD, "print")
        self.expect(LPAREN)
        expr = self.parse_expression()
        self.expect(RPAREN)
        return Print(expr, print_token.line)
    
    def parse_if(self):
        """Parse if statement: if expr: block else: block"""
        if_token = self.expect(KEYWORD, "if")
        cond = self.parse_expression()
        self.expect(COLON)
        self.skip_newlines()
        then_body = self.parse_block()
        
        else_body = None
        if self.current_token().type == KEYWORD and self.current_token().value == "else":
            self.expect(KEYWORD, "else")
            self.expect(COLON)
            self.skip_newlines()
            else_body = self.parse_block()
        
        return If(cond, then_body, else_body, if_token.line)
    
    def parse_while(self):
        """Parse while loop: while expr: block"""
        while_token = self.expect(KEYWORD, "while")
        cond = self.parse_expression()
        self.expect(COLON)
        self.skip_newlines()
        body = self.parse_block()
        return While(cond, body, while_token.line)
    
    def parse_expression(self):
        """Parse an expression (comparison level)."""
        left = self.parse_additive()
        
        token = self.current_token()
        if token.type == LT:
            self.advance()
            right = self.parse_additive()
            return BinOp(left, "<", right, token.line)
        elif token.type == GT:
            self.advance()
            right = self.parse_additive()
            return BinOp(left, ">", right, token.line)
        elif token.type == LE:
            self.advance()
            right = self.parse_additive()
            return BinOp(left, "<=", right, token.line)
        elif token.type == GE:
            self.advance()
            right = self.parse_additive()
            return BinOp(left, ">=", right, token.line)
        elif token.type == EQEQ:
            self.advance()
            right = self.parse_additive()
            return BinOp(left, "==", right, token.line)
        elif token.type == NEQ:
            self.advance()
            right = self.parse_additive()
            return BinOp(left, "!=", right, token.line)
        
        return left
    
    def parse_additive(self):
        """Parse addition and subtraction."""
        left = self.parse_multiplicative()
        
        while True:
            token = self.current_token()
            if token.type == PLUS:
                self.advance()
                right = self.parse_multiplicative()
                left = BinOp(left, "+", right, token.line)
            elif token.type == MINUS:
                self.advance()
                right = self.parse_multiplicative()
                left = BinOp(left, "-", right, token.line)
            else:
                break
        
        return left
    
    def parse_multiplicative(self):
        """Parse multiplication and division."""
        left = self.parse_factor()
        
        while True:
            token = self.current_token()
            if token.type == MUL:
                self.advance()
                right = self.parse_factor()
                left = BinOp(left, "*", right, token.line)
            elif token.type == DIV:
                self.advance()
                right = self.parse_factor()
                left = BinOp(left, "/", right, token.line)
            else:
                break
        
        return left
    
    def parse_factor(self):
        """Parse a factor (number, variable, or parenthesized expression)."""
        token = self.current_token()
        
        if token.type == NUMBER:
            self.advance()
            return Number(token.value, token.line)
        
        if token.type == IDENT:
            name = token.value
            self.advance()
            # Note: semantic checking moved to semantic analysis pass
            # Remove old variable tracking
            return Var(name, token.line)
        
        if token.type == LPAREN:
            self.advance()
            expr = self.parse_expression()
            self.expect(RPAREN)
            return expr
        
        raise ParserError(
            f"Unexpected token in factor: {token.type}",
            token.line, token.col
        )
    

